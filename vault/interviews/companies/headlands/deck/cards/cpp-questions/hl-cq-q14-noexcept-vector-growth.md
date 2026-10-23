---
id: hl-cq-q14-noexcept-vector-growth
node: cpp-questions.c-memory-ownership
type: qa
step: 21
---
## Q
`vector` 扩容时，元素的移动构造函数没有标 `noexcept` 会怎样？为什么？实测数字是多少？

## A
- `vector` 扩容要把旧元素搬到新内存。为了保持**强异常保证**（中途失败时原数据不能被破坏），只有移动构造是 `noexcept` 时才用移动，否则退回**拷贝**。
- 实测（8 个元素，扩容搬 7 个）：
  - 移动是 `noexcept`：`copies=0 moves=7`
  - 移动不是 `noexcept`：`copies=7 moves=0`
- 所以自己写的移动操作要标 `noexcept`。
