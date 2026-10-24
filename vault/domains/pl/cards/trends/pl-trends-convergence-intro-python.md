---
id: pl-trends-convergence-intro-python
node: trends.convergence
type: qa
step: 4
---
## Q
Python 加入的类型注解（type hints）、`dataclass`、`match` 语句和海象运算符分别是什么？一个例子里它们怎样配合，又留下什么缺口？

## A
- **类型注解**（3.5 起，PEP 484）：在函数参数、返回值、变量上写类型，如 `def f(x: int) -> str`。**解释器不检查它们**，由 `mypy`、`pyright` 等外部工具检查。3.9 起可以直接写 `list[int]`，3.10 起联合类型可以写 `int | str`。
- **`dataclass`**（3.7）：装饰器，根据带类型注解的字段自动生成 `__init__`、`__repr__`、`__eq__`，对应 Java 的 `record`。
- **`match` 语句**（3.10）：结构化模式匹配，可以按类型和字段解构。
- **海象运算符** `:=`（3.8）：在表达式里赋值，如 `if (n := len(s)) > 3: print(n)`。

```python
@dataclass
class Circle: r: float
@dataclass
class Square: s: float
@dataclass
class Tri: b: float
def area(shape: Circle | Square | Tri) -> float:
    match shape:
        case Circle(r=r): return 3.14 * r * r
        case Square(s=s): return s * s
```

**缺口**：运行 `area(Tri(3))`，真实结果是 `None`：没有任何分支匹配，`match` 默默什么都不做，函数落到末尾返回 `None`，没有异常。Python 的 `match` **不做穷尽性检查**。用类型检查器 `mypy` 检查，会报 `error: Missing return statement`，等于把穷尽性检查外包给了工具。

**要记住的一点**：Python 的收敛方式是“语法进入语言，检查留给工具”。语言本身仍然是动态的，类型信息是可选的元数据。
