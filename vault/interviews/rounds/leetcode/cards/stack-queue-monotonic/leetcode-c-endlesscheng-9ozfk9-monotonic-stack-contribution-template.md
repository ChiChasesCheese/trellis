---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-contribution-template
node: stack-queue-monotonic.monotonic-stack-contribution
type: cloze
anki: 1788743827738
tags: [concept-cloze, leetcode, recall, template]
---
贡献法处理重复值时，左右边界的比较必须 {{c1::一侧严格、另一侧非严格}}。

```
def sum_subarray_mins(nums: list[int]) -> int:
    mod = 1_000_000_007
    values = [0] + nums + [0]
    stack = [0]
    total = 0
    for i in range(1, len(values)):
        while values[stack[-1]] > values[i]:
            mid = stack.pop()
            left = stack[-1]
            total += values[mid] * (mid - left) * (i - mid)
        stack.append(i)
    return total % mod
```

**Evidence**

三、贡献法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.03%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E8%B4%A1%E7%8C%AE%E6%B3%95)
