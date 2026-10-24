---
id: tlc-python-collections-2-counter-arith
node: python.collections
type: qa
step: 2
---
## Q
**Python 工具箱｜`Counter` 的减法与多重集比较**

`Counter("aabc") - Counter("aab")` 得到什么？两个 `Counter` 能不能直接用 `<=` 判断「前者被后者包含」？`-=` 与 `subtract` 有什么区别？

## A
`Counter` 把次数当多重集（multiset）处理：

```python
from collections import Counter
a, b = Counter(a=3, b=1), Counter(a=1, b=2)
print(a - b)    # Counter({'a': 2})：差里只保留正数，b 的 -1 被丢掉
print(a + b, a & b, a | b)  # 逐键相加 / 取小 / 取大
a.subtract(b)
print(a)        # Counter({'a': 2, 'b': -1})：subtract 保留负数
print(Counter("ab") <= Counter("aabc"), Counter("abb") <= Counter("aabc"))  # True False
```

- 运算符 `-`、`+`、`&`、`|` 都**丢掉非正数**；`subtract`、`update` 原地改，保留零和负数。
- 3.10+ 支持 `<=`、`<`、`==`：`x <= y` 表示每个键 `x[k] <= y[k]`，即多重集包含；每次比较 `O(m)`。
- 典型用法：LC 76 判断窗口是否覆盖 `t`，可写 `not (need - window)`（差为空即覆盖），比手写循环清楚；LC 383 赎金信直接 `not (Counter(ransom) - Counter(magazine))`。

**坑**：在滑动窗口里每步都做一次 `need - window` 是 `O(m)`，总复杂度会退化；热路径上应维护一个「还缺几种」的整数计数，`Counter` 比较只适合只算一次的场合。
