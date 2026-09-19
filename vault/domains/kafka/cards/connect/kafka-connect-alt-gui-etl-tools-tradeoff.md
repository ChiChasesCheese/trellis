---
id: kafka-connect-alt-gui-etl-tools-tradeoff
node: connect.alternatives
type: qa
step: 3
source: kafka-2e
---
## Q
Informatica、Talend、Pentaho、Apache NiFi、StreamSets 这类基于图形界面的 ETL 工具也能把 Kafka 当作数据源或数据池使用。如果团队已经在用这类工具搭建数据管道，是不是应该改用 Connect 来对接 Kafka？这类图形化 ETL 工具的主要缺点是什么？

## A
如果团队已经在用某个图形化 ETL 工具（比如 Pentaho）搭建数据集成流程，通常没有必要仅仅为了接入 Kafka 就额外再引入一套集成工具，继续沿用熟悉的图形化方案即可。这类工具的主要缺点是它们的工作流普遍比较复杂厚重：如果需求只是单纯地把数据从 Kafka 读出来或写进 Kafka，用这种面向复杂可视化流程设计的重型工具会显得大材小用。做数据集成时更应该把注意力集中在「把消息可靠地送到该去的地方」这件核心事情上，而大部分通用 ETL 工具的复杂度已经超出了这个核心需求本身。
