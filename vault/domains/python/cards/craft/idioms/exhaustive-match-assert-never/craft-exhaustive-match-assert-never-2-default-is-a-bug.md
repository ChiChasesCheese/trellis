---
id: craft-exhaustive-match-assert-never-2-default-is-a-bug
node: craft.idioms.exhaustive-match-assert-never
type: qa
step: 2
---
## Q
**穷尽性检查 · `case _:` 兜底成除法，为什么比没有兜底更危险**｜写法

表格引擎对二元运算 `match op:`，列了 `+`、`-`、`*`，最后 `case _:` 直接写除法。现在解析器支持了 `%`，求值时会怎样？应该怎么改？

## A
**要点。** 兜底分支把「其他所有情况」当成某一种具体情况处理，新增的运算符悄悄被当成除法，得到错误的数字却没有任何报错，比崩溃更糟。改法分两步：（1）把兜底的那一种也显式写成 `case "/"`；（2）`case _:` 只留给 `assert_never`。运算符本来是 `str`，类型检查器无从知道有哪些取值，所以要把类型收窄为 `Literal["+", "-", "*", "/"]`，穷尽性才有依据。

```python
Op = Literal["+", "-", "*", "/"]

def apply_loose(op: str, l: float, r: float) -> float:
    match op:
        case "+": return l + r
        case "-": return l - r
        case "*": return l * r
        case _:   return l / r          # 任何未知运算符都被当成除法

def apply_strict(op: Op, l: float, r: float) -> float:
    match op:
        case "+": return l + r
        case "-": return l - r
        case "*": return l * r
        case "/": return l / r          # 显式写出每一个
        case _:   assert_never(op)      # 未来新增运算符时，这里在检查期就红

print("loose : '%' 被当成除法 ->", apply_loose("%", 7, 2))
try:
    apply_strict("%", 7, 2)             # type: ignore[arg-type]
except AssertionError as e:
    print("strict : AssertionError ->", e)
```

实际输出：

```
loose : '%' 被当成除法 -> 3.5
strict : AssertionError -> Expected code to be unreachable, but got: '%'
```

给 `Op` 加上 `"%"` 却忘了写分支时，mypy 的报告：

```
calc.py: error: Argument 1 to "assert_never" has incompatible type "Literal['%']"; expected "Never"  [arg-type]
```

**为什么。** `Literal` 把「合法取值」这个事实交给了类型系统，解析器新增运算符时，所有 `match` 在检查期同时报错，不会漏。

**易错。** 兜底分支真正合理的场景是「其他情况确实都应该同样处理」（例如索引帮不上就全表扫描）。判断方法：如果新增一种情况，你希望它被自动归到兜底，就用 `case _:`；如果希望有人来决定怎么处理，就用 `assert_never`。
