---
id: analytics-idempotent-reruns
node: analytics.batch
type: qa
---
## Q
Why are batch jobs designed so the whole run can be thrown away and re-executed, and what two properties of the job make that safe?

## A
Because failure handling *and* bug recovery both become "just run it again": a crashed job, a bad deploy, or a logic error discovered next week are all fixed by rerunning over the unchanged input. DDIA calls this **human fault tolerance** — the cheapest recovery story in data engineering.

Required properties:
- **Immutable inputs**: the job never mutates its source; it reads raw data and writes elsewhere.
- **Deterministic, atomically-published outputs**: same input → same output, made visible in one atomic step (temp dir + rename, or overwrite a whole partition / table-format snapshot commit) so partial output from a failed attempt is never observed and reruns replace rather than double-count.

## Q zh
为什么 batch job 设计使得整个运行可以被丢弃并重新执行，什么两个 job 属性使那个安全？

## A zh
因为故障处理*和* bug 恢复都变成"只是再运行一次"：崩溃的 job、坏的部署、或下周发现的逻辑错误都通过在不变输入上重新运行来修复。DDIA 称这个为**人性容错** — 数据工程中最便宜的恢复故事。

需要的属性：
- **不可变输入**：job 从不变异其源；它读原始数据并写到其他地方。
- **确定性、原子发布的输出**：相同输入 → 相同输出，在一个原子步骤中可见（temp dir + rename，或覆盖整个 partition / table-format 快照提交），所以失败尝试的部分输出从不被观察，重运行替换而不是双计数。
