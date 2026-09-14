---
id: clone-billing-storage-metrics-columns
node: continuity.clone-storage-billing
type: cloze
tags: [grown]
---
`TABLE_STORAGE_METRICS` 把一张表的计费存储拆成四类：{{c1::`ACTIVE_BYTES`}}（当前表版本引用的数据）、{{c2::`TIME_TRAVEL_BYTES`}}（仍在时间旅行保留期内的历史数据）、{{c3::`FAILSAFE_BYTES`}}（处于故障保护期的数据）、{{c4::`RETAINED_FOR_CLONE_BYTES`}}（已从本表删除但仍被克隆引用的数据）。
