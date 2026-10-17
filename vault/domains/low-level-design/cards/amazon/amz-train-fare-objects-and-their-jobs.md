---
id: amz-train-fare-objects-and-their-jobs
node: amazon.amz-train-fare
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，应有哪几个对象？各自只负责什么？

## A
这个系统是「一条线路 + 一串定价规则」，对象如下。`Money`：整数「分」的值对象（创建后不可变，按值比较），没有浮点。`Route`：线路，拥有站名、各区间价格与前缀和，任意两站票价由它回答。`FareRule`：无状态的定价规则（不记任何历史）（如周末封顶），输入当前价格与行程，输出新价格。`FareCalculator`：把线路与规则按列表顺序串起来，时钟注入。`DailyCapLedger`：唯一有状态的类，记同一乘客同一天已付多少。切分依据：变化原因各不相同。
