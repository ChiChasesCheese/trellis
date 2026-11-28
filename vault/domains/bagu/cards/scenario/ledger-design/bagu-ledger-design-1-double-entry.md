---
id: bagu-ledger-design-1-double-entry
node: b.scenario.ledger-design
type: qa
step: 1
---
## Q
**复式账本 · 分录、余额与冲正**｜必会

面试官：「主播申请提现，运营发现他的余额字段和流水加起来对不上。账本要怎么设计，才能查出差在哪一笔，并且改错时不破坏历史？」

## A
**基本回答。** 账本只追加、不修改：每笔业务一条日志（journal），下挂至少两行分录（posting），借为正、贷为负，同一币种金额之和恒为 0（钱有来处就有去处，少一行写入时就能暴露）；换汇经外汇（FX）中间账户拆成两组各自平衡的分录。金额用整数最小货币单位加币种，浮点会累积误差。余额是分录的投影，可存字段加速读，但必须能由分录重算，且与分录在同一事务里更新；并发扣减写成 `UPDATE ... SET balance = balance - x WHERE balance >= x`，检查与扣减是一条语句，不会透支。改错不动旧记录，追加反向分录冲正：`reverses_id` 指回原 journal 并建唯一约束，一笔最多冲正一次；业务键（business_key）唯一，重复请求返回第一次的结果；数据库账号对账本表只授予 INSERT 和 SELECT。用户钱包对平台是负债，所以充值是借银行存款、贷用户钱包。热点账户（如平台收入）单行更新持锁约 2 ms，上限约 500 次/秒，改为同步路径只追加分录，余额等于快照加增量，后台按秒合并净额。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 288">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">journal J1：主播充值 500 币</text>
<rect x="6" y="22" width="328" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="41" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">借  银行存款</text>
<text x="326" y="41" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">+500</text>
<rect x="6" y="54" width="328" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="73" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">贷  用户钱包</text>
<text x="326" y="73" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">−500</text>
<text x="8" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同币种分录之和 = 0 ✓</text>
<line x1="170" y1="110" x2="170" y2="126" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,126.0 166.8,119.0 173.2,119.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="128" width="260" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额 = 分录之和（可重算）</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">冲正 J2：reverses_id → J1</text>
<rect x="6" y="192" width="328" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="211" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">借  用户钱包</text>
<text x="326" y="211" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">+500</text>
<rect x="6" y="224" width="328" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="243" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">贷  银行存款</text>
<text x="326" y="243" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">−500</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">J1 不改；reverses_id 唯一，最多冲正一次</text>
</svg>
上半部分是充值 J1：银行存款借 +500，用户钱包贷 −500，和为 0。下面是冲正 J2：不改 J1，追加反向分录，用 `reverses_id` 指回 J1。
**举个例子。** 主播提现前，运营发现余额字段比分录之和多 500 币。定期用分录重算该账户发现差额，追到某次人工改库直接改了余额字段、没有对应分录；不涂改旧记录，追加反向分录冲正，余额字段按分录重建，旧记录原样保留供审计。撤销 J1 则追加 J2（钱包 +500，银行存款 −500），J1 与 J2 之和为 0；有人再冲正 J1，`reverses_id` 唯一约束让第二次插入失败。余额 100 两个请求同时扣 80：一个变 20，另一个影响 0 行。
**容易错。**
- **余额字段当唯一真相：** 不一致时以分录为准，差额追到具体 journal。
- **不同币种混在一起平衡：** 每个币种各自平衡。
