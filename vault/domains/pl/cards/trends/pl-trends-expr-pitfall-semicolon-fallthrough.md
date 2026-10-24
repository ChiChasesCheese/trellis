---
id: pl-trends-expr-pitfall-semicolon-fallthrough
node: trends.expression-orientation
type: qa
step: 10
---
## Q
表达式化与语句化的边界在生产里产生哪些典型错误？Rust 的末尾分号和 Java 的 `switch` 穿透各是什么样子？

## A
**Rust：多写了一个分号**。分号把表达式变成语句，值被丢弃，块的值变成 `()`：

```rust
fn double(n: i32) -> i32 {
    n * 2;
}
```

真实报错：

```
error[E0308]: mismatched types
  expected `i32`, found `()`
  implicitly returns `()` as its body has no tail or `return` expression
  help: remove this semicolon to return this value
```

这是新手最常遇到的错误，好在是编译错误并且带修复建议，不会进入生产。

**Java：`switch` 语句的穿透**。老式 `switch` 语句忘写 `break`，编译通过、运行时悄悄多执行一个分支：

```java
case 1: r += "one";       // no break
case 2: r += "two"; break;
// old(1) -> "onetwo",  arrow-form switch expression nu(1) -> "one"
```

真实输出：旧式得到 `onetwo`，箭头式表达式得到 `one`。这类 bug 在代码评审里极难看出来，是 C 家族长期的老问题。改用箭头式 `switch` 即可根除。

**Python：条件表达式的优先级**。

`print("x=" + "a" if x else "b")` 在 `x == 0` 时真实输出是 `b`，而不是 `x=b`：整个 `"x=" + "a"` 被当作条件为真时的值，条件为假时前缀也一起消失。

**Go：漏掉 else**。语句导向没有“所有分支都给值”的检查：`var y int; if x > 2 { y = 1 }`，漏了 else 时 `y` 悄悄是 0，不报错。

**共同的主题**：语句与表达式的边界，是让“我以为产生了值”和“实际产生了值”不一致的地方。

**防线**：优先用能让编译器检查的形式（Rust 的表达式、Java 的 `switch` 表达式）；Python 和 Go 用 linter（`go vet`、`ruff`）加测试覆盖每个分支；评审时凡是出现“声明变量，再分支赋值”的写法，问一句漏分支会怎样。
