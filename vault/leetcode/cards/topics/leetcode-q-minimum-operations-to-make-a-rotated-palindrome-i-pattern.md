---
id: leetcode-q-minimum-operations-to-make-a-rotated-palindrome-i-pattern
node: topics.uncategorised
type: qa
anki: 1787102262832
tags: [lc::4021, leetcode, pattern, recall]
---
## Q
如何求：通过循环左移 + 字符递增(mod 26)两种操作，将字符串变成回文串的最小操作数？

## A
枚举旋转起点 r（0..n-1），把字符串倍长 arr=s+s 避免真的旋转；对每个 r，只需检查前半部分 i=0..n/2-1，计算对称位置 arr[r+i] 与 arr[r+n-1-i] 的字母环上最短递增距离 min(d, 26-d)（d=(x-y)%26），累加即为该旋转下变成回文的代价；对所有 r 取最小值。用 cur>=res 提前剪枝跳出内层/外层循环加速。

**Evidence**

arr = arr + arr ... for r in range(n): ... d = (arr[r + n - 1 - i] - arr[r + i]) % 26; cur += d if d <= 13 else 26 - d ... res = min(res, cur)

[原文 ↗](obsidian://open?vault=lc&file=questions%2F4021%20-%20Minimum%20Operations%20to%20Make%20a%20Rotated%20Palindrome%20I)
