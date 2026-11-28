---
id: hi-fix-gofundme-03-token-write-first
node: fix.gofundme
type: qa
step: 3
---
## Q
**GoFundMe · 第 18:52 分 · 只收令牌、先写后扣**｜复盘

面试官：「卡号由支付服务商（PSP）的前端组件收走，你的服务只拿到一个一次性令牌。那你的捐款接口收什么？扣款的先后顺序是什么？」

你会怎么回答？

## A
**当时的回答。**
- **接口：** POST /donations 的请求里仍然带着 card_details，白板上这个契约一直留到最后。
- **顺序：** 流程里有挂起的捐款和结算任务，但没有明说「先把挂起的行提交，再调 PSP」。
**差在哪。**
- **卡号进了我们的服务：** 面试官刚给出令牌化边界，白板上还留着卡号字段，合规范围一下扩大到整个服务。
- **先后没说：** 面试官无法确认「扣了款却没有记录」不会发生。
**应该这样说。**
- **契约只收令牌：** 「POST /donations 收 campaign_id、amount、checkout_attempt_id 和 payment_token。卡号只经过 PSP 的前端组件，从不进我们的服务。」
- **先写再扣：** 「我先创建或找到这个 key 对应的 Pending 行并提交，再调 PSP；donation_id 同时是 PSP 的订单引用和幂等键。」
- **三种结果：** 「成功改成 Success，拒绝改成 Failed，超时保持 Pending，交给结算任务。」
- **崩溃怎么收口：** 「提交后崩：行是 Pending、没扣款。扣款后崩：行是 Pending、已扣款。两种都由结算任务按 donation_id 查 PSP 得到真相。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 314">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="44" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有令牌</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST {key, amount, token}</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① INSERT Pending 并提交</text>
<polyline points="128,118 212,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,118 205.0,121.2 205.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180.64" y="132" width="62.72" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Pending</text>
<text x="132" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② charge(ref = donation_id)</text>
<polyline points="128,180 298,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,180 291.0,183.2 291.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功 / 拒绝 / 超时</text>
<polyline points="298,214 128,214" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,214 135.0,210.8 135.0,217.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ UPDATE 结果</text>
<polyline points="128,248 212,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,248 205.0,251.2 205.0,244.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="114.52" y="262" width="194.96" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="276" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Success / Failed / Pending</text>
<text x="8" y="302" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">卡号不进我们；扣款前一定先有这一行</text>
<line x1="44" y1="48" x2="44" y2="291" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="306" x2="44" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="260" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="284" x2="128" y2="291" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="306" x2="128" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="76" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="110" x2="212" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="154" x2="212" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="172" x2="212" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="206" x2="212" y2="225" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="240" x2="212" y2="260" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="284" x2="212" y2="291" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="306" x2="212" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="172" x2="298" y2="260" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="284" x2="298" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 229">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩在哪里 → 行里是什么 → 怎么收口</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 提交后、调 PSP 前崩</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">行是 Pending，没扣款</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结算：PSP 无此单 → 标 Failed</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② PSP 扣款后、写结果前崩</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">行是 Pending，已扣款</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结算：按 donation_id 查到 → 标 Success</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 如果先扣款、后写行</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">扣了钱，库里什么都没有</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">没有任何东西可查，只能人工退款</text>
</svg>
白板上：请求只带令牌；三步顺序 ① 先提交 Pending、② 再调 PSP、③ 再写结果；下面是崩溃点对照。
**面试官可能接着问。**
- 为什么不在同一个事务里扣款？ → 事务不能包住外部调用：PSP 要几百毫秒甚至几秒，行锁和连接一直被占着；PSP 的扣款也不能随数据库回滚。所以本地记录先提交，扣款在事务之外。
- 令牌能用几次？ → 通常是一次性的，而且只属于发它的那家 PSP。同一次点击的重试带同一个 key，PSP 那一侧用 donation_id 保证只扣一次。
- 怎么保证卡号不经过我们？ → 卡号输入框由 PSP 托管，我们页面上的脚本读不到它。
**同类题。**
- **限时捐款网站：** 同样的令牌化边界和 Pending 先落库。
- **Payment System、钱包转账：** 先写转账记录，再调外部。
- **Robinhood 下单：** 先写订单，再发给交易所。
- **副作用之前先定重试键：** 写在 Pending 行上的就是这个键。
