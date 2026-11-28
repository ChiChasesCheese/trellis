---
id: hi-fix-asked-race-02-retry-vs-race
node: fix.asked-race
type: qa
step: 2
---
## Q
**先答被问的竞态 · 重试和竞态分开说**｜补强

面试官：「我再问一个：用户点了两次提现，请求重复发了两次。这和刚才的两笔不同提现，有什么区别？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **一句话分清：** 「重复重试是同一个动作发了两次，要返回同一笔；两笔不同的提现是两个动作，争同一笔钱，只放行一笔。」
- **键在客户端生成：** 「客户端在第一次发送之前生成 attempt_id，每次重发都带上同一个；transactions.attempt_id 有唯一约束。」
- **同一个事务里的顺序：** 「先 INSERT pending 行，ON CONFLICT DO NOTHING；0 行说明是重复，读出已有的一笔返回，结束。1 行才继续做条件 UPDATE；条件 UPDATE 影响 0 行，ROLLBACK，pending 行一起撤掉。」
- **同键不同内容：** 「保存首次请求的金额；同一个 attempt_id、金额不同，返回 409，不当成重试。」
- **两个机制互不替代：** 「只有 attempt_id，两笔不同的提现都通过；只有条件 UPDATE，重复的同一笔会各扣一次。」
**白板。**
```
BEGIN;
INSERT INTO transactions
  (txn_id, wallet_id, amount,
   attempt_id, status)
VALUES ($t, $w, $amt, $a, 'pending')
ON CONFLICT (attempt_id) DO NOTHING;
-- 0 行: 重复，读出已有那笔，返回
UPDATE wallets SET ... WHERE ...
  AND ready_to_use >= $amt;
-- 0 行: ROLLBACK，409
COMMIT;
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 155">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先问一句：这两个请求是同一个动作吗？</text>
<rect x="8" y="26" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两个请求同时到达，扣同一个钱包</text>
<polyline points="170,55 170,77" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,77 166.8,70 173.2,70" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="77" width="158" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">是，同一个动作</text>
<text x="87" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重复重试</text>
<text x="87" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">attempt_id 唯一键</text>
<text x="87" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回第一笔</text>
<rect x="174" y="77" width="158" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">不是，两个动作</text>
<text x="253" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">真正的竞态</text>
<text x="253" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件 UPDATE</text>
<text x="253" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只放行一笔</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 155">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个事务里的顺序</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1. INSERT pending，ON CONFLICT (attempt_id)</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DO NOTHING</text>
<polyline points="170,70 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 166.8,85 173.2,85" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="92" width="158" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="87" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">0 行：重复</text>
<text x="87" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读出已有那笔</text>
<text x="87" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原样返回，结束</text>
<rect x="174" y="92" width="158" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">1 行：新请求</text>
<text x="253" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2. 条件 UPDATE wallets</text>
<text x="253" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 行：ROLLBACK，409</text>
</svg>
白板上：先一个判断框，分成两条路；再画同一个事务里的顺序。
**为什么这样说。** （约 1 分钟。）面试官看你能不能把两个相邻的问题拆开，并且知道它们怎么在同一个事务里共存。强的回答说出顺序和 0 行的处理；弱的回答是把二者混成「加个幂等」。
**面试官可能接着问。**
- 两个请求同一个 attempt_id 同时到呢？ → 唯一约束让其中一个 INSERT 等另一个提交；之后它看到冲突，返回已有那笔。
- 为什么先 INSERT，后 UPDATE？ → 先占 attempt_id，重复请求在碰钱之前就被挡住，不会扣两次。
- attempt_id 保留多久？ → 至少比客户端最长的重试窗口久，例如 7 天。它是交易行上的唯一约束，交易行本来要留 7 年，所以随行保留，不单独清理，也不能为清它去删财务记录。
**常见失分。**
- **两个问题混着答：** 面试官分不清你在答哪一个。
- **只有条件 UPDATE：** 超时重发的同一笔会再扣一次。
- **只有 attempt_id：** 两笔不同的提现一起通过。
