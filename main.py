#!/usr/bin/env python3
"""news-summary-01 entry: writes the summary of 11 November 2026 world news to /output/entry.txt."""
import shutil, os

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.txt")
dst = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt")
shutil.copyfile(src, dst)
