---
id: hl-c11-three-way-compare
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 3
---
## Q
`memcpy`、`memmove`、`std::copy` 在单位、重叠区域、非平凡类型、头文件上各有什么区别？

## A
| | `memcpy` | `memmove` | `std::copy` |
|---|---|---|---|
| 单位 / 类型检查 | 字节，无 | 字节，无 | **元素**，有 |
| 重叠区域 | **UB** | 定义良好 | `d_first` 不能落在 `[first,last)` 内（否则用 `copy_backward`） |
| 非平凡类型（`string`、虚函数、自定义拷贝） | **UB** | 同左 | 正确（调用拷贝赋值） |
| 头文件 / 速度 | `<cstring>`，高度优化 | `<cstring>`，略多一次重叠判断 | `<algorithm>`，平凡类型编译成 `memmove`，否则逐元素 |
