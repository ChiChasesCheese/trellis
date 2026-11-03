# Plan — Hello Interview with full access, plus an executable LLD plan (Chi, 2026-11-03)

Durable record: a new session resumes from the state table below. Order: fetch → structure → leaves.

## Layout

```
Hello Interview                                    (Anki deck)
├─ 01 高频真题        qb.{sd,lld}.<question>       先修 · 解答 · 要点        existing + more_selection.json
├─ 02 TikTok          tt.{sd,lld}.<question>, tt.lc.<problem>                existing + every reported TikTok question
├─ 03 系统设计        sd.<section>.<page>.{notes,exam,beyond}                every chapter, in site order
└─ 04 低层设计        lld.<section>.<page>.{notes,exam,beyond}               every chapter, in site order

LLD study plan        vault/interviews/core/low-level-design/                README · roadmap · plan.json · drill.py · problems/
```

Each chapter: 摘要 (one card per section, checked against the page's headings), 考点 (how it is tested), 拓展 (senior material the page omits).
A problem breakdown's first summary card is the whole answer, the same foldable 60-minute format as the question bank.

## What is public

The repo is public and the site is commercial. Anything written from logged-in pages or the logged-in bank stays out of git:
`sources/local/hello-interview/premium/`, `vault/domains/hello-interview/cards/premium/`, `vault/domains/hello-interview/premium/`. They reach Chi through the
local vault and Anki. Tracked: tools, agent rules, the skeleton (titles only), and the LLD plan and drills (own statements and code, not based on those pages).

## Tools

- `chrome_fetch.py`: saves pages through Chi's logged-in Chrome (`pages`, `questions`).
- `gen_skeleton.py`: skeleton, moves cards to their leaves, writes stubs.
- `check_course.py`: every page has its cards and every heading is accounted for.

## Question bank cut

474 system design questions (4,765 reports), 73 object-oriented (171 reports). Take 70% of reports per type (47 and 29 questions), plus every TikTok question.
A question with a course breakdown is answered by that chapter; one with an existing answer or drill reuses it; the rest get a new answer (`more_selection.json`).
Everything below the cut goes to a local index note mapping each question to the nearest covered material.

## Agents (at most 3 at a time, one owner per folder, no commits)

| Group | Rules | Deliverable | State |
|---|---|---|---|
| K1, K2 | `KIT_AGENT.md` | 13 new runnable drills | |
| Q1, Q2 | `QB_MORE_AGENT.md` | 18 new answers with 要点 cards, LC 1926 body | |
| C1…Cn | `COURSE_AGENT.md` | 95 chapters | |
| I1 | `INDEX_AGENT.md` | index of the whole design bank | |

The orchestrator writes the roadmap and `plan.json`, reviews every group, commits tracked work, pushes to Anki.

## Done when

`check_course.py` reports 95/95, every selected question has an answer and 要点 cards, every drill's reference is green and its empty starter is red, `validate` has 0 errors, 0 dead links, and the
new cards are in Anki in the intended order.

## Coding craft (Chi, 2026-11-03)

Goal: much stronger core coding and deeper Python. Branch `craft` of domain `python` (tracked, based only on our own drills): idioms, cross-problem patterns, architecture, tied across LeetCode, LLD and system design.
Order: `research/domains/python/craft_index.py` → agent per `CRAFT_MINE_AGENT.md` → `craft_map.json` reviewed by the orchestrator → skeleton → agents per `CRAFT_CARD_AGENT.md`. The LLD plan's stages then point at these sub-decks.

## Queue

Three agents at once, counting any agent resumed for rework. Next, in order: Q2, Q3 (needs K2), M (mining, needs K1 and K2), C02…C13, X (craft cards after M is reviewed), I1.

State 2026-11-03: drills K1 K2 done, committed. Q1 Q2 done. C01 C02 reviewed. Craft map reviewed (90 leaves, 6 card groups in `research/domains/python/craft_group_X*.txt`). Next after the running agents: F (`research/domains/python/FIX_AGENT.md`) before the craft cards, then alternate X1…X6 with C05…C13, then I1.
