---
id: hi-mock-donations-website-charities-04-entities
node: qb.sd.donations-website-charities.mock
type: qa
step: 4
---
## Q
**限时捐款网站 · 第 4 步 · 核心实体**｜模拟面试

面试官：「好，接下来说说核心实体。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **三个实体：** 「慈善机构（Charity）、捐款（Donation）、发件箱事件（Outbox）。」
- **Charity：** 「固定几行，配置或一张小表就行：charityId、名称。」
- **Donation 的主键：** 「主键不是自增，而是浏览器在捐款页加载时生成的 UUID，叫 donationId。因为用户不登录，没有别的办法把同一次点击的多次重发认成同一笔。」
- **Donation 的字段：** 「charityId、金额、币种、状态、用了哪家 PSP、PSP 返回的引用号 pspRef、邮箱、创建和更新时间。金额存整数分，不用浮点。」
- **不存什么：** 「不存卡号，也不存令牌：令牌一次性，用完即弃，我们只留 PSP 的引用号。」
- **状态机：** 「CREATED → PROCESSING → SUCCEEDED、FAILED 或 UNKNOWN。CREATED 是我们记下了意图，还没碰 PSP；PROCESSING 是已经发给 PSP；UNKNOWN 是没拿到答案。SUCCEEDED 和 FAILED 是终态，UNKNOWN 只能由对账变成前两者之一。」
- **Outbox：** 「成功时和状态更新同一个事务写入，后面用它可靠地触发收据。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 274">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">核心实体（箭头 = 用 id 指向）</text>
<rect x="8" y="28" width="324" height="92" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="55.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">捐款 Donation（主键 donationId）</text>
<text x="18" y="70.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">charityId · 金额（整数分）· 币种</text>
<text x="18" y="85.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">status · psp（用哪一家）· pspRef</text>
<text x="18" y="100.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">email · createdAt · updatedAt</text>
<rect x="8" y="156" width="150" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="176" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">慈善机构 Charity</text>
<text x="18" y="191" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">charityId · 名称</text>
<text x="18" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">固定几行，配置即可</text>
<rect x="182" y="156" width="150" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="192" y="176" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">发件箱 Outbox</text>
<text x="192" y="191" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">eventId = donationId</text>
<text x="192" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">类型 · 已投递标记</text>
<polyline points="83,120 83,156" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83,156 79.8,149.0 86.2,149.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="89" y="143" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">charityId</text>
<polyline points="257,120 257,156" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257,156 253.8,149.0 260.2,149.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="263" y="143" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一事务</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不存卡号，也不存令牌：令牌用完即弃，</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只留 PSP 返回的引用号 pspRef</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 306">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Donation 状态机</text>
<rect x="100" y="28" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CREATED</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已记录，没碰 PSP</text>
<rect x="100" y="96" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PROCESSING</text>
<text x="170" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已发给 PSP</text>
<rect x="4" y="190" width="96" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="52" y="208.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SUCCEEDED</text>
<text x="52" y="223.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已扣款 · 终态</text>
<rect x="122" y="190" width="96" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="208.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UNKNOWN</text>
<text x="170" y="223.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没拿到答案</text>
<rect x="240" y="190" width="96" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="288" y="208.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">FAILED</text>
<text x="288" y="223.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">未扣款 · 终态</text>
<polyline points="170,68 170,96" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,96 166.8,89.0 173.2,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="86" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件更新</text>
<polyline points="170,136 170,190" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,190 166.8,183.0 173.2,183.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">超时 / 5xx</text>
<polyline points="122,116 52,116 52,190" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="52,190 48.8,183.0 55.2,183.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="58" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功</text>
<polyline points="218,116 288,116 288,190" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="288,190 284.8,183.0 291.2,183.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="282" y="112" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拒绝</text>
<polyline points="122,212 100,212" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100,212 107.0,208.8 107.0,215.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="218,212 240,212" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,212 233.0,215.2 233.0,208.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="111" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对账</text>
<text x="229" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对账</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNKNOWN 只能由对账变成前两者之一，</text>
<text x="8" y="294" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">在那之前不允许任何人重发这笔扣款</text>
</svg>
白板上新增：三个实体和 Donation 的状态机；UNKNOWN 用来表示「不知道扣没扣」。
**为什么这样说。** （约 2 分钟，累计第 9 分钟。）面试官看你有没有为这场面试最特别的东西建模：状态机里的 UNKNOWN。强的回答在这里就把 donationId 的来历讲清楚，并且说出 UNKNOWN 为什么不能并进 FAILED。弱的回答只画 Donation 一张表，状态只有 成功 和 失败。
**面试官可能接着问。**
- 为什么要有 UNKNOWN，不直接标 FAILED？ → 超时意味着 PSP 可能已经扣了款。标 FAILED，用户会重试，就是第二次扣款。UNKNOWN 明确说「不知道」，并且禁止重发，直到查清。
- 为什么 CREATED 和 PROCESSING 要分开？ → 两者之间的那次转换是一道闸：只有把状态从 CREATED 改成 PROCESSING 成功的那个请求，才有资格去调 PSP。这是深入一的核心。
- 为什么主键用客户端生成的 UUID，而不是服务端自增？ → 服务端生成的 id 在用户重发时没法和上一次关联；客户端生成的 id 让同一次意图在任何重试里都是同一个键。
- Charity 需要建表吗？ → 固定 5 行，配置文件即可；但回执要显示机构名，一张小表更方便，两者都行。
**常见失分。**
- **漏掉 UNKNOWN：** 状态只有成功和失败，超时无处安放，只能乱标。
- **存卡号或令牌：** 违背令牌化的初衷，合规范围一下子变大。
- **金额用浮点：** 钱用整数分，浮点会有精度误差。
