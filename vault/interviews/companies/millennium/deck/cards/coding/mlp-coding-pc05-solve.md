---
id: mlp-coding-pc05-solve
node: coding.pc05
step: 1
type: qa
---
## Q
**子数组和能被 K 整除：题与解**｜编程轮

整数数组 `nums`（可以有负数）和正整数 `k`，数一数有多少个非空连续子数组的和能被 `k` 整除。例：`[4,5,0,-2,-3,1]`，`k=5`，答案是 7。

## A
**一句话思路。** 前缀和（prefix sum，前 i 个元素的和）把"子数组和"变成两个前缀和之差：子数组 `(l, r]` 的和能被 k 整除，当且仅当两个前缀和对 k 的余数相同。所以边扫边统计每个余数出现过几次，每遇到一个余数，就加上它之前出现的次数。

```python
def count_div_k(nums, k):
    if k < 1:
        raise ValueError("k must be positive")
    seen = {0: 1}        # 余数 -> 出现次数；空前缀的和是 0，余数 0 先算一次
    prefix = 0
    count = 0
    for x in nums:
        prefix = (prefix + x) % k           # Python 的 % 对正 k 总落在 [0, k)，负数不用特殊处理
        count += seen.get(prefix, 0)        # 和之前每个同余的前缀各配成一个子数组
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

print(count_div_k([4, 5, 0, -2, -3, 1], 5))   # 7
```

**复杂度。** 时间 O(n)，空间 O(min(n, k))，因为余数只有 k 种。暴力枚举所有 (l, r) 是 O(n²)。

**边写边讲。**
- "A subarray sum is the **difference of two prefix sums**, so I only need a hashmap of what I've seen."
- "Two prefixes with the **same remainder mod k** cancel out to a multiple of k."
- "I seed the map with `{0: 1}` so subarrays starting at index 0 are counted."
