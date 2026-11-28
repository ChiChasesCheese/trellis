---
id: mlp-data-pandas-vectorize
node: data.pandas
type: qa
step: 6
---
## Q
**向量化：不用 apply 逐行循环**｜pandas 常用操作

"对一百万行算每笔成交额 |qty| × price，再按方向打标签。为什么不要 `apply(axis=1)`？"

## A
**做了什么。** 向量化（vectorization）指对整列一次运算，循环发生在底层 C 代码里；`apply(axis=1)` 对每一行调用一次 Python 函数，每次调用都有解释器开销，百万行下通常慢一到两个数量级。

```
qty   price   notional   side
10    150     1500       buy
-4    152      608       sell
 0     70        0       flat
```

```python
df["notional"] = df["qty"].abs() * df["price"]        # 整列相乘
df["side"] = np.select([df.qty > 0, df.qty < 0],      # 条件向量化
                       ["buy", "sell"], default="flat")
# 慢：df.apply(lambda r: abs(r.qty) * r.price, axis=1)
```

- **算术：** 列与列、列与数字之间直接运算；比较得到布尔列，可当筛选条件 `df[df.qty > 0]`。
- **分支：** 两路用 `np.where(条件, 甲, 乙)`，多路用 `np.select(条件列表, 取值列表, default=…)`，不要在 apply 里写 if。
- **坑：用 `&`、`|` 连接条件时每个比较要加括号**，写成 `(a > 0) & (b < 5)`；用 `and` 会抛 `ValueError`。
- **坑：链式赋值。** `df[df.qty > 0]["x"] = 1` 改的是临时副本，原表不变；写 `df.loc[df.qty > 0, "x"] = 1`。
- **何时还是循环：** 每行逻辑依赖前一行的结果且无法用 shift 或累计函数（`cumsum`）表达时。

**英文答法。**
- "I'd **vectorize** this: whole-column arithmetic instead of `apply` on each row."
- "For branches I use `np.where` or `np.select`."
- "Row-wise apply calls Python a million times, so it's **much slower**."
