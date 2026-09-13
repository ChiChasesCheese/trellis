---
id: leetcode-q-distribute-elements-into-two-arrays-i-pattern
node: design-simulation.simulation
type: qa
anki: 1787268625262
tags: [lc::3069, leetcode, pattern, recall]
---
## Q
两个数组根据末尾元素大小交替追加时，如何用一行代码代替 if/else 分支？

## A
用条件表达式的布尔值作为下标，从元组 (arr1, arr2) 中选出目标列表再 append：`(arr1, arr2)[arr1[-1] <= arr2[-1]].append(num)`。True==1 选 arr2，False==0 选 arr1，天然对应「谁大就往谁后面加」的规则，省去显式 if/else。

**Evidence**

```
def resultArray(self, nums: List[int]) -> List[int]:
    arr1, arr2 = [nums[0]], [nums[1]]
    for num in nums[2:]:
        (arr1, arr2)[arr1[-1] <= arr2[-1]].append(num)
    return arr1 + arr2
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3069%20-%20Distribute%20Elements%20Into%20Two%20Arrays%20I)
