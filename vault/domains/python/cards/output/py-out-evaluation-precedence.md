---
id: py-out-evaluation-precedence
node: output.evaluation
type: qa
step: 3
---
## Q
**优先级**｜读代码说输出

```python
print(-2 ** 2)
print(2 ** 3 ** 2)
print(2 ** -1)
print(not 0 == 1)
```

输出什么？

## A
**输出。**

```
-4
512
0.5
True
```

**为什么。**

- `**` 比左边的一元负号绑得更紧，`-2 ** 2` 是 `-(2 ** 2)`，所以是 -4。
- `**` 右结合：`2 ** 3 ** 2` 是 `2 ** (3 ** 2)` = 512，不是 `(2 ** 3) ** 2` = 64。
- `**` 右边可以直接跟一元负号，`2 ** -1` 是 0.5；`not` 的优先级低于比较，`not 0 == 1` 是 `not (0 == 1)`，为 True。

**语言为什么这样设计。**

- 语言参考写明：幂运算比它左边的一元运算符绑得更紧，右边的则更松；这与数学里 -x² = -(x²) 一致。
- C 没有幂运算符；Excel 里 `-2^2` 却等于 4，因为 Excel 的一元负号优先级更高，同一个式子在不同工具里结果不同。

**怎么写才对。**

```python
(-2) ** 2     # 要平方负数就加括号
```

**面试里一句话。**

In Python the power operator binds tighter than a unary minus on its left and associates to the right, so -2 ** 2 is -4 and 2 ** 3 ** 2 is 512.
