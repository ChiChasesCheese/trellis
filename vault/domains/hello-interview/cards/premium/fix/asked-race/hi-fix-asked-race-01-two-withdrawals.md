---
id: hi-fix-asked-race-01-two-withdrawals
node: fix.asked-race
type: qa
step: 1
---
## Q
**先答被问的竞态 · 两笔不同的提现**｜补强

面试官：「钱包 500 美元，两笔不同的 500 美元提现同时到。你的系统怎么保证只有一笔成功？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **第一句只说案例：** 「两笔不同的提现，我让数据库只放行一笔。」
- **共享状态是钱包这一行：** 「ready_to_use 是两笔提现争的东西；保护它的是一条语句，检查和扣减在一起，见下面的代码。」
- **0 行和 1 行：** 「影响 1 行，说明这笔拿到了钱：同一个事务里把钱从 ready_to_use 挪到 on_hold，并建 pending 提现。影响 0 行，说明余额不够：回滚，返回 409，不用等支付平台。」
- **为什么只有一笔赢：** 「同一行的更新在数据库里排队；后到的等先到的提交，再重新判断 WHERE，这时 ready_to_use 已经是 0。」
- **调支付平台在事务之后：** 「提交之后才调；事务里不等外部，更不能持着钱包行等外部。」
- **然后才说邻居：** 「重复重试是另一个问题，用 attempt_id，我接着讲。」
**白板。**
```
BEGIN;
UPDATE wallets
SET ready_to_use = ready_to_use - $amt,
    on_hold = on_hold + $amt
WHERE wallet_id = $w
  AND ready_to_use >= $amt;
-- rowcount = 0 -> ROLLBACK, 409
INSERT INTO transactions
  (txn_id, wallet_id, amount, status)
VALUES ($t, $w, $amt, 'pending');
COMMIT;
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 277">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">钱包 1,000，三笔提现同时到</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">A 提现 600：影响 1 行</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ready 1,000 → 400，hold 0 → 600</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">建 pending</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">B 提现 500：影响 0 行</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ready 400 &lt; 500，条件不成立</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回余额不足，不等支付平台</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">C 提现 300：影响 1 行</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ready 400 → 100，hold 600 → 900</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">建 pending</text>
<text x="8" y="255" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">到达顺序不同，谁赢不同；不变量不变：</text>
<text x="8" y="271" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ready + hold = 1,000，ready 永远 ≥ 0</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 202">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个事务里：先占钱，再建记录</text>
<rect x="8" y="26" width="324" height="29" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BEGIN；条件 UPDATE wallets</text>
<polyline points="90,55 90,79" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,79 86.8,72 93.2,72" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="71" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 行</text>
<rect x="8" y="79" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ROLLBACK，返回 409 余额不足</text>
<rect x="8" y="114" width="324" height="29" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="132.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 行：INSERT transactions (pending)；COMMIT</text>
<polyline points="90,143 90,169" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,169 86.8,162 93.2,162" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">提交之后</text>
<rect x="8" y="169" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="187.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">才调支付平台：事务里不等外部</text>
</svg>
白板上：一个事务的三步，旁边写三笔提现的先后结果。
**为什么这样说。** （约 1 分钟。）面试官出了一道具体的竞态，评分点是「共享状态是什么、哪一条语句保护它」。强的回答第一句就是案例，第二句就是那条语句；弱的回答先谈别的机制。
**面试官可能接着问。**
- 为什么不先 SELECT 余额，再 UPDATE？ → 两个请求都读到 500，都通过检查，都扣；检查和扣减必须是同一条语句。
- 0 行之后我还继续往下 INSERT 呢？ → 就会有一笔没有钱支撑的 pending 提现；必须检查行数，0 行就回滚。
- 同一个钱包每秒几千笔提现呢？ → 同一行串行，约 2 ms 一次，约 500 次/秒；个人钱包远到不了，平台级的热点账户才需要分桶。
**常见失分。**
- **先讲幂等键：** 回答的是邻居问题，案例没答。
- **先查后改：** 检查与扣减之间有缝，两个请求都能钻进去。
- **没检查行数：** 余额不足也继续建 pending。
