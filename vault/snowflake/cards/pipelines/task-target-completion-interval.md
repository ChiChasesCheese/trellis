---
id: task-target-completion-interval
node: pipelines.task-serverless-vs-warehouse
type: qa
source: snowflake-docs
---
## Q
无服务器任务的「目标完成间隔（target completion interval）」有什么作用？如果任务已经扩到最大规格仍然跑不完会怎样？

## A
设置目标完成间隔后，Snowflake 会估算并扩展资源，力求在该时间内（包括排队时间）完成任务；无服务器触发式任务必须设置它。若任务已达到允许的最大规格仍运行过久，目标完成间隔会被忽略，任务继续运行直到完成、超时或失败。注意：增加资源只能缩短部分 SQL 的运行时间，并不能保证在批处理窗口内完成。
