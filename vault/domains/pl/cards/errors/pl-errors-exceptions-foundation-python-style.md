---
id: pl-errors-exceptions-foundation-python-style
node: errors.exceptions
type: qa
step: 3
---
## Q
Python 的 `try/except/else/finally` 各自何时执行？EAFP 风格是什么意思？

## A
Python 的完整形式有四个部分：

```python
try:
    v = d["b"]               # code that may raise
except KeyError:             # runs only if KeyError was raised
    v = 0
else:
    print("no exception")    # runs only if the try block raised nothing
finally:
    print("always")          # runs in every case, even on return or error
```

- `except 类型`：抛出的异常匹配这个类型时执行；可以写多个，按顺序匹配；不写类型的 `except:` 会捕获一切，包括 `KeyboardInterrupt`，不要用。
- `else`：`try` 块**没有**抛异常时执行。把“不该被 `except` 保护的后续代码”放这里。
- `finally`：无论如何都执行，用于清理。

**EAFP**（Easier to Ask Forgiveness than Permission，请求原谅比请求许可更容易）是 Python 的惯用风格：不先检查再做（LBYL，Look Before You Leap），而是直接做，失败了再处理。例如读字典里的键，直接 `d["b"]` 再 `except KeyError`，而不是先 `if "b" in d`。理由：检查和使用之间状态可能变化（文件在检查后被删），而且 CPython 3.11 起不抛异常时 `try` 不花任何成本。

另外，`raise NewError("...") from e` 会把原异常记在 `__cause__` 里，栈追踪里显示两段，称为异常链。

要记住的一个事实：Python 把异常当作日常控制手段，`StopIteration` 这样的信号都是用异常实现的。
