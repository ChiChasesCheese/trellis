---
id: hl-c10-delete-array
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 3
---
## Q
面试问：`delete` 和 `delete[]` 有什么区别？配对规则是什么？
Interview question: What is the difference between `delete` and `delete[]`?

## A
- `new[]` 在分配块里**记录元素个数**，`delete[]` 据此**逐个调析构**；对 `new Widget[2]` 用 `delete[]` 会运行两次析构，用 plain `delete` 是 UB。
- 配对规则：`new`↔`delete`，`new[]`↔`delete[]`，`malloc`↔`free`，**不能交叉**。
- ASan 能抓到配对错误：`alloc-dealloc-mismatch`。
- 现代做法：不手写，用 `vector` / 智能指针。
