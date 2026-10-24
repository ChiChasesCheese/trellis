---
id: pl-memory-escape-analysis-mechanism
node: memory.escape-analysis
type: qa
step: 4
---
## Q
编译器具体根据什么判断对象逃逸？栈分配和 Java 的标量替换（scalar replacement）各是怎么实现的？

## A
编译器对每个新分配的对象，沿着它的引用在数据流图中追踪它流向哪里。出现下列任一情形，就判定为逃逸：
1. 被 `return` 返回（或作为返回值的一部分）。
2. 被存入堆对象的字段、全局变量、静态变量。
3. 被传给无法看到函数体的调用（接口方法、函数值、未内联的外部函数）。
4. 被闭包捕获，而该闭包本身逃逸；被 goroutine 或另一个线程使用。
5. 大小在编译期未知或过大（Go 里超过一定上限的 `make` 直接放堆）。

**Go**：在编译期（AOT）完成，结果就是机器码里的分配位置。不逃逸的值直接占用栈帧，分配成本等于零。可以用 `go build -gcflags=-m` 看到每个决策。

**Java**：在 JIT 阶段进行，只对已经热起来、被 C2 编译的方法做。除了放栈，HotSpot 更常用的是**标量替换**：如果对象不逃逸，就把它拆开，字段变成独立的局部变量，直接放寄存器，对象本身从未被创建。

```java
record Point(int x, int y) {}
static int sum(int i) { Point p = new Point(i, i + 1); return p.x() + p.y(); }
```

内联之后 `sum` 等价于 `return i + (i + 1)`，对象 `p` 消失了，没有分配，也没有对象头。这个优化依赖内联：如果方法太大没有被内联，调用另一个方法的参数就算逃逸，替换就失败。所以 Java 的逃逸分析是尽力而为，不是保证。
