#!/usr/bin/env python3
"""pumpfun-top5-forecast-01 entry (v3): persistence-anchored forecaster.

Pump.fun top-of-chart churn is extreme; the strongest signal over a 0-1h
horizon is the last mark's chart order, so we anchor a large probability mass
on it (rank k keeps most of its mass, a little spills to neighbors) and add
diffusion: Monte-Carlo log-cap random walks (sd calibrated to the dev
history's 10-minute moves, scaled by sqrt(hours)) give per-place place and
size probabilities. Deterministic via fixed RNG seed.
"""
import json, math, os, random, datetime as dt

IN = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
P_STAY, P_NEI = 0.25, 0.05          # anchor mass on last chart order
SIZE_SD = 0.35
MICRO = 1_000_000
RNG_SEED = 20261112  # deterministic across runs

def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()

def main():
    task = json.load(open(os.path.join(IN, "task.json")))
    marks = []
    for line in open(os.path.join(IN, "history.ndjson")):
        line = line.strip()
        if not line: continue
        m = json.loads(line)
        if m.get("ok") and m.get("rows"): marks.append(m)
    if not marks: raise SystemExit("no marks")
    places = task["places"]; edges = task["size"]["edges"]
    last = marks[-1]
    chart = sorted(last["rows"], key=lambda r: r["rank"])
    t_last = ts(last["at"])
    reads = [ts(r) for r in task["reads"]]

    rng = random.Random(RNG_SEED)
    npaths = 6000
    cand = chart[:60]
    # per-coin: anchor probability from last chart order
    anchor = {}
    for k in range(1, places + 1):
        anchor.setdefault(k, {})
        anchor[k][cand[k - 1]["mint"]] = anchor[k].get(cand[k - 1]["mint"], 0.0) + P_STAY
        if k > 1: anchor[k][cand[k - 2]["mint"]] = anchor[k].get(cand[k - 2]["mint"], 0.0) + P_NEI
        if k < len(cand): anchor[k][cand[k]["mint"]] = anchor[k].get(cand[k]["mint"], 0.0) + P_NEI
    # simulate: each path draws per-coin logcap noise; mix anchor & simulated ranks
    place_counts = {p: {} for p in range(1, places + 1)}
    size_draws = {p: [] for p in range(1, places + 1)}
    paths = []
    for r in cand:
        y = math.log10(float(r["market_cap_lamports"])) - 9.0
        paths.append((r["mint"], y))
    for read_t in reads:
        h = max((read_t - t_last) / 3600.0, 0.02)
        for _ in range(npaths):
            vals = []
            sd_h = SIZE_SD * math.sqrt(h)
            for mn, y in paths:
                vals.append((y + rng.gauss(0.0, sd_h), mn))
            vals.sort(reverse=True)
            for p in range(1, places + 1):
                mn = vals[p - 1][1]
                place_counts[p][mn] = place_counts[p].get(mn, 0) + 1
                size_draws[p].append(vals[p - 1][0])

    probabilities = []
    for p in range(1, places + 1):
        tot = sum(place_counts[p].values()) or 1
        # blend simulation counts with the analytic anchor (anchor keeps floor)
        blended = {}
        for mn, c in place_counts[p].items():
            blended[mn] = blended.get(mn, 0.0) + (c / tot) * (1.0 - 0.25)
        for mn, a in anchor[p].items():
            blended[mn] = blended.get(mn, 0.0) + a * 0.25
        rows = sorted(blended.items(), key=lambda kv: -kv[1])
        acc = 0.0
        for mn, q in rows:
            if acc >= 0.95: break
            qq = min(q, 0.95 - acc)
            if qq <= 0: break
            probabilities.append({"mint": mn, "place": p, "p": round(qq, 6)})
            acc += qq

    sizes = []
    for p in range(1, places + 1):
        arr = size_draws[p]
        if not arr: continue
        mean = sum(arr) / len(arr)
        var = sum((x - mean) ** 2 for x in arr) / max(len(arr) - 1, 1)
        sd = max(math.sqrt(var), 0.15)
        def cdf(x):
            if x == float("inf"): return 1.0
            if x == float("-inf"): return 0.0
            return 0.5 * math.erfc((mean - x) / (sd * math.sqrt(2.0)))
        for b in range(0, 82):
            lo = -math.inf if b == 0 else edges[b - 1]
            hi = math.inf if b == 81 else edges[b]
            pr = cdf(hi) - cdf(lo)
            u = int(pr * MICRO)
            if u > 0:
                sizes.append({"place": p, "bin": b, "p": u / MICRO})

    top5 = []
    used = set()
    for p in range(1, places + 1):
        rows = [r for r in probabilities if r["place"] == p and r["mint"] not in used]
        rows.sort(key=lambda r: -r["p"])
        pick = rows[0]["mint"] if rows else chart[p - 1]["mint"]
        top5.append(pick); used.add(pick)

    os.makedirs(OUT, exist_ok=True)
    fc = {"probabilities": probabilities, "top5": top5, "sizes": sizes}
    with open(os.path.join(OUT, task["output"]), "w") as f:
        f.write(json.dumps(fc) + "\n")

main()
