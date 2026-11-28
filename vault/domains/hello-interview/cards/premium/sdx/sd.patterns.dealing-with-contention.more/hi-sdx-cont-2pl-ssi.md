---
id: hi-sdx-cont-2pl-ssi
node: sd.patterns.dealing-with-contention.more
type: qa
step: 3
---
## Q
**两阶段锁 vs 可串行化快照隔离**｜补充 · 处理争用 · 追问

面试官：「实现可串行化有两阶段锁（2PL）和可串行化快照隔离（SSI）两条路。各自怎么做到，代价是什么，什么时候选哪个？」

## A
**结论。** 2PL 是悲观的：读加共享锁、写加排他锁，所有锁持有到提交，读写互相阻塞；SSI 是乐观的：在快照上不阻塞地运行，提交时发现危险依赖就中止一个。热点行、冲突多用悲观；读多、冲突少用 SSI。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="10" y="8" width="100" height="34" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="60.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">比较</text>
<rect x="116" y="8" width="106" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2PL（悲观）</text>
<rect x="228" y="8" width="102" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="279.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SSI（乐观）</text>
<rect x="10" y="48" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读写互相阻塞</text>
<rect x="116" y="48" width="106" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">是，锁持有到提交</text>
<rect x="228" y="48" width="102" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="279.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">否，读快照</text>
<rect x="10" y="94" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冲突时</text>
<rect x="116" y="94" width="106" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排队等锁</text>
<rect x="228" y="94" width="102" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="279.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交时中止一个</text>
<rect x="10" y="140" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60.0" y="164.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主要代价</text>
<rect x="116" y="140" width="106" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169.0" y="164.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">死锁、长事务排队</text>
<rect x="228" y="140" width="102" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="279.0" y="164.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中止后重做</text>
<rect x="10" y="186" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60.0" y="210.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更适合</text>
<rect x="116" y="186" width="106" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169.0" y="210.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">热点行、冲突多</text>
<rect x="228" y="186" width="102" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="279.0" y="210.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读多、冲突少</text>
</svg>

**要点。**
- **2PL 的代价：** 死锁（检测出环，杀掉一个牺牲者，应用重试），以及任何事务排在长事务后面时延迟抖动很大。
- **SSI 的代价：** 追踪读写依赖，中止后要重做；冲突一多，重做的工作会爆炸。
- **选择依据：** 冲突频繁时重试是白费功夫，选锁；冲突稀少、读为主，选 SSI，读写互不阻塞。
- **引擎对应：** PostgreSQL 的 SERIALIZABLE 是 SSI；MySQL InnoDB 的 SERIALIZABLE 把普通 SELECT 变成加共享锁的读，属于 2PL 一类；SQL Server 的默认可串行化也基于锁。

**面试里这样说。** 「热点行我直接用锁，因为冲突多时乐观重试是白费；读多写少、冲突少的路径我用 PostgreSQL 的 SERIALIZABLE，代价是必须写重试循环。」

**易错。**
- **以为 SERIALIZABLE 都是加锁实现：** PostgreSQL 的不阻塞，而是事后中止。
- **在高争用路径上用 SSI：** 中止率会随争用快速上升。
