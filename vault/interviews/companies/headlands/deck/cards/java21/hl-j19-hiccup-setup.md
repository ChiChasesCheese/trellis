---
id: hl-j19-hiccup-setup
node: java21.j19-runtime-zgc-jit
type: qa
step: 28
---
## Q
「hiccup meter」（jHiccup 的做法）怎么测量 GC 对尾部延迟的影响？

## A
一个线程每 **1 ms** 睡一次，记录**实际醒来比预期晚多少**；若 JVM 全局 STW，它必然晚醒。同时 4 个线程制造分配压力，另有约 600 MB 长寿对象，2 GB 堆。

另跑一个**无分配压力的基线**（`idle`），因为测量工具自己有噪声：macOS 上 `Thread.sleep(1)` 本身的误差让基线 p50 就约 6.67 ms，这不是 GC。**先测基线噪声。**
