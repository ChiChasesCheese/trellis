---
id: bagu-nosql-selection-1-types-olap
node: b.search.nosql-selection
type: qa
step: 1
---
## Q
**NoSQL 选型 · 什么数据放什么存储**｜追问

面试官：「订单数据想从 MySQL 迁到 MongoDB，你要评估哪些方面？运营的实时报表为什么不直接查 MySQL？」

## A
**基本回答。** NoSQL 为水平扩展和灵活数据模型，放弃了部分事务和关联查询。四类：键值（Redis，缓存计数）、文档（MongoDB，结构多变、按文档整取）、宽列（HBase、Cassandra，海量写入加范围扫描）、图（Neo4j，多跳关系）。资金和订单依赖事务和多表关联，默认留关系库；既要分布式又要事务选 NewSQL（TiDB、OceanBase）。订单迁 MongoDB 看三件事：事务（单文档原子；多文档事务副本集 4.0、分片集群 4.2 起支持，但官方说代价更高，应靠内嵌文档建模少用）、查询模式（任意条件多表关联还是按文档整取）、运维成本（备份、分片、团队熟悉度）。MongoDB 默认引擎 WiredTiger（3.2 起）是 B+ 树；写入友好的 LSM 是 HBase、Cassandra、RocksDB。报表用列式 OLAP（Doris、ClickHouse）：按列存储只读用到的列，同列类型相同压缩率高，向量化聚合快；MySQL 行存要读整行。Hive 是 HDFS 上的批处理，延迟分钟到小时，不适合实时看板；时序库按「时间加标签」存监控指标，写多读聚合，自带降采样和过期。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<rect x="4" y="6" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存、计数、会话</text>
<line x1="154" y1="23" x2="159.0" y2="23.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,23 159.0,26.2 159.0,19.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="6" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键值：Redis</text>
<rect x="4" y="46" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结构多变，按文档整取</text>
<line x1="154" y1="63" x2="159.0" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,63 159.0,66.2 159.0,59.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="46" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文档：MongoDB</text>
<rect x="4" y="86" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">海量写入加范围扫描</text>
<line x1="154" y1="103" x2="159.0" y2="103.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,103 159.0,106.2 159.0,99.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="86" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宽列：</text>
<text x="251" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HBase、Cassandra</text>
<rect x="4" y="126" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多跳关系</text>
<line x1="154" y1="143" x2="159.0" y2="143.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,143 159.0,146.2 159.0,139.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="126" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">图：Neo4j</text>
<rect x="4" y="166" width="150" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="79" y="187" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">资金、订单，要事务</text>
<line x1="154" y1="183" x2="159.0" y2="183.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,183 159.0,186.2 159.0,179.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="166" width="170" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="251" y="187" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关系库：MySQL（默认）</text>
<rect x="4" y="206" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="227" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">既要分布式又要事务</text>
<line x1="154" y1="223" x2="159.0" y2="223.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,223 159.0,226.2 159.0,219.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="206" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">NewSQL：</text>
<text x="251" y="234.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TiDB、OceanBase</text>
<rect x="4" y="246" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="267" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">报表、聚合分析</text>
<line x1="154" y1="263" x2="159.0" y2="263.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,263 159.0,266.2 159.0,259.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="246" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="259.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">列式 OLAP：</text>
<text x="251" y="274.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Doris、ClickHouse</text>
<rect x="4" y="286" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79" y="307" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">监控指标</text>
<line x1="154" y1="303" x2="159.0" y2="303.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="166,303 159.0,306.2 159.0,299.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="166" y="286" width="170" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="307" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时序库：时间加标签</text>
</svg>
左边是数据或访问的特点，右边是对应的存储；资金和订单默认留在关系库（蓝色）。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">行存（MySQL）</text>
<text x="186" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">列存（Doris）</text>
<rect x="6" y="22" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="30" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id</text>
<rect x="54" y="22" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">档位</text>
<rect x="102" y="22" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金额</text>
<rect x="6" y="46" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="30" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="54" y="46" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">小</text>
<rect x="102" y="46" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="6" y="70" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="30" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="54" y="70" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中</text>
<rect x="102" y="70" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<rect x="6" y="94" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="30" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="54" y="94" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大</text>
<rect x="102" y="94" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">500</text>
<rect x="186" y="22" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id</text>
<rect x="234" y="22" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">档位</text>
<rect x="282" y="22" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="306" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金额</text>
<rect x="186" y="46" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="234" y="46" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">小</text>
<rect x="282" y="46" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="306" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="186" y="70" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="234" y="70" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中</text>
<rect x="282" y="70" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="306" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<rect x="186" y="94" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="234" y="94" width="48" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大</text>
<rect x="282" y="94" width="48" height="24" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="306" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">500</text>
<text x="6" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">SUM(金额)：</text>
<text x="6" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">也要读整行的每一列</text>
<text x="186" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只读金额一列，</text>
<text x="186" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同列压缩率高</text>
<text x="6" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（高亮的格子 = 要读的数据，数值为示意）</text>
</svg>
同样算金额合计，行存必须读整行，列存只读金额那一列。
**业务场景。** 直播打赏看板按小时统计各档位金额，直接对 MySQL 订单表 `GROUP BY` 要读整行、扫大量数据，还拖慢线上库；流水同步进 Doris，只读时间、档位、金额三列，线上库不受影响。
**容易错。**
- **以为 NoSQL 一定比 MySQL 快或更先进：** 它换来扩展和灵活，放弃了事务和关联。
- **把 Hive 当实时看板：** 它是批处理。
