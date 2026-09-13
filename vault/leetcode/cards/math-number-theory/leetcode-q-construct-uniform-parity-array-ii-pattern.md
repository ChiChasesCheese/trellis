---
id: leetcode-q-construct-uniform-parity-array-ii-pattern
node: math-number-theory.math
type: qa
anki: 1788477632426
tags: [lc::3876, leetcode, pattern, recall]
---
## Q
如何判断数组能否通过合法操作变为全奇或全偶（uniform parity）？

## A
关键看最小值和数组中是否存在奇数：若数组最小值本身是奇数，一定可以构造成功；否则只有当数组中原本就不存在奇数（即已经全偶）时才成立。核心判断：`min(nums) % 2 == 1` 或者 `not any(奇数)`。

**Evidence**

```
def uniformArray(self, nums):
    hasOdd = any(num % 2 for num in nums)
    min_val = min(nums)
    if min_val % 2:
        return True
    return not hasOdd
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3876%20-%20Construct%20Uniform%20Parity%20Array%20II)
