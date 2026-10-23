---
id: hl-net-selector-echo
node: foundations.networking-basics
type: qa
step: 35
---
## Q
写出 `Selector` 回显服务器的主循环骨架，并说出真实代码还要处理哪些问题。

## A
```java
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 1024);
server.configureBlocking(false);
Selector selector = Selector.open();
server.register(selector, SelectionKey.OP_ACCEPT);
ByteBuffer buf = ByteBuffer.allocateDirect(4096);
while (running) {
    selector.select(10);
    Iterator<SelectionKey> it = selector.selectedKeys().iterator();
    while (it.hasNext()) {
        SelectionKey key = it.next();
        it.remove();                       // 必须手动移除
        if (key.isAcceptable()) { /* accept, 非阻塞, 注册 OP_READ */ }
        else if (key.isReadable()) { /* read, flip, write; n<0 则 close */ }
    }
}
```
真实代码还要处理：**背压与 `OP_WRITE`**（`write` 可能写不完，保存剩余并注册 `OP_WRITE`，写完要取消，否则 selector 一直忙转）、**半包**、异常、连接关闭与超时。实际项目用 **Netty** 或 **Aeron**，不手写。
