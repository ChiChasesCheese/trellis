---
id: leetcode-c-endlesscheng-txls3i-kadane-maximum-subarray-template
node: arrays-hash-prefix.kadane-maximum-subarray
type: cloze
anki: 1787272412406
tags: [concept-cloze, leetcode, recall, template]
---
Kadane 转移是 end = {{c1::max(x, end + x)}}。

```
def solve(nums):
    end = nums[0]
    ans = nums[0]
    for x in nums[1:]:
        end = max(x, end + x)
        ans = max(ans, end)
    return ans
```

**Evidence**

§1.3 最大子数组和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.03%20-%20Kadane%20%E6%9C%80%E5%A4%A7%E5%AD%90%E6%95%B0%E7%BB%84%E5%92%8C)
