---
id: hi-fix-airbnb-wallet-03-asked-race
node: fix.airbnb-wallet
type: qa
step: 3
---
## Q
**Airbnb Wallet · 两笔不同的提现**｜复盘

面试官：「钱包里有 500 美元。两笔不同的 500 美元提现同时到达，会发生什么？」

你会怎么回答？

## A
**当时的回答。**
- **先讲了 ID：** 你先谈 transaction id 和 attempt id，怎样让同一个请求只处理一次。
- **后来回到了正轨：** 追问之后，你落到钱包行加条件更新上，这一步是对的。
**差在哪。**
- **答的是邻居问题：** transaction id、attempt id 回答的是重复重试：同一个用户动作发了两次。
- **幂等键帮不上这个案例：** 两笔提现是两个动作，attempt_id 各不相同，都会通过幂等检查，然后一起去扣同一个 500。
- **时间花在了前半段：** 正确答案是一条语句，却在讲了一大圈之后才出现。
**应该这样说。**
- **先用一句话说案例：** 「两笔不同的提现，我让数据库只放行一笔。」
- **再给那一条操作：** 见下面的代码。
- **说清 0 和 1：** 「影响 1 行，就在同一个事务里创建 pending 提现；影响 0 行，返回余额不足。」
- **为什么只有一笔赢：** 「同一行的更新在数据库里排队；第二条等第一条提交后重新判断 WHERE，这时 ready_to_use 已经是 0。」
- **最后才补邻居：** 「重复重试是另一回事：同一个 attempt_id 的第二次请求，返回第一次的交易。」
**白板。**
```
UPDATE wallets
SET ready_to_use = ready_to_use - 500,
    on_hold = on_hold + 500
WHERE wallet_id = $1
  AND ready_to_use >= 500;
-- 1 行：建 pending；0 行：余额不足
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">钱包 500，两笔不同的 500 同时到</text>
<rect x="8" y="34" width="84" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="50" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 A</text>
<rect x="128" y="34" width="84" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 B</text>
<rect x="248" y="34" width="84" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="290" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">wallets 行</text>
<text x="54" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … ready_to_use &gt;= 500</text>
<polyline points="50,110 290,110" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="290,110 283,113.2 283,106.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="54" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 行：ready 500→0，hold 0→500</text>
<polyline points="290,144 50,144" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="50,144 57,147.2 57,140.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一条 UPDATE</text>
<polyline points="170,178 290,178" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="290,178 283,181.2 283,174.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 行：余额不足</text>
<polyline points="290,212 170,212" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,212 177,215.2 177,208.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="50" y1="74" x2="50" y2="234" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="74" x2="170" y2="87" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="101" x2="170" y2="121" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="135" x2="170" y2="234" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="290" y1="74" x2="290" y2="234" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 194">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两个问题，两个答案</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">同一个动作被发了两次</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">例：点了两次，或超时后重发</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">attempt_id 唯一键：返回第一笔交易</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">两个不同的动作争同一笔钱</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">例：两笔不同的 500 对一个 500</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一条条件 UPDATE：只放行一笔</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被问哪个，先答哪个；另一个单独补一句</text>
</svg>
白板上：一条条件 UPDATE，下面是两个请求的先后和各自的行数。
**为什么这样说。** （约 1 分钟。）面试官出的是一道具体的竞态题，看你先答哪个。强的回答第一句就是被问的案例和那一条操作；弱的回答从相邻的问题说起，说完才发现没答到。
**面试官可能接着问。**
- 钱包有 1000，已有一笔 600 在途，再来 500 呢？ → ready_to_use 只剩 400，条件不成立，本地直接拒绝，不用等支付平台。
- 为什么不先 SELECT 余额再 UPDATE？ → 两个请求都读到 500，都通过检查，都扣；检查和扣减必须是同一条语句。
- 那重试怎么处理？ → attempt_id 在 transactions 上加唯一约束，重复请求撞上约束，返回第一笔；这是另一条机制，单独说。
**同类题。**
- **Ticketmaster 两个人抢 A15、秒杀库存 1 件：** 同样先答竞态，再补重试。
- **GoFundMe 的 PSP 重试：** 那里才是重复重试，用 checkout_attempt_id。
