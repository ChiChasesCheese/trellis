---
id: hl-os-offer-spin-code
node: foundations.os-processes-threads-ipc
type: qa
step: 44
---
## Q
给 SPSC 环形缓冲写一个「满了就最多自旋等待 n 次再放弃」的 `offerSpin`，为什么不能无限自旋？

## A
```java
interface Ring { boolean offer(long v); }

static boolean offerSpin(Ring ring, long v, int maxSpins) {
    for (int i = 0; i < maxSpins; i++) {
        if (ring.offer(v)) return true;
        Thread.onSpinWait();   // 提示 CPU 这是自旋（x86 上是 PAUSE 指令）
    }
    return false;              // 放弃，调用方决定丢弃或报警（背压）
}
```
不能无限自旋：消费者挂了，生产者就永远卡死。有限自旋后把失败交给调用方处理（丢弃、报警、背压）。
