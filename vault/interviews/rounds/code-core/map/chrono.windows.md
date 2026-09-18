%% trellis:begin %%
# Time Windows & Buckets
*Time & Intervals*

Fixed buckets vs rolling windows, "within the last hour" as a comparison you must pin down, and per-key window state.

**Requires:** [[interviews/rounds/code-core/map/chrono.arithmetic|Duration & Calendar Arithmetic]]

## Readings
- [[stripe-rate-limiters-four|Scaling your API with rate limiters (Stripe)]]

## Drills
- [[interval-merge-across-offsets|Drill: merging maintenance windows across timezone offsets]]
- [[oa-q23-rate-limiter|Drill: rate-limit a request stream, then swap the algorithm for a token bucket]]
- [[oa-qa05-lc1604-keycard-alerts|Drill: alert on repeated key-card use inside an hour, then generalize and go online]]

## Cards (6)
- [[cc-chrono-windows-boundary]]
- [[cc-chrono-windows-bucket-vs-rolling]]
- [[cc-chrono-windows-denied-not-recorded]]
- [[cc-chrono-windows-no-midnight-wrap]]
- [[cc-chrono-windows-per-key-state]]
- [[cc-chrono-windows-token-bucket]]
%% trellis:end %%

## Notes
