---
id: bagu-rate-limit-algorithms-2-window-boundary
node: a.protect.rate-limit-algorithms
type: qa
step: 2
---
## Q
**限流算法 · 固定窗口的临界问题，滑动窗口怎么解决**｜必会

面试官：「固定窗口限流每分钟 1000 次，有什么漏洞？滑动窗口怎么解决？在 Redis 里怎么实现？」

## A
**基本回答。** 固定窗口不记得上一个窗口：窗口一换计数清零，上一分钟最后一秒放进 1000、下一分钟第一秒又放进 1000，两秒内通过 2000，接近限额两倍，攻击者专门卡边界。滑动窗口让窗口随时间平移，永远统计「最近 60 秒」。两种做法：切格计数（60 秒切 60 格，内存只和格数有关，近似）；记录每个请求时间戳（精确，内存与请求数成正比，高 QPS 大 key 占内存可观，这时改切格）。Redis 日志法用 ZSET：`ZREMRANGEBYSCORE` 删窗口外、`ZCARD` 判断、放行则 `ZADD`、`EXPIRE`，必须放进 Lua 才原子，否则两个请求同时看到 99 都放行。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">固定窗口：窗口一换，计数清零</text>
<text x="170" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两秒内放进 2000，限额才 1000</text>
<rect x="130" y="66" width="40" height="60" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000</text>
<rect x="170" y="66" width="40" height="60" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="190" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="20" y1="126" x2="320" y2="126" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="126" x2="170" y2="134" stroke-width="1.2" stroke="currentColor"/>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 60 秒</text>
<text x="95" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口 1</text>
<text x="245" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口 2</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">滑动窗口：永远数「最近 60 秒」，没有边界</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">前一批 1000 个还在窗口里，下一批就被拒</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">任意连续 60 秒内，通过数都不超过 1000</text>
</svg>
两根柱紧挨在第 60 秒边界两侧：各自不超限额，合起来是两倍；滑动窗口没有边界，永远往回数 60 秒。
**代码。** 限 100 次 / 60 秒（now 为毫秒时间戳），放进 Lua：
```
ZREMRANGEBYSCORE rl:u7 0 <now-60000>   -- 清掉窗口外的
ZCARD rl:u7                             -- 小于 100 才放行
ZADD rl:u7 <now> <now-唯一后缀>          -- 记录本次
EXPIRE rl:u7 60
```
**业务场景。** 短链接创建接口限每用户每分钟 30 次：固定窗口下脚本卡在整分钟边界连发两轮，1 秒内创建 60 个；滑动窗口下任意连续 60 秒都不超过 30。Redis 例（限 3 次 / 60 秒）：第 10、20、30 秒放行，第 40 秒 ZCARD 为 3 拒绝（被拒的不记录），第 75 秒删掉分数 ≤ 15 的那条后 ZCARD 为 2，放行。
**容易错。**
- **以为滑动窗口一定精确：** 切格是近似。
- **忘了 EXPIRE：** 不活跃用户的 key 白占内存。
