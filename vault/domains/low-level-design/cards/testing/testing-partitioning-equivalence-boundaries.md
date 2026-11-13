---
id: testing-partitioning-equivalence-boundaries
node: testing.partitioning
type: qa
step: 1
---
## Q
一个接口参数 `max_tokens` 的规格是「整数，1 到 4096，含两端；不传时默认 256」。用等价类划分（equivalence partitioning）和边界值分析（boundary value analysis）挑出最少的测试用例，并说明为什么是这几个。

## A
**等价类：把输入按「程序应当同样对待」分组，每组挑一个代表。边界值：bug 最常出现在组与组的交界处，所以交界两侧都要测。**

| 类别 | 代表值 | 期望 |
|---|---|---|
| 有效：区间内 | `256` | 接受 |
| 有效：下边界 | `1` | 接受 |
| 有效：上边界 | `4096` | 接受 |
| 无效：低于下界 | `0`、`-1` | 400 错误，信息说明范围 |
| 无效：高于上界 | `4097` | 400 错误 |
| 缺省 | 不传 | 按 256 处理 |
| 类型错 | `"10"`、`10.5`、`null`、`true` | 400 错误 |

```python
@pytest.mark.parametrize("value, ok", [
    (1, True), (256, True), (4096, True),
    (0, False), (-1, False), (4097, False),
    ("10", False), (10.5, False), (None, False), (True, False),
])
def test_max_tokens_validation(value, ok): ...
```

- **为什么测边界两侧：** `<` 写成 `<=` 这类差一错误（off-by-one）只在边界上暴露。只测 1 和 4096 抓不到 `> 4096` 写成 `>= 4096`；只测 0 和 4097 抓不到 `>= 1` 写成 `> 1`。所以测 0、1、4096、4097。
- **`True` 为什么单列：** Python 里 `bool` 是 `int` 的子类，`isinstance(True, int)` 为真，不专门排除就会把 `true` 当成 1 接受。
- **「缺省」和「显式 null」是两类：** 很多 bug 出在把两者混为一谈。
- **用例数：** 7 个类别、10 个值，覆盖了全部区间、边界和类型错误。把 1 到 4096 每个都测一遍并不比这更有信心。
