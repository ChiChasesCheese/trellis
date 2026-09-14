---
id: at-before-clone-default-point
node: continuity.at-before-statement-syntax
type: qa
source: snowflake-docs
---
## Q
`CREATE TABLE t2 CLONE t1` 不带 `AT | BEFORE` 子句时，克隆的是哪个时间点的状态？一个大表克隆耗时几分钟，期间 t1 上的写入会进入克隆吗？

## A
不带子句时克隆的是「现在」的状态：为了让耗时较长的克隆行为一致，Snowflake 在内部把 AT 设为语句开始时的时间戳。所以克隆过程中对 t1 提交的写入不会出现在 t2 中。若需要过去的状态，在 CLONE 后面紧跟 `AT` 或 `BEFORE` 子句即可。
