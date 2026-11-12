---
slug: number-of-adjacent-elements-with-the-same-color
---
## Q
**LC 2672 有相同颜色的相邻元素数目**｜Medium

长度 `n` 的数组初始全 `0`（未染色）。依次执行染色查询 `[index, color]`，每次后返回颜色相同的相邻对数（`0` 不算）。

## A
**一句话。** 增量维护对数：每次只影响被染位置与左右邻居两对，先减旧颜色的贡献，再加新颜色的。

```python
def color_the_array(n, queries):
    colors = [0] * n
    same = 0

    def pairs(i, c):        # i 与左右邻居颜色等于 c 的对数
        return ((i > 0 and colors[i - 1] == c)
                + (i < n - 1 and colors[i + 1] == c))

    ans = []
    for i, color in queries:
        if colors[i]:       # 未染色没有旧贡献
            same -= pairs(i, colors[i])
        colors[i] = color
        same += pairs(i, color)
        ans.append(same)
    return ans
```

**复杂度。** 时间 `O(n+q)`，空间 `O(n)`。

**易错点。**
- 把 `0` 当颜色：初始 `[0,0,0,0]` 会数出 `3` 对，旧贡献只在 `colors[i] != 0` 时减。
- 先赋新颜色再减旧贡献：减的变成新颜色的对数。顺序是减、赋值、加。
- 同色重染直接跳过或只加不减：先减后加才保持原值。

**追问。**
- 颜色取值很大要映射吗？：不用，只比较相等。

**同模式。** LC 307 区域和检索 - 数组可修改、LC 2569 更新数组后处理求和查询、LC 1352 最后 K 个数的乘积
