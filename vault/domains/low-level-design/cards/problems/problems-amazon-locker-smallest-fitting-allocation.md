---
id: problems-amazon-locker-smallest-fitting-allocation
node: problems.machines.amazon-locker
type: qa
step: 2
tags: [grown]
---
## Q
快递柜（Amazon Locker）给一件包裹挑柜格的规则是什么？它的代价是什么？用三维尺寸时「最小」怎么定义？

## A
规则是**最小可容纳优先**（smallest fitting）：在所有装得下它的空柜里挑最小的那个。不是精确匹配——小包裹在小柜用完时必须能占中号柜，否则柜子空着还拒单。

代价要说出口：这是贪心，可能把中号柜浪费给小包裹，导致随后到来的中号包裹无处可放。接受它，因为拒收一次投递的成本远高于柜位利用率低一点。

三维尺寸下「装得下」只是**偏序**（partial order），并列时无法比较，所以要补一个全序排序键打破并列：`sort_key = (volume, name)`——先比体积，再比名字。名字这一项纯粹为了确定性：否则同体积的两个尺寸谁先被选中取决于字典迭代顺序，测试会飘。
