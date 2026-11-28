---
id: py-out-identity-nan
node: output.identity
type: qa
step: 3
---
## Q
**NaN 不等于自己**｜读代码说输出

```python
n = float("nan")
print(n == n, n is n)
print(n in [n], [n] == [n])
print(n in {n}, {n: 1}.get(float("nan")))
print(float("nan") in [float("nan")])
```

输出什么？

## A
**输出。**

```
False True
True True
True None
False
```

**为什么。**

- IEEE 754 规定 NaN 与任何数都不相等，包括自己，所以 `n == n` 是 False；但 `n is n` 是同一个对象，为 True。
- 容器的包含测试和比较先看身份再看 `==`：元素就是同一个对象时直接算相等，所以 `n in [n]` 和 `[n] == [n]` 都是 True，集合同理。
- `float("nan")` 每次新建对象，身份不同，`==` 又是 False，所以第二个 NaN 查不到。

**语言为什么这样设计。**

- 先看身份是语言参考里写明的规则（`x is e or x == e`），目的是让容器满足「放进去的东西一定能找到」，同时跳过昂贵的 `==`。
- NaN 的怪脾气来自 IEEE 754，Python 没有特殊处理。JavaScript 同样 `NaN !== NaN`，但 `includes(NaN)` 为 true、`indexOf(NaN)` 为 -1，也是因为两个方法的比较规则不同。

**怎么写才对。**

```python
import math
math.isnan(x)      # 判断 NaN
```

**面试里一句话。**

NaN is never equal to itself, but containers check identity before equality, so the same NaN object is found while a fresh NaN is not.
