---
id: tlc-design-circular-queue-4-followup
node: p3.design-circular-queue
type: qa
step: 4
---
## Q
**LC 622 设计循环队列**｜追问

循环队列（定长数组、`head` 加 `size`）已经实现。面试官接着问：（1）多线程的生产者和消费者共用它？（2）队满时不拒绝，而是覆盖最旧的元素？（3）容量不够时自动扩容？（4）改成双端（头尾都能入队出队）？

## A
1. **线程安全**：一把锁保护所有方法不够，生产者要在队满时等待、消费者要在队空时等待，用 `threading.Condition`：入队前 `while 队满: cond.wait()`，入队后 `cond.notify()`；出队同理。Python 里生产环境直接用 `queue.Queue(maxsize=k)`，它就是这个结构。
2. **覆盖最旧元素**：队满时入队先 `head = (head + 1) % cap`，再写 `buf[(head + size - 1) % cap]`，`size` 保持 `k`；对应日志缓冲、滑动窗口的最近 `k` 个值。`collections.deque(maxlen=k)` 是同样的语义。
3. **扩容**：满时分配 `2 * cap` 的新数组，按逻辑顺序（从 `head` 开始绕一圈）把 `size` 个元素拷过去，`head` 重置为 `0`；拷贝 `O(size)`，均摊每次入队 `O(1)`。
4. **双端**：队首入队是 `head = (head - 1) % cap` 后写入，队尾出队是 `size -= 1`，其余下标公式不变（LC 641）。

**Python 提醒**：`deque(maxlen=k)` 满了会静默丢掉另一端的元素，不会返回 `False`，和循环队列「满了拒绝」的语义不同，不能拿来直接替换；`list.pop(0)` 是 `O(n)`，不适合做队列。
