---
nodes: [distributed.transactions.isolation, distributed.transactions.concurrency-control]
url: https://martin.kleppmann.com/2014/11/25/hermitage-testing-the-i-in-acid.html
tags: [canonical]
---
# Hermitage: Testing the "I" in ACID (Kleppmann)

The companion post to DDIA's transactions chapter: a test suite that probes
what isolation levels in Postgres, MySQL, Oracle, and SQL Server *actually*
permit, anomaly by anomaly. Turns the isolation-level ladder from vocabulary
into observable behavior — the comparison table alone is worth the visit.

**Extract on read:**
- The anomaly zoo mapped to levels: dirty read, non-repeatable read, phantom, lost update, write skew.
- "Repeatable read" means different things per vendor — snapshot isolation is not serializability.
- How MVCC-based engines permit write skew that 2PL-based ones block.

%% trellis:begin %%
## Source
[Open the original ↗](https://martin.kleppmann.com/2014/11/25/hermitage-testing-the-i-in-acid.html)

## Archived copy
![[hermitage-isolation-levels-clip]]
%% trellis:end %%
