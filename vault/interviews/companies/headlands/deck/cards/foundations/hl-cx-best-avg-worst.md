---
id: hl-cx-best-avg-worst
node: foundations.complexity
type: qa
step: 13
---
## Q
最好、平均、最坏情况（best / average / worst case）各指什么？以线性查找为例各是多少？为什么报平均复杂度必须先说假设？

## A
对同一个 n，**最坏**= 步数最多的输入，**最好**= 最少的，**平均**= 在某个假设的输入分布下的期望步数。

线性查找：
- 最好：target 在 `a[0]`，1 次比较，O(1)；
- 最坏：target 在末尾或不存在，n 次，O(n)；
- 平均：**假设**target 等可能在 n 个位置之一，(n+1)/2 次，O(n)。

若 target 几乎总在开头（热点数据），平均就是 O(1)。**不说假设就报平均复杂度是不严谨的。**
