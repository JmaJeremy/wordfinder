#!/usr/bin/env python3
"""Extract words from sowpods.txt into public/words.txt for the web app."""

import os
import sys

DICT_PATH = os.path.join(os.path.dirname(__file__), "../sowpods.txt")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../public/words.txt")

if not os.path.exists(DICT_PATH):
    print(f"Error: dictionary not found at {DICT_PATH}", file=sys.stderr)
    sys.exit(1)

words = set()
with open(DICT_PATH) as f:
    for line in f:
        word = line.strip().lower()
        if word.isalpha() and len(word) >= 4:
            words.add(word)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    f.write("\n".join(sorted(words)))

print(f"Wrote {len(words)} words to {OUTPUT_PATH}")
