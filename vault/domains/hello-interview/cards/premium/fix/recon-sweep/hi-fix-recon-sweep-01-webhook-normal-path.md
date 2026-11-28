---
id: hi-fix-recon-sweep-01-webhook-normal-path
node: fix.recon-sweep
type: qa
step: 1
---
## Q
**回调是常态路径 · webhook 怎么落状态**｜补强

面试官：「支付平台处理完提现，会发一个 webhook 给你。你的系统收到之后怎么处理？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先存两个 ID：** 「创建转账时先写 pending 行，再调 createTransfer，把 transaction_id 当作我方的引用号一起发过去；平台返回 vendor_transfer_id，我马上存到这一行。」
- **webhook 按 vendor_transfer_id 找行：** 「先验签，再按 vendor_transfer_id 找到这一行。」
- **一个事务做两件事：** 「把 status 从 pending 改成 completed 或 failed，同时改钱包：completed 时 on_hold 减去金额；failed 时 on_hold 减去金额，ready_to_use 加回金额。」
- **终态就忽略：** 「UPDATE 带 WHERE status = 'pending'，影响 0 行说明行已经是终态，什么也不做，返回 200。重复的 webhook、迟到的 webhook，都只是空操作。」
- **提交之后才返回 200：** 「事务没提交就返回 200，平台就不会再重发，更新会丢。」
- **没有 vendor_transfer_id 的行：** 「崩在「平台已接受、我还没存 ID」之间：这一行只有我方的 transaction_id。平台那边的引用号就是它，所以 webhook 和扫描都能按它对上。」
**白板。**
```
UPDATE transactions SET status = $new
WHERE vendor_transfer_id = $v
  AND status = 'pending'
RETURNING wallet_id, amount;
-- 0 行: 已是终态，返回 200，到此为止
-- 1 行才继续下面的钱包更新
UPDATE wallets
SET on_hold = on_hold - $amount,
    ready_to_use = ready_to_use +
      CASE WHEN $new = 'failed'
           THEN $amount ELSE 0 END
WHERE wallet_id = $wallet_id;
COMMIT;
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 322">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先存 ID，webhook 才找得到这一行</text>
<rect x="8" y="34" width="84" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="50" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">钱包服务</text>
<rect x="128" y="34" width="84" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="248" y="34" width="84" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="290" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付平台</text>
<text x="54" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 转账（pending）</text>
<polyline points="50,110 170,110" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,110 163,113.2 163,106.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="54" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">createTransfer（ref = txn_id）</text>
<polyline points="50,144 290,144" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="290,144 283,147.2 283,140.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="54" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回 vendor_transfer_id</text>
<polyline points="290,178 50,178" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="50,178 57,181.2 57,174.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="54" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保存 vendor_transfer_id</text>
<polyline points="50,212 170,212" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,212 163,215.2 163,208.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="234" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">之后某一刻</text>
<line x1="8" y1="230" x2="134" y2="230" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="206" y1="230" x2="332" y2="230" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="54" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">webhook：completed</text>
<polyline points="290,270 50,270" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="50,270 57,273.2 57,266.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="54" y="292" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个事务：pending → completed</text>
<polyline points="50,304 170,304" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,304 163,307.2 163,300.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="50" y1="74" x2="50" y2="326" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="74" x2="170" y2="87" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="101" x2="170" y2="121" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="135" x2="170" y2="155" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="169" x2="170" y2="189" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="203" x2="170" y2="223" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="237" x2="170" y2="247" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="261" x2="170" y2="281" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="295" x2="170" y2="326" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="290" y1="74" x2="290" y2="326" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">webhook 处理：同一个事务规则</text>
<rect x="8" y="26" width="158" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">影响 1 行</text>
<text x="87" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">pending → 终态</text>
<text x="87" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同事务改钱包</text>
<rect x="174" y="26" width="158" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">影响 0 行</text>
<text x="253" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已是终态</text>
<text x="253" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">什么都不做，返回 200</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">钱包怎么改</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">completed：on_hold −= 金额</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">failed：on_hold −= 金额，ready_to_use += 金额</text>
</svg>
白板上：先存 ID 的时序，再画 webhook 的两个分支。
**为什么这样说。** （约 1 分钟。）面试官要确认 webhook 是一条可重复执行的路径，而不是一次性的通知。强的回答说出 ID 怎么存、事务里改哪两个地方、终态怎么忽略；弱的回答是「收到 webhook 就更新状态」。
**面试官可能接着问。**
- 平台重发了同一个 webhook？ → 第二次 UPDATE 影响 0 行，什么也不改；返回 200，让平台停止重发。
- webhook 来得比「保存 vendor_transfer_id」还早呢？ → 按 vendor_transfer_id 找不到行，就按 webhook 里带回的我方引用号（多数平台会带）找；两个键都留着。
- 平台说查不到这笔呢？ → 用同一个引用号重发 createTransfer，平台按它去重；不会转两次。
**常见失分。**
- **只更状态，不更钱包：** 两处分开提交，崩在中间就对不上。
- **不检查当前状态：** 迟到的 webhook 把终态又改回去。
- **先返回 200 再处理：** 处理失败时平台不会重发，更新丢了。
