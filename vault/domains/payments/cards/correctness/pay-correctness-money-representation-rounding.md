---
id: pay-correctness-money-representation-rounding
node: correctness.money-representation
type: qa
step: 3
---
## Q
浮点数为什么会让金额算错？银行家舍入（round half to even）和四舍五入有什么区别？用 Python 演示。

## A
**浮点的问题**：二进制只能精确表示 2 的负幂次的和，0.1 无法精确表示，累加就产生误差。**舍入规则**：当计算结果（如金额 × 费率）超出最小单位，必须按固定规则取整。

- **四舍五入**（half up）：恰好在中间时向上，0.125 → 0.13。
- **银行家舍入**（half even）：恰好在中间时取使最后一位为偶数的方向，0.125 → 0.12，0.135 → 0.14。长期统计上无偏，不会系统性地多进。

```python
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
print(0.1 + 0.2, Decimal("0.1") + Decimal("0.2"))
for s in ("0.125", "0.135", "2.5"):
    d = Decimal(s)
    q = Decimal("0.01") if s != "2.5" else Decimal("1")
    print(s, d.quantize(q, ROUND_HALF_EVEN), d.quantize(q, ROUND_HALF_UP))
```

实际输出：

```
0.30000000000000004 0.3
0.125 0.12 0.13
0.135 0.14 0.14
2.5 2 3
```

**选哪种**：没有绝对正确，取决于对手方。渠道、税务、合同对舍入有规定的，必须与之**完全一致**，否则每笔差一分，累计后对账出现大量小差额。内部没有约束时，银行家舍入更公平；很多税务和商业规则要求四舍五入。关键是：规则写进文档，全系统一个实现。
