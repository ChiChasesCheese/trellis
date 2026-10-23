---
id: hl-cq-cs08-smart-pointers
node: cpp-questions.cheatsheet
type: qa
step: 8
---
## Q
一句话背诵：`unique_ptr`、`shared_ptr`、`weak_ptr` 的大小、线程安全和 `make_shared` 的分配次数。

## A
- `unique_ptr`：**8 字节**，只能移动，默认选它。
- `shared_ptr`：**16 字节**，原子引用计数（控制块线程安全，被指对象不是）。
- `make_shared` **1 次**分配；`shared_ptr(new T)` 是 **2 次**。
- `weak_ptr` 打破循环引用，否则析构不运行。
