---
id: hl-c07-selftest
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 14
---
## Q
自测：折叠表达式 `(xs + ...)` 展开 `sum_all(1, 2, 3)` 得到什么？`consteval` 函数能用运行期值调用吗？

## A
- 展开成 `1 + (2 + 3)`（右折叠），结果 **6**。
- **不能**：`consteval` 函数必须在编译期求值，用运行期值调用是编译错误。普通 `constexpr` 函数则两种都行。
