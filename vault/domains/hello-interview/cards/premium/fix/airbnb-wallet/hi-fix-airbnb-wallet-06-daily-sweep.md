---
id: hi-fix-airbnb-wallet-06-daily-sweep
node: fix.airbnb-wallet
type: qa
step: 6
---
## Q
**Airbnb Wallet · webhook 丢了**｜复盘

面试官：「支付平台的 webhook 没送到，或者你的 endpoint 当时挂了。那笔转账一直是 pending，怎么办？」

你会怎么回答？

## A
**当时的回答。**
- **建模是对的：** 转账先是 pending，之后靠 webhook 或轮询收尾。
- **兜底说得很虚：** 「会有个任务去扫、去轮询」，没有说多久一次，也没有说扫哪些。
**差在哪。**
- **没有频率：** 面试官没法知道丢了的回调多久能恢复。
- **没有选择规则：** 「扫 pending」可以是全表，也可以是上一小时的，差了几个数量级。
- **没有说清为什么安全：** 重复或迟到的更新会不会把余额改两次，没有交代。
**应该这样说。**
- **先存：** 「创建转账时先写 pending 行；createTransfer 返回后，保存 vendor_transfer_id。」
- **webhook 是常态路径：** 「收到 webhook，按 vendor_transfer_id 找到行，在一个事务里把 status 从 pending 改成 completed 或 failed，同时更新钱包的 ready_to_use 和 on_hold；行已经是终态，就什么也不做。」
- **每天一次的扫描：** 「选 status = pending 且 created_at 早于 1 小时前的行，按 vendor_transfer_id 问支付平台，套用同一个事务。」
- **频率从恢复窗口来：** 「丢失的回调要在 24 小时内补上，所以扫描至少每天一次；webhook 通常几分钟内到，1 小时没到的才算可疑。」
- **成本：** 「多一个后台任务，丢失的回调有最长一天的延迟，换来不依赖 webhook 一定送达。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两条路，一个事务</text>
<rect x="8" y="26" width="158" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">常态路径</text>
<text x="87" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">webhook 到达</text>
<rect x="174" y="26" width="158" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">兜底路径</text>
<text x="253" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天一次扫描</text>
<polyline points="170,70 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 166.8,85 173.2,85" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="92" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">同一个数据库事务</text>
<text x="170" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">status 从 pending 改成终态</text>
<text x="170" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同时改 ready_to_use 和 on_hold</text>
<text x="170" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已是终态：什么都不做</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扫描补的是 webhook 没送到的那几笔</text>
</svg>
白板上：两条路进同一个事务框；扫描一侧写上「每天、pending 且超过 1 小时」。
**为什么这样说。** （约 1 分钟。）面试官看你的兜底是不是一个可执行的任务。强的回答给出选择规则、频率和复用同一个事务；弱的回答是「再轮询一下」。
**面试官可能接着问。**
- 扫描会不会和 webhook 同时改同一行？ → 两边都是「WHERE status = pending」的条件更新，只有一个影响 1 行；输的那个看到终态，什么也不做。
- 崩在「支付平台已接受、vendor_transfer_id 还没存」呢？ → 创建时把 transaction_id 当成我方的引用号一起发给平台，扫描可以按它查；见「回调是常态路径，扫描兜底」。
- 一次扫描要调多少次平台？ → 只扫超过 1 小时的 pending；假设 1% 的转账会这样，约 1,430,000 笔/天 × 1% ≈ 14,300 次/天；摊在一天里平均 0.17 次/秒，远低于上限。
**同类题。**
- **GoFundMe 的结算任务：** 同样是 Pending 超时后按 donation_id 去 PSP 查。
- **Payment System：** 异步支付网络下，回调加对账是标准做法。
