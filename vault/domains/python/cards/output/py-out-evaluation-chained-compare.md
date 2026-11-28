---
id: py-out-evaluation-chained-compare
node: output.evaluation
type: qa
step: 1
---
## Q
**链式比较**｜读代码说输出

```python
print(1 < 2 < 3, 3 > 2 > 2)
x = 5
print(1 < x < 10 > x)
print(False == False in [False])
print((False == False) in [False])
```

输出什么？

## A
**输出。**

```
True False
True
True
False
```

**为什么。**

- `a < b < c` 等价于 `a < b and b < c`，且 `b` 只求值一次；`3 > 2 > 2` 的后半段 `2 > 2` 为 False。
- 所有比较运算符（包括 `==`、`in`、`is`）可以链接在一起，从左到右两两比较并短路。
- `False == False in [False]` 是 `(False == False) and (False in [False])`，两段都为 True；加括号变成 `True in [False]`，结果 False。

**语言为什么这样设计。**

- 链式写法照搬数学里的 `1 < x < 10`，`x` 只算一次，也避免重复计算有副作用的表达式。
- C 和 Java 里 `1 < x < 10` 先得到布尔值，再拿它和 10 比较，在 C 里结果恒为真或语义错误；Python 选择贴近数学写法。

**怎么写才对。**

```python
if lo <= x < hi: ...      # 范围检查用链式
# 混着 ==、in 时加括号，别让读者猜
```

**面试里一句话。**

Chained comparisons like a < b < c mean a < b and b < c with b evaluated once, and the rule applies to every comparison operator including in and ==.
