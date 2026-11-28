---
id: hi-mock-gofundme-06-hld-donate
node: fix.gofundme-mock
type: qa
step: 6
---
## Q
**GoFundMe · 第 6 步 · 高层设计（一）：捐款**｜模拟面试

面试官：「很好，现在开始画高层设计，先从捐款这条流程开始。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **打法：** 按功能一条条叠，先捐款，再活动页和结果，最后用数字带出深入；每加一个组件说它做什么、带来什么新问题、怎么处理。
- **付款组件：** PSP 前端组件让卡号只走浏览器到 PSP 一条线，换回一次性令牌；新问题是浏览器可能重发，用 checkout_attempt_id 唯一约束处理。
- **应用服务：** 一个网关加应用服务，活动、用户、支付先合在一起不拆（拆开只多服务间调用失败）；新问题是多实例没有共享内存，所以服务无状态，状态都在数据库。
- **Postgres：** 捐款行是唯一事实记录；新问题是扣款在事务之外，所以先写后调。
- **流程：** 浏览器 POST /donations（K1 + 令牌）；服务端 INSERT 一行 Pending（donation_id D1，K1 唯一）并立刻提交；之后才调 PSP charge，引用号和幂等键都是 D1，超时设 10 秒；成功 `UPDATE … WHERE status='Pending'` 改 Success，拒绝改 Failed，超时不改，留 Pending；返回 {D1, status}。
- **为什么先写后调：** 先调后写，崩在中间就是扣了款没记录；先提交 Pending，崩溃后至少有一行，可拿 D1 去 PSP 查。PSP 的 0.5 秒不包在事务里，否则连接被占住。
- **主动留白：** 重发怎么处理、超时如何收尾（深入一）、总额怎么更新（深入二）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 436">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="44" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">K1</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">K1 = checkout_attempt_id，打开结算页时先生成</text>
<text x="48" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">卡号 → PSP 组件</text>
<polyline points="44,104 298,104" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,104 291.0,107.2 291.0,100.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="48" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">payment_token</text>
<polyline points="298,138 44,138" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="44,138 51.0,134.8 51.0,141.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="48" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST（K1, 金额, token）</text>
<polyline points="44,172 128,172" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,172 121.0,175.2 121.0,168.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT Pending（K1 唯一）</text>
<polyline points="128,206 212,206" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,206 205.0,209.2 205.0,202.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="140.32" y="220" width="143.36" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="234" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Pending D1 · 已提交</text>
<text x="132" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">charge(token, ref = D1)</text>
<polyline points="128,268 298,268" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,268 291.0,271.2 291.0,264.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="290" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功 / 拒绝 / 超时</text>
<polyline points="298,302 128,302" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,302 135.0,298.8 135.0,305.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="324" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Pending → Success</text>
<polyline points="128,336 212,336" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,336 205.0,339.2 205.0,332.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="170.2" y="350" width="83.6" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="364" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Success D1</text>
<text x="48" y="386" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">{D1, Success}</text>
<polyline points="128,398 44,398" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,398 51.0,394.8 51.0,401.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="424" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超时：不改状态，D1 留在 Pending，交给对账</text>
<line x1="44" y1="48" x2="44" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="80" x2="44" y2="413" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="428" x2="44" y2="432" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="80" x2="128" y2="81" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="96" x2="128" y2="115" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="130" x2="128" y2="149" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="164" x2="128" y2="375" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="390" x2="128" y2="413" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="428" x2="128" y2="432" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="80" x2="212" y2="183" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="198" x2="212" y2="218" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="242" x2="212" y2="245" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="260" x2="212" y2="279" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="294" x2="212" y2="313" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="328" x2="212" y2="348" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="372" x2="212" y2="413" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="428" x2="212" y2="432" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="80" x2="298" y2="183" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="198" x2="298" y2="432" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：浏览器、PSP 组件、应用服务、数据库、PSP，以及 Pending 先提交再调 PSP 的顺序。

**常见失分。**
- **先调 PSP 再写库：** 扣了款没记录，最不能出的事故。
- **PSP 调用包进事务：** 连接被占住，事务也回滚不了 PSP 的扣款。
- **把超时当失败：** 用户会重付，PSP 其实已扣。
- **只画方框不说职责：** 分不出是在设计还是在背图。

**面试官可能接着问。**
- 为什么合成一个服务？ → 团队小、一次部署、同一张库；拆开多一跳和这一跳的超时，等真有需要再拆。
- Pending 提交后、调 PSP 前崩了？ → 行留 Pending 没扣款；对账按 D1 查 PSP，查不到就过宽限期后取消并记 Failed，捐款人用新键再来（深入一展开）。
- 为什么 D1 同时做引用号和幂等键？ → 对账只需一个值，查询和防重复都用它。
