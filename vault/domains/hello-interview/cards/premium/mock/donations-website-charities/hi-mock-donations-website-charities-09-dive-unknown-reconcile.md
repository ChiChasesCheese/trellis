---
id: hi-mock-donations-website-charities-09-dive-unknown-reconcile
node: qb.sd.donations-website-charities.mock
type: qa
step: 9
---
## Q
**限时捐款网站 · 第 9 步 · 深入二：结果未知与对账（没有 webhook）**｜模拟面试

面试官：「PSP 调用超时了，你不知道钱到底扣没扣，怎么办？另外不让用 webhook，你怎么拿到最终结果？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **底线：** 不能标 FAILED 让用户重试，PSP 可能已扣，重试就是第二次扣款；也不能直接标成功。标 UNKNOWN，用户看到「处理中，请勿重复付款，结果会发到邮箱」。
- **UNKNOWN 怎么出现：** PSP 超时（10 秒）、连接中断、5xx；另有进程在 PROCESSING 之后崩溃，那行停在 PROCESSING。
- **对账任务：** 每 30 秒扫状态为 PROCESSING 或 UNKNOWN 且更新时间早于 60 秒的行（不碰正在处理的请求）。问 PSP 两种办法都安全：带同一幂等键重发原请求，或按 metadata 里的 donationId 查询。
- **查到什么：** 成功就写 SUCCEEDED 并同事务写 outbox 触发收据；明确失败写 FAILED；查不到这一笔，先在 PSP 取消它，等超过 PSP 超时再加余量才写 FAILED（请求可能还在路上或入账有延迟，先取消后迟到的请求会被拒）；PSP 不可用保持 UNKNOWN，下一轮退避再查。
- **没有 webhook 怎么拿结果：** 一，同步确认，服务端调 PSP 确认接口，响应带最终结果（卡支付通常即时）；二，3-D Secure 由浏览器按 PSP 组件完成验证，再调我们的确认接口，我们向 PSP 查最终状态；三，兜底靠对账轮询。以后即使允许 webhook 也只当加速通知，轮询不拆，因为 webhook 会丢、重复、乱序。
- **量级：** 假设 0.1% 落入 UNKNOWN：386 × 0.001 × 30 秒 ≈ 12 笔，每轮只有十几笔。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 582">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="44" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">捐款页</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API</text>
<text x="128" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">含对账任务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="298" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /donations</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">charge(幂等键 = id)</text>
<polyline points="128,118 298,118" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,118 291.0,121.2 291.0,114.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="84.64" y="132" width="86.72" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 秒没回音</text>
<text x="132" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE → UNKNOWN</text>
<polyline points="128,180 212,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,180 205.0,183.2 205.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180.64" y="194" width="62.72" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UNKNOWN</text>
<text x="48" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">status = 处理中</text>
<polyline points="128,242 44,242" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,242 51.0,238.8 51.0,245.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="270" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">30 秒后 · 对账任务</text>
<text x="132" y="292" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">扫 UNKNOWN 且 &gt; 60 秒</text>
<polyline points="128,304 212,304" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,304 205.0,307.2 205.0,300.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="326" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">donationId</text>
<polyline points="212,338 128,338" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,338 135.0,334.8 135.0,341.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="360" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一幂等键 / 按 id 查</text>
<polyline points="128,372 298,372" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,372 291.0,375.2 291.0,368.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="394" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已扣款（或查无此笔）</text>
<polyline points="298,406 128,406" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,406 135.0,402.8 135.0,409.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="428" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE SUCCEEDED + outbox</text>
<polyline points="128,440 212,440" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,440 205.0,443.2 205.0,436.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="173.68" y="454" width="76.64" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="468" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SUCCEEDED</text>
<text x="170" y="496" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户下一次轮询</text>
<text x="48" y="518" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GET /donations/:id</text>
<polyline points="44,530 128,530" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,530 121.0,533.2 121.0,526.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="48" y="552" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SUCCEEDED</text>
<polyline points="128,564 44,564" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,564 51.0,560.8 51.0,567.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="578" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="154" x2="128" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="234" x2="128" y2="259" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="274" x2="128" y2="485" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="500" x2="128" y2="507" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="522" x2="128" y2="578" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="110" x2="212" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="172" x2="212" y2="192" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="216" x2="212" y2="259" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="274" x2="212" y2="281" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="296" x2="212" y2="349" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="364" x2="212" y2="383" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="398" x2="212" y2="417" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="432" x2="212" y2="452" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="476" x2="212" y2="485" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="500" x2="212" y2="578" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="417" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="432" x2="298" y2="578" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="266" x2="104.24" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="235.76" y1="266" x2="332" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="492" x2="118.64" y2="492" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="221.36" y1="492" x2="332" y2="492" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：超时到对账的时序：先写 UNKNOWN 并告诉用户处理中，30 秒后对账用同一幂等键查到成功，补写 SUCCEEDED。

**常见失分。**
- **超时就标失败：** 等于第二次扣款。
- **对账扫太新的行：** 和正在处理的请求打架。
- **只靠 webhook：** 会丢、重复、乱序，没轮询兜底就永久卡住。
- **没有人工兜底：** 一直查不到的行没人管，钱和记录对不上。

**面试官可能接着问。**
- PSP 没记录就一定没扣？ → 不一定；先取消再等过超时窗口才判 FAILED，用户再捐用新 donationId 和新幂等键，不与旧请求混。
- 对账多实例重复处理？ → 查询只读幂等；写结果用 `WHERE status IN ('PROCESSING','UNKNOWN')` 条件更新，只有一个成功；取任务可用 `FOR UPDATE SKIP LOCKED`。
- UNKNOWN 期间刷新又点一次？ → donationId 存在会话存储，刷新复用同一个，还是同一笔；新开页是新 id，只能靠「上一笔还在处理」提示。
- 一直查不到？ → 超过几小时进人工队列并告警；活动结束后再用 PSP 对账单与 donations 全量比对。
