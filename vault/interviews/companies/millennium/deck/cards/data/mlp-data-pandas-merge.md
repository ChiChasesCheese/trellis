---
id: mlp-data-pandas-merge
node: data.pandas
type: qa
step: 2
---
## Q
**merge：inner、left 与重复键**｜pandas 常用操作

"成交表要加上每个代码所属的柜台（desk）。用 merge 怎么写？合并之后行数为什么可能变多？"

## A
**做了什么。** `merge` 按键把两张表的行配对拼接。`inner` 只留两边都有的键；`left` 保留左表全部行，右边没配上的补 NaN。

```
成交 trades        对照 ref            left merge 结果
sym   qty          sym   desk          sym   qty  desk
AAPL  10           AAPL  EQ            AAPL  10   EQ
MSFT  20     +     MSFT  EQ       →    MSFT  20   EQ
TSLA   5           MSFT  TECH          MSFT  20   TECH   ← 多出一行
                                       TSLA   5   NaN
```

```python
out = trades.merge(ref, on="sym", how="left",
                   validate="m:1")  # 要求右表键唯一，否则抛 MergeError
```

- **坑：右表键重复会让左表行数膨胀。** 上例 MSFT 在对照表里出现两次，成交行被复制成两行，之后按 sym 求和就把 MSFT 的数量算了两遍，而且不报错。
- **`validate`：** `"m:1"` 表示左表多行对右表一行；重复时当场抛 `MergeError`，把静默错误变成响起来的错误。
- **left 与 inner 的选择：** 想保留所有成交、缺对照的行事后检查，用 left；用 inner 会悄悄丢掉 TSLA 这一行。
- **检查习惯：** 合并后立刻比较前后行数，并数一下新列里的 NaN。

**英文答法。**
- "I'll do a **left merge** so no trade is dropped."
- "The reference table must be **unique on the key**, so I pass `validate='m:1'`."
- "After the merge I **compare row counts** and count the NaNs in the new column."
