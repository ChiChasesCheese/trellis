# Daily quiz brief — test cards written from what Chi studied

Chi (2026-11-21): a separate daily quiz deck, independent of the learning flow, that may steer it. It holds the most
important things, written from his cards and leaves, the way an interviewer would probe the theory. Answered questions
go back to the topic's 考察题 deck and serve later as a fast recap. 「内容一定要简洁，能真的考察到是否掌握。」

## The run (each morning, in this order)

```
uv run python scripts/daily_quiz.py settle          # yesterday's answered questions: results recorded, cards moved to 考察题
uv run python scripts/daily_quiz.py score --weak    # read it: topics he got wrong come first in what you write today
uv run python scripts/daily_quiz.py settle --set recog   # 模式识别: record what he answered there too
uv run python scripts/daily_quiz.py pick            # → sources/local/quiz/pick-<date>.md (20 topics + their source cards)
# write sources/local/quiz/questions-<date>.json (rules below)
uv run python scripts/daily_quiz.py import sources/local/quiz/questions-<date>.json
```

`import` lints every question and imports nothing if one fails: fix and run it again. No git, no other deck is
touched; everything stays under `sources/local/quiz/` (system-design sources are private).

## One question

```json
{"topic": "<copy from the pick file: domain::key>", "crumb": "<topic · sub-point, ≤ 14 chars>",
 "point": "<what it tests, ≤ 16 chars>", "source": [<card id from the pick file>],
 "title": "LC 560 和为 K 的子数组", "statement": "整数数组（含负数），统计和为 k 的连续子数组个数。",
 "question": "…", "options": ["correct", "wrong", "wrong", "wrong"], "correct": 0, "why": "…"}
```

Put the correct option first (`"correct": 0`); the importer shuffles the order. Several correct options:
`"correct": [0, 1]` makes it multi-select (2 or more, never all).

- **An algorithm question carries the problem** (Chi, 2026-11-21: a number and a name are not enough to remember it):
  `title` = `LC <n> <name>`, `statement` = what the problem asks in one or two lines (≤ 100 characters), then the
  question. System-design questions need neither.
- **It tests, it does not teach.** One probe an interviewer would ask after the candidate's first answer: predict what
  happens, pick the fix, compute a number, name the failure, choose between two designs. Never "what is X" or
  "which statement is true".
- **Answerable only by someone who understands the mechanism.** If a careful reader could pick the answer from the
  wording alone, rewrite it.
- **Wrong options are real mistakes**: take them from the source card's 易错点 / 常见失分, a neighbouring concept, or an
  off-by-a-power-of-ten number. Each must be something a half-prepared candidate would say, and each must be
  actually wrong under the problem's stated constraints (a slower but valid approach is wrong only when the
  statement rules it out). No "all / none of the above", no joke options.
- **Short.** Question ≤ 90 characters, each option ≤ 34, 3 or 4 options of similar length, `why` ≤ 90 characters and
  it must say why the right one is right and why the most tempting wrong one is wrong. No preamble, no restating.
- **One concept per question**, from the topic's source cards only — add no fact the cards do not hold. For a
  LeetCode topic ask about the idea (invariant, why this structure, the edge case that breaks the naive version),
  never "what is the output" of a long program.
- English technical terms stay English; the rest is plain Chinese. No Markdown inside the fields.
- **20 questions a day**: one per topic in the pick file; two when the pick marks it 答错过 and the cards hold two
  distinct probes.

## 模式识别 (set `recog`) — one recognition question per LeetCode problem

Chi's gap is seeing which technique a problem calls for. Each problem on the algorithm tree gets one question in the
deck `2 算法模式识别`: title, statement, then 「该用哪种思路？」 (or 「最直接的判断是什么？」 for an insight problem, or a
multi-select 「需要哪几样配合？」). The options are concrete approaches, the wrong ones being the patterns a learner
would reach for by mistake; `why` names the signal in the statement that points to the right one and what breaks the
tempting one. The card's crumb is always 模式识别 and the deck deals in random order — the topic would give the answer
away, so never put the pattern in the title or statement. Import with `--set recog`; `score --set recog` lists the
missed problems (→ `sources/local/quiz/recog-missed.json`, which the LeetCode plan should bring back first).
Samples Chi saw: `sources/local/quiz/recog-sample-2026-11-21.json`.

## After the run

Report in three lines: questions written, yesterday's score (correct / answered), and the weakest topic with one
sentence on what to relearn. Do not add learning cards; that is a separate decision of Chi's.
