---
id: pl-types-soundness-foundation-python-annotations
node: types.soundness
type: qa
step: 4
---
## Q
Python 的类型注解在运行时保证什么？为什么说 mypy 通过也不等于类型可靠？

## A
Python 的类型注解是**附在函数和变量上的元数据**，解释器只把它存起来（放进 `__annotations__`），不做任何检查。真正检查类型的是外部工具，如 mypy、pyright，它们读源码做静态分析。

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("x", "y"))        # xy   (runs fine)
print(add.__annotations__)  # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

`mypy` 会对 `add("x", "y")` 报 `Argument 1 to "add" has incompatible type "str"; expected "int"`，但运行 Python 时不会拦住它。

即使 mypy 通过，也不代表可靠，主要有三个洞：

1. **没写注解的函数是 `Any`**。mypy 默认不检查未注解函数的函数体，它的返回值被当作 `Any`，而 `Any` 与所有类型相容：

```python
def untyped(x):
    return x.upper()
n: int = untyped("a")       # mypy: no error; n is actually the str "A"
```

2. **`cast` 和 `# type: ignore`** 是对检查器说「相信我」，检查器照办。
3. **边界处的数据**：`json.loads`、数据库查询、第三方库没有类型标注，返回值是 `Any`。

Python 的立场是「渐进类型」：类型是工具，不是语言保证。好处是可以逐步给大型旧代码库加类型，不改变运行行为，零运行时成本；代价是类型信息只有被检查器看到的那部分才可信。

要在运行时强制，需要额外的库：pydantic、beartype、typeguard，它们在入口处按注解校验数据。

结论：Python 的类型注解在最强的配置（`mypy --strict`）下也只是**静态分析的输入**，不是运行时的不变量。
