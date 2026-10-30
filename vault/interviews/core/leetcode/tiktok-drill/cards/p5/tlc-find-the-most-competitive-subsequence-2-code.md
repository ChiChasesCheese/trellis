---
id: tlc-find-the-most-competitive-subsequence-2-code
node: p5.find-the-most-competitive-subsequence
type: qa
step: 2
---
## Q
**LC 1673 找出最具竞争力的子序列**｜写出 Python 实现

整数数组 `nums`（长度 `1..10^5`，元素 `0..10^9`）和整数 `k`（`1..len(nums)`）。返回 `nums` 中长度为 `k` 的字典序最小的子序列。要求 `O(n)`。

## A
**思路。** 一共要丢掉 `drop = n - k` 个元素。从左到右扫描，只要栈顶比新元素大而且还有丢弃额度，就弹栈并消耗一个额度；然后压入新元素。扫描结束后，栈可能还多出元素（额度没用完时，说明后面是递增的），截取前 `k` 个就是答案。

```python
def most_competitive(nums: list[int], k: int) -> list[int]:
    drop = len(nums) - k               # 一共可以丢掉多少个元素
    stack: list[int] = []
    for x in nums:
        while drop and stack and stack[-1] > x:   # 栈顶比新来的大：丢掉栈顶更优
            stack.pop()
            drop -= 1
        stack.append(x)
    return stack[:k]                   # 丢额度没用完时，末尾多出的部分直接截掉
```

运行：`nums=[3,5,2,6], k=2` → `[2, 6]`，`nums=[2,4,3,3,5,4,9,6], k=4` → `[2, 3, 3, 4]`，`nums=[3,1], k=2` → `[3, 1]`，`nums=[1,2,3,4], k=2（递增，末尾要截断）` → `[1, 2]`，`nums=[5], k=1` → `[5]`。

**复杂度。** 时间 `O(n)`：每个元素入栈一次、至多出栈一次（摊还）；空间 `O(n)`（栈，至多存下全部元素；最终截取前 `k` 个）。

**写法要点。** `while drop and stack and stack[-1] > x` 三个条件分别是「额度」「栈非空」「单调性」，把真值判断直接放在 `while` 里；`stack[:k]` 一次完成截断；`drop` 同时是计数器和开关，比 `len(stack) + n - i > k` 好理解；列表直接当栈，`append` / `pop()` 都是 `O(1)`。
