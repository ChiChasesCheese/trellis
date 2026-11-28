---
id: hi-fix-retry-key-07-ad-click
node: fix.retry-key
type: qa
step: 8
---
## Q
**广告点击聚合 · 重试键**｜补强

面试官：「用户对同一次广告展示连点了三下，浏览器的重试也会重发点击请求。聚合出来的点击数怎么不被刷高？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **键在点击之前就发出了：** 「广告服务在渲染广告时，给每一次展示生成一个 `impression_id`，用 HMAC 和 `ad_id` 一起签名，随广告一起发给浏览器。点击请求带上这个 id。键是服务端更早发出的，先于点击。」
- **为什么是展示，不是用户加广告：** 「再营销会让同一个人多次看到同一则广告，每次展示是一次新机会。每次展示一个新键，所以一次展示最多算一次点击。」
- **验签：** 「点击 API 先验 HMAC：伪造的 impression_id 通不过，换了 ad_id 也通不过。验签只是一次哈希，微秒级。」
- **去重怎么做：** 「`SET impr:{id} 1 NX EX 86400`。返回 OK 是第一次，发布到 Kafka；返回 nil 是重复，直接丢弃。」
- **为什么在进流之前去重：** 「重复点击可能落在两个聚合窗口的两侧，在 Flink 窗口里去重，跨窗口的重复就挡不住。」
- **失败的取舍：** 「SET 成功但发布失败，这次点击会丢。我在发布失败的路径上 `DEL` 这个键；进程恰好崩在中间造成的极少量丢失，我会向面试官说明，并用原始点击日志的定期对账来校正。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 322">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">广告服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">点击 API</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求广告</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="48" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">广告 + impression_id</text>
<polyline points="128,118 44,118" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,118 51.0,114.8 51.0,121.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">点击 {impression_id}</text>
<polyline points="44,152 212,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,152 205.0,155.2 205.0,148.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="166.72" y="166" width="90.56" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET NX → OK</text>
<text x="216" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">发布点击</text>
<polyline points="212,214 298,214" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,214 291.0,217.2 291.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="242" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">连点 / 浏览器重发</text>
<text x="48" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">点击 {同一个 id}</text>
<polyline points="44,276 212,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,276 205.0,279.2 205.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="143.8" y="290" width="136.4" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="304" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET NX → nil，丢弃</text>
<line x1="44" y1="48" x2="44" y2="318" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="110" x2="128" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="144" x2="128" y2="231" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="246" x2="128" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="268" x2="128" y2="318" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="164" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="188" x2="212" y2="231" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="246" x2="212" y2="288" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="312" x2="212" y2="318" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="318" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="238" x2="108.2" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="231.8" y1="238" x2="332" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：键先于点击由服务端发出，点击 API 用 SET NX 裁决第一次。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个人，同一则广告，看了三次</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">展示 I1：点了 3 下</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个键，只计 1 次</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">展示 I2：点了 1 下</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新的键，计 1 次</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">展示 I3：没点</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有点击，计 0 次</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共 2 次点击。键是 (用户, 广告) 的话只能算 1 次</text>
</svg>
白板上：一次展示一个键，同一个人三次展示最多计三次点击。

**为什么这样说。** 面试官要听的是：键是什么、从哪来、谁来裁决第一次。这一题和捐款的区别是键由服务端发出，但它仍然符合同一条规则：在副作用之前，客户端已经拿到了它。弱的回答是「按用户和广告去重」，会把合法的再次点击当成重复。
**面试官可能接着问。**
- 为什么要签名？ → 没有签名，攻击者可以编造一堆互不相同的 impression_id，每个都算一次点击。
- Redis 里的键保存多久？ → 覆盖点击有效期，比如 24 小时；过期之后的点击本来就不计。
- Redis 挂了怎么办？ → 去重短暂失效，期间的重复点击会被多算；这是取舍，我会说明：Redis 做主从，恢复后继续去重，并用原始点击日志的对账来校正。
- 展示本身会被重复请求吗？ → 每次请求广告都生成新的 impression_id，这是新的展示，不是重复。
**常见失分。**
- **按 (用户, 广告) 去重：** 同一个人再次看到同一则广告时的点击被丢掉。
- **只在 Flink 窗口里去重：** 跨窗口的重复点击都算两次。
- **键不签名：** 伪造的键互不重复，全部计入。
- **SET 成功后发布失败没回滚：** 点击丢失且再也不会被计入。
