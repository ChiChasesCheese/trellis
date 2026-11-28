---
id: hi-c-sd-shopify-inventory-reservations-x02-redis-or-mysql
node: sd.in-the-wild.shopify-inventory-reservations.exam
type: qa
step: 8
---
## Q
**Shopify 库存预留 · 你的系统该不该搬**｜考点 · 必会

某抽奖活动：10 万个名额，预留 5 分钟，成功后在同一个 PostgreSQL 里写"中奖记录"。团队在用 Redis 计数做预留。请判断：保留还是换成行池？哪些信号会改变你的结论？

## A
- **看"是否必须一起提交"：** 中奖记录在 PostgreSQL，预留在 Redis，同样有"跨库不能一起提交"的窗口。若偶尔的不一致可以接受（多发或少发几个名额可补偿），Redis 计数更简单；若名额不可多发，就把预留放进同库。
- **看争用规模：** 10 万名额、瞬时数千并发，单行计数在 PostgreSQL 里也会排队，但吞吐是否够用取决于峰值 QPS；先压测单行条件更新，不够再用行池加 `SKIP LOCKED`（PostgreSQL 同样支持）。
- **看过期怎么办：** 行池方案的过期靠 `expires_at` 过滤，不需要额外触发。
- **改变结论的信号：** 峰值更高、名额更大（需要有界池）、对账不能容忍任何不一致（必须同库）。
