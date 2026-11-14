---
id: msd-mlops-testing-ml-data-tests
node: mlops.testing-ml
type: qa
step: 2
---
## Q
数据测试具体怎么写？用 pandera（或 Great Expectations）写一个训练数据的校验，说明哪些检查是硬失败、哪些只报警，以及训练集和评测集重叠该怎么查。

## A
**用 pandera 声明一张表应该长什么样：**

```python
import pandera.pandas as pa

orders = pa.DataFrameSchema({
    "order_id": pa.Column(str, unique=True),
    "amount":   pa.Column(float, pa.Check.in_range(0, 1_000_000)),
    "country":  pa.Column(str, pa.Check.isin(KNOWN_COUNTRIES)),
    "card_age_days": pa.Column(int, pa.Check.ge(0), nullable=True),
    "label":    pa.Column(int, pa.Check.isin([0, 1])),
})

def test_training_snapshot():
    df = load_snapshot("2026-11-01")
    orders.validate(df, lazy=True)              # 一次报告全部违规
    assert df["card_age_days"].isna().mean() < 0.02
    assert 0.0005 < df["label"].mean() < 0.01   # 欺诈率在合理区间
```

Great Expectations 的写法类似，用 `expect_column_values_to_be_between`、`expect_column_values_to_not_be_null` 这类"期望"组成一个套件，在流水线里对每批数据运行并生成报告。

**硬失败（阻断训练）：**
- 列缺失或类型变了；主键重复。
- 金额为负、标签不是 0 或 1。
- 行数比上次少了一半以上。
- 训练集和评测集有重叠。

**只报警（人看一眼）：**
- 某列空值比例从 1% 升到 3%。
- 某个类别特征出现了新值。
- 特征分布相对上次训练有中等漂移。

**查训练集和评测集重叠：**
- **按 ID：** `len(set(train.order_id) & set(test.order_id)) == 0`。
- **按实体：** 同一个用户的订单不能一部分在训练、一部分在评测，否则模型靠"记住这个用户"拿高分。按用户切分后断言用户集合不相交。
- **按时间：** 评测集的所有时间戳都晚于训练集的最大时间戳，防止用未来预测过去。
- **大语言模型：** 评测题目和训练语料做 n-gram 重叠检测（比如连续 13 个词完全相同就算命中），命中的题目单独标出或剔除，否则评测分数被"背过答案"抬高。
