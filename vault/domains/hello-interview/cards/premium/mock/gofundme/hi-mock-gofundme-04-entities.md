---
id: hi-mock-gofundme-04-entities
node: fix.gofundme-mock
type: qa
step: 4
---
## Q
**GoFundMe · 第 4 步 · 核心实体**｜模拟面试

面试官：「好，数字够了。接下来说说核心实体。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **三个实体：** 「用户（User）、活动（Campaign）、捐款（Donation）。」
- **活动：** 「campaign_id、目标金额。它已经存在，创建线外，我只当一张被引用的表。」
- **用户：** 「user_id、显示名。捐款人必须登录。」
- **捐款是核心：** 「donation_id 是主键，服务端生成的 UUID。它同时是我给 PSP 的引用号和幂等键，所以对账时可以拿它去查。」
- **重试身份：** 「另有 checkout_attempt_id，由客户端在打开结算页、第一次扣款之前生成。它有唯一约束，是重试的身份：同一次点击的每次重发都带它。」
- **其他字段：** 「campaign_id、user_id、金额（整数分，不用浮点）、币种、状态、创建和更新时间。」
- **状态机：** 「Pending、Success、Failed。PSP 说成功就改成 Success，说拒绝就改成 Failed，超时不动，留在 Pending。每次转换都是 UPDATE … WHERE status='Pending'，只有一个调用者能赢。」
- **不存的东西：** 「不存卡号，也不存令牌，令牌用完即弃。」
- **主动留白：** 「已募金额、最近 100 笔、最大 10 笔是派生值，我讲到它们时再加表，现在不画。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 340">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">核心实体（箭头 = 用 id 指向）</text>
<rect x="8" y="28" width="324" height="130" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">捐款 Donation</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">donation_id（主键）· 金额（整数分）</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">checkout_attempt_id（唯一约束）</text>
<text x="18" y="104.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">campaign_id · user_id · 币种</text>
<text x="18" y="119.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">status：Pending | Success | Failed</text>
<text x="18" y="134.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">created_at · updated_at</text>
<rect x="8" y="204" width="156" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="224" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">活动 Campaign</text>
<text x="18" y="239" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">campaign_id · 目标金额</text>
<text x="18" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已存在，创建线外</text>
<rect x="176" y="204" width="156" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="186" y="224" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">用户 User</text>
<text x="186" y="239" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">user_id · 显示名</text>
<text x="186" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已登录才能捐</text>
<polyline points="86,158 86,204" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="86,204 82.8,197.0 89.2,197.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="92" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">campaign_id</text>
<polyline points="254,158 254,204" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="254,204 250.8,197.0 257.2,197.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="260" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">user_id</text>
<text x="8" y="292" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有卡号，也不存令牌：令牌用完即弃</text>
<text x="8" y="310" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">总额、最近、最大三个字段是派生值，</text>
<text x="8" y="328" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等讲到它们时再加表，现在不画</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Donation 状态机</text>
<rect x="100" y="28" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Pending</text>
<text x="170" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已提交，等结果</text>
<rect x="24" y="150" width="112" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Success</text>
<text x="80" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">终态 · 已扣款</text>
<rect x="204" y="150" width="112" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Failed</text>
<text x="260" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">终态 · 未扣款</text>
<polyline points="130,72 130,100 80,100 80,150" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,150 76.8,143.0 83.2,143.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="86" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">PSP 成功</text>
<polyline points="210,72 210,100 260,100 260,150" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260,150 256.8,143.0 263.2,143.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="254" y="130" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">PSP 拒绝</text>
<text x="170" y="226" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">超时 / 5xx：留在 Pending，不改状态</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每条转换都是 UPDATE … WHERE status='Pending'，</text>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有一个调用者会赢；终态不再变化</text>
</svg>
白板上新增：三个实体和 Donation 状态机。
**为什么这样说。** （约 3 分钟，累计第 12 分钟。）面试官看实体能不能服务后面的流程：有两个编号，说明你知道客户端要在第一次响应之前就有一个能重发的键；状态机说明你知道超时不是失败。弱的回答只有一个 id，由服务端在创建后返回；或者实体里还有卡号和 card_details。
**面试官可能接着问。**
- 为什么要两个编号？ → donation_id 是服务端在创建行时生成的，如果第一次响应丢了，客户端并不知道它，没有东西可以重发。checkout_attempt_id 是客户端先生成的，所以重试带得出去。
- 为什么 checkout_attempt_id 要唯一？ → 唯一约束让数据库来保证：同一个键最多一行，并发的两个请求也只会有一个插入成功。
- 金额为什么用整数分？ → 浮点有舍入误差，钱的计算不能有；PSP 也是用最小货币单位。
- 为什么没有 Refunded 状态？ → 退款线外。要做的话，它是另一个有状态的流程。
**常见失分。**
- **只有一个 id：** 服务端创建后才返回的 id 没法在第一次响应丢失时重发，重试就对不上同一笔。
- **存卡号或令牌：** 令牌是一次性的，存下来没有用，卡号更不能进我们的系统。
- **把超时当失败：** 超时时 PSP 可能已经扣了款，记成 Failed 会让用户重付一次。
- **金额用浮点：** 钱不能有舍入误差。
