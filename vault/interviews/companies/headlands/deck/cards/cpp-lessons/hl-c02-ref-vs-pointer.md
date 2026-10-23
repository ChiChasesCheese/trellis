---
id: hl-c02-ref-vs-pointer
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 2
---
## Q
面试问：C++ 引用（`T&`）和指针（`T*`）有什么区别？什么时候用哪个？
Interview question: What is the difference between a reference and a pointer in C++?

## A
| | 引用 `T&` | 指针 `T*` |
|---|---|---|
| 能否为空 | 否，必须初始化 | 可以（`nullptr`） |
| 能否重新绑定 | **不能**：`r = b` 是赋值，不是换绑 | 能 |
| 语法 | `r.x`，像值 | `p->x`、`*p` |
| 谁负责释放 | 不拥有 | 裸指针**不应**表示所有权 |

- 引用通常由编译器用指针实现，但语言不保证 `sizeof` 和存储；指针在 64 位下 8 字节，可做算术。
- 选择：引用表达"一定有"；指针表达"可能没有"、需要重绑或算术、或与 C API 交互。
