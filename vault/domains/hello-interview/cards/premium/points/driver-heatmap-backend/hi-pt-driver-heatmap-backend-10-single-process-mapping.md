---
id: hi-pt-driver-heatmap-backend-10-single-process-mapping
node: qb.sd.driver-heatmap-backend.points
type: qa
step: 10
---
## Q
**司机热力图 · 单机计数的对应**｜追问 · 出自：司机热力图 › 取舍与追问

司机热力图在单进程里只要一个 HashMap 加一个计数数组。分布式后，计数更新、失联超时、20 分钟窗口各自对应什么，多出什么问题？

## A
**计数。** 单机 count[old]--; count[new]++ 一个函数，天然不漂移；分布式后这对操作落在两个分区，变成两条消息，出现重复和乱序，需要检查点和定期校正。

**失联。** 按 lastSeen 排序的最小堆，变成流处理定时器，本质是延迟队列。

**窗口。** 按分钟分桶的环形计数器，变成每分钟一份快照加聚合。
