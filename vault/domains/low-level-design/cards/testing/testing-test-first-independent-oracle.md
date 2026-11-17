---
id: testing-test-first-independent-oracle
node: testing.test-first
type: qa
step: 4
---
## Q
税额规则是「按金额的 5% 收，四舍五入，恰好一半进位」。实现用 `round(cents * 5 / 100)`，几个手写例子都通过。怎样让测试的期望值不依赖实现本身，又能发现问题？

## A
**期望值用另一条路算，随机输入对拍**

- **独立**：参照实现只看规则，不看被测代码；这里用整数运算 `(cents * 5 + 50) // 100`，没有浮点，也不用内置的 `round`；
- **对拍**：随机生成上千个输入，固定种子，两边结果逐个比较；手写例子想不到的输入，随机会碰到；
- **这个缺陷**：`round` 对恰好一半取偶数（银行家舍入，banker's rounding），`round(46.5)` 是 46，规则要 47；
- **失败可复现**：固定种子，失败时打印第一个反例，别人照着就能重跑；
- **参照要比实现笨**：越简单、越接近规则原文，越不容易和实现犯同一个错；复制实现的公式再换个写法不算独立。

```python
import random

def tax(cents: int) -> int: return round(cents * 5 / 100)       # 被测实现
def oracle(cents: int) -> int: return (cents * 5 + 50) // 100   # 规则的另一种写法

rng = random.Random(7)                                           # 固定种子
bad = sorted(c for c in (rng.randrange(10_000) for _ in range(500)) if tax(c) != oracle(c))
print(bad[:3])                                                   # [930, 2490, 2530]：930 的 5% 是 46.5，round 给 46，规则要 47
```

<details class="pt"><summary>延伸</summary>

金额数据也可以拿 `fractions.Fraction` 做参照：它精确，没有舍入。对拍时让两个实现各自走完整条流程，不要把参照的中间结果传给被测代码。

</details>

**知识点：**先写失败的测试（Test First）
