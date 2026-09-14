---
id: cc-python-classes-default-factory
node: python.classes
type: qa
---
## Q
`@dataclass class Merchant: charges: list = []` raises `ValueError: mutable default <class 'list'> ... is not allowed` before a single test runs. Why does a dataclass forbid what a plain function permits?

## A
**Because it is the same shared-default bug, and dataclasses refuse to reproduce it.** A class-level `[]` would be evaluated once and shared by every instance.

```python
charges: list[str] = field(default_factory=list)
```

- `default_factory` is called once **per instance**, which is what you meant.
- Plain functions get no such check: `def f(x, bucket=[])` still shares silently ([[cc-python-pitfalls-mutable-default]]).
- Any mutable or unhashable default needs the factory — `{}`, `set()`, another dataclass instance. Immutable defaults (`0`, `""`, `None`, a tuple) are fine written directly.

## Q zh
`@dataclass class Merchant: charges: list = []` 还没跑一个测试就抛出 `ValueError: mutable default <class 'list'> ... is not allowed`。为什么 dataclass 禁止普通函数允许的写法？

## A zh
**因为那是同一个「共享默认值」的 bug，而 dataclass 拒绝重演它。** 类级别的 `[]` 只会被求值一次，然后被所有实例共享。

```python
charges: list[str] = field(default_factory=list)
```

- `default_factory` 是**每个实例**调用一次 —— 这才是你的本意。
- 普通函数没有这道检查：`def f(x, bucket=[])` 仍然静默共享（[[cc-python-pitfalls-mutable-default]]）。
- 任何可变或不可哈希的默认值都要用 factory —— `{}`、`set()`、另一个 dataclass 实例。不可变默认值（`0`、`""`、`None`、tuple）可以直接写。
