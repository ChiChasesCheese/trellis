---
id: hl-ld01-poll-drained
node: problems.ld01-spsc-channel
type: qa
step: 10
---
## Q
`MessageRing.poll` 和 `isDrained` 怎么写？为什么必须先读 `closed` 再读 `tail`，消费者的标准循环是什么？

## A
`poll()` 返回 `null` 有两种可能：现在没有但一会儿还有，或永远不会有了。必须区分，否则消费者要么永远等要么提前退出丢消息。头部放 `closed` 标志，生产者 `finish()` 置 1（release）。

```java
public byte[] poll() {
    long h = head;
    while (true) {
        if (h == cachedTail) {
            cachedTail = (long) LONG.getAcquire(seg, OFF_TAIL);
            if (h == cachedTail) return null;
        }
        int idx = (int) (h & mask);
        long at = HEADER_BYTES + idx;
        int len = seg.get(JAVA_INT_UNALIGNED, at);
        if (len == PAD) {                       // 越过填充，立即发布 head，生产者在等这段空间
            h += capacity - idx; head = h;
            LONG.setRelease(seg, OFF_HEAD, h);
            continue;
        }
        byte[] out = new byte[len];
        MemorySegment.copy(seg, JAVA_BYTE, at + 4, out, 0, len);
        h += recordSize(len); head = h;
        LONG.setRelease(seg, OFF_HEAD, h);      // 先拷出来，读完才归还
        return out;
    }
}
public boolean isDrained() {
    if ((long) LONG.getAcquire(seg, OFF_CLOSED) == 0L) return false;
    return head == (long) LONG.getAcquire(seg, OFF_TAIL);
}
```
`isDrained = closed && head == tail`。生产者先发布最后一次 `tail` 再置 `closed`；消费者**先读 `closed` 再读 `tail`**：看到 `closed==1` 就保证（经 release/acquire）看得到最终 `tail`。若先读 `tail`（旧值，恰好等于 head），生产者随后发布最后几条并置 `closed`，消费者再读 `closed==1` 就误判 drained，**丢最后几条**。

边界：末尾可能残留一条 PAD（offer 发布了 PAD 但真记录没放进，随后 finish），此时 `head != tail`，`isDrained()` 为 `false`，消费者再 `poll` 一次越过 PAD（返回 `null`）后为 `true`。空但没 `finish` ≠ drained；有消息没读完 ≠ drained；`finish` 之后 `offer` 抛异常。

消费者标准写法：
```java
while (!ring.isDrained()) {
    byte[] m = ring.poll();
    if (m == null) { Thread.onSpinWait(); continue; }
    handle(m);
}
```
`bytesPending()` 含 PAD，近似值（`Math.clamp(t - h, 0, capacity)`）。
