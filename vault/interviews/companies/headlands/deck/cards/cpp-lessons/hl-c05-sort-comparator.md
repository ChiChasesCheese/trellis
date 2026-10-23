---
id: hl-c05-sort-comparator
node: cpp-lessons.c05-stl-containers
type: qa
step: 22
---
## Q
`std::sort` 的比较器必须满足什么条件？用 `<=` 会怎样？

## A
- 比较器必须是**严格弱序**（strict weak ordering）：对相等元素必须返回 `false`，且满足传递性。
- 用 `<=` 的比较器在遇到相等元素时返回 `true`，违反规则，`sort` 内部可能**越界访问而崩溃**（UB）。
- 写法：`std::sort(v.begin(), v.end(), [](const auto& a, const auto& b) { return a.px < b.px; });`
