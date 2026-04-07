#!/usr/bin/env python3
"""Build combined word list from NWL2023.txt and sowpods.txt.

Output format: one entry per line: `word<TAB>tag`
  tag n = NWL2023 exclusive
  tag s = SOWPODS exclusive
  tag b = both dictionaries
"""

import os
import sys

SCRIPTS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.join(SCRIPTS_DIR, "..")
NWL_PATH = os.path.join(ROOT_DIR, "NWL2023.txt")
SOWPODS_PATH = os.path.join(ROOT_DIR, "sowpods.txt")
OUTPUT_PATH = os.path.join(ROOT_DIR, "public/words.txt")


def load_dict(path):
    words = set()
    with open(path) as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            word = parts[0].lower()
            if word.isalpha() and len(word) >= 4:
                words.add(word)
    return words


missing = [p for p in (NWL_PATH, SOWPODS_PATH) if not os.path.exists(p)]
if missing:
    for p in missing:
        print(f"Error: dictionary not found at {p}", file=sys.stderr)
    sys.exit(1)

print("Loading NWL2023.txt…")
nwl = load_dict(NWL_PATH)
print("Loading sowpods.txt…")
sowpods = load_dict(SOWPODS_PATH)

both = nwl & sowpods
nwl_only = nwl - sowpods
sowpods_only = sowpods - nwl

print(f"\nNWL2023:            {len(nwl):>7,} words")
print(f"SOWPODS:            {len(sowpods):>7,} words")
print(f"Common (both):      {len(both):>7,} words")
print(f"NWL exclusive:      {len(nwl_only):>7,} words")
print(f"SOWPODS exclusive:  {len(sowpods_only):>7,} words")
print(f"Total unique:       {len(nwl | sowpods):>7,} words")

lines = []
for w in nwl_only:
    lines.append(f"{w}\tn")
for w in sowpods_only:
    lines.append(f"{w}\ts")
for w in both:
    lines.append(f"{w}\tb")

lines.sort()

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    f.write("\n".join(lines))

print(f"\nWrote {len(lines):,} entries to {OUTPUT_PATH}")
