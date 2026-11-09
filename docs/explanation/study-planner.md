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

With `pure_coverage` set, a day's system-design cards are the ones that add the most exam-point coverage, with no personal boosts;
whole questions keep their reserved share.

A day's system-design cards are cut into five sittings of about equal size, each on related material: a domain's topics stay together and cards on one exam point sit side by side, so a card can build on the one before it. Selection compares cards by coverage added per unit of reading (`READ_UNIT`) times one plus their spread, and cards over 2,000 characters wait until they are split. Topics that feel like one subject can share a daily cap (`family_caps`).

The dashboard also ranks unlearned cards by information worth: coverage added per unit of reading times one plus the card's spread, the Shannon entropy in bits of the questions that need its points, weighted by how often each is asked. It lists one card per primary point, because a point needs few cards. The same worth chooses the day's system-design cards, inside each domain (top-level branch), and a domain's share of the budget follows the square root of the coverage it can still add, so the most valuable cards of every area get in, not only of the area every question needs.

Each subject has its own part of the deck and its own daily budget of new cards and reviews, so one cannot starve another:
system design, low-level design and LeetCode. New cards dealt and not learned stay first the next day, in a `0 昨天没学完` part,
and count against that day's budget.

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

## 9. A fixed study sprint

`sprint` in the local config runs a fixed number of days at a fixed new-card rate (`scripts/plan_sprint.py`), for a learner who wants the most common
ideas in a short time. Picking is `trellis.plan.coverage_order`: greedily take the card that adds most exam-point coverage, each leaf in its teaching
order, so the gain of a card shrinks as its point fills up and stops at zero once the point has enough cards. Personal boosts do not enter this
pick. The cards are then laid out over the days by topic, prerequisites first, so a day has a theme; each practice day adds the cards of one
representative question, and the last day is a timed full mock of the next representative. The curriculum is rebuilt on every run before the first
day and frozen from the first day on, so projected coverage stays comparable with what happened. Each morning deals the first unseen cards of the
whole sequence, so a missed day comes first the next day. Budgets return to normal after the last day, with nothing to switch off.

The projection assumes every dealt card is learned that day and passes on schedule, so it is an upper bound on what the plan buys.

Each card's Anki back also carries a short index built from the annotations (`trellis/kp_footer.py`): its points, the questions that ask them in
order of role times frequency, and neighbouring cards that teach the same point in another leaf.

## 10. Known weaknesses

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
- **Mastery measures the schedule, not recall.** Hold is read from the interval the scheduler gave, and the scheduler only sees the button pressed. A
  learner who recognises the answer instead of recalling it gets long intervals and a high coverage figure. The dashboard warns when the forget rate
  is implausibly low; the score itself is not corrected.
- **Oral rounds are counted thinly.** Points asked only in fundamentals rounds have no question behind them, so `oral.json` counts them from 201 public
  oral-round posts (a campus post counts half) and gives them 5% of the question mass. The posts lean to campus Java and agent roles, so a larger share
  displaces design material: at 15%, 11% of a 7-day sprint changes and agent and runtime cards replace data-modelling ones.
- **A question asked under several names.** Their own points were split across duplicate question topics; same-trick points are merged in `merge.json`.

**How stable the judgement constants are.** Each was perturbed alone, and the plan recomputed. The table gives the overlap of the top 100 points by weight
(with their Spearman rank correlation), of one day's picks, of a 560-card sprint, and of 100 reviews.

| Constant | Values tried | Top 100 (rank corr.) | Day | Sprint | Reviews |
|---|---|---|---|---|---|
| role weights 1/0.6/0.3 | 1/0.8/0.5, 1/0.4/0.1 | 0.96 (0.98) | 0.93 | 0.96 | 0.99 |
| `spread` 0.7 | 0.5, 0.9 | 0.79, 0.95 (0.94, 0.96) | 0.94+ | 0.92, 0.94 | 0.99 |
| `HELD_CARDS` 3 | 2, 4, 5 | 1.00 | 0.91+ | 0.82 to 0.89 | 0.99 |
| secondary point 0.5 | 0.25, 0.75 | 1.00 | 0.83, 0.90 | 0.92 | 1.00 |
| `DIMINISH` 0.8 | 0.6, 1.0 | 1.00 | 0.81, 0.84 | 1.00 | 1.00 |
| `DIMINISH_POINT` 0.6 | 0.4, 0.8 | 1.00 | 0.97, 0.86 | 1.00 | 1.00 |
| `LOOKAHEAD` 3 | 1, 5 | 1.00 | 0.57, 0.84 | 0.68, 0.81 | 1.00 |
| `LEARNED` 0.58 | 0.4, 0.75 | 1.00 | 1.00 | 0.99+ | 1.00 |
| question share 20% | 10%, 30% | 1.00 | 0.90 | 1.00 | 1.00 |
| urgency cap 2 | 1, 4 | 1.00 | 1.00 | 1.00 | 0.85, 0.64 |
| value floor 0.3 | 0.1, 0.6 | 1.00 | 1.00 | 1.00 | 0.99, 0.96 |

What this says:
- **Point weights are stable.** They depend only on roles and spread; rank correlation stays at 0.94 or above. A spread of 0.5 changes a fifth of the top 100.
- **`LOOKAHEAD` moves picks but not the objective.** The cards are close substitutes: the projected coverage after the sprint is 29.9% with 1 or 3 and 29.7%
  with 5. It is kept at 3 so a leaf's cheap introduction does not hide a valuable card behind it.
- **`HELD_CARDS` is a real choice.** It decides how many cards a point gets, so it changes 11% to 18% of a sprint. Coverage is defined by it, so its effect on
  coverage cannot be compared; 3 is a judgement.
- **The review urgency cap changes which reviews are taken** (a cap of 4 swaps a third of them). No outcome data can calibrate it yet: it only orders a daily
  budget, and a card it passes over stays due.
