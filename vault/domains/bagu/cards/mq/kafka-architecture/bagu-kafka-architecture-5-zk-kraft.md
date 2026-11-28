---
id: bagu-kafka-architecture-5-zk-kraft
node: a.mq.kafka-architecture
type: qa
step: 5
---
## Q
**Kafka 结构 · ZooKeeper 与 KRaft**｜追问

面试官：「ZooKeeper 在 Kafka 里起什么作用？KRaft 改了什么？」

## A
**基本回答。** ZooKeeper 管元数据：Broker 注册、Topic 与分区信息、选 controller。KRaft 让 Kafka 自己用 Raft 做元数据仲裁，不再依赖 ZooKeeper（ZooKeeper 模式下，controller 也靠它选出）。
ZooKeeper 时代每个 Broker 启动时到 `/brokers/ids` 下注册；Topic 与分区信息、分区与 Broker 的对应关系也存在 ZooKeeper；controller 负责分区 leader 选举，也靠它选出。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZooKeeper 模式</text>
<text x="186" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">KRaft 模式</text>
<rect x="8" y="26" width="146" height="54" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="81.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZooKeeper</text>
<text x="81.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker 注册</text>
<text x="81.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选 controller</text>
<rect x="186" y="26" width="146" height="54" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="259.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka 自己的控制器</text>
<text x="259.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仲裁（Raft）</text>
<text x="259.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">元数据在自己日志</text>
<rect x="8" y="120" width="46" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="31.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B1</text>
<line x1="31" y1="120" x2="31" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="31.0,82.0 34.2,89.0 27.8,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="186" y="120" width="46" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="209.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B1</text>
<line x1="209" y1="120" x2="209" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="209.0,82.0 212.2,89.0 205.8,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="60" y="120" width="46" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B2</text>
<line x1="83" y1="120" x2="83" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,82.0 86.2,89.0 79.8,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="238" y="120" width="46" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="261.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B2</text>
<line x1="261" y1="120" x2="261" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="261.0,82.0 264.2,89.0 257.8,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="112" y="120" width="46" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="135.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B3</text>
<line x1="135" y1="120" x2="135" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="135.0,82.0 138.2,89.0 131.8,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="290" y="120" width="46" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="313.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B3</text>
<line x1="313" y1="120" x2="313" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="313.0,82.0 316.2,89.0 309.8,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="174" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3.3 起：新集群可用 KRaft 上生产</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4.0 起：完全移除 ZooKeeper</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升 4.0 前：先迁到 KRaft（迁移功能 3.6 起正式可用）</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">少一个外部系统，故障切换更快</text>
</svg>
左边 Broker 都向外部的 ZooKeeper 报到；右边元数据收进 Kafka 自己的控制器仲裁。下方是关键版本。
**举个例子。** 一个老集群，三台 Broker，ZooKeeper 模式，版本 3.2。
1. **想升 4.0：**4.0 只支持 KRaft，ZooKeeper 模式的集群不能直接升。
2. **先升级：**版本升到 3.9 这类过渡版本（迁移功能 3.6 起正式可用）。
3. **迁移：**按官方文档把元数据从 ZooKeeper 迁到 KRaft。
4. **再升 4.0：**之后没有 ZooKeeper，少部署一套系统。
**容易错。**
- **以为 ZooKeeper 存消息：** 它只管元数据，消息存在 Broker 的分区日志里。
- **以为 controller 是独立服务：** 它是一个被选出来的 Broker。
- **以为 4.0 还能继续用 ZooKeeper：** 4.0 完全移除了。
- **背迁移细节：** 具体路径和过渡版本以官方文档为准，面试说清楚动机和关键版本即可。
