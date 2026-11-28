---
id: hi-fix-retry-key-01-mechanism
node: fix.retry-key
type: qa
step: 1
---
## Q
**重试键 (Retry Key)｜补强 · 机制**

扣款、下单、占座这类请求会因为超时、双击、网关重试而被再发一遍。「服务端建好记录、再把 id 返回给客户端」为什么挡不住重复扣款？重试键该怎么设计，面试时要怎么说？

## A
**要防的失败。** 坏的版本里，id 是服务端收到请求之后才造出来的。第一次的响应丢了，客户端手里没有任何东西能证明「这是同一次」，只好把同样的请求再发一遍；服务端看到的是一个全新的请求，又建一行、又扣一次款。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 328">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /donations（无键）</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT → id = d1</text>
<polyline points="128,118 212,118" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="212,118 205.0,121.2 205.0,114.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">charge(d1)</text>
<polyline points="128,152 298,152" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,152 291.0,155.2 291.0,148.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢失，浏览器超时</text>
<text x="48" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重试 POST（仍然无键）</text>
<polyline points="44,214 128,214" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,214 121.0,217.2 121.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="236" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT → id = d2</text>
<polyline points="128,248 212,248" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="212,248 205.0,251.2 205.0,244.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="270" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">charge(d2)</text>
<polyline points="128,282 298,282" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,282 291.0,285.2 291.0,278.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="265.08" y="296" width="65.84" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="298" y="310" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣了两次</text>
<line x1="44" y1="48" x2="44" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="169" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="184" x2="128" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="206" x2="128" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="110" x2="212" y2="169" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="184" x2="212" y2="225" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="240" x2="212" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="294" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="318" x2="298" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="176" x2="99.2" y2="176" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="240.8" y1="176" x2="332" y2="176" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：id 由服务端造，响应一丢，重试就成了新请求，PSP 被扣两次。

**常见的半截修法。** 「重试时先查这个用户有没有 pending 的记录」也不行：
- **分不清两种来意：** 同一次结账的重试，和用户刻意再捐的第二笔，在服务端看起来一模一样，一个该返回旧结果，一个该新建。
- **两个标签页：** 同一个用户同时开两个结账页，会互相当成对方的重试。

**机制。** 让「这一次结账」在第一次请求发出之前就有一个名字，并且每次重发都带着它。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 348">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<rect x="4" y="64" width="89.6" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48.8" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K = 新 UUID</text>
<text x="48" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST（带 K）</text>
<polyline points="44,112 128,112" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,112 121.0,115.2 121.0,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT … K → d1，提交</text>
<polyline points="128,146 212,146" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,146 205.0,149.2 205.0,142.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">charge(幂等键 = d1)</text>
<polyline points="128,180 298,180" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,180 291.0,183.2 291.0,176.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢失，浏览器超时</text>
<text x="48" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重试 POST（同一个 K）</text>
<polyline points="44,242 128,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,242 121.0,245.2 121.0,238.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 冲突 → 读 d1</text>
<polyline points="128,276 212,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,276 205.0,279.2 205.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回 d1 + 状态</text>
<polyline points="128,310 44,310" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,310 51.0,306.8 51.0,313.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="336" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">PSP 这一路没有第二次调用</text>
<line x1="44" y1="48" x2="44" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="86" x2="44" y2="325" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="340" x2="44" y2="344" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="89" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="104" x2="128" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="212" x2="128" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="234" x2="128" y2="287" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="302" x2="128" y2="325" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="340" x2="128" y2="344" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="123" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="138" x2="212" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="172" x2="212" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="212" x2="212" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="268" x2="212" y2="344" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="344" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="204" x2="99.2" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="240.8" y1="204" x2="332" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：K 由浏览器在第一次发送之前生成；服务端用唯一约束裁决，同一个 K 只会有一行记录。
- **键先于第一次发送：** 在用户打开结账页或按下按钮的瞬间，客户端生成一个 UUID。键也可以由服务端更早发出（估价单号、广告展示号），关键是它在副作用请求之前就已经在客户端手里。
- **同一意图同一个键：** 同一次点击的所有重发（超时、网关重试、刷新后恢复）都带同一个键。用户刻意再来一次，是新的结账，新的键。
- **唯一约束裁决：** `UNIQUE (user_id, key)`。先 `INSERT … ON CONFLICT DO NOTHING`，没插进去就读已有的行返回。
- **先提交再调外部：** 记录提交之后才去调 PSP。重试撞上这一行时，读到的是已提交的状态，不会卡在别人的事务里。
- **每道边界一个稳定键：** 调 PSP 时也带一个由这个键决定的稳定值（比如 `donation_id`），两边各有一层。
- **同键不同内容：** 返回 409，不进入扣款：这是客户端的 bug。

**在面试里说这一句。** 「重试靠 `checkout_attempt_id`：客户端在第一次扣款之前生成，每次重发都带上；服务端对它有唯一约束，见到同一个键就返回已有的捐款，绝不再调 PSP；用户想再捐一笔，就是新的键。」先把键写进请求体，再解释为什么可以安全地重发。

**怎么认出这类题。**
- **动作有外部副作用：** 扣款、下单、订座、转账、接单，做了就撤不回来或撤了有代价。
- **题面里有重发的词：** 超时、双击、网关重试、响应丢失、手机掉线。
- **你在说「服务端幂等」：** 一旦你说出这四个字，面试官就会问「请求里是哪个字段？谁生成的？」，先把答案说出来。

**常见失分。**
- **只说「服务端幂等」：** 没有说出重试时客户端发的那个值，面试官只能认为你没有想清楚。
- **id 在响应里才出现：** 响应丢了，客户端就没有可重发的东西。
- **按 (用户, 活动, 金额) 判重：** 同一个人给同一个活动捐两次 10 美元是合法的。
