---
id: amz-closest-store-how-asked-and-three-questions
node: amazon.amz-closest-store
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「增删查最近值（Add / Remove / Closest）」这道 OOD 题是怎么问的？开场先问哪三个澄清问题？

## A
报告（一亩三分地，2026-09 电面，只有片段，API 细节为（重建））：维护一组整数，支持 add、remove，以及找离 target 最近的数；后来又给了值域约束（range constraint）。三个问题：(1) 一样近怎么办——决定平局规则（在增删查最近值设计里默认取较小的）；(2) 允许重复值吗——决定 remove 删一个还是全部；(3) 值域多大——有界就能用树状数组，无界只能用有序列表。
