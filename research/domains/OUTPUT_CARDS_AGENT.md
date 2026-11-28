# 读代码说输出 — writer's brief

Chi asked (2026-11-27): cards that show a short piece of code and ask **what it prints**, with the learning material on
the back, so that he understands how and why a language behaves this way: closures in loops, scoping, mutation,
equality, dispatch, initialisation order, overflow. They live in the general decks — Python in the `python` domain
(branch `output`), Java and cross-language comparisons in the `pl` domain (branch `output`) — and are also borrowed by
his Millennium sprint deck. Read the branch you are given in `skeleton/python.yaml` or `skeleton/pl.yaml`.

Work in `/Users/chiserver/sessions/trellis`. Local only: no web, no git, no Anki, no subagents. Card by card: pick
the trap, write and **run** the snippet, then write the card. Scratch in `/tmp/out_<your batch>/`, deleted at the end.

## Installed

Python 3.14 (`python3`), Java 25 (`java File.java` runs one file), Go 1.27 (`go run`; to show pre-1.22 loop variables,
put the file in a module whose `go.mod` says `go 1.21`), Rust 1.99 (`rustc` / `rustc -O`), Node 26, clang++ (`-std=c++23`).
**Every output on a card is the real output of running it**, with the version when it matters ("Python 3.14", "Go 1.22
起"). Never write an output you did not see. Undefined behaviour in C++ is described as undefined, never as a printed
value.

## Files

- python: `vault/domains/python/cards/output/<id>.md`, id `py-out-<leaf>-<short-name>`, e.g. `py-out-scope-late-binding`.
- pl: `vault/domains/pl/cards/output/<id>.md`, id `pl-out-<leaf>-<short-name>`, e.g. `pl-out-cross-closures-loop`.

```
---
id: <id>
node: <leaf id, e.g. output.scope>
type: qa
step: <1, 2, 3 … within the leaf, easiest first>
---
## Q
**<短标题>**｜读代码说输出

```python
<snippet, 4–15 lines, nothing else on screen needed to answer>
```

输出什么？
```

Each branch also gets **one map card on the branch node** (`node: output`, id `py-out-0-map` or `pl-out-0-map`,
step 1): `**一句话。**`, one diagram of the leaves (rules below), `**关键直觉。**` 2–4 bullets — the few ideas that
explain most of these outputs (in Python: names are labels bound to objects, evaluation happens at definition time
versus call time, …).

## The answer

In this order, each a bold label line:

- `**输出。**` the exact output in a code block.
- `**为什么。**` 2–5 bullets that walk the interpreter or compiler through the snippet: which object a name points to,
  when an expression is evaluated, which method the compiler picks. Where a picture helps (names pointing at shared
  objects, a call order), one mermaid diagram instead of words.
- `**语言为什么这样设计。**` 1–3 bullets: the rule in the language reference, the reason behind it (performance,
  simplicity, compatibility, a deliberate trade-off), and how one or two other languages chose differently. This is
  what Chi asked for; make it real, not a slogan.
- `**怎么写才对。**` the idiom or fix in one short code block or one line.
- `**面试里一句话。**` one English sentence he could say when asked.

Each card teaches **one** behaviour (two closely linked at most). A family of cards on one leaf goes from the classic
case to the variations people get wrong. Cover the leaf's summary in the skeleton across 4 cards (3 for a narrow leaf).

## Rules

- Chinese prose, English technical terms in parentheses at first use; code identifiers as they are.
- Self-contained: every term is explained on the card where it is used; no 「上一张卡」, no cross references.
- No tables. No headings inside the answer. ≤ 450 汉字 of prose (code and diagrams do not count).
- Diagrams: `flowchart LR` with first line exactly
  `%%{init: {"flowchart": {"wrappingWidth": 320}, "themeVariables": {"fontSize": "18px"}}}%%`, at most three columns,
  ≤ 12 boxes, labels ≤ 10 字 and quoted; or `sequenceDiagram` with first line exactly
  `%%{init: {"sequence": {"mirrorActors": false}}}%%`, ≤ 4 participants, ≤ 8 messages.
- No annotations of any kind: no 「（推断）」「待确认」, no talk about sources, the card or the reader.
- Do not duplicate an existing card: before each leaf, `grep -rl` the domain's cards for the trap's key words (for
  python: `vault/domains/python/cards/`; e.g. the late-binding closure and mutable default argument already have
  concept cards — your card is the output question, so link the idea but ask it as a fresh snippet).

## Gate

`uv run trellis --domain <python|pl> validate` 0 errors; `uv run python scripts/check_mermaid.py <your files>` renders.

## Report (at most 8 lines)

Cards per leaf; any snippet whose output surprised you or depends on the version.
