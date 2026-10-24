---
nodes: [trends.convergence, trends.expression-orientation, trends.safety-push, types.algebraic-data-types]
tags: [drill]
---
# 练习：给枚举加一个新变体，谁会告诉你漏改了地方

形状计算库原本有 `Circle` 和 `Square` 两种形状，`area` 函数用模式匹配分别处理。现在产品要加第三种 `Tri`（三角形），你只改了定义，忘了改 `area`。四门语言的实现里，有的在编译时就拒绝，有的上线后才返回错误结果。你要预测每种语言的结果，并解释为什么「加类型匹配、加表达式化」的趋势没有给四门语言带来同样强的保证。

```java
sealed interface S permits Circle, Square, Tri {}
double area(S s) { return switch (s) { case Circle c -> ...; case Square q -> ...; }; }
```

```rust
enum Shape { Circle(f64), Square(f64), Tri(f64, f64) }
fn area(s: &Shape) -> f64 { match s { Shape::Circle(r) => ..., Shape::Square(a) => ... } }
```

```python
Shape = Circle | Square | Tri
def area(s: Shape) -> float:
    match s:
        case Circle(r): ...
        case Square(side): ...
print(area(Tri(3, 4)))
```

```go
type Shape interface{ isShape() }       // Circle、Square、Tri 都实现
func area(s Shape) float64 {
    switch v := s.(type) { case Circle: ...; case Square: ... }
    return 0
}
```

**要你给出的**
- 四段代码各自在什么阶段、以什么形式暴露「漏了 `Tri`」（或者根本不暴露），Go 版本调用 `area(Tri{3, 4})` 的返回值。
- Python 版本在 `case _` 分支里调用 `typing.assert_never` 后的行为，以及 `mypy --strict` 会报什么。
- 为什么「模式匹配」在四门语言里都出现了，保证却不同；Go 用什么办法补救。
- 一条团队规则：新增变体时怎样保证所有分支都被检查到。

**评分要点**
- Java：编译错误 `the switch expression does not cover all possible input values`。`sealed` 接口让编译器知道所有允许的子类型，`switch` 表达式必须穷尽 ([[pl-types-algebraic-data-types-found-java-sealed-record]], [[pl-abstraction-pattern-matching-foundation-java-switch-patterns]])。
- Rust：编译错误 `non-exhaustive patterns: &Shape::Tri(_, _) not covered`。`enum` 是封闭的和类型，`match` 必须穷尽，编译器逐个指出漏掉的变体 ([[pl-types-algebraic-data-types-found-rust-enum-data]], [[pl-abstraction-pattern-matching-foundation-rust-match]])。
- Python：`area(Tri(3, 4))` 打印 `None`，没有任何错误，因为 `match` 没有匹配分支时静默通过；加上 `case _ as unreachable: assert_never(unreachable)` 后，运行时抛 `AssertionError: Expected code to be unreachable, but got: Tri(b=3, h=4)`，而 `mypy --strict` 在运行前就报告 `Argument 1 to "assert_never" has incompatible type "Tri"; expected "Never"`（没有 `assert_never` 时报 `Missing return statement`）。穷尽性靠类型检查器而不是解释器 ([[pl-abstraction-pattern-matching-foundation-python-match]], [[pl-types-algebraic-data-types-found-python-dataclass-match]], [[pl-types-gradual-typing-found-mypy-strict]])。
- Go：`area(Tri{3, 4})` 返回 `0`，编译通过，`go vet` 也不抱怨。接口是开放的，任何类型都可以实现，类型开关没有「全部情形」的概念，所以语言无法检查穷尽。补救办法是在 `default` 分支里 `panic`，并用第三方的穷尽性检查工具；这是 Go 保持简单的取舍 ([[pl-types-algebraic-data-types-unique-go-open]], [[pl-abstraction-pattern-matching-foundation-go-type-switch]])。
- 趋势：四门语言都在向「用类型表达可能的情形，并让编译器检查是否处理完」靠拢，Java 有 `sealed` 加 `switch` 模式，Python 加了 `match` 和类型注解，Go 加了泛型和迭代器却保持类型开关不变。趋同的是语法和概念，保证强度取决于该语言的类型系统是封闭还是开放、检查在编译期还是外挂 ([[pl-trends-convergence-mechanism]], [[pl-trends-convergence-pitfall-weak-guarantee]])。
- 表达式化：`switch` 与 `match` 都是表达式，必须产生一个值，因此「漏掉一个分支」直接变成类型错误（没有值可返回）；而 Go 的类型开关是语句，漏掉分支后落到函数末尾的 `return 0` ([[pl-trends-expr-mechanism]], [[pl-trends-expr-pitfall-semicolon-fallthrough]])。
- 与内存安全运动同一思路：把一整类错误从「运行期偶发」变成「编译期必然」。规则：用封闭的和类型表示固定集合，不要在 `match` 里写万能分支 `_` 或 `default` 去吞掉新变体（它会让穷尽检查失效），Go 的类型开关加 `default: panic` 并在 CI 里启用穷尽检查 ([[pl-types-algebraic-data-types-pitfall-wildcard]], [[pl-trends-safety-principle]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
