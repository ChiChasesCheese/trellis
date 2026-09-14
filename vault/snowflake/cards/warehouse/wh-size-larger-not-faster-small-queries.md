---
id: wh-size-larger-not-faster-small-queries
node: warehouse.sizing-t-shirt
type: qa
source: snowflake-docs
---
## Q
BI 看板上都是毫秒到秒级的简单小查询，把仓库从 Small 升到 X-Large 会怎样？该怎么确定合适的规格？

## A
通常不会明显变快：小而简单的查询用不上额外的计算资源，无论并发多少，“更大”都不等于“更快”，却要付几倍的 credit。应让仓库规格匹配预期查询的大小和复杂度：拿同一批查询（最好是一般 5–10 分钟内能跑完的）在 X-Large、Large、Medium 等多个规格上实测，再选性价比最好的。
