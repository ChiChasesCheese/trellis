---
id: hi-mock-airbnb-wallet-05-entities
node: fix.airbnb-wallet-mock
type: qa
step: 5
---
## Q
**Airbnb Wallet · 第 5 步 · 核心实体**｜模拟面试

面试官：「好，数字够了。接下来说说核心实体。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **两个实体：** 钱包（Wallet）和交易（Transaction）；用户当作已存在，不画。
- **钱包：** wallet_id 主键，user_id 唯一；余额拆成 ready_to_use 和 on_hold 两列整数分（不用浮点）；`CHECK (ready_to_use >= 0)` 是最后一道防线，不是主要机制。
- **交易：** transaction_id 服务端生成；wallet_id；type（TOP_UP / WITHDRAWAL）；amount；status。
- **两个编号：** attempt_id 由客户端在点击前生成，`(wallet_id, attempt_id)` 唯一，是重发的身份；transaction_id 同时是发给平台的幂等键。
- **平台相关两列：** vendor_transfer_id 可空，调用返回后才补（崩在中间时它就是空的，扫描靠 transaction_id 重发起）；last_vendor_check_at 做新鲜度窗口。
- **状态机：** pending、completed、failed，转换都是 `UPDATE … WHERE status='pending'`，终态不再变。提现 completed：冻结减金额；failed：冻结减金额并加回可用。充值 completed：可用加金额；failed：不动。
- **余额是派生副本：** 真相是交易行，同一事务里一起改，另有夜间核对（on_hold 应等于 pending 提现之和）。不存银行账号，只存平台给的 destination_id。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 288">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">提现的状态机与钱的去向</text>
<rect x="90" y="28" width="160" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">pending</text>
<text x="170" y="62.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可用 → 冻结（已提交）</text>
<rect x="8" y="140" width="150" height="60" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">completed</text>
<text x="83" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">on_hold − 金额</text>
<text x="83" y="189" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">钱已离开钱包</text>
<rect x="182" y="140" width="150" height="60" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">failed</text>
<text x="257" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">on_hold − 金额</text>
<text x="257" y="189" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ready_to_use + 金额</text>
<polyline points="130,74 130,108 83,108 83,140" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83,140 79.8,133.0 86.2,133.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="210,74 210,108 257,108 257,140" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257,140 253.8,133.0 260.2,133.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="16" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">平台成功</text>
<text x="324" y="104" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">平台失败</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">充值方向相反：先 pending，平台确认才加钱：</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">completed：ready_to_use + 金额；failed：不动</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">终态不再变化：UPDATE … WHERE status='pending'</text>
</svg>
白板上新增：两张表和提现的状态机。刷新队列、扫描是行为，不是实体，现在不画。

**常见失分。**
- **只有一个 balance：** 提现中间状态没处放，两笔提现也无法判断谁该被拒。
- **金额用浮点：** 钱不能有舍入误差。
- **没有 attempt_id：** 第一次响应丢了，重发和再提一笔分不开。
- **存银行账号或卡号：** 合规范围变大，这一步也不需要。

**面试官可能接着问。**
- 余额为什么不每次对交易求和？ → 条件 UPDATE 需要一个能当场检查加锁的行，求和做不到；字段读 O(1)，夜间核对保证一致。
- attempt_id 为什么客户端生成？ → 第一次响应丢了，客户端不知道服务端的 transaction_id，没东西可重发。
