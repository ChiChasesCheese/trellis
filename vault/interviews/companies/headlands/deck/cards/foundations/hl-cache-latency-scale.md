---
id: hl-cache-latency-scale
node: foundations.cpu-cache-locality
type: qa
step: 2
---
## Q
把 1 个 CPU 周期放大成 1 秒，L1、L2、L3、主内存、SSD 的延迟各相当于多久？

## A
- CPU 周期（约 0.3 ns）→ 1 秒
- L1 缓存（约 1 ns）→ 3 秒
- L2 缓存（约 3 ns）→ 9 秒
- L3 缓存（约 13 ns）→ 43 秒
- 主内存（约 100 ns）→ 约 **6 分钟**
- SSD（约 100 µs）→ 约 4 天

量级可信，具体数字别当精确值。一次缓存未命中（cache miss）就是「CPU 去喝了一杯咖啡」。
