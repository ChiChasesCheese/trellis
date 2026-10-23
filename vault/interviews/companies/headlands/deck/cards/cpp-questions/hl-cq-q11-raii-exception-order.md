---
id: hl-cq-q11-raii-exception-order
node: cpp-questions.c-memory-ownership
type: qa
step: 2
---
## Q
一个函数依次创建对象 `a`、`lock_guard`、对象 `b`、文件句柄 `FileHandle`，然后抛出异常。析构按什么顺序发生？文件和锁会怎样？

## A
- 栈展开时按**构造的逆序**销毁：先关文件（`close`），再 `dtor b`，再 `dtor a`；`lock_guard` 也随之解锁。
- 实测：异常路径上依次输出 `close`、`dtor b`、`dtor a`，捕获 `boom` 后互斥量已经空闲（`mutex is free again: yes`）。
- 正常路径是 `normal return` 之后同样按 `close`、`dtor b`、`dtor a` 的逆序。
- 结论：异常展开时文件仍被关闭，这就是 RAII 取代 `finally` 的证据。
