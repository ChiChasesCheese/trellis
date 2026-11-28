---
id: hi-sdx-ch-rebalance-storm
node: sd.core-concepts.consistent-hashing.more
type: qa
step: 3
---
## Q
**自动重平衡为什么会放大故障**｜补充 · 一致性哈希 · 追问

面试官：「某个节点因为一次 GC 停顿被判定下线，集群立刻自动重平衡，结果别的节点也被拖垮。为什么全自动、不限速的重平衡会把小故障变成事故？标准护栏有哪些？」

## A
**结论。** 重平衡消耗的恰好是集群此刻最缺的资源：磁盘 IO、网络和页缓存。误判下线引发复制，复制拖慢其他节点，它们又被判下线，形成死亡螺旋，没丢一台机器也能搞垮集群。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<rect x="10" y="8" width="250" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="135.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 节点 GC 停顿或磁盘变慢</text>
<text x="135.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">心跳超时，被误判下线</text>
<polyline points="135,48 135.0,59.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="135,66 131.8,59.0 138.2,59.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="66" width="250" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="135.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 集群开始复制它的数据</text>
<text x="135.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">占用磁盘 IO、网络、页缓存</text>
<polyline points="135,106 135.0,117.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="135,124 131.8,117.0 138.2,117.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="124" width="250" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="135.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 其他节点被拖慢</text>
<text x="135.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">心跳也开始超时</text>
<polyline points="135,164 135.0,175.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="135,182 131.8,175.0 138.2,175.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="182" width="250" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="135.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 它们也被判下线</text>
<text x="135.0" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">更多数据要复制</text>
<polyline points="260,202 300,202 300,86 267,86" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260,86 267,82.8 267,89.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">护栏：限速（带宽与并发恢复数）、</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">延迟触发（离开几分钟后才搬）、</text>
<text x="8" y="278" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">最大的搬迁由运维批准后执行。</text>
</svg>

**要点。**
- **限速：** 限制数据传输带宽和并发恢复数，例如 Elasticsearch 的 cluster.routing.allocation.node_concurrent_recoveries 与恢复带宽上限，Cassandra 的出站流吞吐上限。
- **延迟触发：** 节点离开几分钟后才开始搬，因为多数下线其实是重启。Elasticsearch 的 index.unassigned.node_left.delayed_timeout 默认 1 分钟。
- **人在回路：** 系统自动给出方案，最大的搬迁由运维批准后再执行。
- **故障检测别太敏感：** 阈值过紧，误判会频繁触发这条链。

**面试里这样说。** 「节点下线我不会立刻重平衡：先等几分钟，因为多数是重启；真要搬就限速、限并发，免得复制流量把其他节点拖过故障检测阈值，引发连锁下线。」

**易错。**
- **只想着尽快恢复副本数：** 副本数暂时少一份，通常比整个集群抖动要便宜得多。
- **只限速不延迟：** 短暂重启也会引来一轮无谓的搬迁和读放大。
