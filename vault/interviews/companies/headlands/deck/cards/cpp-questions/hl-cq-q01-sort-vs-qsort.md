---
id: hl-cq-q01-sort-vs-qsort
node: cpp-questions.a-why-fast
type: qa
step: 2
---
## Q
对 500 万个 `int` 排序，`std::sort` 和 C 的 `qsort` 谁快、差多少？为什么？这说明了什么原则？

## A
- 数字：`std::sort` 约 **81 ms**，`qsort` 约 **303 ms**，差约 4 倍。
- 原因：`std::sort` 的比较函数是**模板参数**，被内联进排序循环；`qsort` 的比较函数是**函数指针**，每次比较一次间接调用，无法内联。
- 原则：这就是“零开销抽象”——抽象在编译期被展开掉。
- 反面：性能是“可以做到”而不是“自动得到”。`std::list`、到处用 `shared_ptr`、热路径抛异常、`-O0` 的 debug 构建，都会很慢。
