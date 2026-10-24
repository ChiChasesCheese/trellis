---
id: tlc-count-number-of-nice-subarrays-2-code
node: a.count-number-of-nice-subarrays
type: qa
step: 2
---
## Q
**LC 1248 统计「优美子数组」**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `50000`，元素 `1` 到 `10^5`）和整数 `k`（`1 <= k <= nums.length`）。返回恰好包含 `k` 个奇数的连续子数组的个数。要求 `O(n)`。

## A
**思路。** 边扫描边维护「前缀里的奇数个数」`odd`。一个子数组恰好有 `k` 个奇数，当且仅当它左边的前缀奇数个数是 `odd - k`。定长数组 `seen` 记录每个奇数个数出现过的前缀数量，初始放入空前缀。

```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    seen = [0] * (len(nums) + 1)            # seen[j]：前缀里“恰好有 j 个奇数”的位置有多少个
    seen[0] = 1                             # 空前缀
    odd = ans = 0
    for x in nums:
        odd += x & 1                        # 前缀里奇数个数
        if odd >= k:
            ans += seen[odd - k]            # 左边前缀的奇数个数为 odd - k，中间恰好 k 个奇数
        seen[odd] += 1
    return ans
```

运行：`([1,1,2,1,1], 3)` → `2`，`([2,4,6], 1)` → `0`，`([2,2,2,1,2,2,1,2,2,2], 2)` → `16`，`([1], 1)` → `1`。

**复杂度。** 时间 `O(n)`：一趟扫描，每步常数；空间 `O(n)`：`seen` 数组，长度 `n + 1`。

**写法要点。**
- `x & 1` 取最低位，奇数为 `1`、偶数为 `0`，比 `x % 2` 更直接，`odd += x & 1` 不需要分支。
- 用定长列表而不是 `dict` / `Counter`：下标就是前缀奇数个数，范围 `0..n` 已知，访问更快；`if odd >= k` 防止 `odd - k` 为负数时读到列表尾部（Python 的负下标不会报错，会悄悄读到末尾元素）。
- 先 `ans += seen[odd - k]` 再 `seen[odd] += 1`，顺序不能反，否则当 `k == 0` 时会数到自己；这里 `k >= 1` 所以不出问题，但习惯要对。
- 滑动窗口替代：`at_most(k) - at_most(k - 1)`，`at_most(m)` 数奇数个数 `<= m` 的子数组，每个右端加 `right - left + 1`，空间 `O(1)`。
