# How the study planner decides what to learn next

The planner (`trellis/plan.py`, fed by `scripts/study_plan.py` and `scripts/plan_evidence.py`) answers one question
every morning: which cards are worth learning next, given what interviews ask and what the learner already holds.
Every number it uses comes from data that can be inspected; this page says which data, how it is combined, and where
it is weak.

## 1. How often each question is asked

Source: an interview-report bank with one row per reported interview: company, level, date and, often, the
candidate's own description of what was probed. Counting rows directly is biased, because a few companies file most
reports (in the bank used here one company files about 40% of all rows). So the index is built in four steps.

1. **Weight each report.** Recency with a half-life of 18 months: `0.5 ^ (months_ago / 18)`. Senior-and-above
   reports count 1.2.
2. **Normalise per company.** Turn each company's weighted reports into shares over questions. Then shrink each
   company's shares toward the pooled shares, so a company with few reports nudges the mix instead of overwriting it.
   This is empirical-Bayes shrinkage: `share(q, c) = (n_qc + 30 · p_q) / (n_c + 30)`.
3. **Mix by target.** Combine the shares by the learner's target groups, for example ByteDance/TikTok, large US tech
   and others. Each group gets a weight, and companies inside a group are averaged.
4. **Add public reports.** Reports collected from public pages (1point3acres, LeetCode Discuss, Glassdoor, GitHub
   compilations, each recorded with URL and date) enter the same way. Each is scaled by its confidence.

Two numbers fall out of this and are reported, not assumed:
- **Coverage:** the share of the mixed frequency that falls on questions the deck has a topic for.
- **The 80/20 line:** how many of the most-asked questions carry 80% of it.

Bank questions that are the same problem under another name are mapped by hand in a reviewed alias file. A neighbour
problem is never aliased.

## 2. How much each concept is worth

A concept earns weight in two ways.

- **Directly.** The same frequency index is computed over the reports whose descriptions name the concept, using
  bilingual keyword lists. This counts 30% against the question mass.
- **By inheritance.** Each question passes half its weight to what it needs, split by edge strength. The flow repeats
  down chains of prerequisites. The edges come from:
  - explicit prerequisites (`requires`);
  - the fundamentals a question's map card links to;
  - the cross-question patterns that list the question;
  - a small universal edge to the delivery framework and to estimation.

A concept that many frequent questions need therefore ends up heavy, even if no report names it.

Personal multipliers sit on top and are kept out of the repository: weak spots found in a mock, a target team's
domain, and topics the learner deprioritises.

## 3. How much each card is worth inside its topic

A topic's weight is shared among its cards by the product of four factors.

- **Level.** The card's own label: 必会 1.0, 追问 0.6, 加分 0.3, unlabelled 0.8. Cards in the declared core get ×1.3.
- **Position.** The topic's teaching order is front-loaded: `(1 + rank / 8) ^ -0.8`. The summary and main chain carry
  most of what an interviewer probes.
- **Frequency,** from 0.68 to 1.61. It multiplies two terms:
  - how often report descriptions use the card's own technical terms, relative to the topic's other cards (0.8 to 1.4);
  - how strongly the card ties in other frequently named concepts (0.85 to 1.15).
- **Cost.** Value is divided by `1 + 0.6 · difficulty`. Before study, difficulty comes from the card's length
  percentile, its level and whether it carries code. After two reviews it is blended half and half with the learner's
  record: forgets, Hard presses and ease. A hard card is worth as much but takes longer, so it pays less per minute.

## 4. What is already held, and what is ready

- **Mastery** of a card is its Hold (the scheduler's interval, normalised against a 21-day mature card and discounted
  by lapses). It decays once the card is overdue: ×0.9 per extra interval.
- **Readiness** of a topic is the average of `min(1, prerequisite mastery / 0.4)` over its prerequisites, with a floor
  of 0.35. A question whose concepts have not taken waits, but it is never fully blocked.

## 5. Picking

The value of learning a card next is:

```
topic weight × card share × (1 − mastery) × readiness / cost
```

Cards are taken greedily by value, under three rules:
- each leaf's own order is kept;
- a topic's further cards lose 20% each (diminishing returns), so a day covers several topics;
- 20% of the budget is reserved for whole questions, so practice on full answers starts early.

The picks are then ordered so that prerequisite topics come first, and they are dealt in three stages: weak spots,
concepts and technologies, whole questions.

## 6. Known weaknesses

- **The bank is self-reported and English-speaking.** Some groups are thin. ByteDance has nine system-design rows in
  the bank used here, which is why its share is shrunk and why public reports matter.
- **Keyword matching is coarse.** Concept mentions in descriptions over-count broad words. The lists were tightened
  after inspection (for example, `file` and `push` were removed), but this remains the noisiest input.
- **Several weights are judgement, not measurement.** These are the 0.5 spread, the 0.3 concept share, the level
  weights and the position decay. They are stated here so they can be changed and compared, not hidden.
- **Readiness uses only `requires` edges.** Looser ties (mentions, patterns) carry weight but do not gate.
