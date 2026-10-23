---
id: hl-c06-nth-partial-partition
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 5
---
## Q
`std::nth_element`、`std::partial_sort`、`std::stable_partition` 各做什么？求 top-k 或中位数该用哪个？

## A
- `nth_element(first, nth, last)`：**O(n)**（平均）把第 n 小的元素放到位，左边都不大于它、右边都不小于它，其余无序。例：`{9,4,7,1,8,2,6}` 的 `w[3]` 是第 4 小的 6。
- `partial_sort(first, middle, last)`：只把最小的 k 个排好序放在前面。
- `stable_partition(first, last, pred)`：按谓词分组且保持相对顺序，返回分界迭代器。
- 求 top-k 或中位数**别全排序**：用 `nth_element` 或 `partial_sort`，或用小顶堆。
