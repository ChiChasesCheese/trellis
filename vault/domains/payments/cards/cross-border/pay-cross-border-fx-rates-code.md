---
id: pay-cross-border-fx-rates-code
node: cross-border.fx-rates
type: qa
step: 5
---
## Q
请写出一个带加价的换汇报价函数：商品以 EUR 标价，用户的卡以 USD 扣款，输出最终汇率和扣款金额（最小货币单位），并说明为什么必须用 Decimal 和舍入规则。

## A
```python
from decimal import Decimal, ROUND_HALF_EVEN

def usd_charge(eur_minor: int, mid: Decimal, markup_bps: int) -> tuple[Decimal, int]:
    """Price is in EUR; the customer's card is charged in USD (USD per 1 EUR)."""
    rate = mid * (Decimal(10000) + markup_bps) / Decimal(10000)   # worse for the customer
    usd = (Decimal(eur_minor) * rate).quantize(Decimal(1), rounding=ROUND_HALF_EVEN)
    return rate, int(usd)

mid = Decimal("1.0850")
print(usd_charge(10000, mid, 0))
print(usd_charge(10000, mid, 200))
```
实际输出：
```
(Decimal('1.0850'), 10850)
(Decimal('1.1067'), 11067)
```
即 100.00 EUR 在中间价下是 108.50 USD，加价 200 个基点后是 110.67 USD，差额 217（2.17 美元）就是换汇收入。

**为什么这样写**
1. **Decimal 而不是 float**：浮点数无法精确表示 1.0850 这类十进制小数，累加或比较会出现 0.1+0.2 这类微小偏差，金额会一分一分地漂。
2. **输入输出都是整数最小货币单位**：10000 表示 100.00 EUR，10850 表示 108.50 USD，避免小数点处理混乱。
3. **舍入只发生一次**：先用高精度算出结果，最后一步按银行家舍入（ROUND_HALF_EVEN）取整，不在中间步骤多次舍入。
4. **加价用基点整数**：200 bps 清晰，避免 0.02 与 2% 混用。
