---
id: mlp-data-pandas-groupby-agg
node: data.pandas
type: qa
step: 1
---
## Q
**groupby 与聚合**｜pandas 常用操作

"一张有几百万行的成交表，按 id 求每个 id 的金额总和。"从零讲：groupby 做了什么，怎么写，哪里会丢行？

## A
**做了什么。** `groupby` 把行按键值分成若干小组（group），每组再用聚合函数（aggregation，如 sum、count、max）压成一行。输入 5 行，输出每个 id 一行：

```
id   amt          id   total  n   top
A    10.50        A    14.25  2   10.50
B     5.25   →    B     6.00  2    5.25
A     3.75        C   100.00  1  100.00
C   100.00
B     0.75
```

```python
out = (df.groupby("id", as_index=False)
         .agg(total=("amt", "sum"),    # 命名聚合：新列名=(列, 函数)
              n=("amt", "count"),
              top=("amt", "max")))
```

- **命名聚合：** `agg(新列名=(原列, 函数))` 一次出多列，列名直接可读，不必事后改名。
- **键要保留成列：** 默认键变成行索引；`as_index=False` 或事后 `reset_index()` 才得到普通列。
- **坑：键为空的行被丢掉。** 默认 `dropna=True`，id 为 NaN 的行不进任何一组，总和少了一块却不报错；要保留写 `dropna=False`。
- **坑：count 不数空值。** `count` 只数非空，数行数用 `size`。
- **规模：** 装不进内存时用 `read_csv(chunksize=…)` 每块先 groupby 求和，再把各块结果拼起来对 id 再 groupby 求和一次；因为求和满足结合律，结果与分块方式无关。

**英文答法。**
- "I **group by** the id and **sum** the amount; that gives one row per id."
- "If the file doesn't fit in memory, I read it in **chunks**, aggregate each chunk, then **re-aggregate** the partial sums."
- "Sum is associative, so the chunk size doesn't change the result."
- "I'd check rows with a **missing id**, because groupby drops them by default."
