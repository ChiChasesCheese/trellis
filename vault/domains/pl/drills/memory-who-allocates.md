---
nodes: [memory.escape-analysis, memory.stack-heap, memory.value-reference-semantics]
tags: [drill]
---
# 练习：这段代码在堆上分配了多少次

一个 Go 服务的火焰图里，`runtime.newobject` 和 GC 占了 20% 的 CPU。同事提议「把所有小结构体改成返回指针，这样省复制」，另一位提议「全部改成值传递，这样不分配」。你要先预测，再说明依据，最后给出不靠猜测的优化流程，并和 Java、Rust、Python 的做法对比。

```go
type P struct{ X, Y int }
func byValue() int      { p := P{1, 2}; return p.X + p.Y }
func localPtr() int     { p := &P{1, 2}; return p.X + p.Y }
func returnPtr() *P     { return &P{1, 2} }
func toInterface(n int) { sink = P{n, 2} }          // sink 是包级 any 变量
func closure() func() int { n := 0; return func() int { n++; return n } }
func smallSlice() int   { b := make([]byte, 64); return len(b) }
func bigSlice() int     { b := make([]byte, 1<<20); return len(b) }
```

Java 里有一个 20,000,000 次的循环，每轮 `new P(i, i+1)`（只有两个 `int` 字段的 `record`），一种写法只在循环体内读取它，另一种写法还把它存进静态字段。

**要你给出的**
- 七个 Go 函数每次调用的堆分配次数（`testing.AllocsPerRun` 的结果），以及用哪个编译选项能直接看到编译器的判断。
- Java 两种写法分别分配多少内存的量级，以及关掉逃逸分析（`-XX:-DoEscapeAnalysis`）后会怎样。
- 一份优化流程：先测什么、改什么、怎样证明改对了；以及对「全改成指针」这个提议的回应。
- Rust 与 Python 在这件事上和 Go、Java 的根本区别。

**评分要点**
- 七个函数依次是 `0, 0, 1, 1, 2, 0, 1`：值和只在函数内使用的指针留在栈上；返回指针必然逃逸；非常量值装进接口要分配；闭包捕获的变量 `n` 和闭包对象各分配一次；64 字节的切片在栈上，1 MiB 的大切片放堆 ([[pl-memory-escape-analysis-foundation-go]], [[pl-memory-escape-analysis-mechanism]])。
- 查看判断的方法是编译选项 `-gcflags=-m`，会逐行报告 `does not escape`、`escapes to heap`、`moved to heap: n`。分配次数再用 `testing.AllocsPerRun` 或基准测试的 `-benchmem` 核对，不能只凭读代码 ([[pl-memory-escape-analysis-foundation-go]], [[pl-memory-escape-analysis-best-practice]])。
- 「全改成指针更省」多半是错的：指针让对象更容易逃逸，把原本在栈上的值推到堆上；返回小结构体的值通常更便宜。反过来「全改成值」也不对，大结构体复制有成本，该看数据而不是看口号 ([[pl-memory-escape-analysis-pitfall-assumptions]], [[pl-memory-value-reference-semantics-table]])。
- Java 的循环：只在循环内使用的写法，JIT 的标量替换让这个对象根本不创建，线程分配量约为 0 MB；存入静态字段后每轮都分配，约 457 MB（每个对象约 24 字节）；关掉逃逸分析后两种写法都约 457 MB ([[pl-memory-escape-analysis-foundation-java-jit]], [[pl-memory-escape-analysis-table]])。
- 设计哲学对比：Go 把逃逸分析做在编译期，结果可以用编译选项看到、用代码结构控制，所以「减少逃逸」成了日常优化手段；Java 在运行时靠 JIT 决定，结果取决于热点和内联，难以从源码预测，需要用分配量验证 ([[pl-memory-escape-analysis-go-visible]], [[pl-memory-escape-analysis-principle]])。
- Rust 没有这个问题：值默认在栈上，上堆必须显式写 `Box`、`Vec`、`Rc`，分配点在源码里可见；Python 的对象全部在堆上，没有逃逸分析，优化手段是减少对象数量（`__slots__`、数组、批量处理）而不是改变放置位置 ([[pl-memory-stack-heap-best-practice]], [[pl-memory-value-reference-semantics-rust-move]])。
- 流程：先用性能剖析确认分配确实是热点，再用 `-gcflags=-m` 找出逃逸点，每次只改一处，用 `AllocsPerRun` 或 `-benchmem` 证明分配次数下降，最后确认总体延迟也改善 ([[pl-memory-escape-analysis-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
