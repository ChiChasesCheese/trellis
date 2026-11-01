---
id: hi-pt-like-unlike-system-6-hot-counter
node: qb.sd.like-unlike-system.points
type: qa
step: 6
---
## Q
**点赞与取消点赞系统 · 热门内容计数**｜出自：点赞与取消点赞系统 › 深入 1

点赞系统里一个爆款每秒 5 万次点赞，天真的 UPDATE count = count + 1 会怎样？有哪些替代？

## A
**问题。** 所有写落在同一行同一分区，成为瓶颈。
**选项。** A 计数分片（sharded counter），拆 N 个子计数器随机加、读时求和；B 流式聚合，聚合器按短窗口（如 1 秒）合并增量，每内容每秒只写一次；C 读时统计事实表，太慢不可行。
**选择。** B 为主，超大热点叠加 A；B 还能削峰，写入量与点赞量脱钩。
