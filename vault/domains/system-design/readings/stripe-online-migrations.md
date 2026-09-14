---
nodes: [storage.relational.operations, infra.delivery]
url: https://stripe.com/blog/online-migrations
tags: [stripe]
---
# Online migrations at scale (Stripe)

How Stripe moved hundreds of millions of Subscriptions records to a new data
model with zero downtime, using a dual-write / backfill / verify / cut-over
sequence. The canonical playbook for changing a schema or datastore under a
system that can never stop serving traffic.

**Extract on read:**
- The four-phase pattern: dual-write → backfill old data → dual-read and compare → switch reads and drop the old path.
- Why each phase is independently verifiable and reversible.
- How they rate-limited and checkpointed the backfill over live production data.
- Using comparison/consistency checks between old and new paths as the gate for cut-over.

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/online-migrations)

## Archived copy
![[stripe-online-migrations-clip]]
%% trellis:end %%
