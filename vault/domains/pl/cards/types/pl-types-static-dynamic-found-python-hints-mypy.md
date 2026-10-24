---
id: pl-types-static-dynamic-found-python-hints-mypy
node: types.static-dynamic
type: qa
step: 4
---
## Q
Python 的类型提示（type hints）是什么？`mypy` 这样的类型检查器在流程里处于什么位置？

## A
类型提示是写在函数参数、返回值和变量后面的可选标注，如 `prices: list[float]`、`-> float`。Python 解释器读到它们，只是把它们存起来，运行时不会据此检查或拒绝任何调用。

真正使用它们的是类型检查器（type checker），如 `mypy`、`pyright`：它们是独立的命令行工具，不运行你的程序，而是读源码，按提示推导每个表达式的类型，报告不一致。它们通常在编辑器和 CI 里运行。

```python
def total(prices: list[float]) -> float:
    return sum(prices)

print(total([1.5, 2.5]))   # 4.0
print(total("oops"))
```

直接 `python th.py`：第一行输出 `4.0`，第二行在运行时才抛出 `TypeError: unsupported operand type(s) for +: 'int' and 'str'`。

对同一个文件运行 `mypy th.py`，程序不会被执行，而是得到：

```console
th.py:5: error: Argument 1 to "total" has incompatible type "str"; expected "list[float]"
```

两个事实支撑后面所有讨论：一，提示是给工具和人看的，运行时不强制；二，没有被检查器运行过的提示等于注释，随时可能和代码不一致。所以在 Python 里「静态类型」是一个可选的、由外部工具提供的层。
