%% trellis:begin %%
# Malformed & Hostile Rows
*Input & Parsing*

Deciding per field whether a bad row is skipped, defaulted or fatal, and keeping the decision in one validator instead of scattered `try` blocks.

## Readings
- [[python-csv|csv — CSV file reading and writing]]

## Drills
- [[csv-parse-validate-report|Drill: parse, validate and report over a hostile CSV]]
- [[oa-q15-kyc-verification|Drill: verify merchant onboarding data against five accumulating KYC rules]]
- [[oa-q16-chargeback-parsing|Drill: parse card-network chargebacks, drop corrupted rows, cancel withdrawn disputes]]
- [[oa-q17-datacenter-router-haversine|Drill: register datacenters and route requests to the nearest healthy one]]
- [[oa-q30-stripe-capital-loans|Drill: Stripe Capital loan ledger — pay, increase, withhold, reject]]
- [[oa-q31-wishlist-mutual-rank|Drill: mutual-rank pairings over ordered wishlists]]

## Cards (5)
- [[cc-input-mal-corrupt-row-participates-in-nothing]]
- [[cc-input-mal-one-validator]]
- [[cc-input-mal-skip-default-fatal]]
- [[cc-input-mal-unknown-vocabulary]]
- [[cc-input-mal-validate-before-mutate]]
%% trellis:end %%

## Notes
