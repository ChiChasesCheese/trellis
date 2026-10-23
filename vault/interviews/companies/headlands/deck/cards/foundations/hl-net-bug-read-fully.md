---
id: hl-net-bug-read-fully
node: foundations.networking-basics
type: qa
step: 48
---
## Q
下面读「4 字节长度 + 内容」的代码有什么 bug？

```java
byte[] lenBuf = new byte[4];
in.read(lenBuf);
int len = ByteBuffer.wrap(lenBuf).getInt();
byte[] body = new byte[len];
in.read(body);
```

## A
两处 `read` 都假设一次读满，但 `InputStream.read(byte[])` 只保证读到**至少 1 个字节**（或 -1），可能只返回部分数据（TCP 字节流没有边界）。要循环读够，或用 `DataInputStream.readFully`。

另外：(1) 没检查 -1（连接关闭）；(2) `len` 没做上限校验，恶意对端发 2 GB 的长度会让你 OOM。
