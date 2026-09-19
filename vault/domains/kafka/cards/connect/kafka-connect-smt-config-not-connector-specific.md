---
id: kafka-connect-smt-config-not-connector-specific
node: connect.smt
type: qa
step: 2
source: kafka-2e
---
## Q
在给某个连接器加一个 SMT（比如给 MySQL 数据源连接器加 `InsertHeader`）时，这个 SMT 的配置和使用方式是不是要针对不同的连接器类型分别学习一套专属语法？

## A
不是。SMT 的配置方式与具体使用哪个连接器无关，是 Connect 框架层面提供的统一能力：不管底层连接的是 MySQL、ElasticSearch 还是其他系统，都在连接器配置里用相同的 `transforms`、`transforms.<name>.type` 等参数声明要用哪个 SMT、传什么参数。这意味着一旦学会了给一种连接器配置 SMT，同样的配置模式可以直接套用到任何其他连接器上，不需要为每种连接器单独学习一套转换配置语法。
