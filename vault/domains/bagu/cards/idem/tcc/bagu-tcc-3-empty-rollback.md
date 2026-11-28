---
id: bagu-tcc-3-empty-rollback
node: a.idem.tcc
type: qa
step: 3
---
## Q
**TCC · 空回滚**｜必会

面试官：「Try 请求超时没到，协调者已经发了 Cancel。参与方收到 Cancel 时没有 Try 记录，怎么办？」

## A
**基本回答。** 这叫空回滚（empty rollback）。Cancel 要识别「没有 Try 记录」，直接返回成功，并插入一条「已回滚」记录。
事务日志表 `(xid, branch_id, status)`：Cancel 查不到记录就插入 `CANCELLED` 并返回成功，查到 `TRIED` 才真正释放资源；重复的 Cancel 看到已取消直接返回。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="20" y="6" width="80" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协调者</text>
<rect x="240" y="6" width="80" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">参与方</text>
<line x1="60" y1="32" x2="60" y2="150" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="280" y1="32" x2="280" y2="106" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="60" y1="56" x2="160" y2="56" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="170" y="60" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">✗</text>
<text x="70" y="48" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Try 超时没到</text>
<line x1="60" y1="100" x2="280" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,100.0 273.0,103.2 273.0,96.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Cancel</text>
<rect x="196" y="108" width="136" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="264" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无 Try 记录</text>
<text x="264" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写 CANCELLED</text>
<text x="264" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回成功</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不报错，也不真去释放资源</text>
</svg>
协调者发出的 Try 因为网络超时没有到达参与方（虚线，被打断），协调者随后发出 Cancel，到达了。参与方发现没有 Try 记录，只写一条 CANCELLED，并返回成功。
**举个例子。** 账户可用 100，订单 30：
1. **正常 Cancel：**Try 冻结 30 → 日志记录 TRIED → Cancel 到达，看到 TRIED，把 30 还回可用，状态改为 CANCELLED，可用回到 100。
2. **再来一次 Cancel：**重复到达，看到 CANCELLED，直接返回成功。
3. **空回滚：**另一笔事务 T2 的 Try 超时没到，Cancel 先到了。日志里没有 T2 的记录，插入 `CANCELLED` 并返回成功，余额一分不动。
4. **如果当时真去释放：**没冻结过却还 30，账户会凭空多出 30 元，这就是为什么不能真释放。
**容易错。**
- **没记录就报错：**协调者会无限重试 Cancel。
- **没记录也照样释放：**没预留过就释放，等于凭空多出资源。
- **空回滚不留痕迹：**不写 CANCELLED，之后迟到的 Try 无法被拒绝，就会悬挂。
