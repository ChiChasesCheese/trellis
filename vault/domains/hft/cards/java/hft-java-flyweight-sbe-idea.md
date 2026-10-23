---
id: hft-java-flyweight-sbe-idea
node: java.flyweight-sbe
type: qa
step: 1
---
## Q
flyweight（享元）编解码是什么思路？为什么不为每条消息创建一个对象？

## A
普通做法：收到一段字节，解析成 `NewOrder` 对象，每个字段赋值，字符串字段还要新建 `String`，每条消息都产生对象，也就是垃圾。

flyweight 的做法：只有**一个可复用的视图对象**，持有字节缓冲区和当前消息的起始偏移，调用 `wrap(buffer, offset)` 把它“对准”某条消息。`getPrice()` 实际上是 `buffer.getLong(offset + 8)`，字段在固定偏移上直接读写，不复制也不解析。同一个视图对象可以处理一百万条消息，零分配。

注意：视图不拥有数据，`wrap` 到下一条消息后，之前读到的内容就变了，不能保存这个视图供以后使用。
