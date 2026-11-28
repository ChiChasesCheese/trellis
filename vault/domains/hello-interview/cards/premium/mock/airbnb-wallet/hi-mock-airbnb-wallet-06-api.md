---
id: hi-mock-airbnb-wallet-06-api
node: fix.airbnb-wallet-mock
type: qa
step: 6
---
## Q
**Airbnb Wallet · 第 6 步 · API**｜模拟面试

面试官：「好，接口怎么设计？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **接口对应功能：** 「四条功能，五个接口，加一个给平台用的回调入口。」
- **先写提现请求：** 「POST /wallet/withdrawals，请求体：amount、destination_id、attempt_id。返回 202，{transaction_id, status: pending}。202 的意思是受理，不是完成：完成是异步的。」
- **余额不足：** 「返回 409 insufficient_funds，当场结束，不去问平台。」
- **重发的语义：** 「同一个 attempt_id、同样的内容，返回首次的那一笔；同一个 attempt_id、内容不同，返回 409。这是另一个问题，后面单独讲。」
- **充值：** 「POST /wallet/top-ups，形状一样，只是换成 payment_method_id。」
- **读：** 「GET /wallet 返回两个余额；GET /wallet/transactions?limit=20&cursor= 返回一页和 next_cursor，limit 最大 100；GET /wallet/transactions/{id} 返回状态和 last_vendor_check_at。」
- **状态接口只读本地：** 「它不调平台。pending 要不要刷新，由后台按新鲜度窗口决定，后面讲。」
- **回调入口：** 「POST /webhooks/vendor，只接受平台，先验签。」
- **身份：** 「wallet 由登录态决定，请求里没有 wallet_id；金额一律是整数分。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 410">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">API（wallet_id 取自登录态）</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /wallet/withdrawals</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：amount · destination_id · attempt_id</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ 202 {transaction_id, status}</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /wallet/top-ups</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：amount · payment_method_id · attempt_id</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ 202 {transaction_id, status}</text>
<rect x="8" y="164" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /wallet</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ {ready_to_use, on_hold, currency}</text>
<rect x="8" y="218" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="237.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /wallet/transactions?limit=20&amp;cursor=</text>
<text x="18" y="252.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ {items, next_cursor}；limit 最大 100</text>
<rect x="8" y="272" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="291.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /wallet/transactions/{id}</text>
<text x="18" y="306.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ {status, last_vendor_check_at}（只读本地）</text>
<rect x="8" y="326" width="324" height="76" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="345.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同 attempt_id + 同内容 = 同一笔，返回首次结果</text>
<text x="18" y="360.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同 attempt_id + 不同内容 → 409</text>
<text x="18" y="375.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">余额不足 → 409 insufficient_funds</text>
<text x="18" y="390.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">vendor 回调：POST /webhooks/vendor（验签）</text>
</svg>
白板上新增：五张便签对应五个接口，和一块写着接口契约的虚线框。
**为什么这样说。** （约 3 分钟，累计第 18 分钟。）面试官看接口有没有把几个关键约定落到字面上：202 而不是 200；attempt_id 在请求里；状态接口只读本地；limit 有上限。弱的回答是同步等平台完成才返回，或者 GET 状态直接去调平台，这两处恰好是后面要被追问的地方。
**面试官可能接着问。**
- 为什么 GET 状态不直接去问平台？ → 用户能触发的外部调用要有上限。如果每次读都去问平台，用户刷新一次就是一次平台调用，平台慢了读也慢。读只读本地行，刷新由后台限速做。
- 提现要不要限流？ → 要。按用户限制，比如每分钟最多 5 次（假设），防止脚本刷接口；每笔提现还要有足够的可用余额，所以也不会无限制地产生平台调用。
- 回调怎么防伪造？ → 验签并检查时间戳。如果更担心，可以只把回调当提示：取出 id，回查一次平台再应用。代价是每个回调多一次平台调用：平均 16.5 次/秒，但峰值 50 次/秒会把新建之外剩下的一半额度吃光，挤掉刷新和扫描。所以我默认验签后直接应用，只在怀疑被伪造时才回查，这是一个取舍。
- 为什么返回 202？ → 完成要几分钟，请求只表示受理。返回 200 会让客户端以为钱已经到了。
**常见失分。**
- **同步等平台：** 请求挂几分钟，连接和用户都被拖住，平台一慢整个服务都慢。
- **GET 状态去调平台：** 用户刷新就变成平台流量，没有上限。
- **wallet_id 由客户端传：** 谁都能改别人的钱包，应该取自登录态。
- **余额不足也调平台：** 在本地就能拒绝的请求，不该消耗平台额度。
