---
id: hi-pt-recently-viewed-items-6-race-tradeoff
node: qb.lld.recently-viewed-items.points
type: qa
step: 7
---
## Q
**"最近浏览"记录 · 可接受的竞态**｜追问 · 出自："最近浏览"记录 › 深入 4

"最近浏览"里客户刚被外层淘汰，另一线程还拿着旧的有序字典写入。会怎样，要不要处理？

## A
**后果。** 这次写入丢失。
**判断。** 对最近浏览这种尽力而为的数据可以接受。
**不能容忍时。** 外层和内层用同一把锁，代价是争用变高。
