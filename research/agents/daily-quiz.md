# Daily quiz brief — test cards written from what Chi studied

Chi (2026-11-21): a separate daily quiz deck, independent of the learning flow, that may steer it. It holds the most
important things, written from his cards and leaves, the way an interviewer would probe the theory. Answered questions
go back to the topic's 考察题 deck and serve later as a fast recap. 「内容一定要简洁，能真的考察到是否掌握。」

## The run (each morning, in this order)

```
uv run python scripts/daily_quiz.py settle          # yesterday's answered questions: results recorded, cards moved to 考察题
uv run python scripts/daily_quiz.py score --weak    # read it: topics he got wrong come first in what you write today
uv run python scripts/daily_quiz.py pick            # → sources/local/quiz/pick-<date>.md (topics + their source cards)
# write sources/local/quiz/questions-<date>.json (rules below)
uv run python scripts/daily_quiz.py import sources/local/quiz/questions-<date>.json
```

`import` lints every question and imports nothing if one fails: fix and run it again. No git, no other deck is
touched; everything stays under `sources/local/quiz/` (system-design sources are private).

## One question

```json
{"topic": "<copy from the pick file: domain::key>", "crumb": "<topic · sub-point, ≤ 14 chars>",
 "point": "<what it tests, ≤ 16 chars>", "source": [<card id from the pick file>],
 "question": "…", "options": ["correct", "wrong", "wrong", "wrong"], "correct": 0, "why": "…"}
```

Put the correct option first (`"correct": 0`); the importer shuffles the order.

- **It tests, it does not teach.** One probe an interviewer would ask after the candidate's first answer: predict what
  happens, pick the fix, compute a number, name the failure, choose between two designs. Never "what is X" or
  "which statement is true".
- **Answerable only by someone who understands the mechanism.** If a careful reader could pick the answer from the
  wording alone, rewrite it.
- **Wrong options are real mistakes**: take them from the source card's 易错点 / 常见失分, a neighbouring concept, or an
  off-by-a-power-of-ten number. Each must be something a half-prepared candidate would say. No "all / none of the
  above", no joke options.
- **Short.** Question ≤ 90 characters, each option ≤ 34, 3 or 4 options of similar length, `why` ≤ 90 characters and
  it must say why the right one is right and why the most tempting wrong one is wrong. No preamble, no restating.
- **One concept per question**, from the topic's source cards only — add no fact the cards do not hold. For a
  LeetCode topic ask about the idea (invariant, why this structure, the edge case that breaks the naive version),
  never "what is the output" of a long program.
- English technical terms stay English; the rest is plain Chinese. No Markdown inside the fields.
- One question per topic in the pick file; two when the pick marks it 答错过 and the cards hold two distinct probes.

## After the run

Report in three lines: questions written, yesterday's score (correct / answered), and the weakest topic with one
sentence on what to relearn. Do not add learning cards; that is a separate decision of Chi's.
