---
id: bagu-mysql-es-sync-1-cdc-dual-write
node: b.search.mysql-es-sync
type: qa
step: 1
---
## Q
**MySQL 到 ES 同步 · 双写、定时与 CDC**｜追问

面试官：「订单搜索走 ES，订单状态以 MySQL 为准。MySQL 的数据怎么同步到 ES？双写和 CDC 各有什么问题？」

## A
**基本回答。** MySQL 是准，ES 是可重建的副本，同步要让 ES 最终追上 MySQL。三类方案：应用层双写、定时扫描、订阅 binlog 的 CDC（Canal、Debezium、Flink CDC）。推荐 CDC 加定期对账。双写无法组成一个事务：MySQL 成功后应用崩溃或 ES 写失败都不一致；ES 超时只是结果未知，可能已写入，重试必须幂等；两次并发更新还会乱序，业务代码侵入大。定时同步简单但延迟高，删除和扫描窗口要额外处理。CDC 从 binlog 读变更，业务无感，要维护位点（断点续传）并衔接全量导入。一致性手段：MySQL 主键作 ES `_id`，重复写变更新，天然幂等；同一主键的事件进同一个 MQ 分区保证有序，再带版本号用 `version_type=external` 丢弃旧版本；DELETE 显式转成 ES 删除；多表聚合文档时某表变化要回查并重建受影响的文档；Bulk 逐条检查结果、只重试暂时性错误，失败重试加死信，ES 写入慢时向上游背压而不是无界队列；最后定期按主键范围或更新时间对账，差异就重刷。Canal 伪装成 MySQL 从库解析 binlog，轻量、只面向 MySQL，适合简单一对一；Flink CDC 基于 Debezium，统一全量快照和增量，有检查点，多数据源，能做关联聚合，但要维护 Flink 集群。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 128">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">双写：两个系统没有共同的事务</text>
<rect x="6" y="26" width="70" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用</text>
<line x1="76" y1="41" x2="111.0" y2="41.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118,41 111.0,44.2 111.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="26" width="80" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="158" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MySQL</text>
<line x1="198" y1="41" x2="255.0" y2="41.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="262,41 255.0,44.2 255.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="214" y="22" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩了</text>
<rect x="262" y="26" width="72" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ES</text>
<text x="6" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">MySQL 已改，ES 没更新：两边不一致</text>
<text x="6" y="102" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ES 超时结果未知，重试必须幂等；</text>
<text x="6" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两次并发更新还会乱序</text>
</svg>
双写的问题：应用写完 MySQL 之后崩了，ES 就永远是旧的。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="6" y="6" width="236" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MySQL（以它为准）</text>
<text x="124" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">变更写进 binlog</text>
<line x1="124" y1="44" x2="124.0" y2="51.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,58 120.8,51.0 127.2,51.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="58" width="236" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="124" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CDC：Canal / Debezium / Flink CDC</text>
<text x="124" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读 binlog，业务无感</text>
<line x1="124" y1="96" x2="124.0" y2="103.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,110 120.8,103.0 127.2,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="110" width="236" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ：同一主键进同一分区</text>
<text x="124" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">保证同一条记录的事件有序</text>
<line x1="124" y1="148" x2="124.0" y2="155.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,162 120.8,155.0 127.2,155.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="162" width="236" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者：_id = MySQL 主键</text>
<text x="124" y="192.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">version_type=external 丢旧版本</text>
<line x1="124" y1="200" x2="124.0" y2="207.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,214 120.8,207.0 127.2,207.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="214" width="236" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="233" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ES：可重建的副本</text>
<line x1="242" y1="232" x2="330" y2="232" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="330" y1="232" x2="330" y2="25" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="330" y1="25" x2="251.0" y2="25.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="244,25 251.0,21.8 251.0,28.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="250" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">定期对账：</text>
<text x="250" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按主键范围</text>
<text x="250" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">比较，差异</text>
<text x="250" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">就重刷</text>
</svg>
推荐的链路：从 MySQL 变更日志一路流到 ES，右边的虚线是定期对账，作为最后的兜底。
**举个例子。** 订单 O1 先「未支付」（版本 1），再「已支付」（版本 2）。事件乱序时 ES 先写版本 2，再收到迟到的版本 1 覆盖回「未支付」，MySQL 已支付而 ES 显示未支付；带 `version_type=external` 后版本 1 因版本更小被丢弃。O1 被删除时 binlog 是 DELETE 事件，不转成 ES 删除搜索就会一直返回已删订单。
**容易错。**
- **把 ES 超时当成失败：** 可能已写入，重试靠 `_id` 幂等。
- **以为有了 CDC 就不用对账：** CDC 也可能漏、重。
