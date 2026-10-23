---
id: hl-j19-q6-spike
node: java21.j19-runtime-zgc-jit
type: qa
step: 39
---
## Q
面试问：线上出现偶发 100 ms 尖刺，怎么查？
You see occasional 100 ms latency spikes in production. How do you investigate?

## A
思路：先**分类**，再对时间线。
1. 把尖刺的时间戳对齐 **GC 日志**和 **JFR 录制**：有没有 GC 暂停事件、去优化风暴、锁竞争事件、safepoint？
2. JVM 侧对不上，就是 **OS 层**：CPU 频率、调度、透明大页（THP）；
3. 先测基线，**一次改一个变量**；
4. 检查测量本身有没有**协同遗漏**，再信分位数。

英文骨架：「Line up the spike's timestamp against GC logs and a JFR recording; if nothing JVM-side lines up, it's OS-level; check for coordinated omission.」
