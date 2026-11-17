---
id: data-primitive-obsession-newtype
node: data.primitive-obsession
type: qa
step: 2
---
## Q
`typing.NewType("AccountId", int)` 能让 `transfer(amount, src, dst)` 这种换位置的错误暴露出来吗？它在运行时做了什么、没做什么？

## A
**NewType 只在类型检查时有用，运行时什么也不加**

- **类型检查器**：`AccountId` 与 `Cents` 是两个不同的类型，把 `Cents` 传给要 `AccountId` 的位置，mypy 和 pyright 报错；
- **运行时**：`AccountId(7)` 就是返回 `7`，它还是普通的 `int`，没有额外开销，也没有额外校验；
- **所以**：没人跑类型检查器的项目里，NewType 等于文档；换位置的错误仍然不会在运行时失败；
- **要运行时保护**：用类（下一张卡），把校验写进构造函数；
- **适合的场景**：已有大量 `int` 代码，想低成本把几类 id 分开；类型检查在 CI 里是强制的。

```python
from typing import NewType

AccountId = NewType("AccountId", int)
Cents = NewType("Cents", int)

def transfer(src: AccountId, dst: AccountId, amount: Cents) -> str:
    return f"move {amount} from {src} to {dst}"

a, b, c = AccountId(7), AccountId(9), Cents(500)
print(type(a), a == 7)                       # <class 'int'> True：运行时就是 int
print(transfer(c, a, b))                     # 类型检查器会报错，运行时照样执行
```

**知识点：**用小类型代替裸值（Primitive Obsession）
