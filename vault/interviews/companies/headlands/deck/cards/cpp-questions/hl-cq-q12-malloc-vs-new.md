---
id: hl-cq-q12-malloc-vs-new
node: cpp-questions.c-memory-ownership
type: qa
step: 7
---
## Q
面试题：`malloc` 和 `new` 有什么区别？
What's the difference between `malloc` and `new`?

## A
| | `malloc` | `new` |
|---|---|---|
| 是什么 | C 函数 | C++ 运算符 |
| 做什么 | 分配**未初始化的原始字节**，返回 `void*` | `operator new`（分配）+ **调用构造函数**，返回有类型的指针 |
| 失败 | 返回 `NULL` | 抛 `std::bad_alloc` |
| 释放 | `free` | `delete`（先析构再释放）；`new[]` 配 `delete[]` |

两套不能混用。`new` 可以重载；**placement new** 在已有内存上构造对象。
