---
id: tlc-4sum-4-followup
node: a.4sum
type: qa
step: 4
---
## Q
**LC 18 四数之和**｜追问

面试官接着问：（1）推广到 k 数之和怎么写？（2）如果只要四元组的个数、不要求去重（四个独立数组）？（3）输入有 `10^9` 级别的数要注意什么？

## A
1. **k 数之和**：递归，每层固定一个数，`k == 2` 时双指针；每层都做「和前一个相同就跳过」，并用 `nums[i] * k > target` 剪枝（后面每个数都不小于 `nums[i]`）。
```python
def k_sum(nums: list[int], target: int, k: int) -> list[list[int]]:
    nums = sorted(nums)

    def search(start: int, k: int, target: int) -> list[list[int]]:
        out: list[list[int]] = []
        if k == 2:
            lo, hi = start, len(nums) - 1
            while lo < hi:
                total = nums[lo] + nums[hi]
                if total < target:
                    lo += 1
                elif total > target:
                    hi -= 1
                else:
                    out.append([nums[lo], nums[hi]])
                    lo, hi = lo + 1, hi - 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
            return out
        for i in range(start, len(nums) - k + 1):
            if i > start and nums[i] == nums[i - 1]:
                continue
            if nums[i] * k > target:
                break
            out += ([nums[i], *rest] for rest in search(i + 1, k - 1, target - nums[i]))
        return out

    return search(0, k, target)
```
2. **只数个数**（LC 454）：两两分组，`Counter` 存前两组的和，查后两组和的相反数，`O(n^2)`。
3. **大数**：Python 整数不溢出；Java/C++ 的 `int` 累加会溢出，要用 `long`。

**Python 提醒**：`out += 生成器` 会逐个追加元素；列表不可哈希，要用 `set` 去重必须先转 `tuple`。
