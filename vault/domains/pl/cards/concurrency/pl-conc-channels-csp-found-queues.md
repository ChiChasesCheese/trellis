---
id: pl-conc-channels-csp-found-queues
node: concurrency.channels-csp
type: qa
step: 5
---
## Q
Java 的 `BlockingQueue` 和 Python 的 `queue.Queue` 是什么？有界队列怎样产生“背压”，没有 `close` 时消费者怎么知道结束？

## A
两者都是**线程安全的阻塞队列**：
- `put(x)` 放入元素；队列已满（有界时）则阻塞到有空位；
- `take()`（Java）/ `get()`（Python）取出元素；队列为空则阻塞到有元素。

**有界队列**：创建时指定容量（Java `new ArrayBlockingQueue<>(2)`，Python `Queue(maxsize=2)`）。生产者比消费者快时，队列满了生产者被阻塞，这就是**背压**（backpressure）：下游慢，自动让上游慢下来，内存不会无限增长。

**结束信号**：它们没有“关闭”的概念，惯例是放一个特殊值作为**毒丸**（poison pill）/哨兵：消费者取到它就退出。

Java 实验（容量 2，生产者放 5 个数再放一个毒丸 `-1`，主线程睡 100 毫秒后才开始消费）：
```java
BlockingQueue<Integer> q = new ArrayBlockingQueue<>(2);
Thread.ofPlatform().start(() -> {
    for (int i = 1; i <= 5; i++) { q.put(i); System.out.println("put " + i); }
    q.put(-1);                    // poison pill
});
Thread.sleep(100);
System.out.println("queue size before consuming: " + q.size());
int v;
while ((v = q.take()) != -1) System.out.println("take " + v);
```
（`put`/`take` 抛出 `InterruptedException`，上面省略了 try/catch。）消费前的输出固定是 `put 1`、`put 2`、`queue size before consuming: 2`。`put 3` 必须等消费者取走一个之后才出现。

Python 同理：
```python
q = queue.Queue(maxsize=2)
q.put(1); q.put(2)
try: q.put_nowait(3)
except queue.Full: print("queue.Full")
```
输出：`queue.Full`。非阻塞版本 `put_nowait`/`get_nowait` 在满/空时直接抛 `queue.Full`/`queue.Empty`；Java 的 `offer` 满时返回 `false`。
