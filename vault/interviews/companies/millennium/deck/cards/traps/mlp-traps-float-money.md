---
id: mlp-traps-float-money
node: traps.float
type: qa
step: 3
---
## Q
**金额与舍入**｜语言陷阱与读代码

下面两段代码输出什么？金额应该怎么存？

```python
print(round(2.5), round(3.5), round(0.125, 2))
print(int(19.99 * 100), round(19.99 * 100))
```

```java
System.out.println(Math.round(2.5) + " " + Math.round(-2.5));
System.out.println((int) (19.99 * 100));
```

## A
**输出。** Python：`2 4 0.12`，然后 `1998 1999`。Java：`3 -2`，然后 `1998`。

- **Python 的 `round` 取偶数：** 恰好在中间的数舍入到最近的偶数（2.5 到 2，3.5 到 4），叫银行家舍入（banker's rounding）；`round(0.125, 2)` 得 0.12，因为 0.125 恰好是二进制精确值，落在中间，取偶数。
- **Java 的 `Math.round` 向正无穷取整：** 2.5 得 3，-2.5 得 -2。两种语言对同一个数不一定给同一个结果。
- **`19.99 * 100` 实际是 1998.9999999999998：** `int()` 截断，丢了一分钱；`round` 才得 1999。
- **金额的存法：** 用整数最小单位（分，cents）存，运算全是整数，只在显示时除以 100；或者用 Decimal、BigDecimal 并显式指定舍入模式。
- **记住：** 金额不用 float；整数分或十进制类型；舍入规则（半入偶还是半入上）要显式写出来，别依赖语言默认。

**英文答法。**
- "I'd store money as **integer cents**, or as Decimal with an explicit rounding mode."
- "`int()` truncates, so `19.99 * 100` becomes **1998**, and we lose a cent."
