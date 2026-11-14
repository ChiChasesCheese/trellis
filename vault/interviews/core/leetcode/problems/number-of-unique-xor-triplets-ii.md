---
slug: number-of-unique-xor-triplets-ii
---
## Q
**LC 3514 不同 XOR 三元组的数目 II**｜Medium

求 `nums[i] ^ nums[j] ^ nums[k]`（`i ≤ j ≤ k`）能取到的不同值个数。`n ≤ 1500`，值 `≤ 1500`。

## A
**一句话。** 下标可重复，等价于从出现过的值里可重复地选三个；先求两两异或的集合，再和每个值异或一次，值域只有 `2^11`。

```python
def unique_xor_triplets(nums):
    vals = set(nums)
    two = {a ^ b for a in vals for b in vals}   # 至多 2048 个
    return len({t ^ c for t in two for c in vals})
```

**复杂度。** 时间 `O(u^2 + u·2^11)`，空间 `O(2^11)`，`u` 为不同值个数。

**易错点。**
- 三重循环枚举下标：`1500^3` 超时。
- 以为下标要互不相同：`i ≤ j ≤ k` 允许同一个元素用多次。

**追问。**
- 为什么能分两步？：异或可结合，三元组的值 = 两元组的值 ^ 第三个数，中间结果的个数被值域卡住。
- `nums` 是 `1..n` 的排列（LC 3513）？：`n ≥ 3` 时答案是 `2^(bit_length(n))`，`n ≤ 2` 时等于 `n`。

**同模式。** LC 136 只出现一次的数字、LC 3513 不同 XOR 三元组的数目 I、LC 1442 形成两个异或相等数组的三元组数目
