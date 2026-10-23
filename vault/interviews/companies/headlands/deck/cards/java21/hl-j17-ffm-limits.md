---
id: hl-j17-ffm-limits
node: java21.j17-ffm-api
type: qa
step: 20
---
## Q
FFM 不能保证什么？什么时候不该用堆外内存？

## A
- **不能让「错误的 C 签名」变安全**：`FunctionDescriptor` 写错（如把 `int` 写成 `long`），JVM 无从得知，轻则乱码，重则崩进程，这就是 `downcallHandle` 是受限方法的原因。
- 热循环里每次访问仍有边界检查，JIT 通常能优化，不保证。
- **何时不该用**：数据量不大、没有 GC 压力证据时，`long[]` / 对象数组更简单更安全，JIT 对它们优化得最好。**先用 JFR 确认 GC 是瓶颈，再考虑堆外。**
