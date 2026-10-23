---
id: hl-javaq-c-q09-say60
node: java-questions.c-languages
type: qa
step: 18
---
## Q
用英文 60 秒回答：What does Java guarantee that C++ does not (and vice versa)? Think undefined behaviour, integer semantics, memory safety.

## A
结构：Java 每个行为都有定义 → C++ 的 UB 换来优化但 bug 沉默 → Java 自己的陷阱（回绕、移位、取模）→ 金额用 addExact 或 long。

> "Java defines every behaviour: signed overflow wraps by two's complement, out-of-range array access throws, null dereference throws, and even a data race has a restricted meaning - you may see stale values, but never out-of-thin-air ones. C++ leaves overflow, out-of-bounds access and data races undefined, which lets the optimizer assume they never happen - faster, but the bugs are silent. In Java the traps are different: ints wrap silently, so for money or sizes I use `Math.addExact` or `long`, and I know that shifts are masked and `%` keeps the sign of the dividend."
