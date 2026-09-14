---
id: ddl-swap-with-atomic-cutover
node: metadata.ddl-metadata-versioning
type: qa
tags: [grown]
---
## Q
要用重新构建好的表 `t_new` 无缝替换线上表 `t`，为什么 `ALTER TABLE t SWAP WITH t_new` 比“先 DROP 再 RENAME”更好？

## A
SWAP WITH 在一个元数据操作中原子地交换两张表的名字，不移动任何数据，瞬间完成；读取方要么看到交换前的 t，要么看到交换后的 t，不存在表名暂时不存在的空窗。先 DROP 再 RENAME 是两步操作，中间有一段时间 t 不存在，并发查询会报错；而且一旦第二步失败，还得靠恢复被删的表来补救。
