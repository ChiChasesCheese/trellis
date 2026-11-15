---
slug: construct-the-minimum-bitwise-array-i
---
## Q
**LC 3314 构造最小位运算数组 I**｜Easy

质数数组 `nums`。对每个 `nums[i]`，求最小的非负整数 `ans[i]`，使 `ans[i] OR (ans[i] + 1) == nums[i]`；不存在则为 `-1`。

## A
**一句话。** `x OR (x+1)` 会把 `x` 末尾连续的 `1` 的最高那位之后的 `0` 变成 `1`，相当于把 `x` 的最低的 `0` 位置 `1`。所以 `nums[i]` 去掉"末尾连续 `1` 的最高位"就是答案；`nums[i] = 2` 时无解。

```python
def min_bitwise_array(nums):
    ans = []
    for p in nums:
        if p == 2:                         # 偶数的 OR 结果必为奇数
            ans.append(-1)
        else:
            low = (p + 1) & -(p + 1)       # 末尾连续 1 的下一位
            ans.append(p - low // 2)       # 去掉其中最高的那个 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 对 `2` 也套公式：`x | (x + 1)` 总是奇数，`2` 无解。
- 去掉最低位的 `1`：应去掉末尾连续 `1` 的最高位，才能得到最小的 `x`。

**追问。**
- 为什么这样最小？：`x` 必须包含 `p` 中末尾连续 `1` 以外的所有位，在这段 `1` 里只需少一位，少最高位值减得最多。

**同模式。** LC 3315 构造最小位运算数组 II、LC 191 位 1 的个数（Number of 1 Bits）、LC 201 数字范围按位与
