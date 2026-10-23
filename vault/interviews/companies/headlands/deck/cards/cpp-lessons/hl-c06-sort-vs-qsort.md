---
id: hl-c06-sort-vs-qsort
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 19
---
## Q
面试问：`std::sort` 为什么比 C 的 `qsort` 快？
Interview question: Why is `std::sort` faster than `qsort`?

## A
- `std::sort` 是模板，比较器（lambda 或函数对象）在**编译期已知**，可以**内联**。
- `qsort` 通过**函数指针**对每次比较做间接调用，没法内联。
- 要点：模板 + lambda 让抽象在编译期消失，这是 C++ 的零开销抽象。
