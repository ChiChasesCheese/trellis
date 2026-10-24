---
id: pl-types-gradual-typing-found-mypy-strict
node: types.gradual-typing
type: qa
step: 3
---
## Q
`mypy` 的默认模式和 `--strict` 有什么区别？`# type: ignore` 又是什么？

## A
`mypy` 默认只检查「有类型提示」的函数。没有任何标注的函数体被整个跳过，参数和返回值当作 `Any`：

```python
def add(a, b):
    return a + b
```

默认模式下 `mypy st.py` 通过。加上 `--strict` 后，它要求每个函数都有完整的标注，并打开一批更严格的检查（禁止隐式 `Any` 泛型、警告返回 `Any` 等）：

```console
st.py:1: error: Function is missing a type annotation  [no-untyped-def]
```

所以渐进采用的典型做法是：整体保持默认，对已经加好类型的模块或新模块逐个启用严格模式（`mypy` 的配置文件里可以按模块设置）。

`# type: ignore[错误代码]` 是写在某一行末尾的注释，告诉检查器「这一行的这个错误我知道，不要报」。它是一个手动的逃生口：当库缺少类型、检查器误判，或者重构还没做完时使用。应当写明错误代码和原因，并定期清理，否则它会悄悄累积，成为没有检查的盲区。

另一个相关概念是 `py.typed` 标记文件：库在包里放一个空的 `py.typed`，宣告自己带有类型提示，检查器才会使用它的标注；没有它，检查器把这个库的所有内容当作 `Any`。
