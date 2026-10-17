---
id: amz-train-fare-how-asked-and-three-questions
node: amazon.amz-train-fare
type: qa
step: 1
tags: [grown]
---
## Q
火车线路票价（Train Fare Calculator）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是一个票价计算器：线路 G→U→H→K→I 上相邻两站费用 1（G 到 I 是 4），实现 calculateFare(start, stop)；之后线路要能动态加站，周末总票价要有上限。三个问题，每个答案都会改变设计：(1) 封顶封「单程」还是「一人一天累计」——前者不用记任何东西，后者要有记账的类；(2) 加站只追加还是可插中间——追加 O(1)，插中间要重排 O(n)；(3) 每区间是否同价——同价用位置差，不同价要存每段价格再用前缀和（逐项累加的和）。
