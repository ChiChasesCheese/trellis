---
id: bagu-expire-eviction-2-expire-cycle
node: a.redis.expire-eviction
type: qa
step: 2
---
## Q
**惰性加定期 · 各自的缺陷，定期删除怎么抽**｜追问

面试官：「定期删除具体怎么做？为什么删不干净？大量 key 同时过期会怎样？」

## A
**基本回答。** 定期删除由时间事件（`serverCron`）触发，频率 `hz`（默认 10，每秒 10 次）；每轮抽样 20 个带过期的 key 删掉过期的（6.0 起用游标逐桶扫，5.0 及以前随机取），过期比例高就再抽，每轮有时间上限（约 25% CPU 时间片，约 25 毫秒）。抽样加上限，不保证删光；惰性删除不访问就不删，两者叠加仍有残留。继续抽的阈值：5.0 及以前是 25%，6.0 起源码常量 `ACTIVE_EXPIRE_CYCLE_ACCEPTABLE_STALE` 是 10 并随 `active-expire-effort` 调整，意思相同。大量 key 同秒过期，每轮比例都很高，一直抽到时间上限，占住主线程，每轮最多多等约 25 毫秒，表现为延迟抖动，还会引发缓存雪崩。对策：TTL 加随机（如 `基础时间 + random(0, 300)` 秒）；`lazyfree-lazy-expire yes` 异步释放；`active-expire-effort`（6.0+，1–10，默认 1）调大更积极清理但占更多主线程。观察 `INFO stats` 的 `expired_keys`、`expired_stale_perc`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<rect x="60" y="6" width="220" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">serverCron 每秒 10 次</text>
<line x1="170" y1="36" x2="170" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,54 166.8,47.0 173.2,47.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="54" width="220" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">抽样 20 个带过期的 key</text>
<line x1="170" y1="84" x2="170" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,102 166.8,95.0 173.2,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="102" width="220" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">删掉其中已过期的</text>
<line x1="170" y1="132" x2="170" y2="150" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,150 166.8,143.0 173.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="150" width="220" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期比例还高？</text>
<line x1="280" y1="165" x2="312" y2="165" stroke-width="1.2" stroke="currentColor"/>
<line x1="312" y1="165" x2="312" y2="69" stroke-width="1.2" stroke="currentColor"/>
<line x1="312" y1="69" x2="280" y2="69" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,69 287.0,65.8 287.0,72.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="306" y="120" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<text x="306" y="140" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">再抽</text>
<line x1="170" y1="180" x2="170" y2="204" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,204 166.8,197.0 173.2,197.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="197" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">否</text>
<rect x="60" y="204" width="220" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">这一轮结束</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每轮有时间上限：约 25% CPU（约 25 毫秒）</text>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一秒大批过期 → 一直抽到上限 → 延迟抖动</text>
</svg>
抽 20 个、删过期的，比例还高就回头继续，直到比例降下来或到时间上限。
**业务场景。** 活动在 20:00:00 给 500 万个任务标记统一设「20:30:00 过期」：20:30 前每轮抽 20 个都没过期，几乎不占 CPU；到点 500 万个同时过期，每轮几乎全过期，一直抽到约 25 毫秒才停，延迟明显抖动；改成 30 分钟加随机 0 到 5 分钟并开异步释放后抖动消失。
**容易错。**
- **以为定期删除扫全部 key。**
- **以为阈值永远是 25%。**
- **以为集中过期只是内存问题。**
