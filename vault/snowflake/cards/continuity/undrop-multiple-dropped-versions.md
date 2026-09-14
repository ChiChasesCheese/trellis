---
id: undrop-multiple-dropped-versions
node: continuity.undrop-recovery
type: qa
source: snowflake-docs
---
## Q
表 `t` 被删除、重建、再删除，于是有两个已删除版本。如何看到它们？UNDROP 会先恢复哪一个，怎样把两个都找回来？

## A
用 `SHOW TABLES HISTORY` 查看：输出包含所有已删除对象和 `DROPPED_ON` 列，同一对象被删除多次时每个版本单独一行；已过保留期被清除的版本不再显示。UNDROP 先恢复最近被删除的版本；把恢复出来的表改名后再执行一次 UNDROP，就能恢复更早的版本。
