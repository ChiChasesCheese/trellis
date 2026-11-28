---
id: hi-mock-donations-website-charities-08-dive-triple-guard
node: qb.sd.donations-website-charities.mock
type: qa
step: 8
---
## Q
**限时捐款网站 · 第 8 步 · 深入一：绝不重复扣款，三层防护**｜模拟面试

面试官：「现在谈最重要的：怎么保证不重复扣款？用户连点两次，或者我们的服务重试，会怎样？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说威胁有哪几处：** 「三处：用户重复提交，比如连点、后退再交；我们自己的重试，比如负载均衡重发；PSP 调用超时之后我们不知道有没有成功。」
- **第一层，前端 donationId：** 「捐款页加载时生成 UUID，同一次捐款的所有重发都带它。按钮点后置灰是体验，不是保证。」
- **第二层，服务端：** 「donationId 是主键，第二次 INSERT 会冲突，冲突就读已有行返回。再用条件更新 `WHERE status='CREATED'` 当闸：两个并发请求里，只有一个影响 1 行，另一个影响 0 行，直接返回当前状态，不去调 PSP。」
- **第三层，PSP 幂等键：** 「调 PSP 时把 donationId 作幂等键，同一个键 PSP 只处理一次，重复请求返回第一次的结果。」
- **缺一层会怎样：** 「没有第一层，一次意图变成两个 id，后面的层都当两笔处理；没有第二层，两个并发请求都去调 PSP，状态也写乱；没有第三层，超时后我们自己重发，PSP 当新请求，可能扣两次。所以三层叠加，缺一个都可能出事故。」
- **为什么用条件更新而不是行锁：** 「条件更新是一条语句、立刻提交，不会在等 PSP 的 0.5 秒里一直占着行锁和连接；SELECT FOR UPDATE 在尖峰时会把连接池耗光。」
- **走一遍双击：** 「请求 A、B 带同一个 id，几乎同时到。A 的 INSERT 成功，B 冲突；A 的条件更新赢，B 影响 0 行；只有 A 去调 PSP，B 返回 PROCESSING，前端轮询等结果。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 500">
<rect x="12" y="8" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器 · 捐款页</text>
<text x="82" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① donationId (UUID)</text>
<rect x="188" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="258" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP 前端组件</text>
<text x="258" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收卡号 · 换令牌</text>
<polyline points="152,22 188,22" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="188,22 181.0,25.2 181.0,18.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="188,40 152,40" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="152,40 159.0,36.8 159.0,43.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">卡号</text>
<text x="170" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌</text>
<rect x="12" y="108" width="316" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款 API</text>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无状态 · 多实例</text>
<polyline points="24,52 24,108" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="24,108 20.8,101.0 27.2,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="24,52 27.2,59.0 20.8,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="34" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /donations</text>
<text x="34" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GET /charities</text>
<text x="34" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GET /donations/:id</text>
<path d="M12,198 a70,6 0 0 1 140,0 v136 a70,6 0 0 1 -140,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M12,198 a70,6 0 0 0 140,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="82" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库 Postgres</text>
<rect x="20" y="232" width="124" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="247" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 条件更新闸</text>
<rect x="20" y="258" width="124" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="273" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">outbox 表</text>
<rect x="20" y="284" width="124" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="299" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">charities 表</text>
<polyline points="60,152 60,192" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="60,192 56.8,185.0 63.2,185.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="60,152 63.2,159.0 56.8,159.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="66" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT / UPDATE</text>
<rect x="188" y="240" width="68" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="258.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主 PSP</text>
<text x="222" y="273.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 幂等键</text>
<polyline points="220,152 220,240" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="220,240 216.8,233.0 223.2,233.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="226" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">扣款 + 幂等键</text>
<rect x="12" y="380" width="140" height="36" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="20" y="403" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="44.8" y="403" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="69.6" y="403" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="94.4" y="403" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="119.2" y="403" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<text x="82" y="395" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息队列</text>
<polyline points="82,340 82,380" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="82,380 78.8,373.0 85.2,373.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="88" y="366" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">投递器</text>
<rect x="12" y="440" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="456.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回执服务</text>
<text x="82" y="471.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">去重 · 重试</text>
<polyline points="82,416 82,440" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="82,440 78.8,433.0 85.2,433.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="188" y="440" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="258" y="456.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">邮件服务</text>
<text x="258" y="471.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发收据</text>
<polyline points="152,460 188,460" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="188,460 181.0,463.2 181.0,456.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
白板上新增：三个蓝色标记：① 浏览器的 donationId，② 数据库里的条件更新闸，③ 主 PSP 的幂等键。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 504">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 A</text>
<text x="44" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先到</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 B</text>
<text x="128" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重复点击</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个 donationId = 7f3a，两个请求几乎同时到</text>
<text x="48" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 7f3a</text>
<polyline points="44,104 212,104" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,104 205.0,107.2 205.0,100.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180.64" y="118" width="62.72" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CREATED</text>
<text x="132" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 7f3a</text>
<polyline points="128,166 212,166" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,166 205.0,169.2 205.0,162.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主键冲突 → 读现状</text>
<polyline points="212,200 128,200" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,200 135.0,196.8 135.0,203.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … WHERE CREATED</text>
<polyline points="44,234 212,234" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,234 205.0,237.2 205.0,230.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">影响 1 行：赢</text>
<polyline points="212,268 44,268" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,268 51.0,264.8 51.0,271.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="170.2" y="282" width="83.6" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PROCESSING</text>
<text x="132" y="318" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … WHERE CREATED</text>
<polyline points="128,330 212,330" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,330 205.0,333.2 205.0,326.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="352" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">影响 0 行：不调 PSP</text>
<polyline points="212,364 128,364" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,364 135.0,360.8 135.0,367.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="386" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">charge(幂等键 = 7f3a)</text>
<polyline points="44,398 298,398" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,398 291.0,401.2 291.0,394.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="420" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功</text>
<polyline points="298,432 44,432" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,432 51.0,428.8 51.0,435.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="454" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写 SUCCEEDED</text>
<polyline points="44,466 212,466" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,466 205.0,469.2 205.0,462.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="492" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B 只返回当前状态，前端轮询等结果</text>
<line x1="44" y1="48" x2="44" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="80" x2="44" y2="481" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="496" x2="44" y2="500" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="80" x2="128" y2="211" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="226" x2="128" y2="245" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="260" x2="128" y2="375" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="390" x2="128" y2="443" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="458" x2="128" y2="481" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="496" x2="128" y2="500" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="80" x2="212" y2="116" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="140" x2="212" y2="177" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="192" x2="212" y2="280" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="304" x2="212" y2="307" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="322" x2="212" y2="341" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="356" x2="212" y2="481" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="496" x2="212" y2="500" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="80" x2="298" y2="500" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：双击竞态的时序：A 赢得条件更新，B 影响 0 行，不碰 PSP。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 272">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三层各挡什么，缺了会怎样</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 前端 donationId</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">挡：连点、后退重交、网络重发</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缺：一次意图变两个 id，后面全当两笔</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 唯一键 + 条件更新</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">挡：同一个 id 的并发请求</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缺：两个请求都去调 PSP，状态写乱</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ PSP 幂等键</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">挡：我们的重试、超时后重发</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缺：PSP 当新请求，超时重发会双扣</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务不跨 PSP 调用：条件更新先提交，</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再调 PSP，再单独写结果</text>
</svg>
白板上新增：三层各挡什么、缺了会怎样。
**为什么这样说。** （约 11 分钟，累计第 34 分钟。）这是整题的核心，面试官看你能不能把「三处威胁」和「三层防护」一一对应，并且说出每层缺失的后果。强的回答能画出竞态时序，说清条件更新的赢家和输家。弱的回答只说「加个唯一约束」或「用幂等键」，说不出为什么要多层，也不知道三层各自拦的是什么。
**面试官可能接着问。**
- 请求 B 到的时候 A 还在处理，B 得到什么？ → 当前状态 PROCESSING。B 不会去调 PSP，前端继续轮询，A 完成后两边看到同一个结果。
- PSP 的幂等键能保存多久？ → 常见的 PSP 只保存约 24 小时，具体以所用 PSP 的文档为准。所以对账必须在这个窗口内查清，我们的对账以分钟计，远小于它。
- 同一个 id，但金额被改了呢？ → 我们在 API 层比较 body，不一致就返回 409，不进入扣款；PSP 看到同键不同参数也会报错。
- 幂等键能每次重试都新生成吗？ → 不能，那就等于没有。键必须稳定，就是 donationId，同一笔的任何重试都用它。
**常见失分。**
- **只靠前端：** 按钮置灰只是体验，网络重发和浏览器后退都挡不住。
- **只靠唯一约束：** 它只管数据库里的行，管不住 PSP 的重复扣款。
- **事务包住 PSP：** 把行锁拖过整个 PSP 调用，尖峰时连接池耗尽。
- **幂等键每次重生成：** 稳定的键才有幂等，随机键等于没加。
