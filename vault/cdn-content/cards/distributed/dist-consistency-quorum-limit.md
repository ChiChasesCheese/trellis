---
id: dist-consistency-quorum-limit
node: distributed.consistency
type: qa
---
## Q
Does choosing `W + R > N` automatically make a leaderless cache strongly consistent?

## A
No. The quorum overlap helps only with assumptions about replica membership, version comparison, concurrent writes, sloppy quorums, clock behavior, and read repair. A read may still see conflicts or stale replicas if failures change the participating set. Use versioned values and conflict resolution, define whether the store is authoritative, and test partition behavior. Quorum arithmetic is one mechanism, not the complete consistency contract.

## Q zh
选择 `W + R > N` 是否会自动让 leaderless cache 变成 strongly consistent？

## A zh
不会。quorum overlap 只有在 replica membership、version comparison、concurrent write、sloppy quorum、clock behavior 与 read repair 等假设成立时才有帮助。若故障改变参与集合，read 仍可能看到 conflict 或 stale replica。应使用 versioned value 和 conflict resolution，明确 store 是否 authoritative，并测试 partition behavior。quorum arithmetic 只是一个机制，不是完整 consistency contract。
