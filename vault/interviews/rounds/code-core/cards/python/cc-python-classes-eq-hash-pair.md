---
id: cc-python-classes-eq-hash-pair
node: python.classes
type: cloze
---
Defining `__eq__` on a class silently sets `__hash__` to {{c1::None}}, so instances become unhashable — no `set`, no dict key, no `Counter`. Restore it deliberately with `__hash__ = object.__hash__` (identity) or by hashing the same fields `__eq__` compares; `@dataclass({{c2::frozen=True}})` does it for you. Two objects that compare equal must hash equal, or dict lookups silently miss.

## zh
在类上定义 `__eq__` 会静默地把 `__hash__` 置为 {{c1::None}}，于是实例变得不可哈希 —— 进不了 `set`、当不了 dict 的键、用不了 `Counter`。要有意识地恢复它：用 `__hash__ = object.__hash__`（按同一性），或对 `__eq__` 比较的同一批字段做哈希；`@dataclass({{c2::frozen=True}})` 会替你做好。相等的两个对象必须哈希相等，否则字典查找会悄悄查不到。
