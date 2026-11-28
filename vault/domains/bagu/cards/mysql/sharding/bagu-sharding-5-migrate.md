---
id: bagu-sharding-5-migrate
node: a.mysql.sharding
type: qa
step: 4
---
## Q
**分库分表 · 平滑迁移与回滚**｜必会

面试官：「线上已有 2 亿行的单表，怎么迁到分库分表而不停机？」

## A
**基本回答。** 不停机迁移五步：全量拷贝（开始前先记 binlog 位点，否则拷贝期间的变更会漏）→ 增量同步（binlog 或 CDC 变更数据捕获，从该位点接，追平为止）→ 双写校验 → 灰度切读 → 切写，并始终保留回滚预案。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="8" width="120" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 全量拷贝</text>
<text x="138" y="26" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先记下 binlog 位点</text>
<rect x="8" y="44" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 增量同步</text>
<text x="138" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">从位点接，追平变更</text>
<rect x="8" y="80" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 双写校验</text>
<text x="138" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">定权威库，比校验和</text>
<rect x="8" y="116" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 灰度切读</text>
<text x="138" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">影子读：返回旧库结果</text>
<rect x="8" y="152" width="120" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 切写</text>
<text x="138" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">排空旧写，等最终位点</text>
<line x1="68" y1="34" x2="68" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="68.0,44.0 64.8,37.0 71.2,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="68" y1="70" x2="68" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="68.0,80.0 64.8,73.0 71.2,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="68" y1="106" x2="68" y2="110" stroke-width="1.2" stroke="currentColor"/>
<polygon points="68.0,116.0 64.8,109.0 71.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="68" y1="142" x2="68" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="68.0,152.0 64.8,145.0 71.2,145.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回滚：新库已有写入，旧库就落后</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要先反向同步，再切回，否则丢更新</text>
</svg>
五步自上而下。第一步的位点是不丢数据的起点；最后一步的停写窗口最短：排空旧库写入，等目标库应用到最终位点，再切路由。底部是回滚的注意点。
**每步的坑。**
- **双写不是原子的：** 一边成功一边失败，要定权威库；回灌时不能用旧数据覆盖新数据，要比较 `gmt_modified`。
- **校验不能只比行数：** 按主键分块比校验和与金额总和。
- **灰度切读先做影子读：** 返回旧库结果，后台查新库比对，不一致告警；一致后先切 1% 读流量再放大。
- **回滚：** 新库一旦接受写入，旧库就落后，直接切回会丢更新；要先把新库增量反向同步回旧库再切路由，并在切写前演练。
**业务场景。** 订单库切写后新库变慢想切回，但新库已接收十分钟的订单，直接切回就丢了这十分钟，必须先反向同步。
**容易错。**
- **全量开始前不记位点：** 新库缺数据。
- **以为双写是原子的：** 要有权威库和补偿。
- **直接切回旧库：** 会丢更新。
