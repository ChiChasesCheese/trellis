---
id: oop-equals-hashcode-contract
node: oop.values
type: qa
step: 3
---
## Q
```python
@dataclass
class Money:
    amount: int
    currency: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Money) and (self.amount, self.currency) == (other.amount, other.currency)
```
`{Money(5, "USD")}` 这个集合字面量会直接抛出 `TypeError`。解释原因，说出被破坏的是哪条契约。

## A
Python 的规则很直接：一个类只要自己定义了 `__eq__` 而没有定义 `__hash__`，解释器会把这个类的 `__hash__` 自动设成 `None`——它的实例就变得**不可哈希**，放进 `set` 或当 `dict` 的 key 会直接抛 `TypeError`。

如果显式提供 `__hash__`，契约是：**相等的对象必须有相等的哈希值**（`x == y ⇒ hash(x) == hash(y)`），反过来不要求——哈希碰撞是允许的，只是查找变慢。而且只有构造之后不再变化的字段才能参与哈希，否则对象放进 `set` 之后一旦被修改，就会永远待在错误的桶里，再也查不到。

最省心的做法：`@dataclass(frozen=True)` 会按字段自动生成互相一致的 `__eq__` 和 `__hash__`，不需要手写。
