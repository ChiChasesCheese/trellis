---
slug: relative-ranks
---
## Q
**LC 506 相对名次**｜Easy

`score` 是各运动员的成绩（互不相同）。前三名依次是 `"Gold Medal"`、`"Silver Medal"`、`"Bronze Medal"`，其余运动员返回名次的字符串。按原顺序返回每人的名次。

## A
**一句话。** 按成绩降序排「下标」，排第几名就是第几名，再按下标写回结果。

```python
def find_relative_ranks(score):
    n = len(score)
    order = sorted(range(n), key=lambda i: -score[i])
    medals = ["Gold Medal", "Silver Medal", "Bronze Medal"]
    res = [""] * n
    for rank, i in enumerate(order):
        res[i] = medals[rank] if rank < 3 else str(rank + 1)
    return res
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 直接排序成绩而丢掉原下标：无法按原顺序输出。
- 名次从 0 开始：`str(rank + 1)` 才是第 4 名起的数字。

**追问。**
- 成绩范围很小可以更快吗？：计数排序把成绩映射到名次，`O(n + 最大成绩)`。
- 成绩可以并列怎么办？：并列名次要先分组，同分同名次，下一名跳过人数。

**同模式。** LC 1331 数组序号转换、LC 1365 有多少小于当前数字的数字、LC 1366 通过投票对团队排名
