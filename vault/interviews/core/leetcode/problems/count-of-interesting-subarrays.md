---
slug: count-of-interesting-subarrays
---
## Q
**LC 2845 统计趣味子数组的数目**｜Medium

子数组中满足 `nums[i] % modulo == k` 的元素个数记为 `cnt`，若 `cnt % modulo == k` 则它是趣味子数组。统计趣味子数组的数目。

## A
**一句话。** 把满足条件的元素记为 `1` 求前缀和（对 `modulo` 取模），用哈希表数满足 `pre[l] ≡ pre[r] - k` 的左端点。

```python
def count_interesting_subarrays(nums, modulo, k):
    seen = Counter({0: 1})       # 空前缀
    pre = ans = 0
    for x in nums:
        pre = (pre + (x % modulo == k)) % modulo
        ans += seen[(pre - k) % modulo]
        seen[pre] += 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(min(n, modulo))`。

**易错点。**
- 条件当成 `cnt == k`（没取模）：`([1,1,1], 2, 1)` 得 `3`，应为 `4`，长度 `3` 的子数组 `cnt=3`，`3 % 2 == 1` 也满足。
- `(pre - k)` 不取模：可能为负，找不到对应余数。
- 漏掉空前缀 `{0: 1}`：以第一个元素开头的子数组全漏，`([3,2,4], 2, 1)` 得 `0`，应为 `3`。

**追问。**
- 条件改成元素和同余（LC 974、LC 523）？：把 `0/1` 换成元素本身，其余同构。
- `modulo` 很小怎么优化？：哈希表换成长度为 `modulo` 的数组。

**同模式。** LC 560 和为 K 的子数组、LC 974 和可被 K 整除的子数组、LC 523 连续的子数组和、LC 1248 统计「优美子数组」
