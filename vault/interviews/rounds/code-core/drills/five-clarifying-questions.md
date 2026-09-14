---
nodes: [round.communication, round.ambiguity, round.reading, verification.invariants, transfer.playbook]
---
# Drill: five clarifying questions before you write a line

Fifteen minutes, spoken or written, no code. You are handed a deliberately
under-specified prompt:

> "Given a log of account activity, report which accounts are at risk. An
> account is at risk when it has too many failed operations relative to its
> total. Print the at-risk accounts."

Produce exactly five questions, ranked by how much the answer changes your
design, plus the assumption you would code against if you got no answer at all,
and where in the code that assumption would be written down.

**Constraints to state and honor**
- Five questions, not ten — ranking is most of the exercise.
- Each question must have at least two answers that lead to *different code*; a
  question whose answers change nothing is wasted.
- For each, state the default you would take and how many lines it would cost to
  switch later.

**Grading points**
- Boundary semantics: is "too many" strict or inclusive, and is it a count or a
  ratio ([[cc-verification-edge-exact-threshold-triple]]).
- The degenerate cases the prompt does not mention: an account with zero
  operations, duplicate log entries, entries out of order
  ([[cc-verification-edge-empty-and-single]], [[cc-verification-edge-duplicate-and-out-of-order]]).
- Output contract: order, tie-break, and what is printed when nothing is at risk
  ([[cc-python-io-exact-stdout]]).
- Scale, because it decides the structure before any code exists
  ([[cc-performance-budget-decide-before-coding]]).
- The assumption is recorded as a comment at the point of use and kept one flag
  away from the alternative ([[cc-verification-invariant-name-it]]).
- Questions that are really statements ("I assume ids are unique?") score lower
  than questions whose answers you genuinely cannot guess.

**Attempt log**
- [ ] Attempt 1 (date, 15 min, self-graded notes):
