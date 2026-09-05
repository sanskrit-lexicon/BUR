_Created: 15-05-2026 · Last updated: 05-09-2026_

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BUR** is the development and correction repository for **Émile Burnouf's *Dictionnaire classique sanscrit-français* (1866)**, a Sanskrit→French dictionary, within the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL).

- **Canonical source text**: [`csl-orig/v02/bur/bur.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/bur/bur.txt) (19,776 entries) — corrections are applied to that file, not stored here.
- This repository holds **development artifacts**: Greek-text insertion, verb identification, and per-issue working files.

## Architecture

| Path | Purpose |
|---|---|
| `greek/` | Greek-text insertion pipeline: `prep1.py`, `digentry.py`, `proof.py`, `updateByLine.py`, `change_1.txt`, `abdata.txt` |
| `verbs01/` | Verb identification: `bur_verb1.txt`, `bur_verb_filter*.py/.txt`, preverb tables, `*_deva.txt` Devanāgarī renderings |
| `burissues/` | Per-issue working directories (issue3–issue5) |
| `DATA_DICTIONARY.md` | Markup tag reference (see **Data format** below) |
| `CITATION.cff` | Citation metadata |

## Key commands

Corrections follow the CDSL `updateByLine.py` pattern, applied against the csl-orig source:

```sh
python updateByLine.py <input> <changefile> <output>
```

Change-file format (paired lines; `;`-prefixed comments):
```
1234 old <original line>
1234 new <replacement line>
```
Supports `new` (replace), `ins` (insert after), `del` (delete). All files UTF-8 (no BOM).

## Data format

Burnouf entries use standard CDSL Sanskrit-lexicography markup. See [DATA_DICTIONARY.md](https://github.com/sanskrit-lexicon/BUR/blob/main/DATA_DICTIONARY.md) for the tag reference.

| Tag | Role | Example |
|---|---|---|
| `<L>NNNN` | Entry begin, with `<pc>` print page-column ref | `<L>1<pc>005,1` |
| `<k1>`, `<k2>` | Primary / secondary headword (SLP1) | `<k1>a<k2>a` |
| `<LEND>` | Entry end | |
| `{#…#}` | Sanskrit text (SLP1) | `{#a#}` |
| `{%…%}` | French gloss / italic display text | `{%akāra.%}` |
| `<ab>…</ab>` | Italic abbreviation | `<ab>priv.</ab>` |
| `<ls>…</ls>` | Literary source citation | `<ls>T.</ls>` |
| `<lang n="greek">…</lang>` | Greek-script reference | `<lang n="greek">α, αν</lang>` |

Annotated example — the first entry of `bur.txt`:
```
<L>1<pc>005,1<k1>a<k2>a            # entry 1; print page 005, col 1; headword "a"
{#a#}¦ {%a%} 1ʳᵉ lettre de l'alphabet sanscrit, nommée {%akāra.%}   # SLP1 headword ¦ French gloss
<LEND>                             # entry end
```

## Dependencies

- Python 3 (correction and pipeline scripts).
- No build step in this repo; XML and web display are generated centrally from `csl-orig` via `csl-pywork`.

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.

_Dr. Mārcis Gasūns_
