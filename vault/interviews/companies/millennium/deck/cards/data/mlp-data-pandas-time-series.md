---
id: mlp-data-pandas-time-series
node: data.pandas
type: qa
step: 4
---
## Q
**时间序列：resample、rolling、shift**｜pandas 常用操作

"一分钟一条的价格序列，要按 2 分钟取收盘价、算滑动平均和收益率。三个操作各做什么？"

## A
**做了什么。** 前提是索引为时间类型（DatetimeIndex）。

```
时间    价格      resample("2min").last()     rolling(2).mean()   pct_change()
09:30   10        09:30 → 11                  NaN                 NaN
09:31   11        09:32 → NaN（这段没数据）    10.5                0.100
09:34   13        09:34 → 12                  12.0                0.182
09:35   12                                    12.5               -0.077
```

```python
bars = s.resample("2min").last()   # 重采样：按固定时间桶聚合
ma   = s.rolling(2).mean()         # 滚动窗口：最近 2 行的均值
prev = s.shift(1)                  # 整体后移一行：每行拿到上一行的值
ret  = s / s.shift(1) - 1          # 收益率，等价于 pct_change()
```

- **resample：** 把时间切成等长的桶再聚合；空桶出现 NaN，用 `ffill()` 或 `fillna` 决定怎么补。
- **rolling：** 窗口按"行数"算，数据有缺口时窗口会跨过缺口；要按时间长度算写 `rolling("2min")`。窗口不满时头几行是 NaN。
- **shift：** 正数向后移，用来拿"上一期"的值；`shift(-1)` 拿到的是未来值，用来造特征会把答案泄露给模型。
- **坑：没排序。** 索引乱序时 shift 和 rolling 得到错位的数，先 `sort_index()`。

**英文答法。**
- "I **resample** to two-minute bars and take the last price in each bucket."
- "I use **shift one** to get the previous price, never shift minus one, to avoid **look-ahead**."
- "I make sure the index is **sorted** first."
