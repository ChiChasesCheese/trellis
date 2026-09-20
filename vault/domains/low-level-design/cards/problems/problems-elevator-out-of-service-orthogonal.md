---
id: problems-elevator-out-of-service-orthogonal
node: problems.machines.elevator
type: qa
step: 7
tags: [grown]
---
## Q
电梯系统要支持“把一部梯停用去检修”。应该给状态机加一个 OUT_OF_SERVICE 状态，还是加一个布尔字段？为什么？

## A
加布尔字段 `in_service`。“是否可用”和“此刻在做什么”是正交的两维：一部梯可以停用中而门正开着（师傅在里面），也可以停用中而正在下行（把最后一车人送到）。塞进同一个枚举就要造出 IDLE_OUT_OF_SERVICE、DOORS_OPEN_OUT_OF_SERVICE……状态数翻倍，这是状态爆炸的标准起点。做成正交字段后它只影响一件事——不再接新的外呼，所以只有派梯前的过滤读它，推进一拍的 `step()` 从头到尾不看它，于是“车里的人照样被送到”成了设计的直接推论，不需要任何特判。
