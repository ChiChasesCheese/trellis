---
id: hi-sdx-cdc-compacted-bootstrap
node: sd.deep-dives.change-data-capture.more
type: qa
step: 2
---
## Q
**压缩主题当作新消费者的起点**｜补充 · 变更数据捕获（CDC） · 追问

面试官：「A 团队给每个新的 CDC 消费者都做一遍「快照加日志位置」；B 团队只让新消费者从压缩主题的 offset 0 开始读。B 为什么可以省掉快照？他们的变更事件要满足什么？」

## A
**结论。** 日志压缩保证每个键至少留下最新一条记录，所以压缩后的主题本身就是当前数据集的完整副本加最近的历史。从 offset 0 读完，就得到完整起点，并且无缝接上实时更新。没有单独的快照流程，也没有位点拼接要出错，第十个消费者和第一个一样用。

**要点。**
- **事件必须自成一体：** 以主键为 key，带整行的 after 镜像，不是差量；压缩会丢掉同键的旧事件，留下的那一条要能独立表示该行。
- **删除要写墓碑：** 删除写成值为空的记录（Debezium 默认在删除事件之后再写一条墓碑），否则已删除的行会对每个新消费者复活。
- **首次填充仍需一次快照：** 主题第一次被填充时做一次，之后新消费者都不用再做。
- **代价：** 启动耗时随存活键的数量增长；读到尾部之前，看到的是新旧混合的状态，消费者仍要幂等 upsert。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 282">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">压缩主题：新消费者从 offset 0 读</text>
<rect x="8" y="26" width="100" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">offset 0 起</text>
<text x="58.0" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每键最新值</text>
<polyline points="108,49 119.0,49.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="126,49 119.0,52.2 119.0,45.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="126" y="26" width="86" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="169.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读到尾部</text>
<text x="169.0" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">追上实时</text>
<polyline points="212,49 223.0,49.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230,49 223.0,52.2 223.0,45.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="230" y="26" width="102" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="281.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">继续订阅</text>
<text x="281.0" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实时变更</text>
<line x1="8" y1="92" x2="332" y2="92" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">事件的两个必要性质</text>
<text x="8" y="136" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 以主键为 key，带整行 after 镜像</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">   压缩只留每键最新一条，它必须自成一体</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 删除写成墓碑（值为空的记录）</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">   否则已删除的行会复活给每个新消费者</text>
<line x1="8" y1="214" x2="332" y2="214" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：启动耗时随存活键数量增长，</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读到尾部之前看到的是新旧混合的状态</text>
</svg>

**面试里这样说。** 「我让变更主题走压缩，事件是带主键的整行镜像，删除写墓碑。新消费者从头读就是完整起点，不用再做快照；它读完追上尾部就进入实时。」

**易错。**
- **事件只带差量：** 压缩之后差量丢了一部分，从头读出来的状态是错的。
- **主题用的是按时间删除而不是压缩：** 超过保留期的键永远读不到，起点不完整。
