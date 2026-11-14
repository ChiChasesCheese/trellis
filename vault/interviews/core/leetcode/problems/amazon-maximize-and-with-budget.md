---
slug: amazon-maximize-and-with-budget
---
## Q
**预算内加值使 K 个数按位与最大**｜Hard

非负整数数组 `nums`，每次可给任一元素加 1、花 1 点，总预算 `budget`。选 `k` 个数，使它们加完后的按位与最大，返回这个值。

## A
**一句话。** 试填法：从高位到低位试着把该位并进答案 `ans`，每个数加到「包含 `ans` 全部位的最小不小于它的数」要花的代价，取最小的 `k` 个，总和不超预算就保留这一位。

```python
def max_and(nums, k, budget):
    def cost(x, mask):        # x 至少加多少才包含 mask
        if x & mask == mask:
            return 0
        for p in range(max(x, mask).bit_length() + 1):
            if x >> p & 1:
                continue
            # 高于 p 照抄 x，第 p 位置 1，低位只留 mask
            y = ((x >> p + 1 << p + 1) | 1 << p
                 | (mask & ((1 << p) - 1)))
            if y & mask == mask:
                return y - x  # p 越低 y 越小，首个即最小

    ans, top = 0, (max(nums) + budget).bit_length()
    for b in range(top, -1, -1):
        cand = ans | 1 << b
        cs = sorted(cost(x, cand) for x in nums)
        if sum(cs[:k]) <= budget:
            ans = cand
    return ans
```

**复杂度。** 时间 `O(B·n(B + log n))`，`B` 为位数；空间 `O(n)`。

**易错点。**
- 代价按缺的位权相加：`x = 3`、`mask = 4` 只要加 1，不是 4；进位会清掉低位。
- 每位单独试 `1 << b`：要试 `ans | 1 << b`，高位已经定下的 1 必须一起满足。

**追问。**
- 为什么贪心对？：高位的 1 比低位全部加起来还大；`mask` 的位越少代价越小，所以先定高位不会让低位的判断出错。
- `n` 很大？：每位不必排序，`heapq.nsmallest(k, ...)` 或快速选择取最小 `k` 个代价。

**同模式。** LC 421 数组中两个数的最大异或值、LC 3022 给定操作次数内使剩余元素的或值最小、LC 2935 找出强数对的最大异或值 II
