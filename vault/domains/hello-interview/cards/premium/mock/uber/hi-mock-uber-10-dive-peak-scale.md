---
id: hi-mock-uber-10-dive-peak-scale
node: sd.problem-breakdowns.uber.mock
type: qa
step: 10
---
## Q
**网约车 · 第 10 步 · 深入三：高峰不丢单，扩展，收尾**｜模拟面试

面试官：「活动散场，同一个地方 10 万人同时叫车，而且某个匹配实例刚好崩了。你的设计会怎样？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **问题：** 叫车服务直接调匹配服务，突发流量来了扩容赶不上，请求被丢；实例崩了，它手里的请求也没了，乘客无限期地等。
- **队列加动态扩容：** 叫车服务写完 Ride 就把订单放进队列，匹配服务从队列取；积压变大就加实例，队列按区域分区。用托管的 Kafka（MSK、Confluent）：要的是偏移量语义和重放，SQS 更省心但不保序；扩容和高可用交给云。
- **不丢单的关键：** offset 等匹配接手成功才提交（有工作流时是工作流启动、状态持久化之后）；实例中途崩了消息还在，新实例接着处理。
- **重复处理要幂等：** 至少一次投递，同一订单可能处理两次，会发给第二位司机、违反一次只问一位；用订单号作工作流 ID，同一订单只有一个工作流在跑，或在订单上用条件更新占住当前报价。
- **队头阻塞：** 先进先出时一个慢请求挡住后面的，换优先级队列或再细分区域分区；热点区域细分成更小的格子分到不同实例。
- **再扩展：** 纵向扩容贵、有上限、升级要停机、仍是单点，不选；按城市或区域分片，服务、队列、数据库都按区域切并加读副本，请求在本区域内处理、延迟更低；只有两个区域边界附近的近邻搜索要查两片再合并。
- **收尾：** 位置用 Redis 地理存储；司机用带 TTL 的锁加工作流，一人一单、不响应换人；请求先入队不丢；按区域分片。没展开的是监控、隐私合规、容灾。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 410">
<rect x="18" y="8" width="304" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乘客 · 司机客户端（带位置）</text>
<rect x="18" y="64" width="304" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">路由：按位置选区域</text>
<polyline points="170,38 170,64" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,64 166.8,57.0 173.2,57.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="18" y="126" width="92" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="64" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上海区域</text>
<polyline points="64,94 64,126" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="64,126 60.8,119.0 67.2,119.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="124" y="126" width="92" height="34" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="170" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">北京区域</text>
<polyline points="170,94 170,126" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,126 166.8,119.0 173.2,119.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="230" y="126" width="92" height="34" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="276" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">纽约区域</text>
<polyline points="276,94 276,126" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="276,126 272.8,119.0 279.2,119.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="76" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">相邻区域的边界处：查两个分片再合并</text>
<polyline points="64,160 64,198" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="64,198 60.8,191.0 67.2,191.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="198" width="324" height="196" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="170" y="213" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上海区域里面：每个区域同一套</text>
<rect x="16" y="232" width="72" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="52" y="254" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关</text>
<rect x="16" y="290" width="72" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="52" y="306.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<text x="52" y="321.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">区域分区</text>
<rect x="96" y="232" width="72" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="132" y="254" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叫车服务</text>
<rect x="96" y="290" width="72" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="132" y="306.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配服务</text>
<text x="132" y="321.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">多实例</text>
<rect x="176" y="232" width="72" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="254" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置服务</text>
<rect x="176" y="290" width="72" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="306.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="212" y="321.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">地理 + 锁</text>
<rect x="256" y="232" width="72" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="292" y="254" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知服务</text>
<rect x="256" y="290" width="72" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292" y="306.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="292" y="321.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">含读副本</text>
<text x="16" y="354" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">请求在本区域内处理：离用户近，延迟低</text>
<text x="16" y="372" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">吞吐随区域数增加；读副本分担读</text>
</svg>
白板上新增：入口路由、三个区域，展开其中一个区域的整套组件；相邻区域边界处的跨片查询。

**常见失分。**
- **不提不丢单：** 只说「加队列」，不说偏移量什么时候提交。
- **忘记重复处理：** 至少一次投递会重复，不说幂等是高级候选人常被抓的地方。
- **没有收尾：** 面试官只记得最后一个深入问题。
