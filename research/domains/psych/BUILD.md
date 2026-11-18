# psych (人性与决策): build record

Goal (Chi, 2026-11-17): a knowledge tree and an Anki deck of the concepts from psychology, behavioural economics and
sociology that guide everyday life, career and personal growth: field → theme → concept, each concept backed by
research that holds up, each card a question on the front and on the back the concept, a real story of how it was
studied, and how to act on it. No comfort talk. Started from the web novel 《十日终焉》, whose hero names such laws.
First wave: 200 cards. The request asked for stories on every card (「卡片内容最好应该有实际的故事」).

## Sources surveyed (step 1)

| Source | Licence | Covers | Mapped to |
|---|---|---|---|
| OpenStax Psychology 2e, chapter list | CC BY | research methods, sleep, learning, thinking, memory, lifespan, emotion and motivation, personality, social, industrial-organisational, stress and health, therapy | `evidence`, `judge`, `learn`, `self`, `social`, `group`, `career`, `life`; biopsychology, sensation, intelligence testing and the taxonomy of disorders are out of scope |
| OpenStax Introduction to Sociology 3e, chapter list | CC BY | groups and organisations, deviance, stratification, networks, marriage and family, work | `group`, `career`, `social.connect` |
| Wikipedia, List of cognitive biases (245 linked entries) | CC BY-SA | the long list of named biases and effects | checked entry by entry: everything with replicated evidence and everyday use is a leaf; trivia (suffix effect, cheerleader effect) is left out |
| Kahneman, Thinking, Fast and Slow (parts) | book outline | two systems, heuristics, overconfidence, choices, two selves | `judge`, `life.happy` |
| Cialdini, Influence (principles) | book outline | reciprocity, commitment, social proof, authority, liking, scarcity | `social.influence`, `group.conform` |
| Munger, The Psychology of Human Misjudgment (25 tendencies) | talk outline | incentives, denial, envy, contrast, association | `game.incentive`, `judge`, `self` |
| Dunlosky et al. 2013, learning techniques review | paper | ten study techniques rated by evidence | `learn.memory` |
| Open Science Collaboration 2015; Many Labs 1–2; Camerer 2018 | papers | which classic findings replicate | the evidence grades and the whole `evidence.myth` theme |
| 《十日终焉》 fan catalogue of the laws the novel names (25 entries) | n/a | 二八定律, 马太效应, 峰终效应, 羊群效应, 囚徒困境, 墨菲定律, 正常化偏误, 蝴蝶效应, 第二十二条军规, plus folk management laws and physics | leaves tagged `十日终焉`; the folk laws (手表定律, 水桶定律, 竹子定律, 米格-25 效应, 雷尼尔效应, 奥格尔维法则) have no research behind them and are one card, `evidence.myth.folk-laws`; physics and logic puzzles are out of scope |
| github.com/lukasz-madon/awesome-concepts | CC0 | software laws (Brooks, Conway, Goodhart, Parkinson, Peter) | `career.org`, `game.incentive` |

## Skeleton (step 2)

`research/domains/psych/tree.txt` is the source; `gen_tree.py` writes `skeleton/psych.yaml` and the per-group anchor
lists. 9 fields, 33 themes, 332 leaves, 200 of them `core: true` (the first wave); it also writes the full map note
`vault/domains/psych/人性与决策 概念全图.md` (every concept, 待写 on the 132 without a card). Each leaf carries an evidence grade:

- A: replicated or supported by a meta-analysis;
- B: real but small, conditional or thinly replicated;
- C: famous and weakened or refuted. These get cards on purpose: knowing which popular claims fail is part of the goal.

Choice of the first 200: how often the situation comes up in an adult's life, strength of evidence, whether there is
something to do about it. Extra weight on learning that sticks and transfers, emotion regulation, habits,
relationships, and age and career timing.

## Cards (step 4)

Brief: `CARDS_TASK.md`. One card per leaf: situation question → bold one-sentence finding → a real story → evidence
line with the grade → who uses it → an action with a trigger. Five groups (A–E), one agent each, anchors in
`anchors-<G>.md`, audit trail with URLs in `claims-<G>.md`. Three model cards were written by the orchestrator.

| Group | Fields | Cards |
|---|---|---|
| A | `evidence.method`, `judge` | 43 |
| B | `self` | 34 |
| C | `evidence.myth`, `learn`, `career` | 44 |
| D | `social`, `life` | 39 |
| E | `group`, `game` | 40 |

## Review (step 5)

The orchestrator read all 200 cards. `review.py` checks the format (layout, tags against the tree, length, banned
phrases, figure share) and `--dump <group>` prints a group's unread cards. What review changed:

- Grades lowered from A to B after the agents read the sources: commitment devices (the self-set deadlines study did not
  replicate), friction and nudges (publication-bias correction), learned helplessness (the 2016 revision rests on rat
  work), end-of-history illusion (recall against forecast, different people), checklists (before-and-after design;
  Ontario found nothing), BATNA, exercise for depression (trial quality), Peter principle (one function), overwork (one
  1916 data set). The tree carries the new grades.
- Anchor errors caught by the agents and recorded in `claims-*.md`: Many Labs 2 replicated 15 of 28, not 14; lifetime
  regrets are split about evenly in the 2,600-person replication; Beshears 2021 did raise savings; the coin-flip study
  counts 22,511 tosses and its effect appears at six months only; the rater-effect ratings were developmental.
- Fixed by the orchestrator: median written as mean (habit, 66 days); a therapy session called a class; a Murphy
  question whose numbers did not add up (now 1,000 runs a day at 1 in 100,000: 97% chance of a failure within a year,
  computed); a loosely sourced 5%/95% line dropped; four action lines rewritten; two figures added from the formula
  (Kelly growth curve, sample-size funnel); 被试 replaced by 参与者.
- Left without numbers on purpose because no primary source was reached: first-offer prices, salary negotiation
  premium, BATNA sample details.

Rules this produced are in `CARDS_TASK.md` (the two sections after the format).

## Next

- Paused (Chi, 2026-11-17): he studies the first 200 before deciding on more. Do not start a second wave unasked.
- When he asks: the 132 leaves without a card are listed in the full map note; their anchors are already in
  `tree.txt` (change `-` to `*` and re-run `gen_tree.py`).
- No readings yet (link coverage 0%): one readable source per theme would be the next step of the skill.
- The deck is not in the daily planner (`scripts/study_plan.py`); Chi decides whether it joins `1 今日计划`.

## Ledger

| Date | Step | Result |
|---|---|---|
| 2026-11-17 | survey, tree, skeleton | 332 leaves, 200 core, `validate` 0 errors |
| 2026-11-17 | model cards | loss aversion, rumination, ego depletion |
| 2026-11-17 | cards, three waves (two cut by the usage limit) | 200 cards, 56 with a figure (28%), 23 mermaid blocks render |
| 2026-11-17 | review | all 200 read; 0 format defects; `validate` 0 errors, `plain_style` ok, `phone_diagrams` ok |
