---
id: hl-cq-q02-why-not-c
node: cpp-questions.a-why-fast
type: qa
step: 9
---
## Q
追问：既然要快，为什么不直接写 C？
Why not just write C?

## A
- **模板和内联**：`std::sort` 比 `qsort` 快约 4 倍（比较函数被内联进排序循环）。
- **RAII** 消除整类资源泄漏：文件、锁、内存离开作用域自动释放。
