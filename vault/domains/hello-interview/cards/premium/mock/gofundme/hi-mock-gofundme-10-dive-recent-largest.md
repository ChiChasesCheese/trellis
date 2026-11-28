---
id: hi-mock-gofundme-10-dive-recent-largest
node: fix.gofundme-mock
type: qa
step: 10
---
## Q
**GoFundMe · 第 10 步 · 深入三：最近 100 笔和最大 10 笔**｜模拟面试

面试官：「活动页要显示最近 100 笔和最大 10 笔捐款。一个爆红活动每秒一万次浏览，怎么做到不每次都去主库查？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **读什么：** 每个字段一个有界小结构：最近 100 笔 `campaign:{id}:recent_donations`（sorted set，成员 donation_id，分数成功时间），最大 10 笔 `campaign:{id}:largest_donations`（分数金额）。
- **何时更新：** 仍是 Success 事件、同一个 worker：最近 `ZADD` + `ZREMRANGEBYRANK 0 -101`；最大 `ZADD` + `ZREMRANGEBYRANK 0 -11`（-1 是最大，-11 是第 11 大，只留前 10）。
- **有界：** 100 × 36 字节 + 10 × 50 字节 ≈ 4 KB/活动，100 万活跃活动约 4 GB（不含 Redis 结构开销，量级不变），一台放得下。
- **重放安全：** ZADD 同 id 同分数结果不变，不会重复，也不会把旧捐款顶到最前；已被裁掉的老捐款重放时分数最小，立刻又被裁掉。
- **读：** `GET /campaigns/{id}` 读 total、两个 ZREVRANGE（0 99、0 9），再按主键 `WHERE id = ANY(最多 110 个 id)` 取摘要；集合存 id 不存摘要，是为了拿到最新显示名。不扫表、不排序。匿名或隐藏金额读摘要时按字段过滤。
- **CDN：** 缓存活动页 5 秒，数字最多旧 5 秒；捐款人自己那一笔前端本地先加上。1 万次/秒、99% 命中，到应用服务 100 次/秒，每次三个 Redis 命令加一次批量主键读，很轻。
- **键丢了：** Redis 重启后从 donations 用索引 `LIMIT 100`、`LIMIT 10` 重建，再由事件更新。
- **不讲分片：** 分片、一致性哈希解决写压力；这里缺的是「活动页该读什么」。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 396">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写：捐款变 Success 时（worker）</text>
<rect x="8" y="26" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="54" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">最近 100：sorted set，分数 = 成功时间</text>
<text x="18" y="69" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZADD ts id → ZREMRANGEBYRANK 0 -101</text>
<text x="18" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重放：同 id 同分数，结果不变</text>
<rect x="8" y="112" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="140" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">最大 10：sorted set，分数 = 金额</text>
<text x="18" y="155" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZADD amount id → ZREMRANGEBYRANK 0 -11</text>
<text x="18" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个 id 再 ZADD 结果不变</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读：GET /campaigns/{id} 未命中缓存时</text>
<rect x="8" y="232" width="324" height="92" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="267" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET total · 两次 ZREVRANGE</text>
<text x="18" y="282" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">再 SELECT … WHERE id = ANY(≤110 个 id)</text>
<text x="18" y="297" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按主键取摘要；不搜索、不排序、不扫表</text>
<text x="8" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">键丢了（Redis 重启）：从 donations 表</text>
<text x="8" y="366" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LIMIT 100 / LIMIT 10 重建一次，</text>
<text x="8" y="384" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">靠 (campaign_id, status, created_at) 等索引</text>
</svg>
白板上新增：CDN（左上），Redis 里的 recent_donations 和 largest_donations 两个有序集合；活动页走 CDN → 应用服务 → Redis。

**常见失分。**
- **绕到分片：** 没回答「活动页读什么」。
- **活动页直接查库排序：** 爆红活动每次浏览一次排序，主库被压垮。
- **最近列表用 LPUSH：** 重放让同一笔出现两次或旧的顶到最前；sorted set 天然幂等。
- **不说上限：** 「一个列表」没说 100 个，等于没有有界。
