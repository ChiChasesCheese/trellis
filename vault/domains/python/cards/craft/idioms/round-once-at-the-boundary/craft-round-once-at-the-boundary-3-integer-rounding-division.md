---
id: craft-round-once-at-the-boundary-3-integer-rounding-division
node: craft.idioms.round-once-at-the-boundary
type: qa
step: 3
---
## Q
**在边界处取整一次 · 纯整数怎么做四舍五入除法和向上取整**｜写法

折扣引擎要算「金额乘一个比例再除以分母，四舍五入到分」，不想引入 `float` 或 `Decimal`。折扣引擎里的 `(2*n + d) // (2*d)` 为什么等价于四舍五入？输入是负数时还对吗？

## A
**要点。** 四舍五入就是 `floor(n/d + 1/2)`。分子分母同乘 2：`floor((2n + d) / (2d))`，也就是 `(2n + d) // (2d)`，全是整数，没有浮点，没有精度问题。向上取整同理：`-(-n // d)`，先取负让地板除变成天花板除，再取负回来（计费里「不足一小时按一小时」就是它）。

```python
def div_half_up(n: int, d: int) -> int:
    """非负整数的四舍五入除法(.5 进位)，不引入 float / Decimal。"""
    return (2 * n + d) // (2 * d)

def div_half_up_signed(n: int, d: int) -> int:
    """对称版：负数按绝对值舍入再加符号(.5 远离 0)。"""
    sign = -1 if n < 0 else 1
    return sign * div_half_up(abs(n), d)

def div_ceil(n: int, d: int) -> int:
    return -(-n // d)                       # 向上取整：先取负，地板除，再取负

print("7/2 ->", div_half_up(7, 2), "| 5/3 ->", div_half_up(5, 3), "| 4/3 ->", div_half_up(4, 3))
print("与 floor(n/d + 1/2) 一致:", all(div_half_up(n, d) == math.floor(Fraction(n, d) + Fraction(1, 2)) for n in range(200) for d in range(1, 12)))
print("负数直接套公式 -7/2 ->", div_half_up(-7, 2))
# -3.5 被取成 -3：.5 向 +无穷进位，不对称
print("对称版         -7/2 ->", div_half_up_signed(-7, 2))
print("向上取整 7/2 ->", div_ceil(7, 2))
print("3601 秒按小时计 ->", div_ceil(3601, 3600), "小时")
```

实际输出：

```
7/2 -> 4 | 5/3 -> 2 | 4/3 -> 1
与 floor(n/d + 1/2) 一致: True
负数直接套公式 -7/2 -> -3
对称版         -7/2 -> -4
向上取整 7/2 -> 4
3601 秒按小时计 -> 2 小时
```

**易错。** Python 的 `//` 是地板除（向 −∞ 取整），所以公式对负数得到的是「.5 向 +∞ 进位」，-3.5 变成 -3，而不是对称的 -4。账务里正负要对称（一笔退款和原来那笔扣款金额相同），所以负数先取绝对值，算完再加符号；或者限制该函数只接受非负数，并在文档里写明（折扣引擎里该函数注明了「非负整数」）。

**为什么。** 这个写法的价值是：所有中间量都是整数，结果可复现、没有浮点环境差异，也比 `Decimal` 快；适合比例是整数百分比或基点的场景。
