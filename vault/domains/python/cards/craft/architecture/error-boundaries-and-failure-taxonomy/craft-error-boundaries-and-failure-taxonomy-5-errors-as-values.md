---
id: craft-error-boundaries-and-failure-taxonomy-5-errors-as-values
node: craft.architecture.error-boundaries-and-failure-taxonomy
type: qa
step: 5
---
## Q
**错误边界与失败分类 · 表格里一个格子出错，为什么把错误当值存进缓存**｜架构

电子表格里 `A1 = 1/0`，`B1 = A1 + 1`，`C1 = B1 + 1`。按依赖顺序重算时，A1 求值抛了异常。如果让异常直接冲出重算循环，其他格子会处于什么状态？把错误存成值，又带来什么好处？

## A
**要点。** 重算是一批格子的更新，异常冲出循环会让这批更新停在半路：有的格子是新值，有的还是旧值。把错误存进缓存，当成这个格子的值：下游读到它时重新抛出，也一样被存成错误；每个格子都有一个确定的状态，要么是数字，要么是 `EvalError`。源头修好后，错误会随重算自然消失，不需要特别清除。

```python
class EvalError(Exception): ...

def div(a: float, b: float) -> float:
    if b == 0:
        raise EvalError("#DIV/0!")
    return a / b

formulas = {"A1": lambda r: div(1, 0), "B1": lambda r: r("A1") + 1, "C1": lambda r: r("B1") + 1}
val: dict[str, float | EvalError] = {}

def read(c: str) -> float:
    v = val[c]
    if isinstance(v, EvalError):
        raise v                          # 读到出错的格子：原样重新抛
    return v

def recompute(c: str) -> None:
    try:
        val[c] = formulas[c](read)
    except EvalError as err:
        val[c] = err                     # 错误当值存进缓存，不冲出重算循环

def show() -> dict:
    return {c: (str(v) if isinstance(v, EvalError) else v) for c, v in val.items()}

for c in ("A1", "B1", "C1"):                 # 按依赖顺序
    recompute(c)
print(show())
formulas["A1"] = lambda r: 4.0               # 修好源头，下游重算
for c in ("A1", "B1", "C1"):
    recompute(c)
print(show())
```

三个格子都依赖前一个；先重算一遍，再把 `A1` 改成 `4.0`，实际输出：

```
{'A1': '#DIV/0!', 'B1': '#DIV/0!', 'C1': '#DIV/0!'}
{'A1': 4.0, 'B1': 5.0, 'C1': 6.0}
```

**为什么。** 只捕获 `EvalError`（这个领域自己的、预期内的错误），不捕获 `Exception`：求值里的真 bug（比如拼写错误引发的 `NameError`）应该照常崩出来，不要被存成一个看似正常的错误格子。

**易错。** 错误值也要有出口：用户看到的是 `#DIV/0!`，而不是 Python 的堆栈；重新抛时要抛同一个错误对象，保留最初是哪个格子、什么原因。
