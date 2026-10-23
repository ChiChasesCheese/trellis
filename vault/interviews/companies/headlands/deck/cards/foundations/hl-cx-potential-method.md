---
id: hl-cx-potential-method
node: foundations.complexity
type: qa
step: 26
---
## Q
摊还分析的势能法（potential method）一句话怎么说？它与核算法什么关系？

## A
给数据结构定义「势能」Φ（例如 Φ = 2 × 元素数 − 容量），一次操作的摊还代价 = 实际代价 + ΔΦ。扩容时势能骤降，正好抵消那次 O(n) 的实际代价。

势能法与核算法本质相同（把预付的硬币看成存在结构里的势能），在复杂数据结构里更方便。
