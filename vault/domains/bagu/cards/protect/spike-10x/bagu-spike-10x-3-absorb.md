---
id: bagu-spike-10x-3-absorb
node: a.protect.spike-10x
type: qa
step: 3
---
## Q
**QPS 突增十倍 · 入口、缓存、队列各怎么削峰**｜必会

面试官：「判断是真实流量后，10 万 QPS 怎么不全部打到数据库？」

## A
**基本回答。** 三层吸收：入口，CDN 和边缘缓存直接回答可缓存请求，网关按优先级、用户、IP 限流，超限 429；读靠缓存，数据库压力 = QPS × (1 − 命中率)；写先入 Kafka，接口立即返回「处理中」，消费者按库能承受的速度落库，把尖峰削成平缓的长流。缓存要防击穿（热点 key 过期瞬间大量请求冲向库，要互斥回源或预热）；热 key 拆成多个子 key 分散到不同节点；队列积压要设上限，超过就拒绝并明确过期任务丢弃，否则队列成新的内存炸弹；异步写要带幂等键，防重复提交和消费重试。削峰是先收下再慢慢处理，限流是直接拒绝，两者配合。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<rect x="8" y="6" width="118" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="25.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户请求</text>
<text x="134" y="26" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 万 QPS 涌来</text>
<line x1="67" y1="38" x2="67" y2="49" stroke-width="1.2" stroke="currentColor"/>
<polygon points="67.0,49.0 70.2,42.0 63.8,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="49" width="118" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="68.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CDN、边缘缓存</text>
<text x="134" y="69" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可缓存的请求不再往里走</text>
<line x1="67" y1="81" x2="67" y2="92" stroke-width="1.2" stroke="currentColor"/>
<polygon points="67.0,92.0 70.2,85.0 63.8,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="92" width="118" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关限流</text>
<text x="134" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按优先级、用户、IP，超限 429</text>
<line x1="67" y1="124" x2="67" y2="135" stroke-width="1.2" stroke="currentColor"/>
<polygon points="67.0,135.0 70.2,128.0 63.8,128.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="135" width="118" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="67.0" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 缓存（读）</text>
<text x="134" y="155" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">命中 99%，只漏下 1000</text>
<line x1="67" y1="167" x2="67" y2="178" stroke-width="1.2" stroke="currentColor"/>
<polygon points="67.0,178.0 70.2,171.0 63.8,171.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="178" width="118" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="197.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka 队列（写）</text>
<text x="134" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按库能承受的速度消费</text>
<line x1="67" y1="210" x2="67" y2="221" stroke-width="1.2" stroke="currentColor"/>
<polygon points="67.0,221.0 70.2,214.0 63.8,214.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="221" width="118" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="240.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="134" y="241" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只吃到少量读和平缓的写</text>
</svg>
请求自上而下被一层层吸收，高亮的缓存层挡掉绝大部分读，剩下的写靠队列放平。
**业务场景。** 10 万 QPS 读：命中率 90% 库收 1 万，99% 收 1000，99.9% 收 100；从 99% 掉到 90% 落库流量放大十倍，所以热点 key 要预热并防击穿、雪崩。直播评论洪峰：评论先写队列再落库，读走缓存和批量推送，队列积压超阈值就丢弃最老的评论展示，而不是让写入超时。
**容易错。**
- **以为缓存越多越好：** 命中率才是关键。
- **以为队列能无限堆。**
- **以为异步写不用幂等。**
