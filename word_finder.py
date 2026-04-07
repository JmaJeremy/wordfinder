#!/usr/bin/env python3
"""Find dictionary words using optional and required letter sets."""

import argparse
import os
from itertools import groupby

NWL_PATH = os.path.expanduser("~/NWL2023.txt")
SOWPODS_PATH = os.path.join(os.path.dirname(__file__), "sowpods.txt")

WORDLIST_CHOICES = ["all", "nwl", "sowpods", "common", "nwl-only", "sowpods-only"]
WORDLIST_LABELS = {
    "all":          "All words (NWL + SOWPODS)",
    "nwl":          "NWL2023",
    "sowpods":      "SOWPODS",
    "common":       "Common to both",
    "nwl-only":     "NWL exclusive",
    "sowpods-only": "SOWPODS exclusive",
}


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


def get_wordlist(wordlist):
    nwl_ok = os.path.exists(NWL_PATH)
    sowpods_ok = os.path.exists(SOWPODS_PATH)

    if wordlist in ("nwl", "nwl-only", "common", "all") and not nwl_ok:
        raise FileNotFoundError(f"NWL2023.txt not found at {NWL_PATH}")
    if wordlist in ("sowpods", "sowpods-only", "common", "all") and not sowpods_ok:
        raise FileNotFoundError(f"sowpods.txt not found at {SOWPODS_PATH}")

    if wordlist == "nwl":
        return load_dict(NWL_PATH)
    if wordlist == "sowpods":
        return load_dict(SOWPODS_PATH)

    nwl = load_dict(NWL_PATH) if nwl_ok else set()
    sowpods = load_dict(SOWPODS_PATH) if sowpods_ok else set()

    if wordlist == "common":
        return nwl & sowpods
    if wordlist == "nwl-only":
        return nwl - sowpods
    if wordlist == "sowpods-only":
        return sowpods - nwl
    # "all"
    return nwl | sowpods


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
    parser.add_argument(
        "--wordlist", "-w",
        choices=WORDLIST_CHOICES,
        default="all",
        help="Which dictionary to use (default: all)",
    )
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

    try:
        words = get_wordlist(args.wordlist)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    found = sorted(
        {w for w in words if matches(w, allowed, required)},
        key=lambda w: (-len(w), w),
    )

    label = WORDLIST_LABELS[args.wordlist]
    if not found:
        print(f"\nNo words found ({label}).")
        return

    print(f"\nFound {len(found)} words ({label}):\n")
    for length, group in groupby(found, key=len):
        group_list = list(group)
        print(f"--- {length} letters ({len(group_list)}) ---")
        for w in group_list:
            print(f"  {w}")
        print()


if __name__ == "__main__":
    main()
