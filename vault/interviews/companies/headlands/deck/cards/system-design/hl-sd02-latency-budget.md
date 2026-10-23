---
id: hl-sd02-latency-budget
node: system-design.sd02-job-scheduler
type: qa
step: 25
---
## Q
任务调度器的延迟预算由哪几项组成？容量不等式是什么？

## A
延迟(job) = 等待到 tick（≤ 10 ms）+ 出轮到分发器入队（< 5 ms）+ **分发排队**（容量不足时！）+ 下游发布 p99（约 20 ms）[+ 故障切换 ≤ 10 s，仅故障期间]。

Δ 是**承诺**，所以必须有容量规划：**最大同时到期数 / Δ ≤ 分发容量**。把这个不等式写出来。
