---
id: craft-money-types-2-choose-by-intermediate
node: craft.idioms.money-types
type: qa
step: 2
---
## Q
**金额类型 · 整数分、基点、Decimal、Fraction 怎么选**｜写法

计费要算 2.9% 的手续费，外卖按每分钟 0.35 元、精确到秒计费，打车要乘以 1.2 倍的涨价系数。这三个场景都叫「金额乘一个系数」，类型选型却不同。判据是什么？

## A
**要点。** 看**中间值**会不会产生无法精确表示的数。成品金额永远存整数分（最小货币单位）。中间计算按下面选：

| 场景 | 类型 | 理由 |
|---|---|---|
| 折扣、满减，比例是整数百分比 | 整数分 + 基点（1 基点 = 0.01%，2.9% = 290） | 全程整数，最快 |
| 费率有小数（手续费、税） | `Decimal`（字符串构造） | 精确，取整留到最后一步 |
| 要除以 60、3 这类会产生循环小数 | `Fraction`（分子分母） | 一路不舍入，最后才取整 |
| 倍数（涨价 1.2） | `Fraction` | 不是 `1.2` 的 float |

```python
# 司机按「每分钟费率」按秒计费：rate/60 是循环小数
rate = Decimal("0.35")        # 元/分钟

per_sec_dec = rate / 60       # Decimal 默认保留 28 位有效数字，之后被舍入
per_sec_frac = Fraction(rate) / 60       # Fraction 存分子分母，不舍入

print("Decimal :", per_sec_dec, "-> *60 回到 0.35?", per_sec_dec * 60 == rate)
print("Fraction:", per_sec_frac, "-> *60 回到 0.35?", per_sec_frac * 60 == Fraction(rate))

# 累加 60 万段(一万分钟)：Decimal 的误差会累积，Fraction 到最后一步才舍入
seg_dec = sum((per_sec_dec for _ in range(60 * 10000)), Decimal(0))
seg_frac = sum((per_sec_frac for _ in range(60 * 10000)), Fraction(0))
print("一万分钟 Decimal :", seg_dec, "| 精确是 3500?", seg_dec == 3500)
print("一万分钟 Fraction:", seg_frac, "| 精确是 3500?", seg_frac == 3500)
```

实际输出：

```
Decimal : 0.005833333333333333333333333333 -> *60 回到 0.35? True
Fraction: 7/1200 -> *60 回到 0.35? True
一万分钟 Decimal : 3499.999999999999999999851948 | 精确是 3500? False
一万分钟 Fraction: 3500 | 精确是 3500? True
```

**为什么。** `Decimal` 也是有限精度（默认 28 位有效数字），除以 60 之后已经舍入，累加几十万段误差会显出来。`Fraction` 存的是 `7/1200` 本身，累加精确。

**代价。** `Fraction` 的分母可能不断变大，运算比整数和 `Decimal` 慢，只在确有除不尽的环节使用；中间值取整的位置是另一个问题（见「在边界处取整一次」）。
