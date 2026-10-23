---
id: hl-bm-three-layers-example
node: behavioral.method
type: qa
step: 10
---
## Q
用"零拷贝克隆"（zero-copy clone）演示三层追问：被问 "克隆要多久？""为什么这么快？""写入克隆会怎样？"，各层怎么答？

## A
- **L1** "How long does a clone take?" → "About two seconds."
- **L2** "Why so fast?" → "A clone copies **metadata**, not data: the data sits in **immutable micro-partitions** and the clone **points** at the same files."
- **L3** "What happens when you write to the clone?" → "New data goes into **new** partitions while shared ones stay immutable, so storage cost appears only when they **diverge**. I know it from using it; I haven't read the engine's code."

L3 的最后一句是合格答案：说清边界，不编。
