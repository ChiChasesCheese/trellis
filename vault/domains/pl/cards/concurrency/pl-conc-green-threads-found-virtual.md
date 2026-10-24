---
id: pl-conc-green-threads-found-virtual
node: concurrency.green-threads
type: qa
step: 4
---
## Q
Java 21 的虚拟线程（virtual thread）是什么？它和平台线程、线程池有什么关系，怎么创建，什么情况下它才有意义？

## A
**平台线程**（platform thread）是传统的 `Thread`：一对一对应一个 OS 线程，重（栈约 1–2 MB 虚拟地址）、数量有限。

**虚拟线程**是 JVM 自己调度的轻量线程：它仍然是 `java.lang.Thread` 的对象，API 完全一样（`start`、`join`、`sleep`、`ThreadLocal`），但**不绑定固定的 OS 线程**。JVM 把大量虚拟线程复用到少量**载体线程**（carrier thread，一个小的 ForkJoin 线程池，默认约等于核数）上执行。虚拟线程的栈保存在堆里，按需增长。

关键行为：虚拟线程遇到**阻塞操作**（`Thread.sleep`、阻塞的 I/O、`BlockingQueue.take`、等锁）时，JVM 把它的栈从载体线程上**卸载**（unmount），载体线程转去跑别的虚拟线程；等待结束后再**挂载**回某个载体线程继续。

创建方式：
```java
Thread v = Thread.ofVirtual().name("v1").start(() ->
    System.out.println("virtual=" + Thread.currentThread().isVirtual()));
v.join();
try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
    var f = ex.submit(() -> { Thread.sleep(100); return 42; });
    System.out.println(f.get());
}
```
输出：`virtual=true`、`42`。`newVirtualThreadPerTaskExecutor()` 为每个任务新建一个虚拟线程，没有池大小限制，`close()` 时等待全部完成。

适用与不适用：
- **适用**：大量并发、每个任务大部分时间在阻塞等待（服务一个请求要调用数据库、远程服务）。用熟悉的同步阻塞写法就能扛几十万并发。
- **不适用**：CPU 密集计算（虚拟线程不会让计算更快，只有核数那么多并行度）；也不该池化——它们本来就是廉价的。
