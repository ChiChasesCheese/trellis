---
id: cc-performance-budget-from-n
node: performance.budget
type: qa
---
## Q
A statement caps the input at 10^5 event lines and the graded performance test allows 2 seconds of wall time in an interpreted language. Which complexity classes are safe, which is the boundary, and which one must you not ship?

## A
**Budget backwards from roughly 10^7 interpreted operations per second.**

- Safe: O(n) and O(n log n) — 10^5 × 17 ≈ 2·10^6 steps, comfortably inside one second.
- Boundary: O(n√n), or O(n log n) with a heavy per-step constant (a regex, a `Decimal` construction, an object allocation per row). Measure it.
- Out: O(n²) = 10^10 steps — minutes to hours, not seconds.

Do this arithmetic before writing the first line. Choosing the structure that makes the hot operation sub-linear costs 30 seconds up front and 15 minutes if you retrofit it.

## Q zh
题面把输入上限定在 10^5 行事件，评分用的性能测试给 2 秒墙钟时间，语言是解释型的。哪些复杂度类是安全的，哪个在边界上，哪个绝对不能交？

## A zh
**用「每秒约 10^7 次解释器操作」倒推预算。**

- 安全：O(n) 和 O(n log n) —— 10^5 × 17 ≈ 2·10^6 步，一秒内绰绰有余。
- 边界：O(n√n)，或者每步常数很重的 O(n log n)（每行一次正则、一次 `Decimal` 构造、一次对象分配）。要实测。
- 出局：O(n²) = 10^10 步 —— 那是几分钟到几小时，不是几秒。

这个算术要在写第一行代码之前做完。提前选好让热点操作次线性的结构只花 30 秒，事后改造要花 15 分钟。
