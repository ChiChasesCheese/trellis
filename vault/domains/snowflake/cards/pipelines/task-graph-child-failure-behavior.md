---
id: task-graph-child-failure-behavior
node: pipelines.task-failure-handling
type: qa
source: snowflake-docs
---
## Q
任务图（task graph）中根任务之后分出 A、B 两条分支，A 分支中间的一个任务失败了。B 分支和 A 分支后续任务会怎样？

## A
子任务只在其所有前驱任务成功完成后才运行，所以失败任务下游的 A 分支后续任务不会执行；与失败任务没有依赖关系的 B 分支照常运行完成。这次任务图运行整体被记为失败，可以用 `COMPLETE_TASK_GRAPHS` 查看最近完成、失败或取消的图运行。修复后可以只从失败的任务重试，而不必重跑已成功的部分。
