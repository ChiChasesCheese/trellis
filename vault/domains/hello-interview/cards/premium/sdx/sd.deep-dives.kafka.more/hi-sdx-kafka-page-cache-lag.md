---
id: hi-sdx-kafka-page-cache-lag
node: sd.deep-dives.kafka.more
type: qa
step: 4
---
## Q
**消费者滞后超过页缓存窗口，会拖慢别人**｜补充 · Kafka · 追问

面试官：「一个 broker 约 50 GB 页缓存，承接的写入约 50 MB/s。为什么消费者滞后超过大约 17 分钟，就会开始影响同一个 broker 上别的生产者和消费者，而不只是它自己变慢？」

## A
**结论。** 页缓存只装得下最近约 1,024 秒（50 GB ÷ 50 MB/s）的数据。追得上的消费者从内存零拷贝读，几乎不占磁盘；滞后超过这个窗口就要读磁盘，和生产者的顺序写争同一块盘。

**要点。**
- **窗口：** 50 GB = 51,200 MB，除以 50 MB/s 约 1,024 秒，约 17 分钟。这是估算，页缓存被所有分区共用，也不严格按时间淘汰。
- **窗口内：** 读命中页缓存，用零拷贝直接送到网卡，对 broker 几乎没有额外成本。
- **窗口外：** 读未命中，要读磁盘；读取的冷数据还会挤掉页缓存里原本热的数据，让别的本来在窗口内的消费者也开始未命中。
- **连锁反应：** 磁盘读占用带宽，后台刷脏页和写入变慢，follower 拉取变慢，生产者延迟上升，同步副本集合可能收缩。
- **对策：** 监控滞后的时间而不是条数，接近窗口就告警；回填历史数据限速或走专用副本；用分层存储让旧数据从远程存储读，不挤本地页缓存。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="10" y="22" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间 →  越靠右越新</text>
<rect x="10" y="30" width="220" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="120.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更早的数据：只在磁盘</text>
<rect x="230" y="30" width="100" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页缓存</text>
<text x="280.0" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">≈ 17 分钟</text>
<polyline points="120,110 120,64" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,64.0 116.8,71.0 123.2,71.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="120" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 滞后 40 分钟：读磁盘</text>
<polyline points="280,150 280,64" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280.0,64.0 276.8,71.0 283.2,71.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="330" y="164" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">A 滞后 3 分钟：读内存</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口 = 50 GB ÷ 50 MB/s ≈ 1,024 秒</text>
</svg>

**面试里这样说。** 「页缓存窗口是缓存大小除以写入速率，这里约 17 分钟。消费者滞后超过它就从磁盘读，和写入争盘，还把热数据挤出缓存，影响所有人。所以我按滞后时间告警，回填限速，或者用分层存储隔离旧数据的读。」

**易错。**
- **只盯滞后条数：** 同样的条数在不同写入速率下对应的时间差很多。
- **回填历史数据直接打生产集群：** 一次大回填就能让所有生产者变慢。
