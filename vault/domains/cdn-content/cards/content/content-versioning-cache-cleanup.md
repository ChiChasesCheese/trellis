---
id: content-versioning-cache-cleanup
node: content.versioning
type: qa
---
## Q
After rollback, should the team purge every cache object produced by the bad deployment?

## A
Usually no broad purge is needed if deployment identity and content-hashed URLs isolate artifacts: repoint traffic, and the bad snapshot becomes unreachable. Purge only mutable aliases or incorrectly keyed objects that can still be selected. A fleet-wide purge can create a cold-cache origin storm during incident recovery. Prove the active pointer and cache-key isolation first, then remove residual unsafe entries surgically.

## Q zh
rollback 后，团队是否应 purge 坏 deployment 产生的所有 cache object？

## A zh
如果 deployment identity 和 content-hashed URL 正确隔离 artifact，通常不需要 broad purge：只需重指流量，坏 snapshot 就不可达。仅 purge 仍可能被选中的 mutable alias 或错误 key object。fleet-wide purge 会在 incident recovery 时制造 cold-cache origin storm。先证明 active pointer 与 cache-key isolation，再外科式清理残余 unsafe entry。
