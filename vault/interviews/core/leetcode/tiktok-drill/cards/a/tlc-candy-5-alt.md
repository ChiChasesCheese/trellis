---
id: tlc-candy-5-alt
node: a.candy
type: qa
step: 5
---
## Q
**LC 135 分发糖果**｜另一种解法

有没有只用 `O(1)` 额外空间、一遍扫描的写法？它的思路是什么，什么时候应该选它而不是两遍数组？

## A
**思路。** 评分序列是一连串"上坡、平地、下坡"。上坡时每走一步糖数加一；平地（相等）重新从 `1` 开始；下坡时，糖数从坡底的 `1` 往上数，长度为 `down` 的下坡需要 `1, 2, …, down` 的和，每多走一步下坡就多发 `down` 颗。唯一的麻烦是坡顶：如果下坡长度 `down` 达到了坡顶已拿的糖数 `peak`，坡顶孩子就需要再补 `1` 颗，使它仍然比下坡第一个孩子多。

```python
def candy_one_pass(ratings: list[int]) -> int:
    total = 1                                      # 第 0 个孩子 1 颗
    up = down = 0                                  # 当前上坡 / 下坡已经走了几步
    peak = 1                                       # 上坡顶那个孩子拿的糖数
    for prev, cur in zip(ratings, ratings[1:]):
        if cur > prev:
            up += 1
            down = 0
            peak = up + 1
            total += peak
        elif cur == prev:
            up = down = 0
            peak = 1
            total += 1
        else:
            up = 0
            down += 1
            total += down + (down >= peak)         # 下坡拉得比坡顶还长时，坡顶要补 1 颗
    return total
```

`[1,0,2]` → `5`，`[1,2,2]` → `4`，`[2,2,2]` → `3`，`[1,3,4,5,2]` → `11`，`[1,2,87,87,87,2,1]` → `13`，与两遍数组版的结果相同。

**什么时候选哪个。**
- 两遍数组：思路直白，每个方向的约束一眼看清，面试中先写它；也能直接给出具体分配方案。
- 单遍计数：空间 `O(1)`，适合评分以流的形式到来、内存紧张的场景；代价是"补坡顶"的边界很容易写错，需要多测下坡刚好等于坡顶的情形（如 `[1,2,1,0]`）。

**Python 提醒**：`zip(ratings, ratings[1:])` 一次拿到相邻对，但 `ratings[1:]` 会复制一份列表，严格 `O(1)` 空间时改用 `itertools.pairwise(ratings)`（Python 3.10 及以上）。
