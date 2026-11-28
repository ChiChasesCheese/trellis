---
id: bagu-kafka-throughput-1-kafka-high-throughput
node: b.mq.kafka-throughput
type: qa
step: 1
---
## Q
**Kafka 高吞吐 · 顺序写、零拷贝、批量与压缩**｜必会

面试官：「Kafka 数据落在磁盘上，为什么吞吐还这么高？消费端为什么用拉模型，零拷贝用在哪？」

## A
**基本回答。** 顺序写（只追加到分区日志末尾）、页缓存（先写操作系统缓存，异步刷盘，读近期数据命中内存）、零拷贝（消费时用 `sendfile`，数据从页缓存直达网卡，不进用户态）、批量加压缩（生产者攒批，整批压缩）、分区并行。
页缓存不占 JVM 堆，没有 GC 压力。批量由 `batch.size`（默认 16384 字节）和 `linger.ms` 控制，`linger.ms` 默认 0，4.0 起改为 5，越大吞吐越高、延迟越大；压缩用 lz4、zstd 或 snappy。默认不逐条 `fsync`，可靠性靠多副本和 `acks=all`，后者延迟比 `acks=1` 高。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写</text>
<rect x="10" y="22" width="92" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产者</text>
<text x="56" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">攒批+压缩</text>
<rect x="126" y="22" width="76" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="164" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页缓存</text>
<text x="164" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存</text>
<rect x="226" y="22" width="104" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区日志</text>
<text x="278" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只追加·顺序写</text>
<line x1="102" y1="41" x2="126" y2="41" stroke="currentColor" stroke-width="1.2"/>
<polygon points="126,41 119.7,44.0 119.7,38.0" fill="currentColor"/>
<line x1="202" y1="41" x2="226" y2="41" stroke="currentColor" stroke-width="1.2"/>
<polygon points="226,41 219.7,44.0 219.7,38.0" fill="currentColor"/>
<text x="214" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">异步刷盘</text>
<text x="10" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读</text>
<rect x="10" y="116" width="76" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页缓存</text>
<text x="48" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">近期数据</text>
<text x="123" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sendfile</text>
<line x1="86" y1="141" x2="160" y2="141" stroke="currentColor" stroke-width="1.2"/>
<polygon points="160,141 153.7,144.0 153.7,138.0" fill="currentColor"/>
<rect x="160" y="116" width="60" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网卡</text>
<line x1="220" y1="135" x2="244" y2="135" stroke="currentColor" stroke-width="1.2"/>
<polygon points="244,135 237.7,138.0 237.7,132.0" fill="currentColor"/>
<rect x="244" y="116" width="86" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="287" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者</text>
<text x="287" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">自己拉取</text>
<text x="123" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不进用户态</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">batch.size 默认 16384 字节</text>
<text x="10" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">linger.ms 默认 0，4.0 起为 5</text>
</svg>
上半条是写路径：攒批压缩、先进页缓存、只追加到日志末尾；下半条是读路径：近期数据从页缓存经 `sendfile` 直达网卡，不经过用户态。
**举个例子。** 一条点击事件从产生到被消费：
1. **生产者攒批：** 点击事件不是一条条发，先在客户端缓冲，凑满 `batch.size` 或等够 `linger.ms` 就整批压缩后发出，一次网络请求带几百条。
2. **Broker 追加：** 整批追加到分区日志末尾，先进页缓存，操作系统稍后异步刷盘。
3. **消费者拉取：** 消费者按自己的节奏拉取最新的一段；刚写入的数据仍在页缓存里，直接命中内存。
4. **sendfile 发送：** 数据从页缓存直达网卡发给消费者，不拷进 Kafka 进程，也不经过 JVM 堆。
5. **换成 TLS：** 数据要在用户态加密，这一步的零拷贝就用不了，吞吐会降一些。
**容易错。**
- **以为磁盘一定慢：** 顺序写没有寻道，可到几百 MB/s，接近内存随机写。
- **以为 Kafka 每条消息都 fsync：** 默认不逐条刷盘，可靠性来自多副本和 `acks=all`，不是单机刷盘。
- **以为零拷贝永远生效：** 开 TLS 后数据要在用户态加密，用不了零拷贝。
- **以为 linger.ms 默认总是 0：** 4.0 起默认改为 5，批量与延迟的取舍发生了变化。
