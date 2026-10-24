---
id: pl-functional-immutability-foundation-python-frozen
node: functional.immutability
type: qa
step: 5
---
## Q
Python 里哪些类型本身不可变？`frozen=True` 的 dataclass 保护到什么程度？

## A
内置的不可变类型：`int`、`float`、`str`、`bytes`、`tuple`、`frozenset`。不可变意味着可以哈希，可以做字典键，可以被安全共享。可变类型：`list`、`dict`、`set`、普通对象。

`tuple` 的不可变是**浅**的：它固定的是每个位置**指向哪个对象**，不是对象的内容。

```python
t = ([1],)
t[0].append(2)      # t 变成 ([1, 2],)
hash(t)             # TypeError: unhashable type: 'list'
```

`@dataclass(frozen=True)` 禁止给字段赋新值（抛 `FrozenInstanceError`）并生成 `__hash__`，同样只是浅的：

```python
@dataclass(frozen=True)
class Cfg:
    tags: list
c = Cfg(["a"])
c.tags.append("b")      # 允许，c 现在是 Cfg(tags=['a', 'b'])
c.tags = []             # FrozenInstanceError
hash(c)                 # TypeError: unhashable type: 'list'
```

这里 `frozen` 允许了列表被修改，`hash(c)` 还失败，因为哈希需要递归哈希所有字段。所以：要真正不可变的值对象，字段也应该用不可变类型（`tuple`、`frozenset`、`frozen` 的子对象）。

Python 不强制不可变，是因为它信任开发者；不可变对象是一种**约定的实现**，由类型选择（`tuple` 取代 `list`）和 `frozen` 共同构成。
