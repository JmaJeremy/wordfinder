# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Web app (Cloudflare Pages)

**One-time setup:** generate the combined word list from NWL2023.txt and sowpods.txt:

```bash
python scripts/build_wordlist.py
```

This writes `public/words.txt` (tab-separated `word<TAB>tag` format, one per line). Commit this file.
Tags: `n` = NWL2023 exclusive, `s` = SOWPODS exclusive, `b` = both.

**Deploy:**

```bash
npx wrangler pages deploy public/
```

Or connect the repo to Cloudflare Pages dashboard (build command: none, output directory: `public`).

## CLI tool

```bash
# Interactive mode
python word_finder.py

# CLI mode: python word_finder.py <optional_letters> [required_letters]
python word_finder.py abcde b

# Filter by dictionary: all (default), nwl, sowpods, common, nwl-only, sowpods-only
python word_finder.py abcde b --wordlist nwl-only
```

## Architecture

**Web app** (`public/`) — static, no build step. `app.js` fetches `words.txt` once on first search, then filters entirely client-side. `wrangler.toml` points Cloudflare Pages at the `public/` directory.

**CLI** (`word_finder.py`) — single-file, stdlib only. Reads NWL2023.txt (`~/NWL2023.txt`) and sowpods.txt (repo root) and computes set operations based on `--wordlist` flag.

**Shared logic (both):**
- `allowed = optional | required` — required letters are also part of the usable pool
- Words must be ≥4 letters, use only `allowed` letters, and contain at least one `required` letter
- Results grouped by length, sorted longest-first then alphabetically

**Dictionary format:** `WORD definition...` per line — only the first token is used. `build_wordlist.py` strips definitions and filters to alpha words ≥4 letters.
