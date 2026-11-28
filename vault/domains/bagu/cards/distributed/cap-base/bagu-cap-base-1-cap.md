---
id: bagu-cap-base-1-cap
node: a.distributed.cap-base
type: qa
step: 1
---
## Q
**CAP · 为什么「三选二」是误解**｜必会

面试官：「CAP 定理是什么？为什么说三选二是个误解？」

## A
**基本回答。** CAP 定理说的是三个性质不能在分区时同时满足。C（Consistency，一致性）：所有节点读到的都是最新写入；A（Availability，可用性）：每个未故障的节点对每个请求都能给出非错误响应；P（Partition tolerance，分区容错）：网络分区时系统仍继续工作。分布式系统里网络故障是常态，P 躲不开，（所谓 CA 等于假设网络永不故障，只可能是单机。）所以真正的选择是：分区发生时，在 C 和 A 之间二选一；没有分区时两者可以同时拥有。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">账户 X 余额 100，两个机房各存一份</text>
<rect x="8" y="26" width="120" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机房 A</text>
<text x="68" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额 100</text>
<rect x="212" y="26" width="120" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机房 B</text>
<text x="272" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额 100</text>
<line x1="128" y1="48" x2="212" y2="48" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="163" y1="41" x2="177" y2="55" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="163" y1="55" x2="177" y2="41" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">专线断了，互相联系不上</text>
<rect x="8" y="102" width="324" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="125" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选一致（CP）：B 侧拒绝扣款，用户稍后重试</text>
<rect x="8" y="148" width="324" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选可用（AP）：两边都继续扣款，余额分叉</text>
</svg>
一份余额存在两个机房里，中间的线断了：选一致就让一侧拒绝请求，选可用就让两侧各干各的、账本分叉。
**容易错。**
- **以为三个里随便选两个：** P 不是可选的，分布式系统里只能在分区时从 C 和 A 里取一个。
- **以为选了就是一辈子：** 取舍发生在分区的那段时间（Brewer 2012 的重述），并且可以按操作、按时刻分别选，比如扣款选一致、读缓存选可用。
- **把 CAP 的 C 当成 ACID 的 C：** CAP 的 C 是任何一次读都读到最近一次成功的写，像只有一份数据（线性一致，linearizability），ACID 的 C 说的是事务前后约束成立。
- **把 CAP 的 A 当成「大部分时间能用」：** CAP 里的可用性要求每个未故障节点对每个请求都响应；日常说的「99.99% 可用」是另一回事。
- **以为没有分区就没有取舍：** 正常运行时仍要在延迟和一致性之间权衡。
**举个例子。** 账户 X 余额 100，机房 A、B 各一份，专线断了：A 扣 30 记成 70，B 看到的还是 100，同时扣 80 记成 20（选可用），恢复后合并出 100 − 30 − 80 = −10，同一笔钱花了两次。选一致则 B 联系不上 A，没法确认自己的 100 是不是最新，拒绝这笔扣款，代价是这段时间 B 侧用户不能扣款。
