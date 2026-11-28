---
id: hi-c-sd-dealing-with-contention-b02-fencing-token
node: sd.patterns.dealing-with-contention.beyond
type: qa
step: 2
---
## Q
**处理竞争 · 带 TTL 的锁为什么需要围栏令牌**｜拓展 · 加分

持有者的租约（lease）过期后它还不知道，继续往存储写，会怎么样？怎么真正挡住它？

## A
- **问题：** 持有者因长 GC 或网络延迟停顿，租约过期，另一个客户端拿到锁；前者醒来后仍认为自己持锁，写入覆盖了新持有者的数据。TTL 只能保证最终释放，不能保证没有重叠。
- **围栏令牌（fencing token）：** 每次授予锁时发一个单调递增的数字，客户端每次写存储时带上它；存储记录见过的最大令牌，拒绝更小的。旧持有者醒来带着旧令牌，被挡在存储一侧。
- **关键：** 检查必须在存储那边做，客户端自己检查没用，因为停顿可以发生在检查和写之间。
- **实践：** ZooKeeper 的事务 ID、etcd 的 revision 天然可作令牌；仅靠 Redis 单实例 TTL 锁给不了这个保证。
