---
id: hl-cq-q23-signed-overflow-demo
node: cpp-questions.f-ub-debug
type: qa
step: 2
---
## Q
函数 `bool always_bigger(int x) { return x + 1 > x; }` 对 `INT_MAX` 在 `-O0`、`-O2`、`-O2 -fsanitize=undefined` 下分别返回什么？这说明什么？

## A
- `-O0`：返回 **0**（真的溢出了，回绕成负数，比较为假）。
- `-O2`：返回 **1**——有符号溢出是 UB，优化器已把整个函数折叠成 `return true`。
- `-O2 -fsanitize=undefined`：报 `runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'`，返回 0。
- 同一段代码，不同优化级别两个答案——这就是 UB。
- 需要检查溢出用 `__builtin_add_overflow`；**无符号溢出有定义**（模 2^N 回绕）。
