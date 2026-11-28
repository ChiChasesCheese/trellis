---
id: mlp-data-pandas-pivot-melt
node: data.pandas
type: qa
step: 3
---
## Q
**pivot 与 melt：长表和宽表互转**｜pandas 常用操作

"每天每个代码一行的价格表，要变成每天一行、每个代码一列。反过来呢？"

## A
**做了什么。** 长表（long）每条观测一行，宽表（wide）把某一列的取值摊开成列名。`pivot` 长转宽，`melt` 宽转长。

```
长表                    pivot 后              melt 还原
d   s  px               d    A    B           d   s  px
d1  A  1                d1   1    2           d1  A  1
d1  B  2        →       d2   3    NaN   →     d2  A  3
d2  A  3                                      d1  B  2
                                              d2  B  NaN
```

```python
wide = long.pivot(index="d", columns="s", values="px")
back = wide.reset_index().melt(id_vars="d",
                               var_name="s", value_name="px")
```

- **宽表适合：** 按列做相关系数、同日对比；长表适合：分组聚合、写库。
- **坑：缺失组合变成 NaN。** d2 没有 B，宽表里就是 NaN，melt 回来后多出一行空值，行数不等于原表；需要时 `dropna()`。
- **坑：pivot 遇到重复。** 同一个 (d, s) 出现两行时 `pivot` 抛 `ValueError`；要先聚合时改用 `pivot_table(..., aggfunc="sum")`，它会悄悄把重复项合并。
- **整数列变浮点：** 出现 NaN 后整数列变成浮点，比较相等前注意类型。

**英文答法。**
- "I'll **pivot** the long table so each symbol becomes a column."
- "If a date and symbol can repeat, I need **pivot_table** with an explicit aggregation."
- "Missing pairs show up as **NaN**, so I decide whether to drop or fill them."
