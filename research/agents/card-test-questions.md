# Test questions written from learning cards — writer's brief

Chi studies through test decks: the front is one choice question answered by tapping; the back shows the answer, why,
and then the learning card it was written from, in full. He meets the question **before** he has studied the card, so a
miss sends him straight to the card on the back. You write **one question per source card**.

Decks: `3 低层设计测验` (set `lld`, from his low-level-design deck) and `AI 测验` (set `ai`: AI 通识, LLM 推理, AI 应用工程,
ML 与 LLM 系统设计). Chi is a senior backend engineer; for the `ai` set assume **no AI or ML background**.

## Your chunk

- Input: `sources/local/quiz/<set>-todo-NN.md` (set and NN are given in your task), about 60 source cards. Per card:
  `source` (the card's id), 位置 (where it sits in the deck), 正面 and 背面 (its two sides as plain text, cut short).
  When a side is cut off before the point is clear, read the whole card:
  `grep -rl "^id: <source>$" vault sources/local --include=*.md | head -1`.
- Output: two files, half of the cards each, in the input's order:
  `sources/local/quiz/<set>-bulk-NN.part1.json` and `part2.json`. Each is a JSON array.
- After writing each part run `uv run python scripts/card_tests.py lint <set> <part file>` and fix it until it prints
  `N questions pass the lint`. Nothing else is run: no import, no Anki, no git, no web, no subagents.
- **Resume rule:** a part file that exists and passes the lint is done; skip it.
- **Card by card.** Read the card, decide what its one central point is, then write. No generator scripts, and no
  script that patches questions by position: fix the one question the lint names, by its `source`, and re-read it.
- Keep helper files in a folder of your own under /tmp (for example /tmp/<set>NN/): other agents use /tmp too.

## One question

```json
{"source": "problems-notification-service-policies-before-the-queue",
 "title": "通知服务：偏好与限额的判断时机",
 "statement": "通知要过用户偏好、静默时段、频次上限、模板渲染几道判断，之后进队列由后台发送。",
 "question": "这些判断放在哪一步做？",
 "point": "策略判断放在入队前",
 "options": ["入队前全部判完，通过的才入队", "发送时再判，入队只管排队", "偏好入队前判，频次上限发送时判"],
 "correct": 0,
 "why": "重试不必再走一遍限额，否则一条通知会被自己的重试重复计数；调用方也能立刻知道为什么没发。"}
```

- `source`: copy the card's id. `title`: what the card is about, at most 44 characters, without giving the answer.
- `statement` (optional, at most 100 characters): the scene someone needs to answer; leave it out when the question
  stands alone. `question`: at most 90 characters; one probe on the card's **central point**: pick the design, predict
  what happens, find the step that breaks, choose the number. Never "which statement is true" or "what does the card say".
- `options`: 3 or 4, each at most 34 characters, **the right one first** (the importer shuffles), all at the same level
  of detail. A multi-select (`"correct": [0, 1]`, 4 or 5 options) only when the point is a combination.
- `why`: at most 90 characters: why the right one is right and what breaks the most tempting wrong one.
- `point`: the lesson in at most 16 characters.
- Plain Chinese; English technical terms stay English. For the `ai` set every term the front uses must be one a
  backend engineer knows, or be explained in the statement in a few words.

## The rules that decide whether a question is accepted

1. **It tests the card's central point**, the thing a senior interviewer would probe, not a side detail or a number
   picked at random. A card that is a table or a list: ask the decision the table supports.
2. **Facts come from the card.** The right option and `why` must be what the card says. No number, product name or
   claim that the card does not contain.
3. **Every wrong option is a real mistake and actually wrong by the card**: the mistake the card warns about (易错点,
   反例, 「常见错误」), the neighbouring concept in the same group, the reversed claim, the right idea with one step
   missing, a number ten times off. Not absurd, not ruled out by its own wording, not a contradiction of the question.
4. **Never list an acceptable answer as wrong**: a second design the card allows, a slower way that still works, a true
   statement. If the card accepts two answers, put both into the right option or ask about something else.
5. **Not answerable from the wording.** The right option must not echo the title or the question, and length must not
   give it away: in a file the right option may be the longest in at most 40% of the questions and the shortest in at
   most 40%, and never more than 1.25 times the longest wrong one. Do not shorten the right option until it is
   cryptic; give the wrong ones the same level of detail.
6. **Self-contained front.** No "见上", "原卡", "本卡", no reference to a figure the learner cannot see.
7. Every option must answer the question that is asked. No "以上都对 / 都不对", no Markdown, no code blocks; short
   inline code such as `dict.get` or `O(n)` is fine.
8. Work every claim and example in `why` before writing it (by hand, or `python3 -c` for anything computable).

## Report (your final message, nothing else)

- The lint line of each part.
- Up to 10 questions you are least sure of: the `source` and one sentence (an option that may be acceptable, a fact
  you could not find on the card, a card whose central point you had to guess).
