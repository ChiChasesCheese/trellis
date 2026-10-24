---
id: pl-trends-convergence-pitfall-weak-guarantee
node: trends.convergence
type: qa
step: 9
---
## Q
“同名特性”在不同语言里保证强度不同，会造成什么事故？Python 的 `match` 与 Java 的密封 `switch` 对比说明什么？

## A
**陷阱**：从 Java 或 Rust 转到 Python 的人看到 `match`，以为得到了同样的“漏处理会被抓住”的保证。其实没有。

**Python**：新增一个变体，忘了处理，`match` 静默地什么都不做：

```python
match shape:
    case Circle(r=r): return 3.14 * r * r
    case Square(s=s): return s * s
# area(Tri(3))  ->  None   (no case matched, no error)
```

真实输出：`3.14 4 None`。函数返回 `None`，之后在别处引发 `TypeError: unsupported operand`，或者更糟，`None` 被当成合法值写进了数据库。

**Java**：同样的遗漏，编译失败：`error: the switch expression does not cover all possible input values`。

**修复 Python**：给 `match` 加兜底分支，并交给类型检查器：

```python
case _ as unreachable:
    assert_never(unreachable)
# mypy: Argument 1 to "assert_never" has incompatible type "Tri"
```

在没有这一行时，`mypy` 对上面的函数也能指出 `Missing return statement`（真实输出），前提是你运行了它。

**其他同类陷阱**：
- **Go 泛型**：类型参数不能用在方法上，也没有特化，`Map` 这样的函数能写，但 `slice.Map(...)` 这种链式方法不行；对期待 Java Stream 风格的人是意外。
- **Python 类型注解**：写错类型，运行时完全不受影响，只在检查器里出错。
- **Java 的 `var`**：仍是静态类型，但编译器得出的类型可能和预期不同（如 `var list = new ArrayList<>()` 得到的是 `ArrayList<Object>`）。

**教训**：学一个“看起来熟悉”的特性时，先问三个问题：它的检查发生在编译期、类型检查器，还是运行时？违规的结果是错误还是静默？我能否在 CI 里强制它？
