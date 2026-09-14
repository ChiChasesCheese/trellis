---
nodes: [distributed.retries]
url: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
tags: [canonical]
---
# Timeouts, retries, and backoff with jitter

Amazon's Builders' Library article explains the production math behind timeout selection, capped exponential backoff, jitter, retry budgets, and retry placement.

**Extract on read:**
- A timeout must cover the intended phases and derive from measured latency.
- Retries are selfish extra load and should occur at one layer under a shared budget.
- Jitter prevents synchronized clients from turning recovery into another traffic spike.

%% trellis:begin %%
## Source
[Open the original ↗](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter)
%% trellis:end %%
