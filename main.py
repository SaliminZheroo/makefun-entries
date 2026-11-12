#!/usr/bin/env python3
"""news-summary-01 entry: writes the summary of 11 November 2026 world news to /output/entry.txt."""
import shutil, os

# Deterministic: copies a fixed file, so both runs write identical bytes.

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.txt")
dst = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt")
# entry.txt must exist with final bytes even if /output already has a stale copy
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copyfile(src, dst)
