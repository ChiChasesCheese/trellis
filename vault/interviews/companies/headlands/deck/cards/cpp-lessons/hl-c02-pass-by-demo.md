---
id: hl-c02-pass-by-demo
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 4
---
## Q
```cpp
struct Big { std::vector<int> data = std::vector<int>(1000, 1); };
void by_value(Big b)  { b.data[0] = 42; }
void by_ref(Big& b)   { b.data[0] = 42; }
void by_ptr(Big* b)   { if (b) b->data[0] = 43; }
```
对同一个 `Big x`（`data[0]` 初值 1）依次调用三个函数后，`x.data[0]` 各是多少？`by_value` 的代价是什么？

## A
- `by_value(x)` 后仍是 **1**：函数改的是副本，调用者不受影响；代价是复制整个 vector 数据（1000 个 `int`，4000+ 字节），而 `sizeof(Big)` 只有 24（vector 的三个指针）。
- `by_ref(x)` 后是 **42**：引用是调用者对象的别名，函数可以修改它。
- `by_ptr(&x)` 后是 **43**：指针可为空（所以要先判空），可重绑，访问要用 `->`。
- 只读时用 `const Big&`：不复制、不可改。
