---
id: leetcode-q-removing-min-max-branch-dominance-proof
node: greedy-sorting.greedy
type: cloze
tags: [grown]
---
某数组只能从开头或结尾删除若干个元素，要求原数组中的最小值和最大值都被删除，求最少删除次数。设最小值所在下标为 p、最大值所在下标为 q、数组长度为 n。「前缀删到覆盖下标 p、后缀删到覆盖下标 q」这一种两端都删的方案，总删除次数化简后是 p+n-q+1；把 p、q 角色互换（前缀删到 q、后缀删到 p）就得到 q+n-p+1。两式相减：(p+n-q+1) − (q+n-p+1) = {{c1::2(p-q)}}。因此当 {{c2::p ≤ q}} 时，p+n-q+1 恒不大于 q+n-p+1，后者绝不可能是最优答案——这就是「先排序 p, q 再列策略可以砍掉一个分支」的代数证明。
