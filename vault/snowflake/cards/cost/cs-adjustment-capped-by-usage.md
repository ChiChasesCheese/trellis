---
id: cs-adjustment-capped-by-usage
node: cost.cloud-services-free-tier
type: qa
source: snowflake-docs
---
## Q
某天仓库用了 100 credit，云服务只用了 4 credit；另一天仓库用了 100 credit，云服务用了 15 credit。这两天云服务各计费多少？月度调整额为什么可能远小于 10%？

## A
第一天：调整额上限为 10 credit，但每日调整额永远不超过当天实际云服务用量，所以抵扣 4 credit，计费 0。第二天：抵扣 10 credit，计费 5 credit。月度账单上的调整额是每天调整额之和；由于云服务用量低的日子只能抵扣实际用量、没用满的额度不能留到别的日子，月度总调整额可能明显小于月度仓库用量的 10%。
