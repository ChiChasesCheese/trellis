---
slug: maximum-xor-of-two-numbers-in-an-array
---
## Q
**LC 421 数组中两个数的最大异或值**｜Medium

给非负整数数组 `nums`，返回 `nums[i] XOR nums[j]` 的最大值（`0 ≤ i ≤ j < n`）。

## A
**一句话。** 从最高位到最低位贪心：假设这一位答案能是 1，把所有数的当前前缀放进哈希集合，看有没有两个前缀异或等于「已确定的高位加上这一位的 1」。

```python
def find_maximum_xor(nums):
    ans = 0
    for b in range(30, -1, -1):        # 从高位到低位
        ans <<= 1
        prefixes = {x >> b for x in nums}   # 各数当前的前缀
        want = ans | 1                 # 试试这一位能否为 1
        if any(want ^ p in prefixes for p in prefixes):
            ans = want
    return ans
```

**复杂度。** 时间 `O(31·n)`，空间 `O(n)`。

**易错点。**
- 先固定整个答案再验证：要逐位确定，每一位都依赖更高位已确定的结果。
- 忘了 `ans <<= 1`：前缀每低一位就多一位，答案也要同步左移。
- 用 `a ^ b == want` 的双循环：`O(n²)`，应利用 `a ^ want = b` 在集合里查。

**追问。**
- 字典树（Trie）怎么做？：把每个数按位插入 Trie，再对每个数沿「相反位」走，能走反就走反，`O(31n)`。
- 为什么贪心正确？：高位的 1 比低位全部加起来都大，所以先保证高位尽量为 1。

**同模式。** LC 2935 找出强数对的最大异或值 II、LC 208 实现 Trie (前缀树)、LC 136 只出现一次的数字
