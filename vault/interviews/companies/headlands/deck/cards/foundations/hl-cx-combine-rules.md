---
id: hl-cx-combine-rules
node: foundations.complexity
type: qa
step: 6
---
## Q
分析代码复杂度时，顺序执行、嵌套、调用函数三种情况分别怎么组合？哪一种最容易漏？

## A
- **顺序执行 → 相加**：先 O(n) 再 O(n²)，总共 O(n + n²) = O(n²)。
- **嵌套 → 相乘**：外层 n 次、每次内层 log n 步，总共 O(n log n)。
- **调用函数 → 代入那个函数的复杂度**：循环 n 次、每次 `list.contains(x)`（O(n)），总共 O(n²)。

第三条**最容易漏**：函数调用藏着一个看不见的循环。
