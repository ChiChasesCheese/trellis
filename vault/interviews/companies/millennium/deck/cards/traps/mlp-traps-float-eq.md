---
id: mlp-traps-float-eq
node: traps.float
type: qa
step: 1
---
## Q
**浮点数相等**｜语言陷阱与读代码

下面的 Python 代码输出什么？

```python
print(0.1 + 0.2 == 0.3)
print(0.9 - 0.8)
t = 0
for _ in range(10): t += 0.1
print(t == 1.0)
```

## A
**输出。**
```
False
0.09999999999999998
False
```

- **为什么：** 浮点数（float，IEEE 754 双精度）用二进制小数存储，0.1、0.2、0.3 都不是有限位二进制小数，存进去的是最接近的近似值；做完运算误差留在最后几位，所以不严格相等。
- **同样的事在 Java 里一样：** `0.9 - 0.8` 在 Java 里也打印 `0.09999999999999998`，因为 `double` 就是同一种格式；换语言不能绕开。
- **累加会放大：** 十次 `+= 0.1` 得到 0.9999999999999999，每一步都带一点舍入误差。
- **什么时候相等能用：** 值本身就是二进制能精确表示的数（0.5、0.25、整数），才可以用 `==`。
- **记住：** 浮点数永远不用 `==` 比较，用差值小于容差（`abs(a - b) < 1e-9` 或 `math.isclose`）；要精确的十进制，用整数或十进制类型。

**英文答法。**
- "Floats are stored in **binary**, so 0.1 has no exact representation."
- "I'd never compare with `==`; I'd use a **tolerance**, like `math.isclose`."
- "For exact decimal values I'd switch to **Decimal** or integers."
