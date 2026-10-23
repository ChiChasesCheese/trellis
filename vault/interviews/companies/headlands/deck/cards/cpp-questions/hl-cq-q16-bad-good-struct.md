---
id: hl-cq-q16-bad-good-struct
node: cpp-questions.c-memory-ownership
type: qa
step: 31
---
## Q
结构体 `Bad { char a; double b; char c; int d; }` 和把成员重排成 `Good { double b; int d; char a; char c; }` 各占多少字节？逐个成员算填充。`alignas(64)` 的 `Line { int64_t v; }` 呢？

## A
```cpp
struct Bad  { char a; double b; char c; int d; };  // a(1)+7填充 b(8) c(1)+3填充 d(4) -> 24
struct Good { double b; int d; char a; char c; };  // b(8) d(4) a(1) c(1) +2填充 -> 16
struct alignas(64) Line { std::int64_t v; };       // 大小被补到 64
```
- 同样四个字段，从 **24 字节**降到 **16 字节**，规则是“大的在前”。
- 为什么 `Line` 是 64：`alignas(64)` 让它独占一条缓存行，大小被补到 64。
