---
id: hl-os-spsc-code
node: foundations.os-processes-threads-ipc
type: qa
step: 29
---
## Q
写出 FFM + `VarHandle` 实现的 SPSC 环形缓冲的 `offer` 和 `poll`（JDK 21）。

## A
```java
static final VarHandle LONG = ValueLayout.JAVA_LONG.varHandle();
// headSeg = mem.asSlice(0, 8); tailSeg = mem.asSlice(128, 8)
// slots = mem.asSlice(256, capacity * 8L); mask = capacity - 1

public boolean offer(long v) {
    long tail = (long) LONG.get(tailSeg);
    if (tail - cachedHead == capacity) {
        cachedHead = (long) LONG.getAcquire(headSeg);
        if (tail - cachedHead == capacity) return false;
    }
    slots.set(ValueLayout.JAVA_LONG, (tail & mask) * 8, v);   // ① 先写数据
    LONG.setRelease(tailSeg, tail + 1);                       // ② 再发布
    return true;
}
public long poll() {
    long head = (long) LONG.get(headSeg);
    if (head == cachedTail) {
        cachedTail = (long) LONG.getAcquire(tailSeg);
        if (head == cachedTail) return Long.MIN_VALUE;
    }
    long v = slots.get(ValueLayout.JAVA_LONG, (head & mask) * 8);  // ③ 读数据
    LONG.setRelease(headSeg, head + 1);                            // ④ 释放槽位
    return v;
}
```
要点：JDK 21 的 `VarHandle` 只接受 `MemorySegment` 一个坐标，所以用 `asSlice` 把 `head` 的 8 字节单独切开；容量必须是 2 的幂（`Integer.bitCount(capacity) == 1`）；`Long.MIN_VALUE` 当「空」哨兵，真实系统会返回布尔值或用变长消息帧。
