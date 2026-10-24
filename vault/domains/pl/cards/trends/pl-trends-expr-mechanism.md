---
id: pl-trends-expr-mechanism
node: trends.expression-orientation
type: qa
step: 6
---
## Q
表达式导向在编译器层面带来什么？类型检查、初始化分析和“所有分支都有值”是怎样被机械检查的？

## A
**语句导向下的问题：definite assignment（明确赋值）分析**。以 Go 为例：

```go
var y int          // zero value, always initialized
if x > 2 { y = 1 } // forgot the else: y stays 0, no error
```

Go 用“零值”保证变量总是初始化，所以漏掉分支不会报错，`y` 悄悄是 0。Java 没有零值默认的局部变量，用“明确赋值”分析：局部变量在使用前必须在所有路径上赋过值，漏分支会编译报错 `variable might not have been initialized`。Python 则是运行时才发现（`UnboundLocalError`）。

**表达式导向下的检查更简单**：`let s = if c { A } else { B }` 的类型检查是两条规则：
1. `if` 必须有 `else`（否则它的类型是 `()`），
2. `A` 与 `B` 的类型必须一致（真实报错 `if and else have incompatible types`）。

没有“中间状态变量”需要分析，不需要流敏感的赋值检查。

**块的值与尾部分号**（Rust）：编译器区分“最后一个表达式”（块的值）和“语句”（值被丢弃，块类型是 `()`）。这引出了一个常见错误，见下面的陷阱。

**穷尽性**：`match`（Rust）和 `switch` 表达式（Java）作为表达式必须**对所有可能值产生一个值**，编译器据此做穷尽性检查；作为语句的 `switch`（C、Java 旧式、Go）没有这个义务，所以“没匹配上就什么都不做”是合法的。

**生成的代码**：表达式和语句在机器码层面没有区别，编译器都转换成同样的基本块和跳转。表达式导向不是性能特性，而是**让错误在更早的阶段、用更简单的规则被发现**。

**结论**：表达式导向把“每条路径都有值”这个性质从流分析变成了类型检查，成本更低、规则更少。
