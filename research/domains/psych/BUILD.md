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
lists. 9 fields, 33 themes, 332 leaves, 200 of them `core: true` (the first wave). Each leaf carries an evidence grade:

- A: replicated or supported by a meta-analysis;
- B: real but small, conditional or thinly replicated;
- C: famous and weakened or refuted. These get cards on purpose: knowing which popular claims fail is part of the goal.

Choice of the first 200: how often the situation comes up in an adult's life, strength of evidence, whether there is
something to do about it, and weight on the themes that matter most for someone who studies a lot alone: learning
that sticks and transfers, rumination and self-worth, habits, loneliness and reaching out, age and career timing.

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

## Ledger

| Date | Step | Result |
|---|---|---|
| 2026-11-17 | survey, tree, skeleton | 332 leaves, 200 core, `validate` 0 errors |
| 2026-11-17 | model cards | loss aversion, rumination, ego depletion |
