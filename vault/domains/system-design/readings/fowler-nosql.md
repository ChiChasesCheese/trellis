---
nodes: [storage.nosql]
url: https://martinfowler.com/nosql.html
tags: [intro, reference]
---
# NoSQL Guide (Martin Fowler)

Fowler's stable hub distilling "NoSQL Distilled" — the aggregate-oriented
framing (key-value, document, wide-column) vs graph, and polyglot persistence
as choosing storage by access pattern, not fashion.

**Extract on read:**
- Aggregate orientation: model around what you read/write together; joins become your job.
- Key-value vs document vs wide-column as points on one axis; graph as the genuine outlier.
- Choose NoSQL for scale-out or model fit — and default to relational absent either.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/nosql.html)

## Archived copy
![[fowler-nosql-clip]]
%% trellis:end %%
