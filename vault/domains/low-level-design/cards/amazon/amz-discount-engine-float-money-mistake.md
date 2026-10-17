---
id: amz-discount-engine-float-money-mistake
node: amazon.amz-discount-engine
type: qa
step: 9
tags: [grown]
---
## Q
在购物车折扣引擎里，用 float 存钱会出什么错？给一个具体输入，并说明怎么修。

## A
`0.1 + 0.2` 在 Python 里是 `0.30000000000000004`；`19.99 * 100` 是 `1998.9999999999998`，`int(19.99 * 100)` 得到 `1998`，少了一分钱。每次相加都累积误差，对账永远差几分。

修复：金额存整数分，字符串价格用 `Decimal` 一次性精确转换：

```python
from decimal import Decimal, ROUND_HALF_UP
cents = int((Decimal("19.99") * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))   # 1999
```
