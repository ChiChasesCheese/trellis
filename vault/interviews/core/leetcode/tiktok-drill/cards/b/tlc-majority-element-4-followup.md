---
id: tlc-majority-element-4-followup
node: b.majority-element
type: qa
step: 4
---
## Q
**LC 169 多数元素**｜追问

面试官接着问：（1）不保证多数元素存在时怎么改？（2）找出现次数超过 `⌊n/3⌋` 的所有元素（LC 229）？（3）还有哪些不同思路，各自的代价？

## A
1. **加验证**：投票之后再扫一遍计数，只有候选人真的超过一半才返回，否则返回 `-1`（或抛出错误）。多一遍 `O(n)`，空间仍是 `O(1)`。
2. **超过 `n/3`**：这样的元素最多两个，所以维护两个候选人和两个计数：遇到等于任一候选人的加一；有空位（计数为零）就占位；否则两个计数同时减一。结束后必须再验证两个候选人的真实次数。推广到「超过 `n/k`」，用 `k - 1` 个候选人。

```python
def majority_third(nums: list[int]) -> list[int]:
    a = b = None
    ca = cb = 0
    for x in nums:
        if x == a:
            ca += 1
        elif x == b:
            cb += 1
        elif ca == 0:
            a, ca = x, 1
        elif cb == 0:
            b, cb = x, 1
        else:
            ca -= 1
            cb -= 1
    return [v for v in (a, b) if v is not None and nums.count(v) > len(nums) // 3]
```

`[3,2,3]` → `[3]`，`[1,2]` → `[1, 2]`，`[1,1,1,3,3,2,2,2]` → `[1, 2]`。
3. **其他做法**：哈希计数 `O(n)` 时间 / `O(n)` 空间；排序后取中位数 `sorted(nums)[n // 2]`，`O(n log n)`；随机抽一个元素验证，成功概率 `> 1/2`，期望两次；按二进制位统计，每一位上 `1` 的个数是否过半，`O(32 n)`、`O(1)` 空间；分治：左右两半各求多数元素，冲突时数一遍决胜负。

**Python 提醒**：`max(set(nums), key=nums.count)` 看起来简洁，但 `nums.count` 每次 `O(n)`，整体是 `O(n^2)`，`n = 5 * 10^4` 时已经很慢；要计数就用 `collections.Counter`。
