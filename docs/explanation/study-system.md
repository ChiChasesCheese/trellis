# The study system (Trellis 1.0)

How the pieces fit together since November 2026. The engine (skeletons, cards, build, Anki sync) is described in
`architecture.md`; this page is the layer that decides what Chi studies each day and where each kind of content lives.

## Content: one source per thing

| Kind | Source of truth | Card |
|---|---|---|
| Concept knowledge | a domain: `skeleton/<domain>.yaml` + `vault/<domain folder>/cards/` | one note per card file |
| LeetCode problem | `vault/interviews/core/leetcode/problems/<slug>.md` (one body) | exactly one card, `lct-<slug>`, on its leaf of the 0x3F knowledge tree (`scripts/lc_tree.py`) |
| Design question | its node in `skeleton/sysdesign.yaml`; 完整答案 cards in `…/premium/answer/<page>/` | cards per part (完整答案, 摘要, 考点, 八股关联, 拓展, 补充) |
| Company prep | `vault/interviews/companies/<co>/` (kit pages) + domain `<co>` | company-only cards; everything general goes to a general domain |

Rules that came out of building it:

- **One card per problem.** Lists (Top Interview 150, Blind 75, NeetCode 150, Hot 100, LeetCode_Tops), companies
  (`公司::Amazon`, `公司::Cerebras`), 已做过 and 必读 are **tags** on that card (`scripts/lc_tags.py`), never decks of
  copies. A problem outside 0x3F's lists hangs on a leaf through `sources/local/lc/expand.json`. Our own leaves are in
  `our_leaves.json`. The rules are in `research/leetcode-unify/`.
- **同模式 unfolds only into a body.** A problem named under 同模式 needs its own body, or the item cannot open.
  `research/leetcode-unify/related_missing.py` lists the named problems without one and hangs them on a leaf.
- **Under the Hood** holds algorithm and data-structure material that is not a problem: tool internals, patterns,
  Python idioms, Amazon patterns.
- **Shown in Chinese.** Chi studies in Chinese. A domain written in English with `## zh` translations sets `show: zh`.
  AI material starts from zero (`llm-inference:basics`, `ml`) and defines every term on first use.
- **Pictures.** At least 25% of every deck's cards carry a diagram (`scripts/diagram_share.py`). A diagram is a mermaid
  block or a bare `<svg>` block. Never fence svg: Obsidian shows a fence as code. Design answers put one on every card.
  `scripts/diagram_queue.py` and the 1:37 task backfill old decks in study order.
- **AI in two layers.** Mechanics from zero live in `llm-inference` (`basics`, `ml`, then serving and hardware).
  What an engineer talks about lives in `ai-literacy`: using models, how models improve, agents, benchmarks, the
  industry, AI at work, safety, in priority order inside each node (`research/domains/ai-literacy/BUILD.md`).
- **People and decisions** (`psych`, deck `9 人性与决策`). Findings from psychology, behavioural economics and
  sociology that hold up when repeated, as field → theme → concept, one card per concept: a situation, the finding,
  the real story of how it was found, an evidence grade (强, 中, 弱) and an action. Famous results that failed
  replication have cards too. Sources for every number are in `research/domains/psych/claims-*.md`, never on a card.
- **新进展 at the bottom of a card.** An AI card may end with a dated block that ties its mechanism to a recent
  development, then a folded 想一想 question answered from the card plus the news. Every dated fact is searched for
  when the card is written (`research/domains/llm-inference/NEWS_TASK.md`).
- **Challenge cards.** A leaf's ordinary cards demonstrate. Its challenge card (tag `挑战`, last `step`) gives a new
  situation, grading points and a folded reference answer. `scripts/challenge.py` keeps it suspended (tag
  `挑战::待放出`) until every other card of the leaf has left the learning steps, and the daily run releases it. The
  daily report card shows the 迁移率: the share of challenge cards answered Good or Easy the first time, next to the
  same leaves' review retention. High retention with a low 迁移率 means wording was memorised, not the mechanism.

## Daily decks

| Deck | Built by | What |
|---|---|---|
| 1 今日计划 | `scripts/study_plan.py daily` (3:58) | the plan's system-design / LLD / review cards |
| 2 算法模式识别 | `daily_quiz.py` (`--set recog`) | one recognition question per tree problem, the problem's own card on the back; replaced 今日算法 on 2026-11-21 |
| 3 今日低层设计 | same | LLD by topic |
| 4 碎片速刷 | `scripts/quick_plan.py` | ten-second cards |
| 5 系统设计高频题 | `scripts/deep_dive.py` (inside the daily run) | one design question at a time: mock fixes, then the foundations of every exam point it needs (prerequisites first), then 完整答案 and its other parts |
| 6+, sprint decks | `scripts/company_deck.py` | borrowed cards for an interview: a **role track** (`tracks/*.yaml`) plus a company overlay, or a LeetCode view (`scripts/lc_view.py <tag>`) |

Cards are always borrowed, never copied. A card's home is recorded (`sources/local/plan/*homes.json`), and
`company_deck.py release` sends a sprint deck's cards home. A card belongs to the first sprint deck whose plan names
it, and the daily plan never deals a card a sprint deck holds. New-card order inside a sub-deck is the plan's order,
set by `scripts/reposition_new.py` while Anki is closed (see below).

## Scheduled tasks

| Time (PT) | Task | Does |
|---|---|---|
| 1:37 | Diagram backfill | ~30 diagrams on the cards studied next |
| 3:43 | LeetCode Daily | newly solved problems → body → tree → tags; moves 必读 |
| 3:58 | Study plan daily | tags new problems, exam points, mock fixes, 完整答案 ahead for the next deep-dive question, rebuilds the daily decks, holds and releases challenge cards, answers card notes |

## Anki: what forces a full sync

A schema change, removing many decks, or writing `collection.anki2` directly (pylib with Anki closed) makes Anki
demand a full sync. While the dialog is open, AnkiConnect answers "Collection lifecycle operation is active". To
avoid it:

- use AnkiConnect with Anki running;
- delete notes, but leave empty decks for Chi to remove;
- reposition new cards with pylib only together with a planned upload.

If the dialog appears anyway:

- **Download** keeps the phone's reviews but loses the local change;
- **Upload** keeps the local change but loses phone reviews made since the last sync.

Ask Chi which one. A pylib full download or upload uses the sync key in `prefs21.db`. Always back up the collection
to `~/.local/state/` first.

## Privacy

Public by default. Only what Chi names stays local: NDA material (Headlands), the Braintree work deck, and employer
internals. `private_guard` checks every commit against `~/.config/trellis/private_terms.txt`. Third-party copies stay
in `research/…/raw/` under `.git/info/exclude`.
