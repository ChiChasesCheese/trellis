---
id: hi-mock-notification-10-dive-resumable
node: fix.notification-mock
type: qa
step: 10
---
## Q
**通知系统 · 第 10 步 · 深入五：千万级扇出，崩溃之后接着做**｜模拟面试

面试官：「一个活动要发给 1,000 万人。扇出的作业做完前 400 万人之后崩溃了。重启之后，什么状态告诉它前 400 万人已经做完？这个状态存在哪里？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **结论：** 作业库里一张任务表加一张分块表，每块一行，done 的块就是做完的部分；重启读分块表接着做没有 done 的块。
- **切块：** 活动开始时把人群固化成快照 `audience_member(audience_id, seq, user_id)`，seq 编到 1,000 万；每块 10,000 个 seq，共 1,000 块。`campaign_job` 一行一个活动，`campaign_chunk` 主键 (campaign_id, chunk_no)，带状态和租约。
- **一块怎么做：** 认领（租约 60 秒）；读这块 10,000 个 user_id、过滤偏好；发布到 bulk 主题，flush 等 acks=all；最后才标 done。多个 worker 用 `FOR UPDATE SKIP LOCKED` 认领不同块。
- **重启：** 前 400 万 = 块 1 到 400 已 done，块 401 做到一半没标 done；重启后查非 done 的块，601 块接着做。
- **重叠：** 块 401 已发布的消息会再发一次；notification_id = `campaign:{campaign_id}:{user_id}`，状态库唯一约束吸收重复。最多重做 10,000 条，约 10,000 ÷ 40,000 条/秒 = 0.25 秒额度。
- **顺序：** 日志和数据库之间没有事务，所以先发布、后标 done，崩溃最坏是重发不会丢整块；若消息是写进库的 outbox 行，就和块状态同事务提交。唯一错的顺序是先标 done 再发布。
- **状态不放哪：** 不放 worker 内存（崩了没了），也不靠消费者位移（只说明消费到哪，不说明展开到哪）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每一块的四步（顺序是关键）</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">① 认领</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抢租约：lease_until = 现在 + 60 秒</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">② 读与过滤</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">按 seq 范围读 10,000 个 user_id；查偏好</text>
<rect x="8" y="130" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">③ 发布并 flush</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写入 bulk 主题，acks=all</text>
<rect x="8" y="182" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="200.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">④ 标记 done</text>
<text x="18" y="215.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 之后才标；反过来崩溃会丢整块</text>
</svg>
白板上新增：两张表，1,000 块的进度条，和每一块的四步。

**常见失分。**
- **用回调回答进度：** 回调是送达结果，不是展开进度。
- **状态放在内存或位移里：** 一崩就没了，说不清做到哪。
- **先标 done 再发布：** 崩溃时整块无声丢失。
- **不说重叠：** 半块重做会发两次，要说唯一键吸收。

**面试官可能接着问。**
- worker 块中间崩了，租约？ → 60 秒过期后别的 worker 认领整块重做，重叠由唯一键吸收。
- 用一个游标行 next_seq 不行吗？ → 单线程作业可以更简单；分块表是并行版本，40 个 worker 时才需要。
- 块多大？ → 太小分块表写和认领多，太大崩溃重做多；10,000 人对应 0.25 秒额度，重做代价小。
- 扇出时用户退订？ → 发布前过滤一次，发送前再查偏好，退订最迟一分钟内生效。
