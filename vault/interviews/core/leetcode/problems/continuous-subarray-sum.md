---
slug: continuous-subarray-sum
---
## Q
**LC 523 连续的子数组和**｜Medium

判断是否存在长度至少为 `2`、和为 `k` 的倍数的连续子数组。

## A
**一句话。** 前缀和对 `k` 取余，同余数的两个前缀之间就是 `k` 的倍数，字典只记余数第一次出现的下标。

```python
def check_subarray_sum(nums, k):
    first = {0: -1}     # 余数 -> 最早下标；空前缀余数 0
    prefix = 0
    for i, x in enumerate(nums):
        prefix = (prefix + x) % k
        j = first.setdefault(prefix, i)
        if i - j >= 2:  # 子数组长度 i - j
            return True
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(min(n, k))`。

**易错点。**
- 漏掉 `{0: -1}`：`[2,4]`、`k=6` 得 `false`，应为 `true`。
- 忘了长度至少 `2`：`[6,1]`、`k=6` 下标差为 `1` 就返回会得 `true`，应为 `false`。
- 每次都覆盖下标：丢了最早位置，`[5,0,0]`、`k=7` 得 `false`，应为 `true`。

**追问。**
- `k` 可以为 `0` 吗？：倍数只有 `0`，改成前缀和相等，取余那行写成 `prefix + x`。
- 统计个数（LC 974）？：字典换成计数，`ans += cnt[prefix]`，没有长度限制。

**同模式。** LC 560 和为 K 的子数组、LC 974 和可被 K 整除的子数组、LC 525 连续数组、LC 437 路径总和 III
