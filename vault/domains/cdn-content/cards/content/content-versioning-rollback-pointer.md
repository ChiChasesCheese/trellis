---
id: content-versioning-rollback-pointer
node: content.versioning
type: qa
---
## Q
Why is rollback safer when it repoints traffic to an existing immutable deployment instead of rebuilding the previous commit?

## A
Repointing restores the exact artifact already tested and previously served. Rebuilding can change dependencies, build images, timestamps, or external data, producing bytes that were never validated. Keep prior deployment artifacts and config available for a defined rollback window, switch the routing pointer atomically, and verify user-facing metrics. A rollback is a routing operation; a rebuild is a new release.

## Q zh
为什么 rollback 应把流量指回现有 immutable deployment，而不是重新 build 上一个 commit？

## A zh
重新指向会恢复已经测试且实际服务过的精确 artifact。rebuild 可能改变 dependency、build image、timestamp 或 external data，产生从未验证过的 bytes。在明确 rollback window 内保留旧 deployment artifact 与 config，原子切换 routing pointer，并验证 user-facing metrics。rollback 是 routing operation；rebuild 是新 release。
