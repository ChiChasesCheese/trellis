---
id: hl-j19-real-tickbook
node: java21.j19-runtime-zgc-jit
type: qa
step: 32
---
## Q
面试被问「这个订单簿怎么降低 GC 压力」，用 `TickBook` 的设计怎么答？朴素版为什么产生垃圾？

## A
朴素的 `OrderBook` 每个订单是一个 `Node` 对象 + `TreeMap`/`HashMap` 的装箱 `Long` key + 每次调用的 `Event` 列表，实测每个操作约 **400 字节垃圾**（订单簿每条命令约 420 字节），垃圾多 → GC 停顿 → 尾延迟抖动。低延迟系统要的是**稳态零分配**。

`TickBook` 的做法：价格是有界范围内的 `long` tick，用**数组/位图索引**，不装箱；**开放寻址**；**预分配**。

降低 GC 压力清单：对象图改数组、开放寻址、回调代替 `List<Event>`、分代 ZGC、预热 JIT、`-Xms=-Xmx` + `AlwaysPreTouch`。
