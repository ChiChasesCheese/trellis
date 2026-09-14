%% trellis:begin %%
# Money as Integer Minor Units
*Business Rules & Money*

Cents as `int`, `Decimal` with an explicit context, zero-decimal currencies, and why a float ever touching money is a bug.

**Unlocks:** [[rules.rounding|Rounding Rules & Where to Apply Them]], [[rules.tiers|Tiered, Metered & Prorated Math]]

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
- [[cc-rules-money-decimal-from-string]]
- [[cc-rules-money-float-symptom]]
- [[cc-rules-money-int-float-coercion]]
- [[cc-rules-money-integer-minor-units]]
- [[cc-rules-money-json-int-precision]]
- [[cc-rules-money-max-digits-overflow]]
- [[cc-rules-money-negative-formatting]]
- [[cc-rules-money-same-currency-different-minor-unit]]
- [[cc-rules-money-unit-in-the-name]]
- [[cc-rules-money-zero-decimal-currencies]]
%% trellis:end %%

## Notes
