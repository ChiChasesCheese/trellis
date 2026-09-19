---
id: kafka-connect-connector-vs-task-division
node: connect.connect-basics
type: qa
step: 3
source: kafka-2e
---
## Q
在 Connect 里，「连接器（connector）」和它启动的「任务（task）」分别负责什么？以 JDBC 数据源连接器为例说明两者是怎么分工的。

## A
连接器本身**不直接搬运数据**，它负责三件事：决定要运行多少个任务、决定如何把数据复制工作拆分给这些任务、把每个任务的具体配置信息传给 worker（Connect 的运行节点）去启动任务。「任务」才是真正把数据搬进或搬出 Kafka 的执行单元。以 JDBC 数据源连接器为例：它连接数据库后统计出要同步的表的数量，在配置参数 `tasks.max`（任务数上限）和实际表数量之间取较小值作为任务数，然后为每个任务生成一份包含「要负责哪些表」的配置；之后真正连接数据库、读取每张表数据的工作，是由各个任务分别执行的。
