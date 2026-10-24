---
id: pl-trends-expr-intro-go
node: trends.expression-orientation
type: qa
step: 5
---
## Q
Go 为什么坚持语句导向：没有三元运算符，`if` 和 `switch` 不是表达式？带初始化语句的 `if` 又是什么？

## A
**事实**：Go 的 `if`、`switch`、`for` 都是语句，不产生值。语言故意**没有**三元运算符 `cond ? a : b`，写它会得到语法错误（真实输出：`invalid character U+003F '?'`）。想“根据条件取值”只能写：

```go
var y int
if x > 2 { y = 1 } else { y = 0 }
```

**带初始化语句的 `if`**：Go 允许在条件前放一个简短语句，其变量只在这个 `if`/`else` 的作用域内：

```go
if v, err := strconv.Atoi(s); err == nil && v > 0 { use(v) }
```

这是 Go 在不引入表达式化的前提下，缩小变量作用域的方式，也让错误检查的惯用写法 `if err := f(); err != nil` 非常紧凑。

**`switch`** 没有穿透（默认每个 `case` 自动 `break`，要穿透显式写 `fallthrough`），`case` 可以是任意表达式，`switch` 没有表达式时相当于 `if-else` 链。

**Go 团队的理由**：他们观察到三元运算符常被用来写出难以阅读的嵌套表达式。语言宁可让简单的情形多写两行，也要让每一行都容易读懂。另一个理由是语法简单：规范里“语句”和“表达式”分得清清楚楚，工具和读者都更容易。

**要记住的一点**：Go 的选择不是“没做到”，而是“故意不做”，换来的是代码形状高度统一。
