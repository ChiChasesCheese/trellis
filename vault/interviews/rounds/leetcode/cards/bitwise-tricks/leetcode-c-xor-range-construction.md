---
id: leetcode-c-xor-range-construction
node: bitwise-tricks.xor-range-construction
type: cloze
anki: 1787102263459
tags: [concept-cloze, leetcode, recall]
---
在 XOR 值域构造问题中，若 n >= 3，可能的 XOR 结果集合恰好覆盖 {{c1::严格大于 n 的最小 2 的幂}} 减一为止的完整区间；这是因为所有操作数都小于 2m（m 为不超过 n 的最大 2 的幂），XOR 无法产生更高位，同时该区间内每个值都能被显式构造出来。

对 LC 3513，令 m = 2^k 且 m <= n < 2m，答案 = 1 << n.bit_length()（即严格大于 n 的最小 2 的幂）。仅证明上界不够，必须同时证明下界内每个值都可构造，两者合起来才能断言结果集合是一个完整区间。

**Evidence**

所有操作数都小于 `2m = 2^(k+1)`，所以它们的第 `k+1` 位以及更高位全部为 `0`。三个数 XOR 后也不可能凭空产生更高位，因此所有结果一定落在 `[0, 2m - 1]`... 因此答案就是严格大于 `n` 的最小 2 的幂。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2FXOR%20%E5%80%BC%E5%9F%9F%E6%9E%84%E9%80%A0)
