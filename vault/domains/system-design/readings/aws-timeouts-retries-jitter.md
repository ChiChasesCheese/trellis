---
nodes: [reliability.resilience]
url: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
tags: [canonical, amazon]
---
# Timeouts, Retries, and Backoff with Jitter (AWS Builders' Library)

The best short piece on why naive retries take systems down and what
disciplined clients do instead. The whole Builders' Library is worth mining.

**Extract on read:**
- Setting timeouts from downstream latency distributions, not vibes.
- Retry budgets / token buckets to cap amplification.
- Why jitter (not just exponential backoff) breaks synchronized retry waves.

Related cards: [[reliability-retry-storm]], [[reliability-deadline-propagation]]

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

## Archived copy
![[aws-timeouts-retries-jitter-clip]]
%% trellis:end %%
