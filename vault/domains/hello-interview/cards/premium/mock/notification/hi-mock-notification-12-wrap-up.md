---
id: hi-mock-notification-12-wrap-up
node: fix.notification-mock
type: qa
step: 12
---
## Q
**通知系统 · 第 12 步 · 收尾：存储、分片键、保留期，以及接下来加什么**｜模拟面试

面试官：「还剩几分钟。你说一个月的请求表每天 5 亿行，一年之后这张表是什么样？分片键选什么？数据要保留多久？最后，你接下来会加什么，什么时候加？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **一分钟总结：** 产品团队调通知 API，消息写进日志，复制成功后回 202；日志按优先级和供应商切成八个主题；worker 查偏好、取令牌、调供应商，失败走带退避的重试主题，五次后进死信，熔断器保护我们；回执和活动各有预留额度；状态库唯一约束去重；活动扇出有分块表，崩溃后接着做；回调加对账兜底。
- **存储：** 5 亿行/天 × 365 = 1.8 × 10^11 行，每行 1 KB = 180 TB/年；热库只留 30 天 = 15 TB，含索引约 30 TB。
- **分片：** 16 片，每片约 1.9 TB；峰值 83k ÷ 16 ≈ 5.2k 行/秒，约单库舒适区（2 万）的四分之一，留余量给重试和回填；8 片时每片 10.4k 已过一半，余量太小。
- **分片键 `hash(notification_id)`：** 均匀（回执 id 来自支付订单号，活动 id 由 campaign 和 user 组合，哈希后都均匀）；唯一约束在单片内成立；按 id 查状态只落一片。不用 campaign_id（一个活动 1,000 万行压一片），不按消息类型（回执和活动量差 4 倍，倾斜）。
- **保留期：** 每片按天分区，每天约 31 GB；第 31 天把元数据（id、状态、时间戳，约 100 字节）导出到对象存储，再 DROP 整个分区（元数据操作，不扫行）；冷数据 335 天 × 5 亿 × 100 字节 ≈ 17 TB，保留 1 年（假设审计要求）。
- **接下来加什么，各有触发：** 备用供应商：熔断累计打开超 1 小时/月；用户历史索引：产品要「我的通知」；每人频次上限：投诉率上升；多区域：业务要求整区故障仍能受理。
- **45 分钟：** 澄清 2、需求 4、估算 4、API 2、高层 7、深入六个共 21、收尾 5。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">接下来加什么：作用 · 代价 · 触发</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">备用供应商（邮件、短信）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：一家挂了可切换；代价：两份合同</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：熔断累计打开 &gt; 1 小时/月</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">按用户查历史的索引</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：「我的通知」；代价：第二份写</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：产品要查用户历史</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">每人频次上限</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：营销每天 ≤ 3 条；代价：每条多一次计数</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：投诉率或退订率上升</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">多区域</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：整区故障时仍可受理；代价：日志跨区</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：业务要求区域级故障下可受理</text>
</svg>
白板上新增：存储与保留期的三层数字，和四个要加的东西。

**常见失分。**
- **分片键是消息类型：** 回执和活动量差 4 倍，倾斜。
- **数字混淆：** 带副本的总量和单库的量混在一起，每片说成 100 TB。
- **「以后加 Kafka、多区域」：** 没有触发条件，分不清是需要还是炫技。
- **保留期说不出机制：** 只说「定时删」，没有按日分区、DROP 分区、先导出元数据。

**面试官可能接着问。**
- 用户查自己的历史？ → 状态库按 notification_id 分片，按用户查要扫 16 片；加一张按 user_id 分片的索引表，单片查询，代价第二份写，产品提出需求时再加。
- 为什么热表只留 30 天？ → 重试窗口和回调迟到都在几天内，更老的只需审计，元数据够。
- 回执和活动的状态库要分开吗？ → 先不分；活动写入拖慢回执状态更新时，再把活动拆到独立集群。
