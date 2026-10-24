---
id: pl-dyncheck-found-jcstress
node: engineering.dynamic-checkers
type: qa
step: 5
---
## Q
Java 为什么需要 jcstress 这样的并发压力测试？它怎样发现 Java 内存模型层面的问题？

## A
Java 是内存安全的，没有 ASan 要抓的那类错误；它的并发问题发生在**内存模型**层面：没有同步的情况下，一个线程的写入，另一个线程可能晚看到、乱序看到。这种问题既不会崩溃，也不会在每次运行中出现，普通测试几乎抓不到。

**jcstress**（Java Concurrency Stress tests，OpenJDK 项目）的做法：把一小段并发代码拆成几个「actor」，让它们在海量次数、各种线程调度和 JIT 编译状态下反复同时运行，**统计每种结果出现了多少次**，并和你声明的「可接受」「不可接受」结果比对。

**例**：写线程先写 `data = 1`，再写 `flag = 1`（都是普通字段，没有 `volatile`）；读线程先读 `flag` 再读 `data`。结果记作 `r1, r2`：

```java
@Actor public void writer() { data = 1; flag = 1; }
@Actor public void reader(II_Result r) { r.r1 = flag; r.r2 = data; }
```

直觉上，既然 `flag` 在 `data` 之后写，看到 `flag == 1` 就一定能看到 `data == 1`。jcstress 在本机（Apple 芯片）一次快速运行的统计：

```text
RESULT      SAMPLES     FREQ       EXPECT
  0, 0  487,448,510   44.32%   Acceptable
  0, 1      415,384    0.04%   Acceptable
  1, 0      136,257    0.01%  Interesting
  1, 1  611,737,203   55.63%   Acceptable
```

结果 `1, 0` 出现了 13.6 万次：读线程看到了 `flag` 的新值，`data` 却还是旧值。这是编译器或 CPU 重排序造成的，只出现在万分之一的执行里，手写测试跑一千次永远看不到。给 `flag` 加上 `volatile`，这一行就会消失。

**用途**：验证自己写的无锁结构和发布模式是否真的满足内存模型，或者弄清某个并发原语到底保证了什么。
