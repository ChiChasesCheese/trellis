---
id: hi-mock-notification-09-dive-no-dup
node: fix.notification-mock
type: qa
step: 9
---
## Q
**通知系统 · 第 9 步 · 深入四：同一张回执不能收两次**｜模拟面试

面试官：「产品团队的请求超时了，他们重试。怎么保证用户不会收到两张支付回执？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给结论：** 「用数据库的唯一约束：notification_id 上建唯一索引，插入若不存在。不用锁，也不在请求路径里先查后插。」
- **键从哪里来：** 「notification_id 由业务事件决定，例如 receipt:po_8841，po_8841 是支付订单号。同一个事件的每次重试用同一个 id，所以重试和原请求撞在同一个键上。」
- **请求路径里没有查询：** 「API 不去查重，两份请求都写进日志。分区键是 notification_id，所以两份落在同一个分区，由同一个消费者先后处理。」
- **worker 的那一条语句：** 见下面的代码。「影响 1 行，说明是新通知，往下发；影响 0 行，说明已经有了。」
- **0 行之后再看一眼状态：** 「状态是 sent、delivered 或 failed：已经处理过，直接提交位移，不发。状态还是 queued：这是同一条消息崩溃后重新投递，要接着发，不能因为『已存在』就丢掉它。」
- **为什么两个并发请求也安全：** 「数据库在唯一索引上把两个插入排队：第一个提交，第二个等到它提交后发现冲突，什么也不做。检查和插入是同一个原子操作，不存在两个都看到『没有』的缝隙。」
- **残余的窗口：** 「worker 在『供应商已接受』和『写 sent』之间崩溃，会多发一次。这个窗口只有一两毫秒；推送用 collapse id（取自 notification_id）让设备上只显示一条，邮件和短信是至少一次的代价，我会把它写在文档里。」
- **为什么唯一键在分片内部有效：** 「状态库按 notification_id 分片，同一个 id 一定在同一个分片，唯一约束只需要在分片内成立。」
**白板。**
```
INSERT INTO notification
  (notification_id, user_id, status)
VALUES ('receipt:po_8841', 42, 'queued')
ON CONFLICT (notification_id)
DO NOTHING;
-- 1 行：新通知，发送
-- 0 行：已存在，读 status 再定
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一张回执发了两次</text>
<rect x="8" y="34" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">产品团队</text>
<rect x="92" y="34" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志</text>
<rect x="176" y="34" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker</text>
<rect x="260" y="34" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态库</text>
<text x="48" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">r1 与超时重试的 r1</text>
<polyline points="44,110 128,110" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,110 121,113.2 121,106.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同分区，相邻两份</text>
<polyline points="128,144 212,144" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,144 205,147.2 205,140.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT r1 若不存在</text>
<polyline points="212,178 296,178" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="296,178 289,181.2 289,174.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 行：新，去发送</text>
<polyline points="296,212 212,212" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,212 219,215.2 219,208.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 2 份：INSERT r1</text>
<polyline points="212,246 296,246" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="296,246 289,249.2 289,242.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="268" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 行：已有，不再发</text>
<polyline points="296,280 212,280" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,280 219,283.2 219,276.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="74" x2="44" y2="302" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="74" x2="128" y2="87" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="101" x2="128" y2="302" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="74" x2="212" y2="121" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="135" x2="212" y2="302" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="74" x2="296" y2="155" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="169" x2="296" y2="189" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="203" x2="296" y2="223" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="237" x2="296" y2="257" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="271" x2="296" y2="302" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三种去重办法</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">锁（Redis 或行锁）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">行还不存在，没有东西可锁</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">锁会过期、会丢；不是最后一道防线</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">先查再插</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两个请求同时查到「没有」，都插入</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个请求还多一次查询</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">唯一约束 + 插入若不存在</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">数据库保证原子：只有一个插入成功</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">无锁、无多余查询</text>
</svg>
白板上新增：一条插入语句，时序图，和三种办法的对比。
**为什么这样说。** （约 3 分钟，累计第 33 分钟。）面试官等的是「唯一约束，插入若不存在」这一个答案。他当时先说加锁，自己发现「行还不存在，锁不到」；又说在服务器里先判断再插入；直到面试官给了提示，才答出「第二次插入返回 0 行」，用了 3 分钟多。强的回答第一句话就说唯一约束，再说 0 行意味着什么。
**面试官可能接着问。**
- 两个请求同时到达呢？ → 唯一索引把它们串行化，一个成功，一个冲突。并发安全是数据库给的，不是我加锁换来的。
- 同一个 id、内容不同呢？ → 以第一次为准，后来的丢弃并记告警；调用方应当用业务事件生成 id，内容不同是调用方的 bug。
- 唯一键的行永远留着吗？ → 留到保留期结束：热表里留 30 天，之后只留元数据。调用方的重试窗口一般几分钟到几小时，30 天足够。
- 为什么不用 Redis 的 SETNX 去重？ → Redis 的键会过期、会因主从切换丢失；它可以作快速前置拦截，但最后一道防线必须是数据库的唯一约束。
**常见失分。**
- **用锁：** 行还不存在时无锁可加，锁还会过期。
- **在请求路径先查后插：** 两个并发请求都能查到「没有」，还多一次查询。
- **0 行就丢弃消息：** 崩溃后重新投递的同一条消息也会被丢掉，这条就永远发不出去。
- **忘了去重的范围：** 唯一键只在分片内有效，所以分片键要选 notification_id。
