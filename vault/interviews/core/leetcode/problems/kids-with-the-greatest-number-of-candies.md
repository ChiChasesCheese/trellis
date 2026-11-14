---
slug: kids-with-the-greatest-number-of-candies
---
## Q
**LC 1431 拥有最多糖果的孩子**｜Easy

对每个孩子判断：把 `extraCandies` 全给他，他的糖果数能否达到所有孩子中的最大值（追平也算）。

## A
**一句话。** 额外糖果不改变别人的数量，最大值只算一次，逐个比较 `c + extra >= max`。

```python
def kids_with_candies(candies, extra_candies):
    top = max(candies)          # 只算一次
    return [c + extra_candies >= top for c in candies]
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（不计输出）。

**易错点。**
- 写成 `>`：追平也算最多，`[2,3,5]`、额外 `3` 时第一个孩子应为 `true`。
- 每个孩子都重新 `max`：`O(n^2)`。

**追问。**
- 额外糖果可以分给多个孩子？：问题变了，要看总额能否把某人抬到最大值。
- 在线更新糖果数？：维护最大值（或计数有序表），查询仍是一次比较。

**同模式。** LC 1672 最富有客户的资产总量、LC 2643 一最多的行
