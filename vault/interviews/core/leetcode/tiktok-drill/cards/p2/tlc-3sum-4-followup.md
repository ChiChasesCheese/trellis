---
id: tlc-3sum-4-followup
node: p2.3sum
type: qa
step: 4
---
## Q
**LC 15 三数之和**｜追问

面试官接着问：（1）和最接近目标值的三个数（LC 16）？（2）推广到 k 数之和 / 四数之和（LC 18）？（3）不排序，用哈希表能做吗？

## A
1. **最接近的三数之和**：同样排序加双指针，但不再找精确等于，而是每一步都用 `abs(和 - target)` 更新最优；和恰好等于目标时可以立即返回。

```python
def three_sum_closest(nums: list[int], target: int) -> int:
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                return s
    return best
```

`three_sum_closest([-1,2,1,-4], 1)` → `2`。
2. **k 数之和**：递归，`k > 2` 时枚举当前数并跳过重复，递归求 `k - 1` 个数；`k == 2` 时用双指针。四数之和是 `O(n^3)`。

```python
def k_sum(nums: list[int], target: int, k: int) -> list[list[int]]:
    nums = sorted(nums)

    def go(lo: int, k: int, target: int) -> list[list[int]]:
        out: list[list[int]] = []
        if k == 2:
            l, r = lo, len(nums) - 1
            while l < r:
                s = nums[l] + nums[r]
                if s < target:
                    l += 1
                elif s > target:
                    r -= 1
                else:
                    out.append([nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
            return out
        for i in range(lo, len(nums) - k + 1):
            if i > lo and nums[i] == nums[i - 1]:
                continue
            out.extend([nums[i], *rest] for rest in go(i + 1, k - 1, target - nums[i]))
        return out

    return go(0, k, target)
```

`k_sum([1,0,-1,0,-2,2], 0, 4)` → `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]`。
3. **哈希表**：固定第一个数后用集合查第三个数，同样 `O(n^2)`；但去重要靠对三元组排序后放进集合或额外的计数处理，不如排序双指针简洁，空间也是 `O(n)`。

**Python 提醒**：`[nums[i], *rest]` 用解包把新数放在已有列表前面，比 `[nums[i]] + rest` 少一次中间列表；`sorted()` 和 `list.sort()` 的区别是前者返回新列表，递归里统一在入口排序一次，不要在递归里反复排序。
