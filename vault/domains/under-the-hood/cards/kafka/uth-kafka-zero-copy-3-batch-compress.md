---
id: uth-kafka-zero-copy-3-batch-compress
node: kafka.zero-copy
type: qa
step: 3
---
## Q
**批量与压缩：把小消息攒成大块**｜Kafka · 4.0

生产者发 10 万条小消息，Kafka 怎么避免 10 万次小 I/O？批次什么时候发出？

## A
**背景。** 一条消息一次 I/O，10 万条就是 10 万次小请求；磁盘和网络都怕又小又碎的请求。

**结构。** 生产者按分区攒批（`RecordBatch`）。批是网络传输、磁盘存储、压缩的共同单位：整批压缩，broker 解压校验后仍以压缩态落盘，消费者才解压。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 118">
<rect x="10" y="24" width="24" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="24" width="24" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="70" y="24" width="24" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="10" y="50" width="24" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="50" width="24" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="70" y="50" width="24" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="52" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小消息</text>
<line x1="104" y1="46" x2="124" y2="46" stroke="currentColor" stroke-width="1.2"/>
<polygon points="130,46 124.0,49.0 124.0,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="130" y="22" width="100" height="56" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RecordBatch</text>
<text x="180" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">整批压缩</text>
<line x1="230" y1="46" x2="250" y2="46" stroke="currentColor" stroke-width="1.2"/>
<polygon points="256,46 250.0,49.0 250.0,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="256" y="28" width="76" height="36" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="50.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">落盘/网络</text>
<text x="170" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">满 batch.size 或等满 linger.ms 就发</text>
</svg>
```

**细节。**

- 批次满 `batch.size`（默认 16384 字节）或等满 `linger.ms` 就发；`linger.ms` 从 4.0 起默认 5（毫秒），之前是 0。
- `compression.type` 默认 `none`。

**坑。** `linger.ms=0` 时只有生产者忙不过来才被动成批。

**为什么。** 重复内容（如 JSON 字段名）散在消息之间，逐条压缩效果很差；成批后，随机的小写变成顺序的大块，才配得上页缓存和 `sendfile`。

**对应 LeetCode：** 无直接对应的题
