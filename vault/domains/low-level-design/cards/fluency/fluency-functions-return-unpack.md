---
id: fluency-functions-return-unpack
node: fluency.functions
type: qa
step: 4
---
## Q
函数要同时返回价格、手续费和币种。返回裸元组 `(100, 2, "USD")` 和返回 `NamedTuple` 各有什么取舍？解包写错个数、某个分支忘了写 `return` 时会发生什么？

## A
**两个值用元组解包，三个以上用有名字的类型**

- **返回多个值就是返回一个元组**：`lo, hi = minmax(xs)` 是对元组的解包；调用方个数写错抛 `ValueError: too many values to unpack`；
- **字段多了用 `NamedTuple` 或 dataclass**：`q.fee` 自说明，调用处不必记顺序；`NamedTuple` 仍然是元组，旧的解包写法继续可用；
- **星号解包**：`first, *rest = items` 取头和余下；`rest` 永远是 `list`，可以为空；
- **漏写 return 返回 `None`**：函数某个分支没有 `return`，调用方拿到 `None`，错误要等到下一步才暴露（`None + 1`）；让每个分支都显式返回，或者用类型检查器的 `-> int` 提示抓出来；
- **返回的类型保持一致**：有时返回列表、有时返回 `None` 会逼每个调用方都加判断，空结果就返回空列表。

```python
from typing import NamedTuple

class Quote(NamedTuple):
    price: int
    fee: int
    currency: str

q = Quote(price=100, fee=2, currency="USD")
price, fee, cur = q                    # 仍然可以按位置解包
print(q.fee, price, cur)               # 2 100 USD

first, *rest = "abc"
print(first, rest)                     # a ['b', 'c']
try: x, y = [1, 2, 3]
except ValueError as e: print(e)       # too many values to unpack (expected 2)

def noret(x):
    if x: return 1
print(noret(0))                        # None：没有走到 return
```

**知识点：**函数签名与参数（Function Signatures）
