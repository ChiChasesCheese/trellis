---
id: dt-adaptive-vs-auto
node: pipelines.dynamictable-adaptive-refresh
type: qa
source: snowflake-docs
---
## Q
`AUTO` 和 `ADAPTIVE` 两种刷新模式都会「自动选择」，二者的决策时机有什么根本区别？

## A
AUTO 只在创建动态表时做一次决定：根据定义是否支持增量刷新选择 INCREMENTAL 或 FULL，之后固定不变。ADAPTIVE 在运行期间持续判断：平时走增量刷新，某次检测到上游变化量很大时，就在那次刷新中改为重新初始化。AUTO 回答的是「能不能增量」，ADAPTIVE 回答的是「这一次增量是否值得」。
