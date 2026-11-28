---
id: bagu-payment-system-5-ledger-safety
node: a.scenario.payment-system
type: qa
step: 5
---
## Q
**账务与资金安全 · 余额不透支、账平、可审计**｜必会

面试官：「用户余额怎么扣才不会透支？怎么保证账是平的，出了问题怎么查？」

## A
**基本回答。** 三层保护。第一层条件更新：`UPDATE account SET balance=balance-80 WHERE id=? AND balance>=80`，影响 0 行就拒绝；先读后写时两个请求都读到 100、都判断够，会互相覆盖或扣成 −60，条件更新靠行锁串行，第二个拿到锁时余额已是 20。第二层复式记账：每次资金变动一借一贷两条分录，和余额更新在同一事务（否则会「钱动了没记账」或反过来），业务单号唯一防重复请求写两遍；全账借贷总和恒为 0，少一条腿立刻不平，余额只是分录之和的缓存，随时可重算校验。第三层分录只追加，记错了写冲销分录（方向相反）抵消，历史可审计。热点账户（平台手续费户）每笔都更新同一行，假设持行锁约 2 毫秒，一行上限约 500 次/秒，要分桶或异步汇总。入账去重别用会淘汰 key 的缓存，去重记录一丢同一笔就能再入账。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="4" y="6" width="332" height="148" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="12" y="22" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个数据库事务</text>
<rect x="14" y="32" width="150" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="89.0" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣用户余额 100→20</text>
<text x="89.0" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">WHERE balance>=80</text>
<rect x="176" y="32" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251.0" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务单号唯一</text>
<text x="251.0" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重复请求写不进去</text>
<rect x="14" y="86" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="89.0" y="105.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分录 1：用户 −80</text>
<rect x="176" y="86" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251.0" y="105.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分录 2：收入户 +80</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">借贷合计 = 0，少一条腿立刻暴露</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分录只追加：记错了写冲销分录，历史不动</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">余额 = 分录之和的缓存，随时可重算校验</text>
</svg>
一次扣款在同一事务里做三件事：条件扣减、写一借一贷两条分录、防重复；全账借贷合计始终为 0。
**举个例子。** 余额 100 币，给主播打赏连点两次各 80：第一次条件更新影响 1 行，余额 20，同事务写分录用户 −80、主播收入户 +80；第二次拿到锁时余额 20 小于 80，影响 0 行，返回余额不足，没有任何分录。发现记错金额时，旧分录不动，写一对冲销分录再写一对正确分录。
**容易错。**
- **以为余额字段就是账本：** 以分录重算为准。
- **改旧分录纠错：** 审计失效，要用冲销分录。
