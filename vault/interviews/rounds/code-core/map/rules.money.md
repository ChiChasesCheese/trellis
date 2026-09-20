%% trellis:begin %%
# Money as Integer Minor Units
*Business Rules & Money*

Cents as `int`, `Decimal` with an explicit context, zero-decimal currencies, and why a float ever touching money is a bug.

**Core** — part of the first pass through this subject.

**Unlocks:** [[interviews/rounds/code-core/map/rules.rounding|Rounding Rules & Where to Apply Them]], [[interviews/rounds/code-core/map/rules.tiers|Tiered, Metered & Prorated Math]]

## Readings
- [[fowler-money-pattern|Money (Patterns of Enterprise Application Architecture)]]
- [[python-decimal|decimal — decimal fixed point and floating point arithmetic]]
- [[python-floating-point|Floating Point Arithmetic: Issues and Limitations]]
- [[stripe-zero-decimal-currencies|Zero-decimal currencies (Stripe docs)]]

## Drills
- [[oa-q03-chat-billing|Drill: monthly billing with metered usage, a fixed plan, and mid-month proration]]
- [[oa-q13-account-balance-ledger|Drill: a cents-exact ledger with overdraft rejection and a platform lender]]
- [[oa-q16-chargeback-parsing|Drill: parse card-network chargebacks, drop corrupted rows, cancel withdrawn disputes]]
- [[oa-qa06-lc2043-simple-bank-system|Drill: a validated bank class, then a reversible log, then platform lending]]
- [[settlement-minimum-transfers|Drill: settling a group of debts in the fewest transfers]]
- [[tiered-billing-exact-output|Drill: tiered billing with an exact-output contract]]

## Cards (10)
1. [[cc-rules-money-decimal-from-string]]
2. [[cc-rules-money-float-symptom]]
3. [[cc-rules-money-integer-minor-units]]
4. [[cc-rules-money-negative-formatting]]
5. [[cc-rules-money-unit-in-the-name]]
6. [[cc-rules-money-zero-decimal-currencies]]
7. [[cc-rules-money-int-float-coercion]]
8. [[cc-rules-money-json-int-precision]]
9. [[cc-rules-money-max-digits-overflow]]
10. [[cc-rules-money-same-currency-different-minor-unit]]
%% trellis:end %%

## Notes
