---
id: hl-net-multicast-java
node: foundations.networking-basics
type: qa
step: 29
---
## Q
用 NIO 写组播接收器：关键的几行代码是什么？真实行情接收器还有哪些要点？

## A
```java
try (DatagramChannel ch = DatagramChannel.open(StandardProtocolFamily.INET)) {
    ch.setOption(StandardSocketOptions.SO_REUSEADDR, true);
    ch.bind(new InetSocketAddress(45678));
    MembershipKey key = ch.join(group, ni);       // 发 IGMP 加入报文
    ch.configureBlocking(false);                  // receive 没数据返回 null
    ByteBuffer buf = ByteBuffer.allocateDirect(2048);
    while (running) {                             // 忙轮询
        buf.clear();
        if (ch.receive(buf) == null) continue;
        buf.flip();
    }
    key.drop();                                   // 离开组
}
```
要点：`ni` 必须是实际收组播的网卡（多网卡机器选错会收不到）；非阻塞 + 忙轮询 + 预分配直接缓冲区 + 绑核；包到达后**立刻**取走交给下游，绝不在接收线程里做重活，否则 `SO_RCVBUF` 溢出丢包。
