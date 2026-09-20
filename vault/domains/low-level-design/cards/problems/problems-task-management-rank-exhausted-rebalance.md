---
id: problems-task-management-rank-exhausted-rebalance
node: problems.social.task-management
type: qa
step: 3
tags: [grown]
---
## Q
任务看板设计里，如果反复把新卡插到同一对相邻卡片之间，秩的间距会怎样，系统该怎么应对？

## A
取中点 `prev + (next - prev) / 2` 算出来的值会越来越逼近其中一端，因为浮点数的精度有限，最终中点会因为舍入直接等于 prev 或 next，这时候已经分不出一个严格夹在两者之间的新秩，插入操作会抛出一个信号异常。调用方捕获它之后，把这一整列的秩重新铺成等间距的整数（0, 1, 2, …），代价是 O(列长)，但只在这条缝真的被挤爆的那一次才发生，不是每次插入都要付出的成本——这样插入的均摊代价仍然接近 O(1)。
