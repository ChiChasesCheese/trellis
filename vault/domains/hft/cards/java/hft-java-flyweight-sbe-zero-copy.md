---
id: hft-java-flyweight-sbe-zero-copy
node: java.flyweight-sbe
type: qa
step: 5
---
## Q
flyweight 编解码怎样和堆外缓冲区配合，让一条消息从网卡到策略再到发出几乎不拷贝？

## A
典型路径：网卡收到的数据进入一块堆外接收缓冲区 → 同一个 decoder 直接 `wrap` 在这块内存上读字段 → 策略计算 → encoder `wrap` 在发送缓冲区上直接写字段 → 发出。整条路径只有少量复用的视图对象，没有为每条消息创建的对象，数据只在必要的次数被移动。

Aeron 的订阅回调就是这个模式：回调参数是 `(buffer, offset, length)`，decoder 直接对着这个区域 `wrap`。Agrona 的 `UnsafeBuffer` 能统一包装 `byte[]`、`ByteBuffer` 或原始内存地址，让 SBE 的编解码器不关心底下的内存来自哪里。

结果是 GC 的工作量不再随消息数量增长，因为堆上没有消息对象。
