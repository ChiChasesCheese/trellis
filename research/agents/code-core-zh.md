# Task: give every Code Core card its Chinese text

`skeleton/code-core.yaml` says `lang: en`, `show: zh`: the cards are written in English and each carries a `## zh`
translation that Anki shows. 56 of 397 card files under `vault/interviews/rounds/code-core/cards/` have it; Chi
studies in Chinese, so the other 341 need it (Chi, 2026-11-28).

Read first: `docs/translation-spec.md` (the `## zh` format and rules), five cards that already have `## zh`
(`grep -l '^## zh' vault/interviews/rounds/code-core/cards -r | head -5`), `proposals/WRITING_RULES.md`, and the deck
rules in `AGENTS.md` (English technical terms in parentheses, Chinese prose, remove filler).

Do it card by card, never with a script that rewrites text: for each card without `## zh`, read the English, write
the Chinese below it exactly as the spec says (same structure: question, answer, code blocks unchanged, identifiers
and code untouched, numbers re-checked). Keep the English as it is. Work through branches in skeleton order; after
each branch run `uv run trellis --domain code-core validate` (must stay at 0 errors) and append a line to
`research/agents/code-core-zh.progress` (`<branch> <cards done>`).

Resume rule: skip any card that already has `## zh`; read the progress file first.
Do not touch Anki, do not commit, do not push. Do not spawn agents. When done, report counts per branch, the five
translations you are least sure about (card ids), and any English card that looked wrong (id + one line).
