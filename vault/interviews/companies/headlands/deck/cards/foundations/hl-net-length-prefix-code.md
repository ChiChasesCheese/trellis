---
id: hl-net-length-prefix-code
node: foundations.networking-basics
type: qa
step: 34
---
## Q
写出长度前缀（4 字节长度 + 内容）的解码函数：从读模式的 `ByteBuffer` 里取出所有完整消息，半包留在缓冲区。调用前后要做什么？

## A
```java
static List<byte[]> decode(ByteBuffer buf) {
    List<byte[]> out = new ArrayList<>();
    while (buf.remaining() >= 4) {
        buf.mark();
        int len = buf.getInt();
        if (buf.remaining() < len) {   // 内容还没收全
            buf.reset();               // 回退到长度字段之前
            break;
        }
        byte[] msg = new byte[len];
        buf.get(msg);
        out.add(msg);
    }
    return out;
}
```
调用前要 `flip()`（写模式切读模式），调用后要 `compact()`，把半包留着等下次 `read` 追加。例：缓冲区放入长度 3 的消息和一条只到了 2/5 的消息，解出 1 条，剩 6 字节。生产代码还应校验 `len` 上限，防止恶意对端发超大长度。
