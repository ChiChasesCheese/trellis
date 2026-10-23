---
id: hl-omap-why-ordered
node: foundations.ordered-maps-trees
type: qa
step: 1
---
## Q
`HashMap` 回答不了哪些问题？为什么订单簿的价位要放进有序 Map，有哪三种有序做法？

## A
`HashMap` 能 O(1) 回答「key = 100 的值」，但答不了：最小的 key（订单簿**最优卖价**）、≤ 104 的最大 key（前驱 / 向下取整）、key 在 [103, 110) 的全部条目（范围查询）、按 key 从小到大遍历。

订单簿每秒几十万次新增或删价位，每次撮合还要取最优价：排好序的数组插入 O(L)（L 是价位数），平衡树 O(log L)。

三种做法：
1. **二叉搜索树（BST）**：最直观，但会退化；
2. **平衡树（红黑树）**：自动保持矮胖，`TreeMap` 就是红黑树；
3. **跳表（skip list）**：用随机数代替复杂规则，天然适合并发，`ConcurrentSkipListMap` 就是跳表。
