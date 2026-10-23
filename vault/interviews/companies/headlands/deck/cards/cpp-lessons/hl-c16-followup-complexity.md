---
id: hl-c16-followup-complexity
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 17
---
## Q
面试问：你的解法复杂度？空间？能优化吗？为什么用 `unordered_map` 不用 `map`？
Interview question: What is the complexity of your solution and why that container?

## A
- 先答 O(·)，再说瓶颈（哈希 vs 排序 vs 堆）：「k 很小用堆，k 接近 n 用排序 / `nth_element`」。
- 只需点查 → `unordered_map` 平均 O(1)；要有序遍历/范围查询/最小最大 → `map` O(log n)。
- 自定义 key 要提供哈希和 `==`。
