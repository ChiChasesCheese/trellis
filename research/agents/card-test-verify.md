# Test questions written from learning cards — verifier's brief

A writer produced one chunk of test questions, one per learning card (rules: `research/agents/card-test-questions.md`,
read it first). You are the second reader. Assume some questions are flawed, find them, repair them in place.

## Your chunk

- Questions: `sources/local/quiz/<set>-bulk-NN.part1.json` and `part2.json` (set and NN are given in your task).
- The cards: `sources/local/quiz/<set>-todo-NN.md`. When a side is cut off, read the whole card:
  `grep -rl "^id: <source>$" vault sources/local --include=*.md | head -1`.

## Check every question, one by one — not only the ones the writer flagged

0. Do the question, options and `why` belong to this `source` (not a neighbour's)?
1. Is the right option what the card says, and does the question test the card's central point?
2. Is any wrong option acceptable by the card (a design it allows, a slower way that works, a true statement)?
3. Is any wrong option absurd, ruled out by its wording, or not an answer to the question asked?
4. Does a fact appear that is not on the card (a number, a product, a claim)?
5. Can the answer be picked from the wording (the right option echoes the title or question, or stands out by detail)?
6. Is `why` true? Work every example and number (by hand, or `python3 -c` for anything computable).
7. For the `ai` set: does the front use a term a backend engineer would not know, without explaining it?

## Repair

The smallest change that fixes the flaw, addressing the question by its `source`, then re-read it. Keep `source` and
the order unchanged, keep the right option first, keep the limits: run
`uv run python scripts/card_tests.py lint <set> <part file>` after your edits; both parts must pass. Do not rewrite
questions that are fine. Keep helper files in a folder of your own under /tmp. No import, no Anki, no git, no web,
no subagents.

## Report (your final message, nothing else)

- How many questions you checked (it must be all of them) and how many you changed.
- One line per change: `source`: what was wrong → what you changed.
- Questions you could not settle, one line each.
- The lint line of each part after your edits.
