---
id: hl-c09-defence-checklist
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 14
---
## Q
防御 C++ 未定义行为的七条清单是什么？

## A
1. 用 `vector`/`string`/`array` 与迭代器代替裸数组和指针算术；调试时用 `.at()`。
2. 不手写 `new/delete`，用智能指针（悬空和 double free 大幅减少）。
3. 变量声明即初始化（`int x{};`）。
4. 溢出敏感处用 `long long`/`uint64_t`，或检查边界后再运算；倒序循环写 `for (size_t i = n; i-- > 0;)`。
5. 多线程数据要么 `atomic`、要么 `mutex`、要么不共享。
6. 位重解释用 `memcpy` / `bit_cast`。
7. 所有警告都当作 bug 处理。
