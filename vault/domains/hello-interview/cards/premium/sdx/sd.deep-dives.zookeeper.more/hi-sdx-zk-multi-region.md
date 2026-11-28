---
id: hi-sdx-zk-multi-region
node: sd.deep-dives.zookeeper.more
type: qa
step: 9
---
## Q
**一个共识集合拉伸到多区域，每次写多一个往返**｜补充 · ZooKeeper · 加分

面试官：「为了让协调服务扛住整个区域故障，你把 5 个节点分到三个区域（2、2、1），区域间往返约 60 ms。每次写的延迟大概多少？有没有更好的部署方式？」

## A
**结论。** 每次写约 60 ms，而单区域内通常是几毫秒以内。多数是 3 票，领导者所在区域只有 2 票，必须再等另一个区域的一票，要付一个区域间往返。更好的默认是每个区域一个独立集合，另有一个小的全局集合只放必须全局唯一的决定。

**要点。**
- **为什么要三个区域：** 2、2、1 的分布下，丢掉任何一个区域仍剩至少 3 个节点，能容忍整个区域故障；只有两个区域的话，区域间断开整个集合不可写。
- **写延迟：** 领导者加同区域一个邻居共 2 票，不足多数，必须等另一区域的确认，所以每次写至少一个区域间往返，约 60 ms，比单区域慢一到两个数量级。锁的获取与释放、选主、配置变更都变慢。
- **读：** 本地读不受影响，但可能陈旧。
- **更好的方案：** 区域内锁和选主走区域内的独立集合（几毫秒）；少量必须全局唯一的决定（如全局配置、数据归属区域）放到小的全局集合，接受 60 ms 级延迟。
- **取舍：** 区域内集合不能保证跨区域互斥。要远端读可以放不投票的 observer。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="10" y="10" width="96" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="34.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 A</text>
<text x="58.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">领导者 + 1 台</text>
<rect x="122" y="10" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="34.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 B</text>
<text x="170.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2 台</text>
<rect x="234" y="10" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="34.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 C</text>
<text x="282.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 台</text>
<text x="10" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写要多数 3 票，区域 A 内只有 2 票</text>
<text x="10" y="110" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">必须再等 B 或 C 的一票</text>
<text x="10" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">提交 ≈ 1 个区域间往返 ≈ 60 ms</text>
<text x="10" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">更好：每区域一个独立集合（≈ 几 ms）</text>
<text x="10" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全局集合只放少量必须全局唯一的决定</text>
</svg>

**面试里这样说。** 「把一个集合拉伸到三个区域，每次写都要等一个区域间往返，约 60 ms。我会每个区域部署独立集合处理区域内协调，再放一个小的全局集合，只负责真正需要全局唯一答案的少量决定。」

**易错。**
- **为了高可用把所有锁放在跨区域集合上：** 所有锁操作都慢了几十倍。
- **只用两个区域各放一半节点：** 区域间断开时两边都没有多数，整个集合不可写。
