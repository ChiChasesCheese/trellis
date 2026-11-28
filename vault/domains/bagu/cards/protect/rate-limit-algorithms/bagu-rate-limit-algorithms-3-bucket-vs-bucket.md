---
id: bagu-rate-limit-algorithms-3-bucket-vs-bucket
node: a.protect.rate-limit-algorithms
type: qa
step: 3
---
## Q
**限流算法 · 令牌桶和漏桶的区别，什么场景用哪个**｜必会

面试官：「令牌桶和漏桶看起来都是『桶』，到底差在哪？给第三方短信通道发消息和给用户开放查询接口，分别用哪个？」

## A
**基本回答。** 漏桶控制出口：请求入队、以恒定速率流出，输出永远平滑，突发被排队拖慢或丢弃；队列要设上限，否则排队时间超过调用方超时，调用方放弃了请求还在排（Sentinel 的匀速排队就是漏桶）。令牌桶控制入口许可：令牌按速率攒、空闲时攒满，一次突发最多放行 b 个，平均速率仍是 r，延迟更低。需要匀速保护脆弱下游（对方严格限速、超了封号）用漏桶；面向用户、允许合理突发用令牌桶。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">漏桶：管出口</text>
<text x="176" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">令牌桶：管入口许可</text>
<rect x="8" y="26" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">突发进来 5 个</text>
<line x1="86" y1="54" x2="86" y2="63" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,70.0 82.8,63.0 89.2,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="70" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列（桶）</text>
<text x="86" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要设上限</text>
<line x1="86" y1="110" x2="86" y2="123" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,130.0 82.8,123.0 89.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="130" width="156" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每 10ms 放出 1 个</text>
<text x="86" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每秒 100 个</text>
<rect x="176" y="26" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">突发进来 5 个</text>
<line x1="254" y1="54" x2="254" y2="63" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,70.0 250.8,63.0 257.2,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="70" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌桶</text>
<text x="254" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌按速率 r 攒</text>
<line x1="254" y1="110" x2="254" y2="123" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,130.0 250.8,123.0 257.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="130" width="156" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">桶里有 5 个令牌</text>
<text x="254" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一次全放过</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">漏桶：出口永远匀速，突发被拖慢</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">令牌桶：突发最多放行 b 个，平均仍是 r</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对方限速、超了封号 → 漏桶；面向用户 → 令牌桶</text>
</svg>
同样突然来 5 个请求：漏桶进队列、每 10ms 放一个；令牌桶桶里有 5 个令牌，一次全放过。
**业务场景。** 速率每秒 100、容量都是 100，瞬间来 300 个：漏桶队列装下 100 个、其余 200 丢弃，100 个按每 10ms 一个整整 1 秒放完，下游始终匀速；令牌桶当场放过 100 个，其余 200 拒绝，下游一瞬间看到 100 个。所以给第三方短信通道发验证码（对方限每秒 100 条、超了封号）用漏桶，用户端查询接口允许秒级突发用令牌桶；营销和验证码要分开配桶，验证码独立额度、优先。
**容易错。**
- **以为两个都能应对突发：** 漏桶把突发抹平成排队。
- **对严格限速的第三方用令牌桶：** 一瞬间突发可能被判超限封号。
- **把「平滑」当作「快」。**
