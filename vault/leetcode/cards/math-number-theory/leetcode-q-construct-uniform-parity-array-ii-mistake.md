---
id: leetcode-q-construct-uniform-parity-array-ii-mistake
node: math-number-theory.math
type: qa
anki: 1788477632523
tags: [lc::3876, leetcode, mistake, recall]
---
## Q
写 uniformArray 类问题时，为什么不要用『排序后比较 evens[0]-min_odd』这种边界判断？

## A
这种写法（uniformArray0）把问题复杂化了：先分别统计/排序奇偶子数组，再用 `evens[0] - min_odd >= 1` 做条件判断，但这个条件并不能正确刻画『能否构造成功』的本质，只是凑数值关系。真正决定性的只有『最小值的奇偶性』和『是否存在奇数』这两个全局信息，不需要分别排序两个子数组。

**Evidence**

```
def uniformArray0(self, nums):
    ...
    odds.sort()
    evens.sort()
    min_odd = odds[0]
    if evens[0] - min_odd >= 1:
        return True
    return False
```

（后被更简单且正确的 uniformArray 替代）

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3876%20-%20Construct%20Uniform%20Parity%20Array%20II)
