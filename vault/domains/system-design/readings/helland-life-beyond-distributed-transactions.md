---
nodes: [distributed.transactions.distributed]
url: https://www.ics.uci.edu/~cs223/papers/cidr07p15.pdf
tags: [canonical, paper]
---
# Life beyond Distributed Transactions: An Apostate's Opinion (Pat Helland, CIDR 2007)

The clearest statement of *why practitioners stop using 2PC* and what they build
instead. Helland spent years trying to make distributed transactions scale, gave
up, and wrote down the discipline that replaces them: entities as the unit of
atomicity, and messaging between entities as the unit of everything else.

**Extract on read:**
- 2PC is the "anti-availability protocol" — the coordinator's failure blocks participants holding locks.
- The entity/almost-infinite-scale model: transactions may not span entity keys, so cross-entity work becomes messages.
- Because messages retry and reorder, workflow state and idempotence (activities) are mandatory, not optional.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ics.uci.edu/~cs223/papers/cidr07p15.pdf)

## Archived copy
![[helland-life-beyond-distributed-transactions-clip]]
%% trellis:end %%
