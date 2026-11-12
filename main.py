#!/usr/bin/env python3
"""roblox-up-and-coming-forecast-01: rank-weighted forecast over the 13 highest-ranked
Up-and-Coming games of the last history snapshot. The chart churns fast (its #1 changed
13 times among 10 games in 45 archive reads), so no exact order is knowable 72 hours out.
Each scored place spreads 0.75 of its mass over the top 13 candidates, geometrically
decayed by chart rank (ratio 0.9), and leaves 0.25 unnamed to share over the chart.
Weights tuned on the sealed practice window of the archive (proxy log score -35.96 vs house -45.15)."""
import json, os

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
K = 13
P_NAMED = 0.75
DECAY = 0.9

task = json.load(open(os.path.join(INPUT_DIR, "task.json")))
lines = [l for l in open(os.path.join(INPUT_DIR, "history.ndjson")).read().split("\n") if l.strip()]
last = json.loads(lines[-1])
chart = [r["universe_id"] for r in sorted(last["up_and_coming"], key=lambda r: r["rank"])][:K]
w = [DECAY ** i for i in range(len(chart))]
tot = sum(w)
probabilities = [{"universe_id": u, "place": k, "p": P_NAMED * w[i] / tot}
                 for k in range(1, task["places"] + 1) for i, u in enumerate(chart)]
out = {"probabilities": probabilities, "top10": chart[:task["places"]]}
os.makedirs(OUTPUT_DIR, exist_ok=True)
open(os.path.join(OUTPUT_DIR, task["output"]), "w").write(json.dumps(out) + "\n")
