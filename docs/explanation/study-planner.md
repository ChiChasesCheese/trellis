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
4. **Add public reports.** Reports collected from public pages enter the same way. The sources are 1point3acres,
   LeetCode Discuss, Blind, Nowcoder and GitHub mirrors of question vendors, each recorded with URL and date.
   - The same interview seen on several sites (same company, month and prompt) is merged into one report.
   - Each report is scaled by its confidence (high 1.0, medium 0.7, low 0.4). It counts as senior only if it says so.
     Campus and intern loops count half.
   - One report is one unit: a report naming two topics gives each half.
   - A named design prompt with no topic of ours still counts, as an uncovered question. A report with no named prompt
     only feeds concept mentions.

Two numbers fall out of this and are reported, not assumed:
- **Coverage:** the share of the mixed frequency that falls on questions the deck has a topic for.
- **The 80/20 line:** how many of the most-asked questions carry 80% of it.
- **Agreement between the two sources:** the Spearman rank correlation of the bank-only and public-only indexes over the
  topics both contain, and the overlap of their top 20.

Bank questions that are the same problem under another name are mapped by hand in a reviewed alias file. A neighbour
problem is never aliased.

## 2. How much each concept is worth

A concept earns weight in two ways.

- **Directly.** The same frequency index is computed over the reports whose descriptions name the concept, using
  bilingual keyword lists. This counts 30% against the question mass.
- **By inheritance.** Each question passes a share of its weight to what it needs, split by edge strength. The share
  is the `spread` setting: 0.5 by default, 0.7 for a learner who wants shared knowledge first. The flow repeats
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

Where exam points exist they replace the frequency term above.

- **An exam point** is what an answer cites in one breath or a follow-up probes in one question. Each concept topic is cut
  into points, each card is mapped to one to three points, and the same idea under several topics is merged.
- **Each design question** lists the points its answer needs, with a role: must cover (1.0), common follow-up (0.6) or
  bonus (0.3). It also lists its own points, the tricks no other question shares.
- **A point's weight:** a question passes `spread` of its frequency to the shared points it needs, by role. The rest
  stays with its own points. A topic's directly reported frequency is shared among its points, core points double.
- **A card's value** sums what its points are worth, divided by how many cards teach each. The primary point counts
  fully, the others half.
- **Coverage is measured on points.** A point's mastery is the mean of its three best-held cards. Overall coverage is
  the weight-averaged mastery of all points, and a topic's weight and mastery are what its points add up to.
- **A card's value is what it adds:** its points' weight, shared among the three cards a point needs, on the part of the
  point not yet held, multiplied by personal boosts and readiness and divided by cost. Whole questions are excluded from
  this budget and keep their own reserved share.
- **Question edges** come from the same needs instead of links in the card text.
- **In one day** a second card on the same point is worth 40% less, so a day covers more points.

Points about the interview itself (levels, prep plans, scoring rubrics) are kept out of the weights.

The map itself is drawn into two Obsidian notes by `scripts/knowledge_points.py`: titles and counts only, nothing about the
learner.

New cards must be annotated too: `scripts/plan_maintain.py` lists cards with no points and problems with no tags.

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
- 20% of the budget is reserved for whole questions, so practice on full answers starts early. That share is dealt
  only from a few representative questions (next section).

The picks are then ordered so that prerequisite topics come first, and they are dealt in three stages: weak spots,
concepts and technologies, whole questions.

## 6. One deck for the day

`scripts/daily_extra.py` extends the daily deck beyond system design, so the learner opens one deck.

- **LeetCode:** problems just solved, new problems by importance, and similar problems after a forget. A similar problem
  is one the failed problem's solution lists, or one sharing its techniques, patterns and pitfalls.
- **Reviews:** every deck's due cards, ranked by `deck weight × (0.3 + value percentile in its deck) × urgency`, where
  `urgency = 1 + min(2, days overdue / interval)`. A daily budget takes the top; the rest wait in their decks. One copy
  of a LeetCode problem is reviewed at a time.

Moved cards record their home deck and go back on the next run. The decks the plan owns deal no new cards themselves.

## 7. Shared knowledge first

