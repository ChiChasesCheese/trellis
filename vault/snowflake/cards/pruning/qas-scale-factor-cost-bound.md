---
id: qas-scale-factor-cost-bound
node: pruning.query-acceleration-service
type: qa
source: snowflake-docs
---
## Q
给一个 Medium 仓库（每小时 4 credit）开启查询加速服务（QAS），并把 `QUERY_ACCELERATION_MAX_SCALE_FACTOR`（最大扩展系数）设为 5，最多会多花多少钱？设为 0 意味着什么？

## A
扩展系数是成本上限：仓库最多可租用相当于自身规模 5 倍的计算资源，即最多额外 4 × 5 = 20 credit/小时。这个上限作用于整个仓库，不论同时有多少查询在用 QAS；实际只按秒计费、仅在服务使用时计费，并与仓库费用分开出账。设为 0 则取消上限，查询可以租用所需且可用的任意多资源。
