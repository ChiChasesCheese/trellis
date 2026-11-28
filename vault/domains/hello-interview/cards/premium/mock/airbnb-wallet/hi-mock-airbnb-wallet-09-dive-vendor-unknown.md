---
id: hi-mock-airbnb-wallet-09-dive-vendor-unknown
node: fix.airbnb-wallet-mock
type: qa
step: 9
---
## Q
**Airbnb Wallet · 第 9 步 · 深入二（上）：平台结果不确定**｜模拟面试

面试官：「你要把钱交给支付平台。调用超时了，或者你的服务在调用前后崩了。你怎么知道钱有没有出去？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **前提：** 平台的结果我可能拿不到，不猜，让每一步先留本地记录，之后能查清。
- **顺序：** 一个事务写 pending 行并冻结，提交；再调平台；最后存 vendor_transfer_id。平台一收下请求，本地必须已有一行能对应它。createTransfer 的幂等键是 transaction_id，同键重发平台返回同一笔。
- **三个崩溃点：** A，调平台前崩：行 pending 且无 vendor id，平台没见过，扫描用同一个键重发。B，平台收到但响应丢了：本地看起来同 A，同键重发返回同一笔，不重复；换新键就会转两次。C，已存 vendor id，等回调。
- **超时是未知，不是失败：** 不回滚、不退冻结，行保持 pending；当失败退回而平台已转出，用户就拿到两份钱。只有平台明确返回 failed 才释放冻结。
- **webhook 是常态路径：** 带 vendor_transfer_id 和 metadata 里的 transaction_id（所以 webhook 比存 vendor id 早到也找得到行）；验签后一个事务把 pending 改终态并更新 on_hold / ready_to_use。
- **一个门：** webhook、刷新 worker、每日扫描都调同一个 `settle(transaction_id, outcome)`，状态更新带 `WHERE status='pending'`，重复、迟到、乱序的回调更新 0 行，返回 200 让平台别再发。提现 completed：on_hold 减；failed：on_hold 减、ready_to_use 加回；充值 completed：ready_to_use 加；failed：不动。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付平台</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">webhook</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">钱包行</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST transfer.completed</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="128,102 154,102 154,116 128,116" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,116 135.0,112.8 135.0,119.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="160" y="113" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">验签</text>
<text x="132" y="136" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE txn … WHERE pending</text>
<polyline points="128,148 212,148" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,148 205.0,151.2 205.0,144.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="110.92" y="162" width="202.16" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 行 → 继续；0 行 → 200 退出</text>
<text x="132" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一事务：on_hold − 金额</text>
<polyline points="128,210 298,210" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,210 291.0,213.2 291.0,206.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">200</text>
<polyline points="128,244 44,244" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,244 51.0,240.8 51.0,247.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="258" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="160" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="184" x2="128" y2="258" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="125" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="140" x2="212" y2="160" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="184" x2="212" y2="187" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="202" x2="212" y2="258" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="125" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="140" x2="298" y2="160" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="184" x2="298" y2="258" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：三个崩溃点各自的本地状态和处理，以及 webhook 的处理时序。

**常见失分。**
- **超时当失败：** 平台已转出，退回冻结就是出两次钱。
- **先调平台再写库：** 平台收下了，本地没有行，回调对不上。
- **回调直接加余额：** 重复回调加两次；要条件更新并忽略终态。
- **三处各写一份更新逻辑：** 迟早不一致。

**面试官可能接着问。**
- 回调乱序，failed 后又来 completed？ → 第二个遇终态更新 0 行被忽略；若结果真的矛盾是平台问题，记日志告警，不改账。
- 回调处理为什么要快？ → 验签、一个短事务、返回 200；平台超时会重发，而我们幂等，重活不放请求里。
- 平台没有幂等键也不能按 id 查？ → 不能盲目重发，超时后进人工对账直到结果对上，所以澄清阶段先问它。
