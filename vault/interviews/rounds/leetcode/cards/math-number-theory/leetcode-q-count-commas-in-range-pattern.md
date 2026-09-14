---
id: leetcode-q-count-commas-in-range-pattern
node: math-number-theory.math
type: qa
anki: 1789002116996
tags: [lc::3870, leetcode, pattern, recall]
---
## Q
LeetCode 3870 Count Commas in Range：如何快速计算 1~n 中所有数字标准格式化后逗号总数？

## A
只有 >=1000 的数才会带逗号（4位数及以上，每3位一个逗号，本题n<=10^5，最多5位数，只会出现1个逗号）。因此逗号总数 = 满足条件的数字个数 = n - 1000 + 1（当 n>=1000），否则为0。核心洞察：不用逐个数字格式化统计逗号，而是利用「每个>=1000的数恰好贡献1个逗号」这一数量关系直接计数。

**Evidence**

```
class Solution:
    def countCommas(self, n: int) -> int:
        if n < 1000:
            return 0
        return n - 1000 + 1
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3870%20-%20Count%20Commas%20in%20Range)
