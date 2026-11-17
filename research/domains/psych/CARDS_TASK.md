# Task: cards for the `psych` domain (人性与决策)

Repo: `/Users/chiserver/sessions/trellis`. Domain `psych` (`skeleton/psych.yaml`). Today is 2026-11-17.

The reader is a software engineer in his late twenties in the Bay Area. He asked for the findings of psychology,
behavioural economics and sociology that hold up under scrutiny and change how a person runs his life, written so
that each card is a real story he enjoys reading, the evidence behind it, and something he can do this week. His
words: 不要心灵鸡汤，要实证研究过的结论和实践指南；卡片最好有实际的故事，这样更好读；不要牵强附会。

Your prompt names your group letter. `research/domains/psych/anchors-<G>.md` lists your cards in order: one card per
entry, with the node id, the file path, the evidence grade and an *anchor* (the study, the numbers and the story to
start from). You write exactly those cards and nothing else.

## Steps

1. **Resume rule.** A card file that already exists is done: do not rewrite it. Three exist as models. Work down
   your list in order and write each card file as soon as that card is finished.
2. **Read the three model cards first**: `vault/domains/psych/cards/judge/psy-judge-loss-aversion.md` (svg figure),
   `vault/domains/psych/cards/self/psy-self-rumination.md` (mermaid loop),
   `vault/domains/psych/cards/evidence/psy-evidence-ego-depletion.md` (a famous claim that failed). Match their
   length, tone and layout.
