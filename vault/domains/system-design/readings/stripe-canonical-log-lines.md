---
nodes: [reliability.observability]
url: https://stripe.com/blog/canonical-log-lines
tags: [stripe]
---
# Fast and flexible observability with canonical log lines (Stripe)

A short, sharp idea: emit one wide, structured log line per request that
carries every fact you might later query — and make that line, not traces or
scattered debug logs, the workhorse of production debugging. Cheap to adopt
and disproportionately useful; a favorite "small idea, big leverage" answer
for observability questions.

**Extract on read:**
- What fields belong on the canonical line (identity, routing, timing, rate-limit decisions, error class).
- Why one wide line per request beats grepping many narrow lines.
- How the lines feed ad-hoc SQL-style querying during incidents.
- Relationship to (not replacement of) metrics and tracing.

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/canonical-log-lines)

## Archived copy
![[stripe-canonical-log-lines-clip]]
%% trellis:end %%
