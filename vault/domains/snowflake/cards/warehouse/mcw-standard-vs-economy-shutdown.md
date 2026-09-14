---
id: mcw-standard-vs-economy-shutdown
node: warehouse.multi-cluster-scaling-policy
type: qa
source: snowflake-docs
---
## Q
多集群仓库（multi-cluster warehouse）负载下降时，Standard 与 Economy 伸缩策略（scaling policy）如何决定关掉哪个集群、何时关？

## A
Standard：在持续一段时间低负载之后，关闭一个或多个负载最轻的集群，并等其上的查询跑完才关。Economy：若估计负载最轻的集群剩余工作不足 6 分钟，就把它标记为待关闭，跑完其上正在执行的查询后关闭。两种策略下，集群数 ≤10 时空闲集群逐个关闭，>10 时可能一次关闭多个。
