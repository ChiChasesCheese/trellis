---
id: delivery-rollback-state
node: delivery.rollback
type: qa
---
## Q
The binary rollback completed, but users still receive bad cached objects. Why was rollback incomplete?

## A
The release changed durable data-plane state that the old binary continues to read. A rollback plan must inventory cache entries, manifests, config versions, schema, and background jobs; then choose versioned isolation, targeted purge, or backward-compatible readers. Verify both code version and state recovery. Reverting compute alone does not undo cache poisoning or incompatible writes.

## Q zh
binary rollback 已完成，但用户仍收到 bad cached object。为什么 rollback 不完整？

## A zh
release 改变了 durable data-plane state，而旧 binary 仍会读取它。rollback plan 必须清点 cache entry、manifest、config version、schema 和 background job，再选择 versioned isolation、targeted purge 或 backward-compatible reader。要同时验证 code version 和 state recovery。只回退 compute 无法撤销 cache poisoning 或 incompatible write。
