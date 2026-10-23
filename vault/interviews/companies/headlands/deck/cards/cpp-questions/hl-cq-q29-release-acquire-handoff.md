---
id: hl-cq-q29-release-acquire-handoff
node: cpp-questions.g-concurrency
type: qa
step: 9
---
## Q
用 release/acquire 发布数据（一个标志 `ready` 加一份 `payload`）：生产者和消费者各按什么顺序做哪四步？为什么需要它？

## A
1. 生产者：写 `payload = {round, round*2};`
2. 生产者：`ready.store(true, release);`
3. 消费者：`while (!ready.load(acquire)) {}`
4. 消费者：`use(payload);`——一定能看到 payload 的新值。

为什么需要：CPU 和编译器都会**重排**内存操作。没有 release/acquire，消费者可能看到 `ready == true` 而 `payload` 还是旧值。实测此握手跑 20,000 次零错误读。
