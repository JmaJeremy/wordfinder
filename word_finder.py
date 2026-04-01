#!/usr/bin/env python3
"""Find dictionary words using optional and required letter sets."""

import argparse
from itertools import groupby

DICT_PATH = "./NWL2023.txt"


def load_words(path):
    """Load words from NWL2023 word list (format: 'WORD definition...')."""
    words = []
    with open(path) as f:
        for line in f:
            word = line.split()[0].lower() if line.strip() else ""
            if word.isalpha():
                words.append(word)
    return words


def matches(word, allowed, required):
    if len(word) < 4:
        return False
    if not all(c in allowed for c in word):
        return False
    if required and not any(c in required for c in word):
        return False
    return True


def parse_letters(s):
    return set(s.replace(",", "").replace(" ", "").lower())


def main():
    parser = argparse.ArgumentParser(description="Find words from a set of letters.")
    parser.add_argument("optional", nargs="?", help="Optional letters (e.g. abcde)")
    parser.add_argument("required", nargs="?", default="", help="Required letters (e.g. xy)")
    args = parser.parse_args()

    if args.optional is None:
        optional_str = input("Optional letters: ").strip()
        required_str = input("Required letters (leave blank to skip): ").strip()
    else:
        optional_str = args.optional
        required_str = args.required

    optional = parse_letters(optional_str)
    required = parse_letters(required_str)
    allowed = optional | required

    words = load_words(DICT_PATH)
    found = sorted(
        {w for w in words if matches(w, allowed, required)},
        key=lambda w: (-len(w), w),
    )

    if not found:
        print("\nNo words found.")
        return

    print(f"\nFound {len(found)} words:\n")
    for length, group in groupby(found, key=len):
        group_list = list(group)
        print(f"--- {length} letters ({len(group_list)}) ---")
        for w in group_list:
            print(f"  {w}")
        print()


if __name__ == "__main__":
    main()
