---
id: pl-foundations-paradigms-found-java-stream
node: foundations.paradigms
type: qa
step: 2
---
## Q
Java 的 `Stream` 是什么？它是怎样把「过滤、映射、求和」写成一条惰性管道的？

## A
`Stream`（Java 8 引入）是对一串元素的「计算流水线」的描述，由三部分组成：数据源（如 `IntStream.rangeClosed(1, 4)`）、零个或多个中间操作（`filter`、`map`、`peek`，每个接受一个 lambda，即一小段匿名函数 `i -> i * i`）、一个终端操作（`sum`、`collect`、`forEach`）。

关键事实：中间操作是惰性的（lazy），只是把步骤登记下来，直到终端操作被调用，数据才开始流动，而且是一个元素一个元素地依次穿过整条管道。

```java
var pipeline = IntStream.rangeClosed(1, 4)
    .peek(i -> System.out.println("visit " + i))
    .filter(i -> i % 2 == 0)
    .map(i -> i * i);
System.out.println("built, nothing visited yet");
System.out.println("sum = " + pipeline.sum());
```

实际输出：先是 `built, nothing visited yet`，然后才是 `visit 1` 到 `visit 4`，最后 `sum = 20`。建好管道时没有任何元素被处理；调用 `sum()` 时才开始。

两个后果：一是 `Stream` 只能消费一次，终端操作之后管道作废；二是管道里的 lambda 最好是纯函数（不改外部变量），因为执行时机和顺序（尤其并行流）由库决定，不由你写的代码顺序决定。
