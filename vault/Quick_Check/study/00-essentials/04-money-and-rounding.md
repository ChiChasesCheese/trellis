# 04 · 金额、精度、舍入、费率、分摊

> 这是隐藏测试最密集的一章。53 道题里有 14 道直接考钱，全部 965 个测试里
> `fmt` 类占 60 个 —— 而 `fmt` 挂掉的第一大原因就是舍入。

---

## 1. 三条铁律

1. **金额从解析那一刻起就是整数最小单位（分）。** 中间计算全程 `int`。
2. **浮点数不得出现在任何金额路径上。** 包括中间比较、包括排序键。
3. **只在最终输出时格式化一次。** 格式化函数只有一个。

违反任意一条，你会在 10^5 条数据的 perf 测试上漂移几分钱，而那个测试期望的是精确值。

---

## 2. 字符串 → 分

输入通常是 `"10.99"` 或 `"1099"`。两种情况分开处理：

```python
from decimal import Decimal

def to_cents(s: str) -> int:
    """'10.99' -> 1099。输入可能是 '10'、'10.9'、'10.990'、'-3.50'。"""
    return int(Decimal(s).scaleb(2))          # scaleb(2) = × 10^2，精确
```

为什么不用 `int(float(s) * 100)`：`float("1.15") * 100 == 114.99999999999999`，
`int(...)` 截断成 114。**少一分**。

为什么不用 `int(round(float(s) * 100))`：能对，但 `round` 是 banker's rounding，
在 `.005` 这一档上和题面要求的 half-up 不一致，而题面几乎一定有一个 `x.xx5` 的测试。

**小数位数超过 2 位怎么办**：题面会说。常见三种：
- 拒绝该行（`input.malformed` 的范畴）
- 按题面的舍入模式收敛到 2 位
- 保留高精度直到最后（此时用 `Decimal` 全程，最后 `quantize` 一次）

---

## 3. 分 → 字符串

```python
def fmt_cents(c: int) -> str:
    sign = "-" if c < 0 else ""
    c = abs(c)
    return f"{sign}{c // 100}.{c % 100:02d}"
```

**为什么要先取绝对值**：`-1 // 100 == -1`、`-1 % 100 == 99`，
直接套公式会得到 `"-1.99"` 而正确答案是 `"-0.01"`。

需要 `$` 或千分位时：

```python
f"${c // 100:,}.{c % 100:02d}"      # $1,234.56
```

**零小数货币**（JPY、KRW、VND、UGX、CLP…）：最小单位就是 1，不除 100。

```python
ZERO_DECIMAL = {"JPY", "KRW", "VND", "UGX", "CLP", "ISK", "XOF", "XAF", "PYG", "RWF"}
def fmt(amount_minor: int, cur: str) -> str:
    if cur in ZERO_DECIMAL:
        return str(amount_minor)
    return f"{amount_minor // 100}.{amount_minor % 100:02d}"
```

题面给了货币列表时就用题面的，不要用记忆中的列表。

---

## 4. 四种舍入模式

| 模式 | 2.5 → | 3.5 → | -2.5 → | 何时用 |
|---|---|---|---|---|
| **half-up**（四舍五入） | 3 | 4 | -3 | 题面说 "round"、"round half up"、大部分计费 |
| **half-even**（银行家舍入） | 2 | 4 | -2 | 题面明确说 "banker's rounding"；Python `round()` 的默认 |
| **floor**（向下取整） | 2 | 3 | -3 | 题面说 "round down"、"floor" |
| **truncate**（向零截断） | 2 | 3 | -2 | 题面说 "truncate"、"drop the fraction"；**放贷、还款常用** |

`floor` 和 `truncate` 只在负数上不同 —— 而题面几乎一定有一个负数（退款）测试。

**整数实现**（`a / b` 的四种舍入，`b > 0`）：

```python
def div_half_up(a, b):    return (a * 2 + b) // (2 * b) if a >= 0 else -((-a * 2 + b) // (2 * b))
def div_floor(a, b):      return a // b
def div_trunc(a, b):      return a // b if a >= 0 else -((-a) // b)
def div_half_even(a, b):
    q, r = divmod(a, b)
    if 2 * r > b or (2 * r == b and q % 2):  q += 1
    return q
```

**`Decimal` 实现**：

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_FLOOR, ROUND_DOWN
x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

`ROUND_DOWN` = 向零截断；`ROUND_FLOOR` = 向下取整。**不是同义词。**

---