Eighty percent of reported interviews spread over dozens of distinct questions, too many to practise one by one. Most
of what their answers need is shared. Two numbers make that visible:

- **A concept's share of the answers.** Each question's answer leans on its concepts in proportion to edge strength.
  Summing over questions, weighted by frequency, gives each concept's share. The dashboard shows how few concepts carry
  80%.
- **Readiness.** A question is ready once the learned concepts carry 80% of its edges. The dashboard shows how much of
  the question frequency is ready after the first 5, 10, 20 … concepts.

**Representative questions** are picked greedily from the 25 most-asked design questions. Each next pick has the largest
product of the exam-point weight it adds and its own frequency; weight alone favours whichever answer was annotated
with the most points. Coverage is measured on points several questions share, as the share
of their total weight that the picks' answers use; it is reported in any role and for must-cover points alone. A second figure weights by question: draw a question by how
often it is asked, and take the average share of the shared points its answer needs (by role) that the picks use. A
question's own tricks are left out because they transfer to nothing else. Using a point in one answer is not mastering
it. Whole-question practice is dealt only from these picks, eight by default.

## 8. LeetCode

Coding problems have a better source: the GitHub company-wise lists (LeetCode Premium frequency per company and per
window, for several hundred companies). `scripts/lc_analysis.py` uses them alone:

```
importance = 0.6 × target frequency + 0.4 × breadth
```

- **Target frequency** is the higher of TikTok and ByteDance. Each is half all-time frequency and half the highest
  recent window (30 days, 3 months, 6 months), as a value from 0 to 1.
- **Breadth** is the sum of all-time frequency over every company, divided by the largest such sum.

The same score over every problem in the repository says how much of what is asked the deck covers.

Each problem is tagged by pattern, technique, pitfall and Python idiom. A dimension's priority is:

```
importance × (1 − mastery) × clip(1 + 0.5 · (slip / overall slip − 1), 1, 1.5)
```

- Slip counts Again as 1 and Hard as 0.5, smoothed with 15 pseudo-reviews at the learner's overall rate.
- A weakness can raise priority by at most half; it never outranks how often a dimension is asked.

A problem has several cards that open the same solution, one per deck it sits in (a company deck, a module deck). Its
mastery is that of its best card, so learning it anywhere counts everywhere.

Fixed problem sets are tracked as progress views. These are the classic lists (Blind 75, NeetCode 150, Hot 100, Top
Interview 150), each target company's last six months, and each module. They do not enter importance. A view's history
is rebuilt from the review logs, which give each card's interval as it stood at any past date.

The code keeps processing apart from analysis.
- `scripts/lc_data.py` holds the fixed inputs: frequency statistics, the lists and the Anki client.
- `scripts/lc_analysis.py` reads the reviews and computes everything personal.
- `scripts/lc_lists.py` shapes the deck from the fixed inputs only. It tags one card per listed problem,
  `榜单::<list>`, always the whole answer in the problem's module deck, so each list can be studied as a filtered deck.

## 9. Known weaknesses

- **The bank is self-reported and English-speaking.** Some groups are thin. ByteDance has nine system-design rows in
  the bank used here, which is why its share is shrunk and why public reports matter.
- **Public reports are thin and skewed too.** Forum thread bodies sit behind logins, and vendor catalogues over-represent
  the companies they sell to. Most public reports state no level. The two sources agree only moderately (a rank
  correlation near 0.4), so neither alone should set the weights.
- **Keyword matching is coarse.** Concept mentions in descriptions over-count broad words. The lists were tightened
  after inspection (for example, `file` and `push` were removed), but this remains the noisiest input.
- **Several weights are judgement, not measurement.** These are the 0.5 spread, the 0.3 concept share, the level
  weights and the position decay. They are stated here so they can be changed and compared, not hidden.
- **Exam-point roles are read from the deck's own answers.** They say what a good answer covers, not what interviewers
  were counted asking. Frequency stays at question level. Points asked only in oral fundamentals rounds have no question
  behind them, so they are underweighted.
- **Readiness uses only `requires` edges.** Looser ties (mentions, patterns) carry weight but do not gate.
