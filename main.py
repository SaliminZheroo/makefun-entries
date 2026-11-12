#!/usr/bin/env python3
"""pumpfun-top5-forecast-01 entry (v2): persistence-anchored forecaster.

Pump.fun top-of-chart churn is extreme; the strongest signal over a 1-6h
horizon is the last mark's order (house baseline), so we anchor on it and add
a small momentum tilt: coins with strong positive weighted drift earn extra
probability, coins fading lose some. Monte-Carlo over per-coin drift+diffusion
provides place probabilities; sizes use per-place projected cap with sd from
the observed dispersion of the chart (house-like 0.35 when data is thin).
"""
import json, math, os, random, datetime as dt

IN = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
P_STAY, P_NEI = 0.35, 0.10          # anchor mass on last chart order
TILT = 0.10                          # total extra mass reshaped by momentum
SIZE_SD = 0.35
MICRO = 1_000_000

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

    # per-coin recent slope (log10 cap per hour, weighted to recent marks)
    series = {}
    for i, m in enumerate(marks):
        for r in m["rows"]:
            cap = float(r["market_cap_lamports"])
            if cap > 0:
                series.setdefault(r["mint"], []).append((ts(m["at"]), math.log10(cap) - 9.0))
    slope = {}
    for mn, s in series.items():
        s = sorted(s)
        pts = s[-4:]
        if len(pts) < 2:
            slope[mn] = 0.0
        else:
            # robust: median of pairwise slopes
            gs = []
            for a in range(len(pts)):
                for b in range(a + 1, len(pts)):
                    dtv = pts[b][0] - pts[a][0]
                    if dtv > 0:
                        gs.append((pts[b][1] - pts[a][1]) / (dtv / 3600.0))
            gs.sort()
            slope[mn] = gs[len(gs) // 2] if gs else 0.0
    # cap the tilt pool: momentum score normalized
    maxslope = max((abs(slope.get(r["mint"], 0)) for r in chart[:40]), default=1.0) or 1.0

    rng = random.Random(20261112)
    npaths = 6000
    cand = chart[:60]
    # per-coin: anchor probability from baseline + momentum tilt
    anchor = {}
    for k in range(1, places + 1):
        anchor.setdefault(k, {})
        anchor[k][cand[k - 1]["mint"]] = anchor[k].get(cand[k - 1]["mint"], 0.0) + P_STAY
        if k > 1: anchor[k][cand[k - 2]["mint"]] = anchor[k].get(cand[k - 2]["mint"], 0.0) + P_NEI
        if k < len(cand): anchor[k][cand[k]["mint"]] = anchor[k].get(cand[k]["mint"], 0.0) + P_NEI
    tilt = {}
    for k in range(1, places + 1):
        tilt[k] = {}
        for r in cand[:30]:
            s = slope.get(r["mint"], 0.0)
            if s <= 0: continue
            w = (s / maxslope) ** 2
            tilt[k][r["mint"]] = tilt[k].get(r["mint"], 0.0) + w
    # simulate: each path draws per-coin logcap noise; mix anchor & tilt ranks
    place_counts = {p: {} for p in range(1, places + 1)}
    size_draws = {p: [] for p in range(1, places + 1)}
    paths = []
    for r in cand:
        s = slope.get(r["mint"], 0.0)
        y = math.log10(float(r["market_cap_lamports"])) - 9.0
        paths.append((r["mint"], y, max(min(s, 0.5), -0.5)))
    for read_t in reads:
        h = max((read_t - t_last) / 3600.0, 0.02)
        for _ in range(npaths):
            vals = []
            for mn, y, s in paths:
                # diffusion: hourly sd ~0.35 (chart churn), drift capped
                sd = SIZE_SD * math.sqrt(h)
                vals.append((y + s * h + rng.gauss(0.0, sd), mn))
            vals.sort(reverse=True)
            # probability mix: with prob (1-TILT) follow simulated ranks, else tilt-weighted sample
            if rng.random() < (1.0 - TILT):
                for p in range(1, places + 1):
                    mn = vals[p - 1][1]
                    place_counts[p][mn] = place_counts[p].get(mn, 0) + 1
                    size_draws[p].append(vals[p - 1][0])
            else:
                for p in range(1, places + 1):
                    w = tilt[p]
                    tot = sum(w.values()) or 1.0
                    x = rng.random() * tot
                    acc = 0.0; pick = vals[p - 1][1]
                    for mn, wt in w.items():
                        acc += wt
                        if x <= acc:
                            pick = mn; break
                    place_counts[p][pick] = place_counts[p].get(pick, 0) + 1
                    cap = next((y for mn2, y, s2 in paths if mn2 == pick), 3.0)
                    size_draws[p].append(cap)

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
        sd = max(math.sqrt(var), 0.30)
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
