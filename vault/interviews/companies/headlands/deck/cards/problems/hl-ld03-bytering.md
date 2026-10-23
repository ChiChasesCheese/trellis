---
id: hl-ld03-bytering
node: problems.ld03-async-tcp-channel
type: qa
step: 3
---
## Q
`ByteRing`（字节环）的 `write` / `read` 怎么处理回绕？`writeAll`、`peekInt`、`take`、`skip` 的语义是什么？为什么用环而不是 `arraycopy` 前移？

## A
固定容量数组，读写位置到末尾绕回开头；`ByteRing` 单线程，容量任意正整数（用 `%` 而非 `& mask`），变量 `head`（下一个读位置）和 `size`，写入位置 = `(head + size) % capacity`；回绕时一次拷贝拆成两段。
```java
public int write(ByteBuffer src) {
    int n = Math.min(src.remaining(), free());
    int tail = (head + size) % buf.length;
    int first = Math.min(n, buf.length - tail);
    src.get(buf, tail, first);
    src.get(buf, 0, n - first);
    size += n;
    return n;
}
public int read(ByteBuffer dst) {
    int n = Math.min(dst.remaining(), size);
    int first = Math.min(n, buf.length - head);
    dst.put(buf, head, first);
    dst.put(buf, 0, n - first);
    head = (head + n) % buf.length;
    size -= n;
    return n;
}
```
例：容量 8，head=6，size=4（占 6,7,0,1），写入位置 (6+4)%8 = 2；读 4 字节先读下标 6,7 再读 0,1。`first` 是起点到末尾能放多少，剩下 `n − first` 从 0 开始；两次 `get` 之间 `position` 自动前进；满时 `n = 0`，两次拷贝都是空操作，不需特判。

其他 API：
- `writeAll(src, off, len)`：**全有或全无**，放不下一个字节都不写；用 `Objects.checkFromIndexSize(off, len, src.length)` 抛标准 IOOBE 且正确处理 `off + len` 溢出；
- `peekInt()` / `peekInt(offset)`：大端读，**不消费**，能跨回绕点；不足 4 字节 → `IllegalStateException`；
- `take(n)` / `skip(n)`：不足 → `IllegalStateException`（状态不变）；`n < 0` → `IllegalArgumentException`；
- `clear()`；`capacity/size/free/isEmpty`。

**为什么用环不用 `arraycopy` 前移**：前移每次 O(n)，环只改 `head`，O(1)。

`ByteBuffer` 三个游标：`position`、`limit`、`capacity`；写完要 `flip()` 才能读，读完要 `clear()` 或 `compact()` 才能再写；`allocateDirect` 的堆外缓冲让 `SocketChannel` 读写少一次拷贝，两个 16 KB 中转缓冲（`rbuf`、`wbuf`）用它。

边界测试：容量 1；写满再写（部分写）；回绕分两段；`peekInt` 跨回绕、符号位；随机操作对照 `ArrayDeque<Byte>`。
