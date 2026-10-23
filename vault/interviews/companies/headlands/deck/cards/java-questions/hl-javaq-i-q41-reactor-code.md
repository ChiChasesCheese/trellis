---
id: hl-javaq-i-q41-reactor-code
node: java-questions.i-network
type: qa
step: 6
---
## Q
写出单线程 `Selector` 事件循环的核心结构。反应器的优缺点是什么？

## A
```java
sel.select();                       // sleep until events
for (SelectionKey k : sel.selectedKeys()) {
    if (k.isAcceptable()) { /* accept, register OP_READ */ }
    else if (k.isReadable()) { /* channel.read(buf) -> handle -> channel.write */ }
}
```
accept、read、write 都在一个线程里；实测处理 2 万次请求，约 17 µs/次（含客户端与服务端两端的 loopback 往返）。

- **优点**：连接数多时线程少、没有线程切换、可以绑核。
- **缺点**：回调式 / 状态机代码复杂；任何一处阻塞（慢处理、GC、日志）会卡住该线程上的**所有连接**——耗时工作丢给另一个线程池。
- **直接缓冲区** `ByteBuffer.allocateDirect` 让内核直接读写，少一次堆内拷贝。
