---
id: hi-sdx-rel-shuffle-assign
node: more.reliability
type: qa
step: 13
---
## Q
**洗牌分片怎么落地：谁算组合、存在哪、加节点会怎样**｜补充 · 可靠性 · 追问

面试官：「你说每个租户分到 100 台里的 8 台。这 8 台是谁算的、存在哪？网关、存储、查询三层怎么保证看到同一个组合？加一台机器，所有租户都要搬家吗？」

## A
**结论。** 组合不存，现算：每个路由方用同一个确定性函数，以租户 ID 为种子，从当前成员列表（或一致性哈希环）里挑出 k 个节点。成员列表一致，算出来就一致；加减一台节点，每个租户的组合最多变一个成员。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="16" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8 个节点，每个租户随机 2 个</text>
<rect x="8" y="26" width="34" height="30" rx="5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="25" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="49" y="26" width="34" height="30" rx="5" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="66" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="90" y="26" width="34" height="30" rx="5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="107" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="131" y="26" width="34" height="30" rx="5" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="148" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="172" y="26" width="34" height="30" rx="5" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="189" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="213" y="26" width="34" height="30" rx="5" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="230" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="254" y="26" width="34" height="30" rx="5" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="271" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="295" y="26" width="34" height="30" rx="5" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="312" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="8" y="82" font-size="12" font-family="sans-serif" fill="currentColor">租户 A = hash("A") 选出 {1, 3}（实线着色）</text>
<text x="8" y="102" font-size="12" font-family="sans-serif" fill="currentColor">租户 B = hash("B") 选出 {5, 7}（虚线）</text>
<text x="8" y="122" font-size="12" font-family="sans-serif" fill="currentColor">租户 C = {3, 6}：与 A 只共享节点 3</text>
<text x="8" y="150" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A 打死 1 和 3：</text>
<text x="8" y="170" font-size="12" font-family="sans-serif" fill="currentColor">B 不受影响；C 还剩节点 6，重试即可</text>
<text x="8" y="194" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有组合完全等于 {1, 3} 的租户全挂：1/C(8,2) = 1/28</text>
</svg>

**怎么算。**
- **确定性选择：** 以租户 ID 的哈希为种子，在一致性哈希环上从种子位置起依次取 k 个不同的节点；或者用种子初始化伪随机数，从排好序的节点列表里抽 k 个。网关、存储、查询用同一个函数和同一份成员列表，算出同一组节点，不需要一张"租户到节点"的表。
- **成员列表从哪来：** 服务发现或环的存储（etcd、Consul、gossip 的成员表）。各层看到的列表短暂不一致时，算出的组合会差一个节点，写入层要容忍"写到了组合外的节点"，查询层要多查一个。
- **组合大小按租户设：** 普通租户 k 小，隔离好；大租户 k 大，容量够。Grafana Mimir 对写入、查询、存储网关、规则引擎各有一个按租户的分片大小，0 表示用全部实例。

**加减节点。**
- **基于环的选择是稳定的：** 加入或移除一台实例，每个租户的组合最多换一个成员，大部分数据不动。
- **直接用 `hash % N` 抽：** N 一变，所有租户的组合全变，等于全量迁移，不能用。

**数字。**
- **重合概率：** 100 台里每租户 8 台，组合数 C(100, 8) 约 1.86×10¹¹，两个随机租户完全重合的概率约 5×10⁻¹²。Mimir 文档的例子：50 个分区每租户 4 个，约 23 万种组合，两租户完全重合约 0.0004%，完全不相交约 71%。
- **Route 53：** 2048 个虚拟名字服务器，每个域分 4 个，约 7300 亿种组合，并保证任意两个域最多共享 2 个。

**面试里这样说。** 「组合不落表，用租户 ID 做种子在成员环上确定性地挑 k 台，各层算出来一样；加一台机器每个租户最多换一个成员。」
