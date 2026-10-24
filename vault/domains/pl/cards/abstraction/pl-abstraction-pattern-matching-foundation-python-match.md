---
id: pl-abstraction-pattern-matching-foundation-python-match
node: abstraction.pattern-matching
type: qa
step: 4
---
## Q
Python 3.10 的结构化模式匹配（`match` / `case`）能匹配哪些形状？它和 Rust 的 `match` 最大的区别是什么？

## A
`match` 语句对一个值依次尝试每个 `case`，第一个成功的执行。支持的模式有：字面量、序列（`[a, b]`、`(a, *rest)`）、映射（`{"k": v}`）、类（`Point(x, 0)`）、`|` 组合，以及 `if` 守卫。

```python
@dataclass
class Point: x: int; y: int
def where(p):
    match p:
        case Point(x=0, y=0): return "origin"
        case Point(x, 0): return f"x-axis {x}"
        case Point(x, y) if x == y: return "diagonal"
        case (a, b): return f"pair {a},{b}"
        case _: return "other"
```

`where(Point(3, 0))` 得 `x-axis 3`，`where((1, 2))` 得 `pair 1,2`，`where(7)` 得 `other`。类模式按位置匹配时，依赖类的 `__match_args__`（`dataclass` 自动生成）。

与 Rust 的区别：

- **没有穷尽检查**。Python 的 `match` 是语句，漏了情形就什么都不做（返回 `None`），不会报错；静态检查器（`mypy`、`pyright`）可以对联合类型和 `Enum` 做穷尽性检查，但需要你自己写 `assert_never`。
- **它是语句不是表达式**，不产生值。
- 它在**运行期动态**判断结构，没有封闭类型保证，所以可以匹配任何对象。

这符合 Python 的取向：匹配是对数据形状的运行期解构，不是类型系统的一部分。
