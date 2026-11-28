---
id: bagu-io-pagecache-zerocopy-1-pagecache-sendfile
node: b.net.io-pagecache-zerocopy
type: qa
step: 1
---
## Q
**文件 I/O · Page Cache 与零拷贝**｜追问

面试官：「Page Cache 是什么，写日志时机器掉电会怎样？零拷贝是怎么减少拷贝的，Kafka 为什么快？」

## A
**基本回答。** Page Cache 是内核对磁盘文件的内存缓存：读先查缓存（顺序读有预读），写先写缓存并标记脏页，`write` 就返回，之后由内核线程异步回写（write-back）。所以 `write` 成功不等于落盘，掉电会丢；要持久化必须 `fsync`，它强制把脏页和元数据写回并等落盘，延迟高，所以要攒一批再 `fsync`。脏页默认存活约 30 秒（`vm.dirty_expire_centisecs=3000`）或比例超阈值才被刷。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 134">
<rect x="4" y="14" width="88" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="30.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用</text>
<text x="48" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">write()</text>
<line x1="92" y1="34" x2="119.0" y2="34.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126,34 119.0,37.2 119.0,30.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="14" width="88" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="30.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Page Cache</text>
<text x="170" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">脏页</text>
<line x1="214" y1="34" x2="241.0" y2="34.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="248,34 241.0,37.2 241.0,30.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="248" y="14" width="88" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<text x="4" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">write 返回成功：只是写进了内存</text>
<text x="4" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">约 30 秒后内核线程异步回写；fsync 则立刻回写</text>
<text x="4" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">掉电：还没回写的脏页就丢了</text>
</svg>
`write` 返回时数据只在内存里，落盘靠后台回写或 `fsync`。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">read + write</text>
<text x="6" y="30" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 次拷贝，4 次切换</text>
<text x="196" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">sendfile</text>
<text x="196" y="30" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2 次拷贝，2 次切换</text>
<rect x="6" y="40" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<line x1="61" y1="66" x2="61.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="61,90 57.8,83.0 64.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="69" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DMA</text>
<rect x="6" y="90" width="110" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内核缓冲区</text>
<text x="61" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(Page Cache)</text>
<line x1="61" y1="128" x2="61.0" y2="143.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="61,150 57.8,143.0 64.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="69" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CPU</text>
<rect x="6" y="150" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户缓冲区</text>
<line x1="61" y1="176" x2="61.0" y2="191.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="61,198 57.8,191.0 64.2,191.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="69" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CPU</text>
<rect x="6" y="198" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="215" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">socket 缓冲区</text>
<line x1="61" y1="224" x2="61.0" y2="239.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="61,246 57.8,239.0 64.2,239.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="69" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DMA</text>
<rect x="6" y="246" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="263" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网卡</text>
<rect x="196" y="40" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<line x1="261" y1="66" x2="261.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="261,90 257.8,83.0 264.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="269" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DMA</text>
<rect x="196" y="90" width="130" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内核缓冲区</text>
<text x="261" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(Page Cache)</text>
<line x1="261" y1="128" x2="261.0" y2="143.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="261,150 257.8,143.0 264.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="269" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SG-DMA</text>
<rect x="196" y="150" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网卡</text>
<text x="196" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不经过用户态</text>
<text x="196" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CPU 一次都不搬数据</text>
<text x="196" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前提：网卡支持</text>
<text x="196" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SG-DMA</text>
</svg>
传统 `read` + `write` 发文件：4 次切换、4 次拷贝（DMA 两次，CPU 两次）。`sendfile` 不经用户态，2 次切换；网卡支持 SG-DMA 时只剩 2 次 DMA 拷贝，CPU 一次都不搬，所以叫 CPU 零拷贝。`mmap` + `write` 只省内核到用户那一次拷贝，仍有 4 次切换。
**Kafka。** 消费者读用 `sendfile`（Java 里 `transferTo`），热数据直接来自 Page Cache，冷数据多一步 DMA 从磁盘读入，慢在磁盘不在拷贝；顺序写加 Page Cache 获得高吞吐。大文件传输不宜走 Page Cache（冲掉热数据、预读用不上），应用直接 I/O。
**业务场景。** 订单日志只 `write` 不 `fsync`，掉电丢最后几十秒；关键账务日志每批写完 `fsync`，等返回才算落盘，攒一批再调一次以摊薄延迟。
**容易错。**
- **以为 write 成功就落盘。**
- **以为零拷贝一次拷贝都没有：** `sendfile` 仍有 2 次 DMA 拷贝，省的是 CPU 拷贝和用户态切换。
- **到处用 sendfile：** 数据不进用户态，无法在应用里加工。
- **以为 inode 里有文件名：** 文件名在目录项里，硬链接可有多个名字；小文件太多耗尽 inode 时 `df -h` 还有空间，`df -i` 才显示满。
