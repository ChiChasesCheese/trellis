---
id: mlp-data-pandas-merge-asof
node: data.pandas
type: qa
step: 5
---
## Q
**merge_asof：按时间对齐最近一条**｜pandas 常用操作

"每笔成交要配上成交当时的最新报价。时间戳不会完全相等，怎么合并？"

## A
**做了什么。** `merge_asof` 为左表每行，在右表里找时间不晚于它的最近一行（默认向后看，即 backward）。常规 `merge` 要求时间戳严格相等，对不上。

```
成交 trades            报价 quotes         结果
ts        px           ts        bid        ts        px      bid
09:29:59  99.90        09:30:00  100.0      09:29:59  99.90   NaN
09:30:03  100.05       09:30:05  100.1      09:30:03  100.05  100.0
09:30:06  100.12       09:30:09  100.2      09:30:06  100.12  100.1
```

```python
out = pd.merge_asof(trades.sort_values("ts"), quotes.sort_values("ts"),
                    on="ts",
                    tolerance=pd.Timedelta("2s"))  # 报价太旧就不配
```

- **坑：两边必须按键排序。** 没排序会抛错；排了序但另一列有问题，会得到错位的数。
- **坑：只有报价之前才能配。** 09:29:59 的成交早于第一条报价，结果为 NaN，这是对的，不要往后找，否则用到了成交之后才出现的数据（前视偏差，look-ahead bias）。
- **`tolerance`：** 最近一条报价如果比成交早超过 2 秒就不配。上例中 09:30:03 的成交离 09:30:00 的报价已 3 秒，结果变为 NaN，只有 09:30:06 仍配到 100.1。
- **`by="sym"`：** 多个代码混在一张表里时，加 `by` 让配对只发生在同一代码内。

**英文答法。**
- "I use **merge_asof** to attach the **latest quote at or before** each trade."
- "Both frames must be **sorted by time**, and I add `by` the symbol."
- "I set a **tolerance** so a stale quote isn't used, and I never look forward."
