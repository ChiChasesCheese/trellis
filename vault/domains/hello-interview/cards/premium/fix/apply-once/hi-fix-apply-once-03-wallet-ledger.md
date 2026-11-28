---
id: hi-fix-apply-once-03-wallet-ledger
node: fix.apply-once
type: qa
step: 3
---
## Q
**钱包转账与账本 · 只应用一次**｜补强

面试官：「转账完成的事件会被重放，钱包余额又是账本分录的汇总。怎么保证一笔转账只入账一次，余额不多不少？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先分清事实和派生：** 「账本分录是事实，只追加不修改；钱包余额是由分录派生的缓存。重放要防的是余额多加，所以关键是让分录本身有唯一的身份。」
- **分录的 id 由转账号派生：** 「借方分录 `entry_id = 转账号:debit`，贷方 `转账号:credit`，主键唯一。同一笔转账再入账一次，主键冲突。」
- **这里分录就是已应用记录：** 「不需要另外一张已应用表：分录里已经有来源转账号和唯一约束，插进去等于登记了「这笔我入过账」。」
- **一个事务里怎么写：** 「先插两条分录 `ON CONFLICT DO NOTHING`；插进 2 行才继续，0 行就是重放，直接返回；然后借方 `UPDATE wallets SET balance = balance - :a WHERE id = :src AND balance >= :a`，贷方 `balance + :a`，提交。」
- **余额不足也是结果：** 「借方 UPDATE 影响 0 行，就回滚分录和余额变更，另外把转账记为 REJECTED；同一个转账号重放，读到的还是 REJECTED。」
- **避免死锁：** 「两个账户都要更新，按账户 id 升序更新，两个方向相反的转账不会互相等待。」
- **怎么对账：** 「周期性比较 `wallets.balance` 和 `SUM(delta)`，不一致说明有人绕过了分录直接改了余额。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个事务，四步</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 插两条分录</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">entry_id = 转账号:借 / 转账号:贷，唯一</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 插进了 2 行吗？</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">没有 = 重放：直接返回，不动余额</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 借方 UPDATE</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">balance = balance − a WHERE balance &gt;= a</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">④ 贷方 UPDATE；COMMIT</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">③ 影响 0 行：ROLLBACK，记 REJECTED</text>
</svg>
白板上：一个事务里的四步，没插进 2 行就整个跳过。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ledger_entries（事实）</text>
<rect x="8" y="26" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">t1:debit    账户 1    −2000</text>
<text x="18" y="69" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">t1:credit   账户 2    +2000</text>
<text x="18" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">entry_id 主键：同一笔再插一次，冲突</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">wallets（派生，可由分录重算）</text>
<rect x="8" y="138" width="324" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="158.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">账户 1：5000 → 3000</text>
<text x="18" y="173.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">账户 2：0 → 2000</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对账：balance = SUM(delta)，</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不一致说明某处绕过了分录</text>
</svg>
白板上：分录是事实，余额是可重算的派生值。

**为什么这样说。** 面试官要看你能不能识别：有时候「已应用记录」就是事实表本身。弱的回答会再加一张表、一个缓存、一个重试逻辑；强的回答让分录带来源转账号并加唯一约束，余额变成可以重算的派生值。
**面试官可能接着问。**
- 为什么不直接 `UPDATE balance` 然后记一条日志？ → 日志和余额分两步写，崩在中间，两者不一致；分录先落、余额随事务派生，不一致时以分录为准重算。
- 转账事件乱序到达怎么办？ → 每笔转账独立，加减是可交换的；需要保证的只是余额不能为负，由条件更新在写入时检查。
- 外部渠道的回调重放呢？ → 回调带渠道的流水号，同样用它派生分录 id。
- 余额读很多怎么办？ → 读 `wallets.balance`，必要时再放一层缓存；缓存只能 SET 成已提交的值。
**常见失分。**
- **余额直接 `+=` 没有记录：** 重放就多入一次账。
- **先查有没有入过再入账：** 两个并发的重放都查不到，都入账。
- **分录和余额分开提交：** 崩在中间，两边对不上。
- **拒绝不保存：** 同一个转账号重放时，也许余额已经够了，结果就变了。
