---
id: wh-size-bigger-can-cost-same
node: warehouse.sizing-t-shirt
type: qa
source: snowflake-docs
---
## Q
一条复杂的大查询在 Medium 仓库上跑 20 分钟。换成 Large 仓库，为什么总 credit（信用点）花费可能差不多，却更快出结果？

## A
规格决定仓库中每个集群可用的计算资源，每升一档资源翻倍、每小时 credit 也翻倍。对较大、较复杂的查询，性能大体随仓库规格线性提升，所以 Large 可能约 10 分钟跑完：费率是 2 倍、时长是一半，总花费接近。Snowflake 按秒计费，查询跑完即可挂起，因此不必执着于把规格压到最小，而应通过实验找到延迟与成本最合适的组合。
