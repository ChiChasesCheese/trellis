---
id: hl-ld03-frame-decoder
node: problems.ld03-async-tcp-channel
type: qa
step: 4
---
## Q
增量解码器 `FrameDecoder` 的 `feed` / `next` 怎么写？为什么解码器自己也是有界的，容量为什么必须 ≥ `maxFrame + 4`？

## A
有状态对象：`feed(bytes)` 喂任意长度字节，`next()` 吐出完整消息，不够返回 `null`。
```java
public byte[] next() {
    if (failed != null) throw failed;                      // 粘性失败
    if (ring.size() < FrameCodec.HEADER) return null;
    int len = ring.peekInt();                              // 不消费
    if (len < 0 || len > maxFrame) {
        failed = new FrameException("bad frame length " + len + " (maxFrame " + maxFrame + ")");
        throw failed;
    }
    if (ring.size() < FrameCodec.HEADER + len) return null;  // 头到了负载没到：什么都不改，下次 feed 后再看
    ring.skip(FrameCodec.HEADER);
    return ring.take(len);
}
```
- `feed(ByteBuffer)` 返回**实际消费数**，环里放不下的字节**不消费**，调用方必须先 `next()` 腾空间再继续喂——这是入站背压在最低层的体现；`capacity < maxFrame + 4` → `IllegalArgumentException`；
- `hasFrame()`、`buffered()`、`free()`；`hasTruncatedTail()`：完整帧之后是否还有一截不完整的尾巴（EOF 时判断流是否在帧中间被截断）；非法头不算截断；
- `FrameCodec.encode(out, payload, maxFrame)`：放不下返回 `false`，**不留半个帧头**；超 `maxFrame` → `IllegalArgumentException`；`HEADER = 4`。

**为什么解码器有界**：缓冲区可增长的话，对端发一堆没凑成消息的字节内存就无限涨。**为什么容量 ≥ `maxFrame + 4`**：入站环必须装得下一条最大完整消息，否则环里是半条消息且已满，无法继续读也凑不齐——死锁；出站方向则是最大的消息永远 `offer` 失败。

验证方法：在**每一个**切分点切开三条消息结果必须相同；字节逐个到达；解码器满了 `feed` 返回部分；随机切块 100 条 × 40 轮；一次写入「两条半」。样例：`FrameDecoder(10, 64)`，喂 `{0,0,0,3,'a'}` → `next()` 为 null；再喂 `{'b','c',0,0}` → `"abc"`，剩两字节是下一帧的半个头，`hasTruncatedTail()` 为 true。

边界：空负载；恰好 `maxFrame`；`maxFrame+1`；负长度；`0x7FFFFFFF`；半个头；头完整负载不全；完整帧后接半个头。性能：100 万条 32 字节经环 + 解码器 < 2 s。
