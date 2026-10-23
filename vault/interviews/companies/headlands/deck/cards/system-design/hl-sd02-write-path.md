---
id: hl-sd02-write-path
node: system-design.sd02-job-scheduler
type: qa
step: 20
---
## Q
`schedule` 的写路径怎么保证「返回成功 ⟹ 持久」？为什么先日志后内存，group commit 是什么？

## A
写路径：
1. 路由到分片 leader；
2. 单写线程把 `Scheduled` 记录追加到 WAL 缓冲；
3. **group commit**：一个刷盘周期内的所有记录一起 fsync，并并行发送给 2 个 follower；
4. 收到 ≥ 1 个 follower 的持久化确认（2 份副本）后回复调用方成功；
5. 之后才修改内存（job 表 + 时间轮）。

先日志后内存：若先改内存、日志落盘前崩溃，调用方没收到成功、内存也丢了，是安全的；**已经回复成功但日志没落盘**才危险。该顺序保证回复成功 ⟹ 日志在 ≥ 2 处。

group commit：NVMe 单次 fsync 从几十 µs 到 ms 不等，2 万条/s 峰值若每条一次 fsync 会压垮设备，所以把「上一次 fsync 期间到达的所有记录」凑成一批再刷，吞吐随负载自适应，延迟只增加一个 fsync 周期。
