---
slug: random-pick-index
---
## Q
**LC 398 随机数索引**｜Medium

数组 `nums` 可含重复数。设计 `pick(target)`：从所有值为 `target` 的下标中等概率随机返回一个。

## A
**一句话。** 水塘抽样：遍历数组，遇到第 `k` 个等于 `target` 的位置就以 `1/k` 的概率换成它，不用额外空间。

```python
class Solution:
    def __init__(self, nums):
        self.nums = nums

    def pick(self, target):
        ans = cnt = 0
        for i, x in enumerate(self.nums):
            if x == target:
                cnt += 1
                if random.randrange(cnt) == 0:  # 以 1/cnt 换
                    ans = i
        return ans
```

**复杂度。** 时间 `pick` 为 `O(n)`，空间 `O(1)`（不计输入）。

**易错点。**
- 概率写成 `1/n` 或固定概率：必须随已见个数变成 `1/cnt`，这样每个位置最终被选中的概率都是 `1/总数`。
- 先 `cnt += 1` 再抽：`randrange(cnt)` 里 `cnt` 已是含本次的个数，顺序反了第一个位置永远选不上。
- 把 `random.randrange(cnt) == 0` 换成 `randint(0, cnt)`：多一个取值，概率变成 `1/(cnt+1)`。

**追问。**
- 为什么每个位置概率相等？：第 `k` 个被选中是 `1/k`，之后不被换掉是 `(k/(k+1))·…·((m-1)/m) = k/m`，乘起来恰为 `1/m`。
- `pick` 调用很多次呢？：预处理成 `值 -> 下标列表`，每次 `random.choice`，`O(1)` 但多用 `O(n)` 空间。

**同模式。** LC 382 链表随机节点、LC 528 按权重随机选择、LC 497 非重叠矩形中的随机点、LC 470 用 Rand7() 实现 Rand10()
