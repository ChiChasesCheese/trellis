# Ordering cards inside a leaf — instructions for one agent

You are given a list of prompt files `proposals/steps/<domain>/<branch>.prompt.md`.
For each one, produce `proposals/steps/<domain>/<branch>.json` next to it.

## For each prompt file, in order

1. **Resume rule.** If `<branch>.json` already exists, run the check below. If it
   passes, skip this branch. If it fails, fix that file rather than starting over.
2. Read the prompt file fully. It contains the ordering rules, every topic (leaf)
   of the branch, and each topic's cards (id, question, start of the answer).
3. Decide the teaching order of the cards **inside each topic**, following the
   rules in the prompt. Think about what a learner must already understand to
   make sense of each card. Do not order topics against each other; only the
   cards within a topic.
4. Write `<branch>.json`: one JSON object, `{"<leaf id>": ["<card id>", ...], ...}`,
   containing **every topic in the prompt file**, each with **every one of its
   card ids exactly once**. Plain JSON only — no code fence, no comments.
5. Check it (from the repository root, `/Users/chizhang/Code/trellis`):

   ```
   uv run trellis --domain <domain> steps --import proposals/steps/<domain>/<branch>.json --check
   ```

   It prints `ok: N leaves, M card(s)` or lists exactly which id is missing,
   duplicated, or under the wrong topic. Fix and re-run until it prints `ok`.

## Rules

- Write only your own `<branch>.json` files. Do not edit card files, skeletons,
  code, or any other file. Never run the command without `--check`.
- Do not run any `git` command. Do not start other agents.
- Copy card ids exactly as they appear in backticks in the prompt.
- When finished, reply with one line per branch: `<branch>: ok N leaves, M cards`,
  copied from the check output. If a branch could not be made to pass, say so
  and paste the error.
