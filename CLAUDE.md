# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the tool

```bash
# Interactive mode
python word_finder.py

# CLI mode
python word_finder.py <optional_letters> [required_letters]
# Example: find words using letters a,b,c,d,e that must contain 'b'
python word_finder.py abcde b
```

## Architecture

Single-file CLI tool (`word_finder.py`) with no dependencies beyond the standard library.

**Dictionary:** Expects NWL2023 word list at `./NWL2023.txt` (hardcoded path). Format: one entry per line, `WORD definition...` — only the first token is used.

**Core logic:**
- `load_words` — reads dictionary, lowercases, filters non-alpha
- `matches` — filters words ≥4 letters that use only `allowed` letters and contain at least one `required` letter
- `allowed = optional | required` — required letters are also valid to use, not separate from the pool
- Output is grouped by word length, sorted longest-first then alphabetically
