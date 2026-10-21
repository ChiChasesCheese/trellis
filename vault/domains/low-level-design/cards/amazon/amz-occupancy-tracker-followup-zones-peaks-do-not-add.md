---
id: amz-occupancy-tracker-followup-zones-peaks-do-not-add
node: amazon.amz-occupancy-tracker
type: qa
step: 6
tags: [grown]
---
## Q
在办公室人数追踪里，面试官追问「有多个楼层或楼栋」。该怎么改？区域的最大人数能相加吗？

## A
事件加 `zone` 字段，追踪器给每个区域一条 `Timeline`，再加一条全局的，每个事件同时写进两条；`zone=None` 表示整个办公室，所有查询仍是一次二分。换楼层是一次离开加一次进入，离开的区域必须与进入时一致。前缀和可以相加，峰值不能：1 楼 1 点有 1 人，2 楼 3 点有 1 人，两个峰值相加得 2，办公室任意时刻最多 1 人。所以全局峰值要查全局时间线。
