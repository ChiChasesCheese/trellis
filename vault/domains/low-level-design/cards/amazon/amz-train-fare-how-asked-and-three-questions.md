---
id: amz-train-fare-how-asked-and-three-questions
node: amazon.amz-train-fare
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「火车线路票价（Train Fare Calculator）」是怎么问的？开场先问哪三个澄清问题？

## A
报告（一亩三分地，2026-10-12 现场面）：线路 G→U→H→K→I，相邻站费用 1（G 到 I 是 4），实现 calculateFare(start, stop)；再支持动态加站；再追问周末总票价封顶。三问：(1) 封顶封「单程」还是「一人一天累计」——前者无状态，后者要记账；(2) 加站只追加还是可插中间——O(1) 对 O(n)；(3) 每区间是否同价——决定用位置差还是前缀和。
