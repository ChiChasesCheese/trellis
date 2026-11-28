---
id: bagu-no-loss-3-broker
node: a.mq.no-loss
type: qa
step: 3
---
## Q
**消息不丢 · Broker 端副本配置**｜必会

面试官：「Broker 端副本数和 min.insync.replicas 怎么配？代价是什么？」

## A
**基本回答。** `replication.factor=3`、`min.insync.replicas=2`、`unclean.leader.election.enable=false`：至少两个副本有数据，不允许落后太多的副本当 leader。
默认值不安全：`min.insync.replicas` 和 `default.replication.factor` 默认都是 1，必须显式调大。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="31" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">三台都在</text>
<rect x="84" y="12" width="30" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="99.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R1</text>
<rect x="122" y="12" width="30" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="137.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R2</text>
<rect x="160" y="12" width="30" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R3</text>
<text x="206" y="31" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写入成功</text>
<text x="8" y="77" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">挂一台</text>
<rect x="84" y="58" width="30" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="99.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R1</text>
<rect x="122" y="58" width="30" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="137.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R2</text>
<rect x="160" y="58" width="30" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="175.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">R3</text>
<text x="206" y="77" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仍可写，数据在</text>
<text x="8" y="123" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">挂两台</text>
<rect x="84" y="104" width="30" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="99.0" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R1</text>
<rect x="122" y="104" width="30" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="137.0" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">R2</text>
<rect x="160" y="104" width="30" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="175.0" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">R3</text>
<text x="206" y="123" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ISR&lt;2：拒绝写入</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">replication.factor=3，min.insync.replicas=2</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">unclean.leader.election.enable=false</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">副本分在不同 Broker，最好不同机架</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">选一致性，不选可用性</text>
</svg>
三排分别是三台都在、挂一台、挂两台；高亮的方块是还在 ISR 里的副本。只剩一个时，写入被拒绝。
**举个例子。** 三台 Broker，replication.factor=3，min.insync.replicas=2，acks=all。
1. **三台都在：**ISR 有 3 个，写入需 3 个都写入，成功。
2. **挂一台：**ISR 剩 2 个，满足不少于 2，写入仍成功，数据在两台上。
3. **再挂一台：**ISR 只剩 1 个，小于 2，写入被拒绝，生产者报错并告警。
4. **没配 min.insync 会怎样：**只剩 leader 时 acks=all 也返回成功，这条消息只有一份，机器一坏就丢。
**容易错。**
- **只配副本数 3 不配 min.insync：** ISR 缩到 1 时形同单副本。
- **以为默认就安全：** 默认的副本数和 min.insync 都是 1。
- **为了可用性开 unclean 选举：** 落后副本当 leader，缺的消息永久丢。
- **三个副本放在同一机架：** 一次故障可能同时丢多个。
