---
id: hi-sdx-derived-view-v2-swap
node: sd.patterns.scaling-reads.more
type: qa
step: 2
---
## Q
**修派生表的 bug：新建 v2 再切换**｜补充 · 扩展读 · 追问

面试官：「生产里消费方在查的一张派生表，背后的转换逻辑发了个 bug。你怎么修？能不能直接 UPDATE 把错的行改掉？」

## A
**结论。** 不要原地打补丁。修好逻辑，从保留的日志或原始数据另建一张 v2，追平后验证，再原子切换消费方，旧 v1 先留着以便回退。

**要点。**
- **第一步：** 修好逻辑，把它当成新的派生视图，从保留的日志或原始数据生成，写到另一张表或索引。
- **第二步：** 让 v2 追平线上位置，和 v1 对比，如行数、抽样差异。
- **第三步：** 原子切换消费方：改别名（alias）、重新定义视图、翻配置开关；v1 先保留一段时间，出问题可以回退。
- **成立的条件：** 输入不可变，视图可重算；这也是批作业能整体重跑的同一性质。
- **原地打补丁的风险：** 消费方会读到修了一半的数据，出问题没有回退路径，还可能漏改一部分行。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<rect x="60" y="8" width="220" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">保留的日志 / 原始数据</text>
<text x="170.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不可变，可重放</text>
<rect x="10" y="90" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v1（线上，有 bug）</text>
<text x="85.0" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">继续服务，先保留</text>
<rect x="180" y="90" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v2（修复逻辑）</text>
<text x="255.0" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① 重算 ② 追平 ③ 对比</text>
<polyline points="115,44 88.8,84.1" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="85,90 86.1,82.4 91.5,85.9" fill="currentColor"/>
<polyline points="225,44 251.2,84.1" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,90 248.5,85.9 253.9,82.4" style="fill:var(--accent,#3b6fd4)"/>
<rect x="70" y="196" width="200" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="210.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">别名 orders_live</text>
<text x="170.0" y="225.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">消费方只认这个名字</text>
<polyline points="150,196 89.9,135.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="85,130 92.2,132.7 87.6,137.2" fill="currentColor"/>
<polyline points="190,196 250.1,135.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,130 252.4,137.2 247.8,132.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ 验证通过后原子改别名指向 v2</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v1 留着，出问题改回去即可回退</text>
</svg>

**面试里这样说。** 「我不会原地改，而是用修好的逻辑从日志另建 v2，追平后和 v1 对比，再通过别名或配置原子切换，v1 留着可以回退。这依赖输入不可变、视图可以重算。」

**易错。**
- **切换前不验证：** 新逻辑可能有别的错，切完才发现，回退窗口已经过去。
- **切换不是原子的：** 先切一半消费方，同一份报表里新旧口径混在一起。
