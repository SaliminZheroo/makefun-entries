# pumpfun-top5-forecast-01

make.fun bounty entry: predict the top 5 new Solana pump.fun coins by market
cap, 24 hours out.

`main.py` (Python 3.13, standard library only) reads the house snapshots at
`/input` and writes `/output/forecast.json`: per-place coin probabilities, a
top-5 tie-break guess, and per-place market-cap size bins. Deterministic:
same input, same output.

Model: persistence-anchored Monte Carlo over the last mark's chart order with
a momentum tilt from weighted recent drift, plus log-normal size bins.

Built for the make.fun bounty pumpfun-top5-forecast-01 by agent sessions
(bundled transcripts submitted with the entry).
