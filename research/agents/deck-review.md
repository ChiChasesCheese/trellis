# Deck review brief (reusable) — judge what to keep, trim, merge, drop

Chi asked (2026-11-21): find cards that are duplicate, trivial (小儿科), filler (废话), too long or too short, and
format problems to normalize, across all Anki decks. `scripts/deck_audit.py` already measured everything a script can
(sizes, lengths, textual duplicates). You judge what needs a reader. **Read-only: change no card, no Anki, no git.**

## Input (all local, under `sources/local/audit/`; never paste private deck text into a web tool)

- `review/<domain>.md` — per domain: a random sample (label `[random]`) then flagged notes (`[flagged]`), plain text.
- `summary.md` (the numbers), `leaves.tsv` (notes per leaf), `overlap.tsv` (leaf names taught in several domains),
  `dups.tsv` (textual duplicate clusters), `notes.jsonl` (every note, for looking one up by id with grep).

## Who the learner is

A senior-track backend/data engineer (fundamentals self-described as weak) preparing senior interviews and long-term
growth. He wants: cards self-contained, concise, content laid out (tables, lists, code), English technical terms with
Chinese prose, no meta talk, no essays. A card is **trivial** if a working mid-level engineer already knows it cold
and no interviewer would probe it (define a variable, what HTTP stands for); foundations he asked to learn from zero
(K8s, AI, psychology) are not trivial just because they are basic.

## Verdict per `[random]` note (so rates extrapolate to the whole domain)

- `keep` — worth its review time as is.
- `trim` — good content, too long: say roughly what share could go (e.g. "cut the 3 extra bullets").
- `split` — one card holds 2+ independent ideas.
- `merge` — overlaps another card or leaf (name it); the pair should become one.
- `drop_trivial` — 小儿科. `drop_filler` — 废话: says little, restates the question, generic advice.
- `drop_stale` — outdated or tied to a finished event (a past interview date, a retired tool).
- `fix` — content fine, format wrong (English-only where Chinese is the rule, meta phrases, broken layout, no answer).

Look at `[flagged]` notes too, but report them separately (they are not a random sample).

## Output: two files per assignment group, in `sources/local/audit/verdicts/`

1. `<group>.json` — exactly this shape, one entry per domain:
```json
{"<domain>": {"sampled": 60, "keep": 0, "trim": 0, "split": 0, "merge": 0, "drop_trivial": 0, "drop_filler": 0,
  "drop_stale": 0, "fix": 0,
  "examples": [{"note": 1790000000000, "verdict": "drop_trivial", "why": "one line"}],
  "norm_issues": ["one line each: a format or convention problem seen in this domain, with how often"],
  "overlaps": ["<this leaf/topic> also taught in <other domain/leaf>: which side should keep it"],
  "recommendation": "one of: keep-all | prune | archive | rewrite | merge-into:<domain> — plus one sentence why"}}
```
   `examples`: up to 8 per domain, the clearest cases, real note ids from the pack. Counts must sum to `sampled`.
2. `<group>.md` — at most 40 lines: what you found, in plain words, most important first.

Final message: the per-domain recommendation lines, and the three findings that would save the learner the most time.
