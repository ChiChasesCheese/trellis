---
id: leetcode-q-nth-digit-pattern
node: binary-search.binary-search
type: qa
anki: 1787102262732
tags: [lc::400, leetcode, pattern, recall]
---
## Q
LeetCode 400. Nth Digit：如何在 O(log n) 时间内定位无限数字序列 1,2,3,...,10,11,... 的第 n 位数字？

## A
按位数分段计数：1~9 位数为 1 位，共 9 个数字占 9 位；10~99 为 2 位，共 90 个数字占 180 位；以此类推，每段数字个数 = 9*10^(d-1)，占用字符数 = 9*10^(d-1)*d。先用 while 循环减去每个位数段的总字符数，确定 n 落在哪个位数 d 里；再用 (n-1)//d 定位是该段内第几个数字（加上该段起始值 10^(d-1)），用 (n-1)%d 定位是该数字的第几位，最后转字符串取该位字符。

**Evidence**

```
class Solution:
    def findNthDigit(self, n: int) -> int:
        if n <= 9:
            return n
        d = 2
        n -= 9
        while True:
            total = 9 * (10 ** (d - 1)) * d
            if n <= total:
                break
            n -= total
            d += 1
        n -= 1
        start = 10 ** (d - 1)
        num = start + n // d
        pos = n % d
        return int(str(num)[pos])
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F400%20-%20Nth%20Digit)
