---
id: uth-kafka-zero-copy-2-sendfile
node: kafka.zero-copy
type: qa
step: 2
---
## Q
**sendfile：数据不经过用户态**｜Kafka · 4.0

consumer 拉取消息时，broker 为什么几乎不花 CPU 搬数据？开了 TLS 之后还是这样吗？

## A
**背景。** 把磁盘上的消息发给消费者，数据要经过页缓存、程序缓冲区、socket 缓冲区才到网卡，每经过一处就拷贝一次，CPU 一直在搬数据。

**结构。** 磁盘上的日志格式和网络上的消息批格式相同，fetch 时不用重新编码，所以直接调 Java 的 `FileChannel.transferTo`，对应 Linux 的 `sendfile`：数据在内核里从页缓存直达网卡。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 134">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">传统: 4 次拷贝</text>
<rect x="6" y="20" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<rect x="74" y="20" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="102" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页缓存</text>
<line x1="62" y1="33" x2="68" y2="33" stroke="currentColor" stroke-width="1.2"/>
<polygon points="74,33 68.0,36.0 68.0,30.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="142" y="20" width="56" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户缓冲</text>
<line x1="130" y1="33" x2="136" y2="33" stroke="currentColor" stroke-width="1.2"/>
<polygon points="142,33 136.0,36.0 136.0,30.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="210" y="20" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="238" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">socket</text>
<line x1="198" y1="33" x2="204" y2="33" stroke="currentColor" stroke-width="1.2"/>
<polygon points="210,33 204.0,36.0 204.0,30.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="278" y="20" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="306" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网卡</text>
<line x1="266" y1="33" x2="272" y2="33" stroke="currentColor" stroke-width="1.2"/>
<polygon points="278,33 272.0,36.0 272.0,30.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">sendfile: 不经用户态</text>
<rect x="6" y="82" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="99.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<rect x="74" y="82" width="56" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="102" y="99.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页缓存</text>
<rect x="278" y="82" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="306" y="99.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网卡</text>
<line x1="62" y1="95" x2="68" y2="95" stroke="currentColor" stroke-width="1.2"/>
<polygon points="74,95 68.0,98.0 68.0,92.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="130" y1="95" x2="272" y2="95" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="278,95 272.0,98.0 272.0,92.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="204" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数据在内核里直达网卡</text>
</svg>
```

**细节。**

- 传统路径：磁盘 → 页缓存 → 用户缓冲区 → socket 缓冲区 → 网卡，4 次拷贝、2 次系统调用（程序请内核办事）；`sendfile` 只剩最后一次到网卡。
- 多个消费者读同一段数据，它只进页缓存一次。

**坑。** 开了 TLS（加密传输）就失效：加密要在用户态做，`SslTransportLayer` 只能每次读 32768 字节文件、加密、再写出。

**对应 LeetCode：** 无直接对应的题
