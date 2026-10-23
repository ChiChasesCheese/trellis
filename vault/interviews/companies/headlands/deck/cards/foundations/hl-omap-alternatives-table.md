---
id: hl-omap-alternatives-table
node: foundations.ordered-maps-trees
type: qa
step: 2
---
## Q
无序数组 / `HashMap`、排好序的 `ArrayList`、「`HashMap` 每次排序」、平衡树 / 跳表，在取最小、插入、范围查询上的复杂度各是多少？

## A
- 无序数组 / `HashMap`：取最小 O(n)，插入 O(1)，范围查询 O(n)；
- 排好序的 `ArrayList`：取最小 O(1)，插入 **O(n)**（二分找位置 O(log n)，但要挪元素），范围查询 O(log n + k)；
- `HashMap` + 每次用时排序：取最小 O(n log n)，插入 O(1)，范围 O(n log n)；
- **平衡树 / 跳表**：取最小 **O(log n)**，插入 **O(log n)**，范围查询 **O(log n + k)**，缺点是常数较大。
