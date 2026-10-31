---
id: tlc-rotate-array-2-code
node: p2.rotate-array
type: qa
step: 2
---
## Q
**LC 189 轮转数组**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `10^5`，元素在 32 位整数范围内），把元素向右轮转 `k` 个位置（`0 <= k <= 10^5`），原地修改、不返回，额外空间 `O(1)`。

## A
**思路。** 先 `k %= n`。整体翻转让后 `k` 个元素排到最前（但顺序倒了），再分别翻转前 `k` 个和其余部分，恢复各自的顺序。

```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n                                    # k 可能大于 n
    def reverse(i: int, j: int) -> None:
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    reverse(0, n - 1)                         # 整体翻转：后 k 个跑到最前（但是倒序）
    reverse(0, k - 1)                         # 前 k 个翻回正序
    reverse(k, n - 1)                         # 其余翻回正序
```

运行：`([1,2,3,4,5,6,7], 3)` → `[5, 6, 7, 1, 2, 3, 4]`，`([-1,-100,3,99], 2)` → `[3, 99, -1, -100]`，`([1], 5)` → `[1]`，`([1,2], 3)` → `[2, 1]`，`([1,2,3], 0)` → `[1, 2, 3]`。

**复杂度。** 时间 `O(n)`：三次翻转共交换约 `n` 次；空间 `O(1)`：只有几个下标变量。

**写法要点。** `nums[i], nums[j] = nums[j], nums[i]` 是 Python 的元组交换，不需要临时变量；`k %= n` 一行同时处理 `k > n` 和 `k == n`；`reverse` 定义成闭包，直接修改外层的 `nums`，三次调用只传下标。内存不是问题时，`nums[:] = nums[-k:] + nums[:-k]` 更短，但 `k > n` 时仍要先取模，且会分配新列表。
