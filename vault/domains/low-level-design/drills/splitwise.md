---
nodes: [method.modeling, oop.values, quality.errors, structure.api]
tags: [classic, hard, fintech]
---
# Drill: Splitwise (Expense Sharing)

Design and code expense splitting: groups, equal/exact/percentage splits,
balances, simplify-debts.

**Constraints to state and honor**
- Money is never a float; splits must sum exactly to the total (who eats the rounding penny?).
- New split types must be addable without touching existing ones.
- Invalid splits (percentages ≠ 100, exact ≠ total) rejected at the boundary with actionable errors.
- Simplify-debts as a follow-up: min-cash-flow greedy.

**Grading points**
- Money as a value object; rounding policy explicit — [[oop.values|Value Objects & Immutability]].
- Split hierarchy with a validate contract per subtype — [[method.modeling|Requirements to Objects]].
- Validation and failure paths designed, not sprinkled — [[quality.errors|Error Handling Design]].
- Balance-sheet API that supports both "my view" and group settlement — [[structure.api|In-Process API Design]].
- Bridge to your day job: this is a baby ledger — the invariant is double-entry's little sibling ([[correctness.ledger|Ledgers & Reconciliation]] in the SD domain).

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
