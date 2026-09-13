---
id: leetcode-c-endlesscheng-wr1mjp-contribution-counting-template
node: arrays-hash-prefix.contribution-counting
type: cloze
anki: 1787272471280
tags: [concept-cloze, leetcode, recall, template]
---
元素 nums[i] 作为区间最小值的典型贡献是 {{c1::nums[i] * 左侧选择数 * 右侧选择数}}。

```
def sum_subarray_mins(nums):
    mod = 10**9 + 7
    arr = [float("-inf")] + nums + [float("-inf")]
    stack = []
    ans = 0
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] > x:
            mid = stack.pop()
            left = stack[-1]
            ans += arr[mid] * (mid - left) * (i - mid)
        stack.append(i)
    return ans % mod
```

**Evidence**

其他算法套路（每日一题题解精选）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.06%20-%20%E8%B4%A1%E7%8C%AE%E6%B3%95)
