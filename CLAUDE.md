# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BUR** is the corrections and research repository for the Cologne digitization of Burnouf's *Dictionnaire classique Sanskrit-Français* (1866). The canonical source lives in `csl-orig/v02/bur/bur.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `burissues/` | Per-issue correction workflows (`issueNNN/` pattern) |
| `verbs01/` | Root identification: maps Burnouf entries to MW root spellings, identifies prefixed verbs (upasargas) |
| `greek/` | Greek loanword and citation research |

### Issue correction pattern (`burissues/issueNNN/`)

Each issue folder follows the standard workflow:
1. Copy current `bur.txt` to a local `temp_bur_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_bur_1.txt`, `temp_bur_2.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit the corrected file to `csl-orig`, then sync to Cologne
5. Commit issue documentation back here

### Verb root pipeline (`verbs01/`)

Identifies Burnouf verb entries and maps them to their MW equivalents, resolving prefixed-verb (upasarga) structures.

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh bur ../../BURScan/2020
sh xmlchk_xampp.sh bur
```

## Dependencies

- **Python 3**
- **bur.txt** — in `$BASE/cologne/csl-orig/v02/bur/bur.txt`
