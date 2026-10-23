---
id: hl-sd02-architecture
node: system-design.sd02-job-scheduler
type: qa
step: 10
---
## Q
推荐设计「每分片一个单写者 + WAL + 分层时间轮」的组件有哪些？命令和数据怎么流动？

## A
- **API / 网关**（无状态）：`schedule` / `cancel` / `get`，校验、幂等（客户端 job id）、路由 shard = `hash(jobId) % N`；
- **分片**：一个 leader + 2 个 follower；
- **单写线程**依次：① 追加 WAL（group commit，复制到 follower）；② 修改内存状态（job 表 + 时间轮）；命令通过 MPSC 队列进来，时钟 tick 也驱动它；
- **job 表**（open addressing：id → slot）：`long[] fireAt`、`int[] state`、`int[] next/prev`、`long[] payloadOff`；
- **分层时间轮**（近期 ≤ 10 分钟）：L0 10 ms × 256，L1 2.56 s × 64……；
- **远期桶**：磁盘上按小时分段的有序文件，距离到期 < 10 分钟时装载进时间轮；
- **分发器**（异步）：限速、按租户公平，把到期批交给队列 / 回调，成功后回写单写线程追加 `Fired(jobId, epoch)`；
- **快照**（每 N 分钟或日志段滚动）+ WAL ⇒ 崩溃恢复 / follower 追赶。
