---
nodes:
- async.delivery
- async.log
url: https://kafka.apache.org/documentation/
tags:
- reference
- canonical
- index
---
# Apache Kafka Documentation (Design section)

The official docs' "Design" chapter is the definitive statement of delivery
semantics from the system that defined them: at-most-once, at-least-once,
and how idempotent producers plus transactions yield effectively-exactly-once.
Also the authority on partitions, consumer groups, offsets, and retention.

**Extract on read:**
- Exactly-once = idempotent producer (dedup by sequence) + transactional offsets, not magic.
- Ordering is per-partition only; the partition key is therefore an API contract.
- Consumer-tracked offsets: why redelivery happens and where dead-letter queues fit.

%% trellis:begin %%
## Source
[Open the original ↗](https://kafka.apache.org/documentation/)
%% trellis:end %%
