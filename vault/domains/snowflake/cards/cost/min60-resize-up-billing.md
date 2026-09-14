---
id: min60-resize-up-billing
node: cost.warehouse-billing-60s-minimum
type: qa
source: snowflake-docs
---
## Q
把正在运行的 Small 仓库（2 credit/小时）调整为 Medium（4 credit/小时），调整本身会产生最低计费吗？按多少计？

## A
会。每次把仓库调大，都会对新增的算力收取 1 分钟的费用，只按增量计：Small → Medium 新增 2 credit/小时，所以收取 1 分钟 × 2 credit/小时的费用，之后按新尺寸按秒计费。新增资源不影响已在运行的查询，只在就绪后服务排队或新提交的查询。另外，从 5X-Large 或 6X-Large 调小到 4X-Large 及以下时，旧资源停止（quiesce）期间会短暂同时计费新旧两份资源。
