---
id: bagu-mvcc-4-rc-rr-view
node: a.mysql.mvcc
type: qa
step: 4
---
## Q
**RC 与 RR · ReadView 什么时候创建，为什么这决定了可重复读**｜必会

面试官：「RC 和 RR 都用 MVCC，为什么一个会不可重复读，一个不会？」

## A
**基本回答。** 读已提交（RC，Read Committed）和可重复读（RR，Repeatable Read）都用 MVCC，差别只在 ReadView 什么时候创建。RC：每次普通 `SELECT` 都新建一个 ReadView，所以每次都能看到「此刻」已经提交的数据；两次读之间别人提交了修改，第二次就读到新值。RR：事务里第一次快照读时创建一次 ReadView，整个事务复用，之后别人提交什么，只要事务 ID 在创建时是活跃的或者晚于创建，一律不可见。
RR 的视图创建点是第一次快照读，不是 `BEGIN`；想在事务开始时就固定，用 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">会话A 两次读，中间会话B 提交了修改</text>
<line x1="14" y1="50" x2="326" y2="50" stroke-width="1.2" stroke="currentColor"/>
<rect x="79" y="46" width="8" height="8" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="290" y="46" width="8" height="8" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读1</text>
<text x="294" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读2</text>
<line x1="190" y1="74" x2="190" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,56.0 193.2,63.0 186.8,63.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="190" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 改成 200 并提交</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RC</text>
<rect x="40" y="110" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">视图1 → 100</text>
<rect x="236" y="110" width="96" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="284.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">视图2 → 200</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RR</text>
<rect x="40" y="154" width="292" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="186.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一个视图 → 两次都是 100</text>
<line x1="83" y1="56" x2="83" y2="110" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="294" y1="56" x2="294" y2="110" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RC 每次读都新建视图：会读到新提交的值</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RR 第一次读建视图后一直用：读到的不变</text>
</svg>
会话 A 读了两次，中间会话 B 提交了修改：RC 的两次读各建一个视图，第二次读到 200；RR 只在第一次建视图，两次都是 100。
**举个例子。** 8.0.46 上两个会话（账户行 `id=1` 余额 100，B 的事务 ID 记为 210）：
1. A 开事务，`SELECT balance FROM account WHERE id=1` → 100。RR 下此时创建视图，B 还没拿到事务 ID，所以视图的 `max_trx_id` 不会超过 210。
2. **B 提交：**B 执行 `UPDATE account SET balance=200 WHERE id=1; COMMIT;`，行上变成 `(200, trx_id=210)`，旧版本 100 进了 undo。
3. **A 再读一次：**
   - RC：新建视图，B 已经提交，不在 `m_ids` 里，且 210 小于新的 `max_trx_id`，可见 → 200。
   - RR：复用第一次的视图，210 大于等于它的 `max_trx_id`（视图创建后才开始的事务），不可见，顺着回滚指针读到旧版本 → 100。
4. **自己改的看得到：**如果 A 在 RR 下自己 `UPDATE` 了这行再读，看到的是自己改的值。
**容易错。**
- **以为 RR 靠锁实现可重复读：** 是靠固定读视图，普通读不加锁。
- **以为 RR 在 BEGIN 建视图：** 是第一次快照读时创建；中间如果别的事务在 BEGIN 和第一次读之间提交了，也会被看到。
- **以为 RC 完全没有 MVCC：** RC 也用 MVCC，只是每次读都新建视图。
- **以为 RR 下看不到任何新数据：** 自己的修改看得到；混用当前读时还会看到别人新插入的行（见下一张卡）。
