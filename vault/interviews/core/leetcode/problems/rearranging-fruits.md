---
slug: rearranging-fruits
---
## Q
**LC 2561 重排水果**｜Hard

两个果篮 `basket1`、`basket2`，交换 `basket1[i]` 与 `basket2[j]` 的成本是两者较小值。求让两篮排序后相同的最小总成本，做不到返回 `-1`。

## A
**一句话。** 两篮的差额凑成待换列表，只处理较小的一半，每次花 `min(x, 2 * 全局最小值)`。

```python
def min_cost(basket1, basket2):
    diff = Counter(basket1)
    diff.subtract(basket2)     # 每种水果两篮的数量差
    extra = []                 # 需要换走的水果
    for fruit, d in diff.items():
        if d % 2:              # 总数为奇数，无法平分
            return -1
        extra += [fruit] * (abs(d) // 2)
    extra.sort()
    cheap = min(min(basket1), min(basket2))
    # 直接换花 x；借最便宜的水果换两次花 2*cheap
    half = extra[:len(extra) // 2]
    return sum(min(x, 2 * cheap) for x in half)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 忘了借中转：`[100,100,1]` 与 `[200,200,1]` 借 `1` 换两次只花 `2`，直接换花 `100`。
- 全局最小只在 `basket1` 里找：`[100,100,5,5]` 与 `[200,200,1,1]` 得 `6`，应为 `3`。
- 累加了 `extra` 的全部元素：一次交换同时解决两个水果，只取较小的一半。

**追问。**
- 为什么只取较小的一半？：每次交换换走两篮各一个多余水果，用最便宜的去换最划算。
- 怎么输出交换方案？：配对时记下 `(篮 1 的水果, 篮 2 的水果)`，借中转时多记两步。

**同模式。** LC 1648 销售价值减少的颜色球、LC 1647 字符频次唯一的最小删除次数、LC 2333 最小差值平方和、LC 462 最少移动次数使数组元素相等 II
