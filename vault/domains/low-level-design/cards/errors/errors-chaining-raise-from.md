---
id: errors-chaining-raise-from
node: errors.chaining
type: qa
step: 1
---
## Q
在 `except` 里再抛一个新异常，`raise X`、`raise X from exc`、`raise X from None` 有什么区别？各用在什么时候？

## A
**换类型时写 `from exc`，只在刻意隐藏时写 `from None`**

- **`raise X`（隐式）**：Python 自动把正在处理的异常挂在 `__context__` 上，回溯里写“处理上一个异常时又出现了另一个异常”，读起来像两个无关的错；
- **`raise X from exc`**：明确声明因果，`__cause__ = exc`，回溯里写“上面的异常是下面异常的直接原因”；
- **`raise X from None`**：切断链，回溯里看不到原异常，只在刻意不暴露内部细节时用，平时不用；
- **不要 `raise X(str(exc))` 不带 `from`**：类型和栈都丢了，只剩一句话；
- **翻译异常是边界的事**：底层的 `KeyError`、`OSError` 在公开接口那一层换成自己的异常，换的时候带上 `from`。

```python
def f(mode: str):
    try: {}["k"]
    except KeyError as exc:
        if mode == "from": raise ValueError("x") from exc
        if mode == "none": raise ValueError("x") from None
        raise ValueError("x")                           # 隐式

for m in ("from", "none", "implicit"):
    try: f(m)
    except ValueError as e:
        print(m, type(e.__cause__).__name__, type(e.__context__).__name__, e.__suppress_context__)
# from KeyError KeyError True / none NoneType KeyError True / implicit NoneType KeyError False
```

**知识点：**保留原因（Wrapping & Chaining）
