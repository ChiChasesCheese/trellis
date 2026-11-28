---
id: mlp-traps-thread-stop
node: traps.cache-thread
type: qa
step: 3
---
## Q
**用布尔标志停止后台线程**｜语言陷阱与读代码

主线程睡 200 毫秒后把标志改成 `false`，想让后台线程停下来。下面的 Java 代码会怎样？怎么修？Python 里怎么写？

```java
static boolean running = true;
// 后台线程
Thread t = new Thread(() -> { long n = 0; while (running) n++; });
t.setDaemon(true);
t.start();
Thread.sleep(200);
running = false;
t.join(2000);
System.out.println("alive: " + t.isAlive());
```

## A
**输出。** 在 JDK 25 上实际运行，打印 `alive: true`：线程没有停下。

- **为什么：** 没有同步，Java 内存模型不保证后台线程能看到主线程写入的新值；即时编译器（JIT）可以把 `running` 读出来一次放进寄存器，循环永远读旧值。结果不确定，有时能停，有时不能，所以不能依赖。
- **修法一，`volatile`：** 声明 `static volatile boolean running`，保证写入对其他线程立即可见；同样的代码加了 `volatile`，实际运行打印 `worker stopped` 和 `alive: false`。
- **修法二，中断：** 调用 `t.interrupt()`，循环里检查 `Thread.currentThread().isInterrupted()`；线程在 `sleep` 或 `wait` 时会直接收到 `InterruptedException`，比标志响应更快。
- **`volatile` 的限度：** 只管可见性，不管原子性；`count++` 加了 `volatile` 仍然会丢更新，要用 `AtomicInteger`。
- **Python 写法：** 用 `threading.Event`，循环里 `while not stop.is_set()`，主线程 `stop.set()`；等待用 `stop.wait(0.01)`，既能睡眠又能被立刻唤醒，实际运行打印 `worker stopped, loops > 0: True` 和 `alive: False`。
- **记住：** 停线程用 `volatile` 标志、中断或 `Event`，不用普通变量。

**英文答法。**
- "Without `volatile` there's **no visibility guarantee**, so the worker may never see the change."
- "I'd use a `volatile` flag, or `interrupt()`; in Python, a `threading.Event`."
