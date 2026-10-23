---
id: hl-hc02-interrupt-close
node: problems.hc02-merge-k-streams
type: qa
step: 12
---
## Q
Java 线程中断（interrupt）怎么取消阻塞的生产者？`catch (InterruptedException e) {}` 为什么危险？`close()` 怎么写？

## A
Java 没有强杀线程（`Thread.stop` 已废弃），标准取消是**中断**：`thread.interrupt()` 设中断标志，线程阻塞在 `take()`、`put()`、`sleep()`、`join()` 时立刻抛 `InterruptedException` 并清标志。

`catch (InterruptedException e) { }` 吞掉取消信号，线程继续运行，是最常见的并发 bug。正确处理：(1) `return` / 退出循环；(2) `Thread.currentThread().interrupt()` 重设标志让上层感知，再退出或抛出。

只有可中断的阻塞方法响应中断，读网络的老 API 不一定，所以 `close()` 里等线程退出必须**带超时**：
```java
public void close() {
    if (!closed.compareAndSet(false, true)) return;   // 幂等
    producers.forEach(Thread::interrupt);
    for (Thread t : producers) {
        try { t.join(Duration.ofSeconds(1)); }
        catch (InterruptedException _) { Thread.currentThread().interrupt(); return; }
    }
}
```
`AtomicBoolean.compareAndSet(false, true)` 原子地「若 false 就设 true」，保证只有第一次调用执行。不响应中断的 source，`close()` 只能带上限地 `join` 然后放弃它，这是要说清楚的权衡。