3. **Check before you write.** Load the tools with ToolSearch `select:WebSearch,WebFetch`. The anchor was written
   from memory and marks doubtful numbers with `(check)`; treat every number in it as unverified. For each card
   confirm the story and each number you put on the card against the paper (abstract, PubMed, the journal page, the
   author's page) or two independent reliable summaries. Rules:
   - A number, a year, a sample size, a name goes on the card only when confirmed. One you cannot confirm is left
     out or replaced by words (「约一半」 only if a source says so). Never invent a figure, a quote or an anecdote.
   - Where the source disagrees with the anchor, the source wins. Look for the newest replication or meta-analysis
     and for known criticism; if what you find changes the evidence grade, change the line on the card.
   - After each card append one row to `research/domains/psych/claims-<G>.md`:
     `| card id | each claim on the card that carries a number or a name | source URL(s) | what differs from the anchor |`
     (create the file with a header row first). This file is the audit trail; URLs go here, never on a card.
4. **Run the gate** (below) and reply.

## Card format

File path and id are given in your anchor list. Frontmatter exactly:

```
---
id: psy-judge-anchoring
node: judge.dual.anchoring
type: qa
step: 1
tags: [证据强]
---
```

`tags`: one of `证据强` (grade A), `证据中` (B), `证据弱` (C), plus `十日终焉` where the anchor entry lists it.

```
## Q
<一个处境或一个可答的问题，1–3 行>

## A
**概念名（English term）：一句话，就是全部答案。**

<图：只在它能说明问题时放>

**故事。** <3–5 句：一件真实发生的事>

- **证据 · 强：** <一两句>
- **谁在用：** <一句；没有确凿的例子就不要这一条>
- **动手：** <一到两句>
```

- **Q.** A concrete situation from an adult's life, ending in a question he can answer by understanding, never
  「什么是 X」. Draw on: work and code review, interviews and job change, pay negotiation, studying with flashcards
  and AI tools, saving and investing, gym and diet, sleep, drinking, making friends in a new city, dating, family,
  reading news. Second person (「你」). For a grade C card the question states the popular claim and asks what the
  original study was and what happened when it was repeated. Do not put the concept's name in the question unless the
  situation alone would be ambiguous.
- **Lead sentence.** Bold. The concept's Chinese name, the English term in full-width parentheses, a colon, then the
  finding in one sentence a friend would understand.
- **故事。** This is the heart of the card. One real event told as a scene: who, where, what they did, what came out,
  with the one or two numbers that make it stick. The original experiment is usually the best story (the stooges in
  Asch's room, the day-care that started fining parents, the earthquake two weeks after the questionnaire). A
  historical event or a company's documented decision is as good. Rules: it happened and you confirmed it; names,
  year and place are in it; no composite characters, no 「小明」, no 「有一位经理」; nothing that only illustrates
  loosely. If the famous version of the story is itself wrong (38 witnesses, the boiling frog), say what actually
  happened.
- **证据 · 强 / 中 / 弱：** how far to trust it: replications, a meta-analysis and its effect size, where it stops
  working, who it was tested on. One or two sentences. For grade C, what failed.
- **谁在用：** a documented use by a named company, institution, profession or policy. Leave the bullet out rather
  than stretch. You may replace it by a differently named bullet when the card needs one (`**分辨：**` to tell it
  from a look-alike, `**站得住的部分：**` on a grade C card).
- **动手：** what he does, with a trigger: 「下次……的时候，先……」, an amount, a time. Something he can start this
  week. Not an attitude (「保持开放心态」), not 「意识到这一点」. Where the finding is a warning about a claim,
  the action is what to do instead.
- **Tags for 十日终焉.** The request grew out of the web novel 《十日终焉》, whose hero 齐夏 names such laws while
  solving deadly games. For a card tagged `十日终焉` you may add one last line `**《十日终焉》里：** …` only if a web
  search finds the scene where the novel uses it and you can state it in one sentence. If you do not find it, leave
  it out; never make a scene up.

## Writing rules

- **Chinese, spoken.** Short sentences. Technical terms in English in full-width parentheses on first use.
  Researchers' names stay in Latin letters (Kahneman, Nolen-Hoeksema). Numbers as digits.
- **Length.** The answer is at most about 330 Chinese characters, not counting a figure or a table. Read on a phone
  in under a minute. If it does not fit, cut the second example, not the story.
- **Self-contained.** No 「见上一张」「如前所述」; a term another card explains is glossed in a few words here.
- **Name the study, do not gesture at it.** 「研究表明」「科学家发现」「据报道」 are banned: say who, when and what
  they did, or say nothing. No URLs, no 「来源」, no journal volume numbers. A journal's name is fine when it helps.
- **No process talk.** Never how you found something or that you could not find it.
- **No comfort talk.** No encouragement, no 「你并不孤单」, no moral at the end, no 「记住」「所以说」「总之」.
  No diagnosis and no disclaimers: state what was measured and what to do.
- **Honest size.** Give the effect size or the percentage when the source has one, and say when it is small. Do not
  call a correlational study causal. Do not round 36% to 「近一半」.
- **Tables** for same-shaped comparisons (before and after, group against group). Keep to 3 columns where you can.
- **Figures.** At least 30% of your cards carry a figure, where a loop, a curve, a flow or a 2×2 is the point:
  a mermaid block (`flowchart TB` only, at most 10 nodes, every label quoted and at most 14 characters, no
  parentheses or colons inside a label) or a bare `<svg>` block (viewBox about `0 0 340 210`, `currentColor` strokes
  and fills, font-size 12, blank line before and after, none inside, never fenced). A table is not a figure. A figure
  must show something true: a curve's shape follows the data, not decoration. Check every mermaid block renders:
  write its body to `/tmp/psy_<G>.mmd`, then
  `uv run python -c "import sys; from trellis.build import _mermaid_svg; print(bool(_mermaid_svg(open(sys.argv[1]).read())))" /tmp/psy_<G>.mmd`
  must print `True`.

## Rules added after reviewing the first 78 cards

- **Q is short.** At most about 80 Chinese characters: one or two sentences of situation, then at most two
  questions. Do not list three or four questions and do not preview the answer's structure.
- **Hard length.** Above 360 characters the answer is too long: cut the second study from the story, or move one
  number out of the evidence line.
- **Median is not mean.** Write 「中位数」 when the paper reports a median (Lally's 66 days), 「平均」 for a mean.
  「提高 81%」 and 「高 81 个百分点」 are different claims: copy the paper's.
- **A therapy session is 「一次治疗」**, not 「一节课」. A study's participants are 「参与者」 or what they were
  (students, nurses), not 「被试」.
- **Some groups had already found** that a classic in the anchor no longer holds (Ariely & Wertenbroch's deadlines,
  the Capilano bridge). Keep doing that: say so on the card in the evidence line, in one clause.
- `记住`, `有研究`, `研究发现` (without naming whose) are flagged by the review script: rephrase.

## Search budget (added for the third wave)

All agents of one turn share a limit of 200 web searches, and the account's usage window is short. So:

- At most 3 WebSearch calls per card. Prefer WebFetch on a page you can name without searching: the PubMed or
  journal abstract page, the DOI link, the author's lab page, the Wikipedia article on the study (good for sample
  sizes and percentages, and it cites the paper).
- One search should confirm several of a card's numbers at once: put the authors, the year and the key figures in
  one query.
- When searches run out, stop writing new cards and report which ones remain. Never write a card from memory.
- Do not re-verify cards that already exist. Do not read other groups' cards.

## Gate

- `uv run trellis --domain psych validate` shows 0 errors (warnings about leaves without cards or readings are fine).
- `python3 scripts/plain_style.py vault/domains/psych/cards/<field>/<your files>` prints `ok` (pass the files, not
  the folder; one call per field folder with a `psy-<field>-*.md` glob is fine, complaints about files that are not
  yours are not your problem).
- `python3 scripts/phone_diagrams.py vault/domains/psych/cards/<field>` prints `ok`.
- Then `git checkout -q uv.lock`.
- Do not commit, do not touch Anki, do not edit the skeleton, `tree.txt`, the model cards or another group's files.
  No subagents. Shell steps are plain single commands (no heredocs, no loops, no `$var`); write helper scripts with
  the Write tool under `/tmp/` and run them.

## Reply (at most 8 lines)

- cards written and cards with a figure;
- every card whose evidence grade you changed, with the reason in a few words;
- the five claims you are least sure of, each with its card id;
- anything left out because it could not be confirmed.
