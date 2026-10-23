---
id: hl-hc02-cpp-followups
node: problems.hc02-merge-k-streams
type: qa
step: 22
---
## Q
C++ 面试官追问合并流：线程安全队列怎么写、一万个 source 怎么办、怎么测并发、`try_next()` 能不能忙等？

## A
- **线程安全队列**：`mutex` + 两个条件变量（`not_full` / `not_empty`）+ `deque`；条件变量一定配谓词（虚假唤醒）；通知可以在释放锁之后。无锁则是单生产者单消费者（SPSC）环形缓冲区 + `atomic` 读写下标，acquire/release；每条流一个生产者一个消费者，正好是 SPSC。
- **一个 source 永远不返回**：`close()` / 析构会一直等它。要有界就必须让 source 自己支持超时或取消，真实系统在 source 外套超时，超时算 `Failed`。
- **一万个 source**：OS 线程太贵，改成线程池 + 非阻塞 I/O（`epoll` / `kqueue`），或限制「同时在读的 source 数 m」（有界并发）；`capacity` 是每流预读深度，不是并发数。
- **测试并发**：多次重复 + 随机 `yield` 打乱交错 + 与顺序实现对拍；ThreadSanitizer（`-fsanitize=thread`）找数据竞争；看门狗线程把死锁变成失败。
- **`try_next()` 忙等**：能但烧 CPU；更好的是 `next()` 在缺队首的流上阻塞；要和别的事件一起等时，加回调或用 `eventfd` / 管道通知。
- **只可移动的元素**：`Merger` 现在不支持，因为 `prev_` 要保留上一个元素做顺序检查需拷贝；可让比较器只看可拷贝的「键」，或把顺序检查交给 source。
