---
nodes:
- quality.fitness-functions
title: A claim without a probe is a guess
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0012-findings-carry-executable-probes
---

# A claim without a probe is a guess

Make an executable check the entry ticket for any architectural claim: a probe that exits non-zero while the defect exists and zero once it is fixed. Three properties do the work. It must have a positive control — a probe that can never go red is measuring something else, and one real example here asserted 'no delisted names' against a calendar-padded archive, so it could never have failed. It stays in CI after the fix, which turns a one-off finding into a guard and stops the same defect being rediscovered later as if it were new. And it draws a line between prose and fact: comments describe intent, probes describe what is true, so a stale comment asserting a guard that no longer exists is worse than no comment, because it stops readers from checking.

The family extends beyond correctness tests: allowlists that may only shrink, import contracts, and budgets on complexity all measure the codebase itself rather than a unit's behaviour. The measured payoff in this codebase was blunt — roughly 62% of claims that had not been probed first turned out to need correction.
