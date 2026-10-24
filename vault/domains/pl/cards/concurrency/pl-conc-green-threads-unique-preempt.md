---
id: pl-conc-green-threads-unique-preempt
node: concurrency.green-threads
type: qa
step: 7
---
## Q
一个死循环的 CPU 密集任务会饿死同一调度器上的其他任务吗？Go 的 goroutine 和 Java 的虚拟线程在这点上有什么区别？

## A
区别在于运行时能不能**抢占**（preempt，强行打断正在计算的任务）。

Go（把 P 限制成 1，起一个什么都不调用的死循环 goroutine）：
```go
runtime.GOMAXPROCS(1)
go func() {
    for { } // tight loop, no calls, no blocking
}()
time.Sleep(10 * time.Millisecond)
fmt.Println("main got the CPU back")
```
输出：`main got the CPU back`。Go 1.14 起有异步抢占：监控线程给运行太久的 goroutine 发信号，在安全点把它打断，所以单个 P 上也不会被死循环独占。

Java（调度器限制为一个载体线程，一个虚拟线程自旋，另一个虚拟线程等着打印）：
```java
Thread spin = Thread.ofVirtual().start(() -> { while (!flag) {} });
Thread other = Thread.ofVirtual().start(() -> System.out.println("ran"));
other.join(2000);
```
输出：`other starved for 2s`，第二个线程 2 秒后仍然没有机会运行。虚拟线程只在阻塞点（`sleep`、锁、I/O）让出载体线程，运行时不会打断纯计算。

结论：
- Go 是抢占式的，goroutine 之间公平，但要付出信号、安全点的运行时复杂度。
- Java 虚拟线程是协作式的，目标是海量 I/O 等待型任务；CPU 密集任务应放在平台线程池里，不要放虚拟线程。
