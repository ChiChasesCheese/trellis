---
id: hl-cq-cs07-malloc-new
node: cpp-questions.cheatsheet
type: qa
step: 7
---
## Q
一句话背诵：`malloc` 和 `new` 的区别（失败方式、释放、数组、能否混用、placement new）。

## A
- `malloc`：未初始化字节，失败返回 `NULL`，`free`。
- `new` = `operator new` + **构造函数**，失败抛 `bad_alloc`，`delete` 先析构。
- `new[]` 配 `delete[]`，不能混用；`new` 可重载。
- placement new 在已有内存上构造。
