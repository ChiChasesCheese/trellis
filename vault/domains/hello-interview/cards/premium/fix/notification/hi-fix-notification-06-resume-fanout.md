---
id: hi-fix-notification-06-resume-fanout
node: fix.notification
type: qa
step: 6
---
## Q
**通知系统 · 活动扇出崩了怎么续**｜复盘

面试官：「一个活动要发给 1,000 万用户。扇出任务在发完 400 万之后崩了。重启之后，什么状态告诉它前 400 万已经处理过？这个状态存在哪里？」

你会怎么回答？

## A
**当时的回答。** 同一个问题被问了三遍：先答受众存在哪个库（27:51），再答分批和限速（30:41，面试官说「I still don't hear what records progress」），最后转到 webhook 和 cron（32:25），讲的都是投递状态，没有任务进度。

**应该这样说。**
- **两种状态别混：** 投递状态（每条到没到）靠 webhook 加对账；任务进度（扇出做到第几个用户）必须在任务自己的记录里。
- **游标：** 任务表存 `cursor_user_id`，受众按 user_id 顺序读，每块 10,000 个，共 1,000 块；状态就在这个库里，任务一行，要看每块进度再加 1,000 行的块表。
- **同一个事务：** 读下一块（`user_id > 游标` 取 10,000 个）、写这块的通知行、把游标推到这块最大的 user_id，一起提交。游标先写，崩了丢 10,000 人；游标后写只是重复，被唯一键（活动号 + 用户号）吸收。
- **崩溃之后：** 读游标继续，400 万完成就从第 401 块开始，最多重做 1 块，约 1.8 秒（每秒发 5,600 条）；重做的行 INSERT 返回 0 行。
- **不用 OFFSET：** OFFSET 4,000,000 每次扫过 400 万行；游标是主键范围查询，每块一样快。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 211">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个事务里：这一块的消息 + 游标</text>
<rect x="8" y="26" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读：user_id &gt; 游标，取 10,000 个</text>
<polyline points="170,55 170,73" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,73 166.8,66 173.2,66" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="73" width="324" height="29" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写：这一块的通知行（唯一键）</text>
<polyline points="170,102 170,120" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,120 166.8,113 173.2,113" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="120" width="324" height="29" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写：游标 = 这一块最大的 user_id</text>
<polyline points="170,149 170,171" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,171 166.8,164 173.2,164" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">COMMIT</text>
<text x="8" y="189" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">游标晚于消息：只会重复，唯一键吸收</text>
<text x="8" y="205" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">游标早于消息：会丢 10,000 个用户</text>
</svg>
白板上：一条事务（块 + 游标），下面是 400 万完成的进度条，和崩溃后从哪里开始。

**常见失分。**
- **用 webhook 回答进度：** 那是投递状态。
- **游标在内存里：** 崩了就没了。
- **先推进游标再发消息：** 崩在中间，这块的用户永远丢了。

**面试官可能接着问。**
- 两个实例同时跑？ → 任务行加租约 `leased_until`，拿到租约的才处理；或按活动号固定分配实例。
- 发日志怎么和库原子？ → 通知行本身就是 outbox，relay 把 queued 行发到营销 topic 后才改状态；至少一次，worker 靠唯一键去重。
- 每块 10,000 个怎么定？ → 事务约 1 至 2 秒、崩了最多重做这么多；太大重做多、事务长，太小游标写太频繁。
