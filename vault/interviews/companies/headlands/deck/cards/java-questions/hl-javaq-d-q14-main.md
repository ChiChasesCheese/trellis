---
id: hl-javaq-d-q14-main
node: java-questions.d-memory
type: qa
step: 14
---
## Q
自动装箱（autoboxing）的成本是什么？解释 `Integer` 缓存，以及为什么两个 `Integer` 用 `==` 可能给出不同答案。
What's the cost of autoboxing? Explain `Integer` caching and why `==` on two `Integer`s can give different answers.

## A
一句话：自动装箱 `int → Integer` 调 `Integer.valueOf`：**-128..127 返回缓存对象，其他新分配**；所以 `==`（比引用）对 127 是 `true`、对 128 是 `false`，必须用 `equals`。

- 输出：`127 == 127 (boxed): true`；`128 == 128 (boxed): false`，但 `equals` 为 true。
- 成本：**分配 + 间接访问 + 拆箱时的 NPE 风险**（拆箱 `null` 会抛 NPE）。
- 缓存范围默认 -128..127（`-XX:AutoBoxCacheMax` 可调大 `Integer` 的上界）；`Long`、`Short`、`Byte`、`Character` 也有缓存。
- 缓存存在的原因：小整数使用频繁、省分配；JLS 要求至少覆盖 -128..127。