## 5. 在哪一步舍入（比用哪种模式更容易错）

同一批数据，两种舍入位置的结果可以差好几分：

```
每行费率 2.9%，三笔 $10.00
逐行舍入：round(1000*0.029)=29 ×3 = 87
先汇总再舍入：round(3000*0.029) = round(87.0) = 87        ← 这个例子恰好相同
每行 $3.33 三笔：
逐行：round(333*0.029)=10 ×3 = 30
汇总：round(999*0.029)=round(28.97)=29                     ← 差 1 分
```

**规则：题面描述规则的粒度 = 舍入的粒度。**
- "each transaction is charged 2.9%" → 每笔算完就舍入。
- "the total is charged 2.9%" → 汇总后舍入一次。
- 没说 → 逐行舍入（这是支付行业的默认，因为每笔交易在账上是独立的一条），写注释声明。

---

## 6. 百分比 + 固定费

Stripe 的经典费率是 `2.9% + $0.30`。整数实现：

```python
def fee(amount_cents: int, bps: int, fixed_cents: int) -> int:
    """bps = 万分之几（2.9% = 290 bps）。half-up 到分。"""
    return (amount_cents * bps + 5000) // 10000 + fixed_cents
```

用 **basis points（万分比）** 而不是浮点百分比，是让整个链条留在整数里的关键。
`(x * bps + 5000) // 10000` 就是 `x * bps / 10000` 的 half-up。

**净额 = 毛额 − 费用**，不是"毛额 × (1 − 费率)"。后者会在舍入上差一分。

---

## 7. 分摊：让各部分加回去正好等于总额

把 100 分按 1:1:1 分给三个人，每人 33 分，少了 1 分。银行不接受这个。

**最大余数法（largest remainder）**：

```python
def split(total: int, weights: list[int]) -> list[int]:
    W = sum(weights)
    base = [total * w // W for w in weights]           # 先向下取整
    rem  = total - sum(base)                            # 剩下的分
    # 余数最大的先拿；平手按下标升序（确定性！）
    order = sorted(range(len(weights)),
                   key=lambda i: (-(total * weights[i] % W), i))
    for i in order[:rem]:
        base[i] += 1
    return base
```

不变量：`sum(split(t, w)) == t`，永远成立。**平手的 tie-break 必须写死**，
否则输出不确定，perf 测试会随机挂。

---

## 8. 阶梯计费

见 `02-core-topics.md` S07。补充两个易错点：

**档位边界恰好命中**：档位 `[0, 1000]` 和 `[1001, ∞)`，用量恰好 1000 时全在第一档。
题面写 "first 1000 units" 是**含 1000** 的。写 `min(units, upper)` 而不是 `upper - 1`。

**免费额度和阶梯的先后**：`included = 100` 免费，之后阶梯计价。
是"前 100 单位免费，第 101 单位开始进第一档"，还是"前 100 单位免费，但计档时仍算进总量"？
两种都出现过。样例能反推出来，反推不出来就写注释。

---

## 9. 台账不变量

```python
# 不变量（每个方法结束时都必须成立）：
#   balance[a] == sum(credits[a]) - sum(debits[a])
#   balance[a] >= 0                     除非 a 有平台授信
#   sum(balance.values()) + platform_loaned == total_deposited
```

**转账要么两端都成功，要么两端都不动**：

```python
def transfer(self, src, dst, cents):
    if cents <= 0:              return "REJECTED:invalid amount"    # 先校验
    if self.bal[src] < cents:   return "REJECTED:insufficient"      # 再校验
    self.bal[src] -= cents                                          # 最后才改
    self.bal[dst] += cents
    return None
```

**先全部校验，再全部修改。** 不要"先扣了再看看够不够"。

---

## 10. 自检清单

写完金额相关代码，逐条问：

- [ ] `float` 出现在金额路径上了吗？（搜一下 `float(`、`/`）
- [ ] 除法用的是 `/` 还是 `//`？（`/` 返回 float）
- [ ] 舍入模式和题面一致吗？`round()` 是 half-even，不是 half-up
- [ ] 舍入发生在题面描述规则的那个粒度上吗？
- [ ] 负数金额（退款、拒付）格式化对吗？`-0.01` 而不是 `-1.99`
- [ ] `x.xx5` 的用例试过吗？（例如 `to_cents("0.005")`）
- [ ] 零小数货币处理了吗？
- [ ] 分摊后各部分加起来等于总额吗？
- [ ] 拒绝路径上余额没被改动吗？
