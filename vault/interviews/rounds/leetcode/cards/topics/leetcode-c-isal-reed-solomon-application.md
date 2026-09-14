---
id: leetcode-c-isal-reed-solomon-application
node: topics.uncategorised
type: qa
anki: 1787361363472
tags: [algorithm::finite-field, algorithm::matrix-inversion, algorithm::reed-solomon, application, case, case::isal-reed-solomon, category::distributed-streaming, chapter::09, chapter::13, leetcode, system::intel-isa-l]
---
## Q
Reed-Solomon 恢复为什么要求在 GF(2^8) 上做矩阵求逆，而不是普通整数矩阵？

## A
shard 编码系数定义在有限域，只有按该域的加法、乘法和逆元运算，编码矩阵的可逆性与恢复公式才成立；其中加法是 XOR，乘法按不可约多项式约简。

**Evidence**

Intel ISA-L 官方 erasure_code 实现定义 GF matrices、encode tables 与 decode/recovery workflow。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FIntel%20ISA-L%20Reed-Solomon%EF%BC%9A%E6%9C%89%E9%99%90%E5%9F%9F%E7%9F%A9%E9%98%B5%E4%B8%8E%E7%BA%A0%E5%88%A0%E7%A0%81)
