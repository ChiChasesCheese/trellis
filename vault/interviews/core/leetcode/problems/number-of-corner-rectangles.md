---
slug: number-of-corner-rectangles
---
## Q
**LC 750 角矩形的数量**｜Medium

`grid` 是 `0/1` 矩阵，求「角矩形」个数：四个角都是 `1` 的轴对齐矩形（只看四个角，边和内部可以是 `0`）。

## A
**一句话。** 逐行处理：该行里每一对都是 `1` 的列 `(a, b)`，之前出现过 `c` 次就新增 `c` 个矩形，然后计数加一。

```python
def count_corner_rectangles(grid):
    cnt, ans = Counter(), 0
    for row in grid:
        ones = [j for j, v in enumerate(row) if v]
        for a in range(len(ones)):
            for b in range(a + 1, len(ones)):
                p = (ones[a], ones[b])
                ans += cnt[p]      # 之前每次出现都能和当前行配对
                cnt[p] += 1
    return ans
```

**复杂度。** 时间 `O(m·n²)`，空间 `O(n²)`。

**易错点。**
- 先 `cnt[p] += 1` 再累加：当前行会和自己配对，多算一个。
- 把「两行共有 `c` 个 1 列」直接加 `c`：应加 `C(c,2)`；逐对计数天然满足这点。

**追问。**
- 行数远多于列数怎么办？：枚举「行对」，数共同的 `1` 列数 `c`，加 `c(c-1)/2`，转置后选较短的一边。
- 哪边枚举更省？：对 `min(m, n)` 那一维做平方枚举。

**同模式。** LC 939 最小面积矩形、LC 1128 等价多米诺骨牌对的数量
