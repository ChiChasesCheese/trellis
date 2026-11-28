---
id: hi-mock-uber-03-nonfunctional
node: sd.problem-breakdowns.uber.mock
type: qa
step: 3
---
## Q
**网约车 · 第 3 步 · 非功能需求与估算**｜模拟面试

面试官：「好。再说说非功能需求，有没有什么数字你想先算一下？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **低延迟匹配：** 「叫车后一分钟内，要么匹配成功，要么明确告诉乘客失败。」
- **匹配强一致：** 「同一个司机同一时刻不能被派两单；一个订单同一时刻也只问一位司机。」
- **高吞吐：** 「活动散场时，同一地点可能一次来 10 万个叫车请求，一个都不能丢。」
- **先算位置写入：** 「1000 万司机 ÷ 5 秒 = 每秒 200 万次位置更新。」
- **再算成本：** 「每条约 100 字节：200 万 × 100 字节 ≈ 每秒 200 MB。每天 200 万 × 86400 ≈ 1728 亿次写入，按托管键值库每百万次写 1.25 美元，约 21.6 万美元一天。所以位置不能直接写进普通数据库。」
- **再算能问几位：** 「每位司机 10 秒内决定：60 秒 ÷ 10 秒 = 最多问 6 位。名单排好序，问完没人接，就明确告诉乘客失败。」
- **线外：** 「隐私合规（GDPR）、容灾、监控、持续发布，我只提一句，不展开。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 360">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非功能需求 → 数字 → 逼出什么设计</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">低延迟：一分钟内匹配或明确失败</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">60 秒 ÷ 10 秒每位 = 最多问 6 位司机</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 候选名单有上限，超时要明确报失败</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">强一致：一司机同一时刻只收一单</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一个订单同一时刻也只问一位司机</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 司机锁（深入二）</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">高吞吐①：司机位置上报</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1000 万 ÷ 5 秒 = 200 万次写/秒</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 约 21.6 万美元/天，不能直接写库（深入一）</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">高吞吐②：活动散场同地点 10 万请求</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求不能丢，实例崩溃也不能丢</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 队列 + 分片（深入三）</text>
<text x="8" y="314" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写入量：200 万 × 100 字节 ≈ 200 MB/秒</text>
<text x="8" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天 1728 亿次 × 1.25 美元/百万次</text>
<text x="8" y="350" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线外：隐私合规、容灾、监控、持续发布</text>
</svg>
白板上新增：四张便签，每张三行：需求、数字、它逼出的设计。后面的深入问题就从这四张里选。
**为什么这样说。** （约 2 分钟，累计第 5 分钟。）面试官看数字能不能变成设计决定。强的回答每一条非功能需求都带一个数字和一个去向：200 万次/秒推出「不能直接写库」，10 万同地点推出「队列加分片」，一分钟推出「最多问 6 位」。弱的回答只说「要高可用、高并发」，没有数字，也没有去向。
**面试官可能接着问。**
- 为什么强一致排在这里？ → 派单出错代价最大：一个司机收到两单，总有一位乘客白等。位置差几十米、几秒影响很小，所以位置可以稍旧，派单必须严格互斥。
- 200 万次写能少一点吗？ → 能。司机端按速度自适应上报，静止时每 15 秒一次、移动时每 5 秒一次：假设一半静止，写入约降到每秒 133 万。深入一再展开。
- 读多还是写多？ → 位置是写多读少：每秒 200 万次写，读只发生在叫车时查附近司机，量级和叫车请求相当，小得多。
**常见失分。**
- **只说空话：** 「高可用、可扩展」没有数字，面试官无法判断你要的是什么系统。
- **算了不用：** 算出 200 万次/秒却没说它改变了哪个决定，估算就成了表演。
- **漏掉强一致：** 网约车最容易出错的是一人两单，这条不提，后面的锁就没有来由。
