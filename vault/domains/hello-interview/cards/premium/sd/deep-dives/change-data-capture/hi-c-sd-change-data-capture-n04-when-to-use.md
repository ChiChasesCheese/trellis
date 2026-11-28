---
id: hi-c-sd-change-data-capture-n04-when-to-use
node: sd.deep-dives.change-data-capture.notes
type: qa
step: 4
---
## Q
**变更数据捕获 · 什么时候该用 CDC**｜摘要 · 必会

什么样的场景最适合 CDC？三个共同特征是什么？

## A
- **核心：** 一个系统是真相来源，另一个系统需要它的派生副本（derived copy）。派生的意思是：把下游整个丢掉，也能从源头重建，下游没有任何别处没有的东西。
- **三个典型：** 保持派生索引同步；把线上库复制到数据仓库；零停机数据库迁移。
- **共同特征一，源始终权威：** 同步期间 Postgres 一直是 system of record。
- **共同特征二，可以有滞后：** 下游不必在原请求返回前就反映这次写入。
- **共同特征三，目标可重建：** 出问题可以从源头重建或修复，CDC 同时继续运行。
