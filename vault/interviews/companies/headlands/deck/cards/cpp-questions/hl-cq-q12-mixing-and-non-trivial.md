---
id: hl-cq-q12-mixing-and-non-trivial
node: cpp-questions.c-memory-ownership
type: qa
step: 9
---
## Q
对有构造函数的类型（比如带 `std::string` 成员的类）用 `malloc` 分配会怎样？`new[]` 配 `delete`、`malloc` 配 `delete` 呢？现代 C++ 里怎么写？

## A
- 用 `malloc` 给有构造函数的类型分配，得到的是“**不是对象的字节**”，使用是**未定义行为**；只有 trivially copyable 的类型在原始内存上用 `malloc` 才没问题。
- `new[]` 配 `delete`、`malloc` 配 `delete` 都是未定义行为（AddressSanitizer 报 `alloc-dealloc-mismatch`）。
- 现代 C++ **几乎不直接写 `new` / `delete`**：用 `std::make_unique` 和容器。
- 大分配的失败差异：`malloc` 给巨大尺寸返回 `NULL`，`operator new` 则抛 `std::bad_alloc`。
