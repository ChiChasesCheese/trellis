---
id: tlc-minimum-area-rectangle-4-followup
node: a.minimum-area-rectangle
type: qa
step: 4
---
## Q
**LC 939 最小面积矩形**｜追问

面试官接着问：（1）点数到 `10^5`，`O(n^2)` 太慢，怎么办？（2）要返回矩形的四个顶点？（3）矩形可以倾斜（边不与坐标轴平行）？

## A
1. **按列扫描**：把点按 `x` 分组。依次处理每一列，对该列内每一对 `(y1, y2)`（`y1 < y2`），若字典里已有这一对，说明前面某一列也有这两个纵坐标，两列夹出一个矩形，面积 `(x - last[(y1, y2)]) * (y2 - y1)`；然后把这一对的最近列更新为当前 `x`。只和“最近的一列”配对就够，因为更早的列宽度更大。

```python
def min_area_rect_columns(points: list[list[int]]) -> int:
    cols: dict[int, list[int]] = {}
    for x, y in points:
        cols.setdefault(x, []).append(y)
    last: dict[tuple[int, int], int] = {}      # (y1, y2) -> 最近一次出现这对纵坐标的列 x
    best = 0
    for x in sorted(cols):
        ys = sorted(cols[x])
        for i, y2 in enumerate(ys):
            for y1 in ys[:i]:
                if (y1, y2) in last:
                    area = (x - last[y1, y2]) * (y2 - y1)
                    if best == 0 or area < best:
                        best = area
                last[y1, y2] = x
    return best
```

   两个示例都得到 `4` 和 `2`。复杂度是 `O(Σ c_x^2)`，`c_x` 是第 `x` 列的点数：每列点少时远小于 `n^2`；全部点挤在少数几列时仍是 `O(n^2)`。可以选取值更多的那一维当“列”，让每列更短。
2. **返回四个顶点**：保留当前最小面积对应的那一对对角点（或 `x`、`y` 的两对坐标），最后拼出四个角。
3. **倾斜矩形（LC 963）**：矩形的两条对角线互相平分且等长。对每一对点，计算（中点，长度的平方）作为键，把点对放进字典；键相同的两条线段就是一个矩形的两条对角线，面积由一条对角线和另一条对角线的端点算出。仍是 `O(n^2)` 个点对。

**Python 提醒**：字典键可以用元组，`last[y1, y2]` 等价于 `last[(y1, y2)]`；`ys[:i]` 每次创建新列表，大列要改成 `for j in range(i)` 下标访问；`dict.setdefault(x, []).append(y)` 比先判断再赋值更短，列表不要用作默认参数的共享对象（`setdefault` 里的 `[]` 每次新建，没有这个问题）。
