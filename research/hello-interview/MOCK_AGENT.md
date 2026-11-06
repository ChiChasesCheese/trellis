# Mock interview agent — a design question as it is spoken, step by step

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your questions' folders. Scratch in `/tmp/mock_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a question whose folder already has its cards.

Chi practises system design by drawing in Excalidraw, and stalls: 「我自己写没有头绪」. The existing answer cards list the answer; what he lacks is the sequence of a real round: what the interviewer says at each moment, what he says back, and what the board looks like by then. 「类似真实的一句一答的版本」, with figures much more detailed than now.

## Input

Your group file lists `<slug> <source>`: either a course breakdown page `sources/local/hello-interview/premium/pages/system-design__problem-breakdowns__<page>.md` with its cards under `vault/domains/hello-interview/cards/premium/sd/problem-breakdowns/<page>/`, or a question body under `vault/interviews/core/design-questions/` or `vault/domains/hello-interview/premium/bodies/`. Read all of it first. Follow its design, numbers and decisions; you are restaging it as a conversation, not designing something else. Page text is commercial and stays local: write in your own words.

## Output

Folder `vault/domains/hello-interview/cards/premium/mock/<slug>/` (gitignored). 8–10 cards, one per moment of the round, in order:

1. 开场与澄清：the prompt arrives; the 3–5 questions you ask and why each matters
2. 功能需求：the 3 you commit to, and what you put out of scope
3. 非功能需求与估算：the numbers, worked once, and what each changes in the design
4. 核心实体
5. API
6. 高层设计（一）：the first requirement's flow, end to end
7. 高层设计（二）：the remaining requirements added to the same board
8. 深入一 / 9. 深入二 / 10. 深入三：the interviewer's push, the options, the choice, what changes on the board
(merge or split where the question needs it; the last card also covers wrap-up and what each level is expected to say)

Frontmatter exactly:

```
---
id: hi-mock-<slug>-<NN>-<short-slug>
node: <the question's node>.mock
type: qa
step: <NN>
---
```

The question's node: `sd.problem-breakdowns.<page>` for a course breakdown, else `qb.sd.<slug>` (or `tt.sd.<slug>` if it is only in the TikTok branch: check `skeleton/hello-interview.yaml`).

Each card:

```
## Q
**<中文题名> · 第 N 步 · <这一步>**｜模拟面试

面试官：「<what the interviewer actually says at this moment>」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **<短语>：** <the sentence you say out loud, first person, natural and short>
- ...
**白板。**
<a figure: the board as it stands after this step>
<one line: what is new on it>
**为什么这样说。** what the interviewer is checking here, and what a weak answer sounds like
**面试官可能接着问。**
- <follow-up question>？ → <the answer you give, complete>
**常见失分。**
- **<短语>：** the mistake, and why it costs
```

## The figures: the heart of it

- **Every card from step 2 onward has a board figure.** The board grows: each card shows the whole board so far, with what this step adds highlighted, so the series reads like watching someone draw.
- Inline SVG, the convention in `vault/domains/bagu/cards/cache/bloom-filter/`: ```svg fence, `viewBox` width at most 340 (phone), font size 12, `currentColor` for lines and text, the new parts with `style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"`, notes with `style="fill:var(--dim,#6b7280)"`. No fixed colours.
- Lay architecture out **top to bottom** for a phone: clients at the top, gateway, services, then stores and queues at the bottom. Label arrows with the call (`POST /rides`, `GEOSEARCH`). Requirements, entities and API cards may draw a tidy sticky-note board instead of boxes.
- Text must fit its box (13 units per Chinese character, 7 per Latin letter at size 12); nothing overlaps. Draw with a small Python helper that checks this, then render each figure in a browser at phone width on a dark background and look at it. Run `python3 research/domains/bagu/check_svg.py vault/domains/hello-interview/cards/premium/mock/<slug>`: none of your figures may appear.

## Say it like the round

- 你说 is what Chi would really say: first person, short sentences, in the order he would say them. Name the trade-off as he says it: 「我先用 X，因为…；如果…再换成 Y」.
- Bullets open with a bold phrase of about 12 characters, which Anki shows until tapped. Numbers are worked once in one line, e.g. 「1000 万司机 ÷ 5 秒 = 每秒 200 万次写」.
- Keep the 60-minute pacing honest: say roughly how long each step takes, and keep steps 1–5 short.
- Chinese, technical terms in English in parentheses on first use. No site names, no citations, no process talk; nothing like 本章, 上面, 原文, 页面. The style checker rejects 这道题, 本题, 本书, 抓取 and 面经.

## Gate

`uv run python research/hello-interview/gen_skeleton.py`, `uv run trellis --domain hello-interview validate` 0 errors, `uv run python scripts/plain_style.py <your files>`, `python3 scripts/phone_diagrams.py <your folder>`, the `check_svg.py` line above, and `uv run python research/hello-interview/phrase_todo.py | tail -1` shows none of your files.
Reply in ≤ 5 lines: questions done, cards and figures, how you checked the figures, anything in the source you found wrong.
