# Trim brief — compress the long system-design cards (2026-11-21)

Chi reviewed 20 before/after samples and approved them (「很好 开始搞」). Do the same to every card in your batch.
The samples are the standard: `sources/local/plan/samples-src/sysdesign-trim/before/` and `after/`, and the per-family
rules in `…/sysdesign-trim/REPORT.md`. **Read REPORT.md and at least three before/after pairs of your family first.**

## Your batch

A text file under `sources/local/audit/trim/` lists the card files, one path per line. Edit those files in place and no
others. Originals are backed up in `~/.local/state/sysdesign-trim-backup-20261121/` — never touch the backup.
Resume rule: a card whose answer already passes `scripts/card_len.py --over 700` and shows no template leftovers
(一句话 / 讲明白 sections) is done; skip it.

## Rules for every card

- Only `## A` changes (and `## Q` only where a family rule says so). Frontmatter `id`, `node`, `type`, `step`, `tags` stay.
- No new facts. No fact lost that an interviewer would probe: when a deleted section holds a unique, probe-worthy
  fact (a number, a failure mode, a version, an exception), fold it into 基本回答 or 容易错 as one clause.
- Each conclusion is said once. Content laid out (lists, a table, a diagram), not prose that talks about the content.
- Diagrams stay as they are (inline `<svg>` or mermaid). Code stays only when it is the point and ≤ 25 lines.
- English technical terms stay English; prose is plain spoken Chinese. Section labels keep the form `**标签。**`
  (the deck renders labelled sections as a foldable outline, so keep labels, do not invent `<details>`).
- Target: ≤ 700 Chinese characters per answer (`uv run python scripts/card_len.py --over 700 <files>` prints offenders).
  A card may stay above 700 only when cutting more would lose a probe-worthy fact — list such cards in your report.

## How to work (added after the first batch came back scripted)

- **Card by card, not by a bulk script.** Read each card whole (the backup copy is the original), decide what to keep,
  then write. A script may only help you list sections or measure length.
- A recovered fact is **woven into** the section it belongs to (基本回答 if it is part of the answer, 容易错 only if it
  is a mistake people make). Never append a deleted paragraph as an extra bullet; never leave two bullets saying the
  same thing.
- **`2026 亮点` bullets are kept**: one line, as its own labelled line `**2026 亮点。** …` after 基本回答 (Chi values
  current practice). Shorten it, do not drop it.
- **业务场景 always stays** (the 八股 deck's standing rule: every card has a payment or Douyin scenario), 1–2 lines.
  **举个例子** also stays when it carries numbers or a step-by-step state change, compressed to 2–4 lines; when both are
  short, merge them into one section. Drop the example only when it restates 基本回答.
- **Code** stays when it is the point of the card and ≤ 25 lines (a Lua script, a SQL statement, a config); drop only
  code that repeats what the prose already says.

## Per family

1. **八股追问模板** (`vault/domains/bagu/cards/**`): keep **基本回答** (3–6 lines, the single statement of the answer),
   **2026 亮点** (one line, when the original has one), **先看图** (the figure and its one-line reading), **容易错**,
   **业务场景** (always) and **举个例子** when it has numbers. Delete **一句话**, **讲明白**, **系统设计**, **相关题**;
   **可能问法** survives only as one line when it opens a different angle.
2. **完整解答 stubs** (`hi-qb-*`, `hi-tt-*`: the file has `body: <path>` and no Q/A — its text comes from
   `vault/<path>.md`, the full solution article, which must stay untouched): turn the stub into a standalone card.
   Remove the `body:` line; keep the other frontmatter (including `meta:`). Add `## Q` = the article's question, with
   the first bold header line ending in `｜<the stub's meta text>` (that is what the shared-body mechanism rendered).
   Add `## A` with: **一句话。**, **60 分钟路线。** (the route table or list, ≤ 6 rows), **必讲。** (the must-discuss
   decisions as 问题 → 选择 → 为什么, 3–5 items), **取舍。** (one spoken line each, the ones a senior is probed on),
   **级别期望。** (one line). No 需求 list, no 实体 list, no code, no 运行输出, no 先修 / 同类题.
3. **分步答案** (`hi-ans-*`) and **补充** (`hi-sdx-*`): keep the sections (一句话, 图, 步骤, 故障, 为什么, 数字) with
   3–5 items each; merge adjacent steps; keep only failures that have a mechanism and numbers that support a conclusion.
4. **模拟面试** (`hi-mock-*`, `hi-fix-*`): keep **你说** as points, **常见失分**, and the last whiteboard figure; delete
   **为什么这样说** and earlier whiteboards; keep **面试官可能接着问** but as one line per follow-up (question → the
   one-clause answer) — do not delete it (Chi's choice: fold, not drop).
5. **概念卡** (`hi-c-*`): apply the general rules; these have no fixed template.

## Gates (run before you report)

```
uv run python scripts/card_len.py --over 700 $(cat sources/local/audit/trim/<batch>.txt)   # ideally no output
uv run python scripts/plain_style.py $(cat sources/local/audit/trim/<batch>.txt)           # a "被报告" hit in a hi-qb/hi-tt header is expected; anything new is yours to fix
uv run python scripts/check_mermaid.py $(cat sources/local/audit/trim/<batch>.txt)
uv run trellis --domain sysdesign validate                                                  # 0 errors
```

No Anki, no git, no agents, no web. Final message: cards trimmed, median characters before → after (card_len total
on the backup copy vs now), cards left above 700 and why, facts you folded in from deleted sections (5 examples),
and anything you were unsure about.
