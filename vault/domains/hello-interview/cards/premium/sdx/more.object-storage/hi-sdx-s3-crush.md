---
id: hi-sdx-s3-crush
node: more.object-storage
type: qa
step: 3
---
## Q
**放置组加确定性放置：加节点不改元数据**｜补充 · 对象存储（S3） · 加分

面试官：「对象存储的元数据里只记每个对象的放置组（PG）号，不记存储节点地址。为什么加一批新节点，不用改写几百 TB 的元数据？」

## A
**结论。** 对象到放置组是对名字的固定哈希；放置组到节点由 CRUSH 这类确定性函数，按「放置组号 + 集群地图」现算。加节点只改集群地图，重算后只有一小部分放置组换位置，元数据一条都不用改，客户端和存储节点也无需查表，就能独立算出同样的答案。

**要点。**
- **两层映射：** 对象名哈希到放置组，放置组经 CRUSH 得到一组节点。
- **元数据只存稳定的东西：** 放置组号不随拓扑变化。
- **加节点的代价：** 数据按新地图迁移，迁移量约等于新容量占比：100 台加 10 台，约 10/110 ≈ 9% 的放置组换位置。
- **故障域规则：** 地图里写明同一放置组的副本或片要分散在不同机架、可用区。
- **对比显式清单：** 每个对象存节点列表，拓扑一变就要改写所有受影响的元数据行，是 TB 级的写放大。
- **要预先规划：** 放置组数太少不均匀，太多则开销大；地图要带版本，客户端地图过期会被存储节点纠正。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="10" y="28" width="74" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="47.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对象名</text>
<rect x="124" y="28" width="80" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="164.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">放置组</text>
<text x="164.0" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">PG</text>
<polyline points="84,47 124,47" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="124.0,47.0 117.0,43.8 117.0,50.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="104" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">哈希</text>
<rect x="244" y="14" width="86" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="287.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 1</text>
<rect x="244" y="48" width="86" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="287.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 2</text>
<rect x="244" y="82" width="86" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="287.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 3</text>
<polyline points="204,47 244,28" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="244.0,28.0 236.3,28.1 239.1,33.9" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="204,47 244,62" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="244.0,62.0 238.6,56.5 236.3,62.5" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="204,47 244,96" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="244.0,96.0 242.1,88.6 237.1,92.6" style="fill:var(--accent,#3b6fd4)"/>
<text x="164" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CRUSH(PG, 集群地图)</text>
<rect x="70" y="124" width="200" height="30" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="170.0" y="143.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群地图：新增节点只改这里</text>
<text x="10" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">元数据只存 PG 号，加节点不用改写</text>
<text x="10" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有约 10/110 ≈ 9% 的 PG 换位置</text>
</svg>

**面试里这样说。** 「元数据只存放置组号，放置组到节点用 CRUSH 按集群地图现算。加节点改的是地图，大约新容量占比的放置组会迁移，元数据不用动。如果存的是节点列表，拓扑一变就要改写几百 TB。」

**易错。**
- **以为不用迁移数据：** 数据要迁，只是元数据不用改。
- **放置组数选得太小：** 负载不均，且以后无法细粒度迁移。
