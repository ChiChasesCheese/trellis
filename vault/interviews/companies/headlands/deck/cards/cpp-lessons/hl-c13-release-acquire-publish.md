---
id: hl-c13-release-acquire-publish
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 7
---
## Q
用 release/acquire 写出「发布数据」的标准模式：生产者写 `msg.a=1; msg.b=2`，消费者保证读到。配对规则是什么？

## A
```cpp
Msg msg;                                // 普通数据
std::atomic<bool> ready{false};

void producer() {
    msg.a = 1; msg.b = 2;                                 // (1) 写数据
    ready.store(true, std::memory_order_release);         // (2) 发布
}
void consumer() {
    while (!ready.load(std::memory_order_acquire)) {}     // (3) acquire 与 release 配对
    assert(msg.a == 1 && msg.b == 2);                     // (4) 保证看到 (1) 的写入
}
```
**配对规则**：线程 A 对原子变量做 `release` 写，线程 B 的 `acquire` 读读到了这个值，则 A 在 release **之前**的所有写入，B 在 acquire **之后**都能看到（synchronizes-with / happens-before）。
