---
id: errors-values-in-band-sentinel
node: errors.exceptions-vs-values
type: qa
step: 2
---
## Q
`str.find` 找不到返回 `-1`，`charge` 余额不够返回 `False`。用合法值范围里的数字当“失败标记”，会出什么问题？

## A
**错误标记不能和合法值混在同一个值域里**

- **`-1` 是合法下标**：`s[s.find(x)]` 在找不到时不报错，悄悄取到最后一个字符；
- **`False` 是 `0`**：`bool` 是 `int` 的子类，`False + 5` 等于 5，算出一个看着正常的错误结果；
- **后果**：失败没有变成失败，而是变成了一个错误的数，往下游传，查起来要回溯很远；
- **标准库自己也两种都有**：`str.find` 返回 `-1`，`str.index` 抛 `ValueError`；要继续的用 `find`，不该找不到的用 `index`；
- **更好的值域**：用 `None`（`T | None`）做“没有”，调用方被类型检查器逼着先判断；或者直接抛异常。

```python
s = "abc"
print(s[s.find("z")])                       # c：找不到却取到了最后一个字符

def charge(balance: int, n: int):
    return balance - n if balance >= n else False

print(charge(10, 50) + 5)                   # 5：本应失败，却得到一个数
try: s.index("z")
except ValueError: print("index 抛异常，错误不会被悄悄吞下")
```

**知识点：**异常与错误值（Exceptions vs Values）
