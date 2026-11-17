---
id: data-invariants-conservation
node: data.invariants
type: qa
step: 7
---
## Q
贷款系统要求“所有账户余额的总和永远不变”。怎样让这个不变量不靠自觉维持？

## A
**把所有改动收口到一个入口**

- **守恒**：每次余额变化都经过 `transfer(src, dst, n)`，一处扣、一处加，总和天然不变；
- **先检查，后写入**：余额不足先抛错，扣款与加款之间不会出现“只扣不加”；
- **不留别的入口**：没有 `set_balance`；
- **同类的不变量**：只增不减的计数（违规次数、累计转出）只有一个 `+= 1` 的地方；`Funds(original, remaining)` 里 `original` 不动、`remaining` 只减不增，“负数请求造钱”在入口就被拒绝；
- **测试**：随机操作序列之后断言总和等于初始值。

```python
class Bank:
    def __init__(self, balances: dict[str, int]):
        self._bal = dict(balances)
    def transfer(self, src: str, dst: str, n: int):
        if type(n) is not int or n <= 0 or self._bal[src] < n:
            raise ValueError("bad transfer")       # 先查，后写
        self._bal[src] -= n
        self._bal[dst] += n
    def total(self) -> int:
        return sum(self._bal.values())

b = Bank({"a": 60, "b": 0})
b.transfer("a", "b", 20)
print(b.total())     # 60
```

**知识点：**不变量与封装（Invariants）
