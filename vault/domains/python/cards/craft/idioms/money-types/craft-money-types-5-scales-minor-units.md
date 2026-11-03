---
id: craft-money-types-5-scales-minor-units
node: craft.idioms.money-types
type: qa
step: 5
---
## Q
**金额类型 · 从整数分到账务系统的「最小货币单位加币种」**｜写法

LLD 里金额是一个整数分。放到账务系统和接口里，所有币种都是「分」吗？金额怎么穿过 JSON 接口和数据库而不丢精度？

## A
**要点。** 不是所有币种都是两位小数：日元没有小数，科威特第纳尔有三位（ISO 4217）。所以存的是**最小货币单位（minor unit）的整数加币种代码**，每个币种带自己的小数位数。数据库用整数列（`BIGINT`），接口里用整数或字符串。

```python
# 每种币种的小数位(最小货币单位的指数)；ISO 4217：JPY 无小数，USD 2 位，KWD 3 位
EXPONENT = {"JPY": 0, "USD": 2, "KWD": 3}

def to_minor(amount: str, currency: str) -> int:
    return int(Decimal(amount).scaleb(EXPONENT[currency]))

def to_display(minor: int, currency: str) -> str:
    return str(Decimal(minor).scaleb(-EXPONENT[currency]))

for amt, cur in [("1500", "JPY"), ("19.99", "USD"), ("1.234", "KWD")]:
    m = to_minor(amt, cur)
    print(f"{amt} {cur} -> 存 {m} -> 显示 {to_display(m, cur)}")

# 传输：JSON 数字默认解析成 float，金额用整数最小单位或字符串
body = '{"amount": 19.99}'
print("默认解析 * 100:", json.loads(body)["amount"] * 100)
print("parse_float=Decimal * 100:", json.loads(body, parse_float=Decimal)["amount"] * 100)
```

实际输出：

```
1500 JPY -> 存 1500 -> 显示 1500
19.99 USD -> 存 1999 -> 显示 19.99
1.234 KWD -> 存 1234 -> 显示 1.234
默认解析 * 100: 1998.9999999999998
parse_float=Decimal * 100: 1999.00
```

**变化。** 进程内的 `Money(cents, currency)` 默认「分」是两位小数；系统扩展到多币种，换算表（币种到指数）成为配置的一部分，显示和输入都要查它。费率与汇率不是金额，用定点小数（`Decimal`、数据库 `NUMERIC`）保存，并且标明精度。

**易错。** JSON 的数字在大多数语言里默认解析成 `float`（上面的 `19.99 * 100` 重新变成 `1998.9999999999998`）。接口约定为整数最小单位或字符串，或者解析时指定 `parse_float=Decimal`。

**代价。** 整数分让加减绝对精确，但每次涉及比例（税、分账）都要决定怎么取整，以及余数给谁，见「在边界处取整一次」。

**信号。** 金额需要跨进程、跨语言、持久化。
