---
id: mlp-traps-float-compare
node: traps.float
type: qa
step: 2
---
## Q
**容差、Decimal 与 BigDecimal**｜语言陷阱与读代码

下面两段代码输出什么？

```python
import math
from decimal import Decimal
print(math.isclose(0.1 + 0.2, 0.3))
print(Decimal(0.1) == Decimal("0.1"))
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
```

```java
System.out.println(new BigDecimal(0.1).equals(new BigDecimal("0.1")));
System.out.println(new BigDecimal("2.0").equals(new BigDecimal("2.00")));
System.out.println(new BigDecimal("2.0").compareTo(new BigDecimal("2.00")));
```

## A
**输出。** Python：`True`、`False`、`True`。Java：`false`、`false`、`0`。

- **`isclose` 为 True：** 它按相对容差（默认 1e-9）比较，吸收了二进制近似的误差。
- **`Decimal(0.1)` 不等于 `Decimal("0.1")`：** 前者拿到的是已经不精确的浮点数 0.1 的全部二进制展开（0.1000000000000000055…），后者才是精确的十进制 0.1。Java 的 `new BigDecimal(0.1)` 同理。
- **构造时用字符串：** 十进制类型的精度只在从字符串（或整数）构造时才保住。
- **`BigDecimal.equals` 比较标度：** `2.0` 和 `2.00` 数值相同但小数位数不同，`equals` 返回 false，放进 `HashSet` 会被当成两个元素；比较数值大小用 `compareTo`，等于 0 才相等。
- **记住：** 十进制类型用字符串构造；Java 比较数值用 `compareTo`，不用 `equals`；容差比较只用于确实是浮点的数据。

**英文答法。**
- "I'd construct the decimal from a **string**, never from a float."
- "In Java, `BigDecimal.equals` also compares **scale**, so I'd use `compareTo`."
