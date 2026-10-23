---
id: hl-c06-java-mapping
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 1
---
## Q
Java 的 `Collections.sort`、`binarySearch`、`stream().filter().map()`、`Comparator.comparing` 在 C++ 里分别对应什么？C++ 算法的设计特点是什么？

## A
- `Collections.sort(list, cmp)` ↔ `std::sort(v.begin(), v.end(), cmp)`
- `Collections.binarySearch` ↔ `std::lower_bound` / `upper_bound` / `binary_search`
- `stream().filter().map().collect()` ↔ `v | views::filter(..) | views::transform(..)`（C++20）
- `Comparator.comparing(...)` ↔ lambda 或 ranges 的**投影**（projection）
- 匿名内部类 / lambda ↔ lambda，可显式选择按值/按引用捕获

特点：C++ 算法接受**迭代器区间 `[first, last)`**，不依赖具体容器；与 lambda 一起会被**内联**，没有装箱、没有虚调用。
