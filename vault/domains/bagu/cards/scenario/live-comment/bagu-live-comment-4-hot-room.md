---
id: bagu-live-comment-4-hot-room
node: a.scenario.live-comment
type: qa
step: 4
---
## Q
**热点房间隔离 · 评论排序和分页**｜追问

面试官：「顶流直播间和普通房间怎么隔离？评论怎么排序、分页？」

## A
**基本回答。** 热点房间流量比普通房间高几个数量级，混在一起评论洪峰占满推送队列，同批网关上其他房间弹幕也延迟；所以在线人数超阈值的房间独占一组推送网关、MQ 分区和限流配额，普通房间共享，监控人数自动升降级。排序用服务端递增的评论序号（或房间内自增 ID），不用客户端时间（不可靠、会重复）。进房首屏的最近几百条放 Redis List 或 Stream；按热度排序用 ZSet，精彩、置顶评论单独存。分页用游标：`OFFSET` 要先数出前面的行再丢弃越翻越慢，游标直接走索引，翻多深都一样快：`WHERE room_id = ? AND id < ? ORDER BY id DESC LIMIT 20`，游标是上一页最后一条的 ID。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">隔离：热点房间独占资源</text>
<rect x="8" y="24" width="150" height="64" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">热点房间 A</text>
<text x="83" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">独占网关、MQ 分区</text>
<text x="83" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限流配额</text>
<rect x="182" y="24" width="150" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">普通房间 B、C、D</text>
<text x="257" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">共享一组资源</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分页：游标，不用 OFFSET</text>
<rect x="8" y="122" width="100" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 1 页</text>
<text x="58" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id 100 ~ 81</text>
<rect x="120" y="122" width="100" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 2 页</text>
<text x="170" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id < 81 取 20</text>
<line x1="108" y1="144" x2="113.0" y2="144.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120,144 113.0,147.2 113.0,140.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="122" width="100" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 3 页</text>
<text x="282" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id < 61 取 20</text>
<line x1="220" y1="144" x2="225.0" y2="144.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232,144 225.0,147.2 225.0,140.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">游标 = 上一页最后一条的 ID</text>
</svg>
第一部分：热点房间单独成组，别的房间不受影响。第二部分：翻页靠上一页最后一条的 ID，不数页码。
**举个例子。** 评论 id 从 100 往下：第 1 页 100 到 81，游标 81；第 2 页查 `id < 81` 得 80 到 61。翻页过程中新评论 101 进来，也不会让后面的页错位，因为游标是 id 而不是第几页。
**业务场景。** 顶流直播间评论洪峰塞满共享推送队列，同批网关上其他几十个房间弹幕延迟十几秒；迁到独立资源组后其他房间立即恢复。
**容易错。**
- **热点只靠限流、不隔离：** 限流是丢请求，隔离才让别的房间不受影响。
