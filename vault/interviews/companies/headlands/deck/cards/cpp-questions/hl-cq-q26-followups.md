---
id: hl-cq-q26-followups
node: cpp-questions.f-ub-debug
type: qa
step: 21
---
## Q
三个追问：不用临时变量交换两个 `int` 怎么写，有什么限制？怎么给 N 位字段做符号扩展？不用 `popcount` 怎么数 1 的个数？

## A
- **异或交换**：`a ^= b; b ^= a; a ^= b;`。对两个不同对象有效；如果两个是同一个变量就会清零；相比 `std::swap` 没有实际优势。
- **符号扩展**：先左移把字段最高位放到符号位，再算术右移：`(int32_t)(x << (32-N)) >> (32-N)`。
- **数位**：Kernighan 循环是 O(1 的个数)；查表或 SWAR 技巧是常数时间。
