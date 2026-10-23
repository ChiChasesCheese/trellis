---
id: hl-javaq-d-q14-say60
node: java-questions.d-memory
type: qa
step: 31
---
## Q
用英文 60 秒回答：What's the cost of autoboxing? Explain `Integer` caching and why `==` on two `Integer`s can give different answers.

## A
结构：装箱调用 valueOf → -128 到 127 缓存所以 `==` 碰巧成立 → 总用 equals → 成本（分配、间接、拆箱 NPE）→ 实测 240 MB → 热路径替代品。

> "Autoboxing calls `Integer.valueOf`, which returns a cached instance for values between -128 and 127 and allocates a new object otherwise - so `==` on boxed values compares references and works by accident for small numbers and fails for 128. Always use `equals`. The cost is an allocation, an extra pointer hop, and a potential NPE on unboxing null. In a quick test a boxed `Long` accumulator over 20 million iterations allocated around 240 MB while the primitive loop allocated nothing. In latency-sensitive code I use primitive arrays, `LongAdder`, or primitive-specialised maps."
