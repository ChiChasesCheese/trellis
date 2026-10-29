---
id: uth-os-net-page-cache-3-kafka
node: os-net.page-cache
type: qa
step: 3
---
## Q
**Kafka 为什么不自己做缓存**｜Kafka · 设计文档

Kafka 把消息直接写文件，不在 JVM 里缓存，读还会快吗？

## A
**背景。** 常见思路是应用自己在进程里缓存热数据。Kafka 反其道：消息直接写文件，不在 JVM（Java 虚拟机）里做缓存，缓存交给操作系统的页缓存。这样读还会快吗？

**结构。** Broker（Kafka 的服务进程）的日志只是一个文件目录：写入先进内核页缓存，读取也走页缓存；发给消费者用 `sendfile`（让内核直接把文件数据送到网卡，不经过应用程序）从页缓存送到网卡。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="12" y="56" width="72" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">磁盘文件</text>
<rect x="132" y="56" width="76" height="30" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">页缓存</text>
<rect x="262" y="56" width="66" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">网卡</text>
<line x1="84" y1="71" x2="127" y2="71" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M132.0,71.0 L125.2,74.3 L125.2,67.7 Z" fill="currentColor" stroke="none"/>
<line x1="208" y1="71" x2="257" y2="71" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M262.0,71.0 L255.2,74.3 L255.2,67.7 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="235" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">sendfile</text>
<rect x="110" y="124" width="120" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="170" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">JVM 堆 不缓存</text>
<line x1="170" y1="124" x2="170" y2="94" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="176" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">只发命令</text>
<text x="16" y="24" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">消息不经过用户态拷贝</text>
</svg>
```

**细节。**

- 文档的估算：32 GB 内存的机器上，缓存可达 28–30 GB，且没有 GC（垃圾回收）开销
- 服务重启后页缓存依然是热的；进程内缓存要重建（文档以 10 GB 约 10 分钟为例）
- `sendfile` 省掉“内核到用户态再回内核”的拷贝，只剩最后拷到网卡缓冲区
- 消费者基本追平时，磁盘几乎没有读活动

**为什么。** 自己缓存会和页缓存重复存一份；一致性与预读交给操作系统更简单，也更准。

**对应 LeetCode：** 无直接对应的题
