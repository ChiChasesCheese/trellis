---
id: hl-cq-q44-pitfalls
node: cpp-questions.k-experience
type: qa
step: 9
---
## Q
`for (size_t i = v.size()-1; i >= 0; --i)` 对空 `vector` 为什么出问题？怎么安全反向遍历？`int` 求和和求中点分别要注意什么？价格该用什么类型存？

## A
- 空 `vector`：`v.size() - 1 = 18446744073709551615`（无符号回绕），循环 `i >= 0` 永远为真，**永不结束**。
- 安全反向循环：`for (std::size_t i = v.size(); i-- > 0;)`。
- 求和溢出：先转成更宽的类型再加（`int + int` 会溢出，转 `long long` 后得 4000000000）。
- 中点：`lo + (hi - lo) / 2`，不要写 `(lo + hi) / 2`（会溢出）。
- 价格用**整数（定点）**存，不用浮点。
