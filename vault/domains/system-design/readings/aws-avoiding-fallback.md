---
nodes: [reliability.resilience.containment]
url: https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/
tags: [amazon]
---
# Avoiding fallback in distributed systems (AWS Builders' Library)

A contrarian and battle-earned position: the "backup path" you plan to fail
over to is the least-tested code in your system and it is exercised for the
first time during your worst outage. Amazon largely bans in-process fallback
and this piece explains the alternatives that actually survive incidents.

**Extract on read:**
- Why fallback paths fail exactly when needed: untested, cold, entered under overload.
- The bimodal-behavior objection: two operating modes means the rare mode is always broken.
- Alternatives: fail fast, improve the primary path, run the "fallback" work all the time (constant work), static stability.
- When fallback is acceptable (rare, simple, continuously exercised).

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/)

## Archived copy
![[aws-avoiding-fallback-clip]]
%% trellis:end %%
