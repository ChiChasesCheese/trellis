---
id: pl-types-null-safety-found-python-none
node: types.null-safety
type: qa
step: 5
---
## Q
Python 的 `None` 是什么？哪些情形会隐式得到 `None`？

## A
`None` 是 Python 内置的一个单例对象，类型是 `NoneType`，用来表示「没有值」。因为全程只有一个 `None` 对象，判断用身份比较 `x is None`（不用 `==`）。任何变量都可以指向 `None`；对它调用不存在的方法，会抛出 `AttributeError`。

隐式得到 `None` 的常见情形：字典 `get` 找不到键、函数没有 `return` 语句（或只写 `return`）、会就地修改的方法（`list.sort()`、`list.append()`）。

```python
d = {"a": "x"}
v = d.get("b")
print(v, v is None, type(v).__name__)   # None True NoneType
def f(): pass
print(f() is None)                      # True
```

实际输出 `None True NoneType` 和 `True`。

最典型的 bug：`d.get("b").upper()` 抛出 `AttributeError: 'NoneType' object has no attribute 'upper'`。类型提示里用 `str | None` 表示可选，`mypy` 会强制你先检查。

与 Java 的 `null` 不同的是 `None` 是真正的对象，能放进列表、当字典的值，也能调用少数方法；与 Rust 的 `Option` 不同的是，它不在类型里区分，除非你自己加类型提示并用检查器。
