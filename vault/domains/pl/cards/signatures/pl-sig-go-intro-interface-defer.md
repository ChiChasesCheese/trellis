---
id: pl-sig-go-intro-interface-defer
node: signatures.go
type: qa
step: 3
---
## Q
Go 的隐式接口（implicit interface）和 `defer` 是什么？它们各自解决什么问题，一个例子里行为是什么样？

## A
**隐式接口**：Go 的接口只描述一组方法。**任何类型只要有这些方法，就自动满足接口**，不需要声明 `implements`。

```go
type Speaker interface{ Speak() string }
type Dog struct{}
func (Dog) Speak() string { return "woof" }   // no "implements Speaker"
var s Speaker = Dog{}                          // compiles
```

真实输出 `woof`。好处：
1. **接口定义在使用方**。消费者说“我需要能 `Read` 的东西”，标准库、第三方、你自己的类型都自动满足，无需修改它们的代码，没有循环依赖。
2. **小接口**：Go 惯例是接口只有一两个方法（`io.Reader`、`error`），组合起来使用。

这与 Java 的名义类型（必须显式声明实现）相对：Go 是结构化类型，鸭子类型的静态版本。

**`defer`**：延迟执行一个函数调用，直到外层函数返回时才执行，不论是正常返回还是 panic。多个 `defer` 按**后进先出**顺序执行。

```go
defer cleanup("first")
defer cleanup("second")
// at function exit prints: cleanup second, then cleanup first
```

真实输出顺序：`cleanup second`、`cleanup first`。典型用法：打开文件后立刻写 `defer f.Close()`，释放锁 `defer mu.Unlock()`。它把“获取”和“释放”放在相邻两行，不论函数有多少个返回路径都不会漏。这是 Go 对资源管理的答案，不是 RAII 的自动，也不是 `try/finally` 的块嵌套。

**要记住的一点**：这两个特性都体现 Go 的口味：用最小的机制，把常见模式做得顺手，并且让代码读起来平铺直叙。
