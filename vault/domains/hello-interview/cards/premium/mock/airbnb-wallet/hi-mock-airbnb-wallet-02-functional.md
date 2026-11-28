---
id: hi-mock-airbnb-wallet-02-functional
node: fix.airbnb-wallet-mock
type: qa
step: 2
---
## Q
**Airbnb Wallet · 第 2 步 · 功能需求**｜模拟面试

面试官：「好。那你先说说功能需求，准备做哪几条？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给四条：** 「线内我做四件事。」
- **第一条，充值：** 「用户把外部账户里的钱充进钱包。我先写一条 pending 的交易，平台确认到账之后，余额才增加。」
- **第二条，提现：** 「用户把钱转到自己的银行账户。金额先从可用余额挪到冻结，再交给平台；平台完成后冻结消失，失败后钱退回可用。」
- **第三条，看余额：** 「两个数，不是一个：可用（ready_to_use）和冻结（on_hold）。」
- **第四条，看历史和状态：** 「用户看到交易列表，每笔是 pending、completed 或 failed。pending 的要能看到最新状态，但不能因此无限地去调平台。」
- **线外，说一次：** 「订房支付、钱包间转账、KYC、多币种，您已经划掉了。我把它们当作不存在，后面不再提，也不列接口。」
- **点出难点：** 「这四条看着简单，难在三处：两笔不同的提现抢同一笔钱；平台的结果可能丢，我怎么知道钱有没有出去；用户一直刷新 pending，我怎么不把平台打爆。后面的需求和深入都围绕这三处。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 332">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">线内四条 · 线外划掉</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 充值：外部账户 → 钱包</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等支付平台确认后才加钱</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 提现：钱包 → 银行账户</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先冻结，再交给支付平台</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 看余额：可用 · 冻结</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个数，不是一个</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">④ 看历史与状态</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">含 pending 的那几笔</text>
<rect x="8" y="242" width="324" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="261.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">线外：订房支付 · KYC · 多币种</text>
<text x="18" y="276.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">钱包间转账 · 支付平台内部</text>
<text x="8" y="304" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">难点三处：两笔提现抢同一笔钱；</text>
<text x="8" y="322" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">平台结果丢了怎么办；pending 怎么查</text>
</svg>
白板上新增：四张便签（线内四条）和一块虚线框（线外）。
**为什么这样说。** （约 2 分钟，累计第 5 分钟。）面试官看你能不能把需求收到四条，并把被划掉的范围放下。强的回答顺带点出三个难点，让面试官知道你已经看到了重点；弱的回答是划掉之后仍然回头去讲订房支付，或者列一长串优惠券、积分、账单。
**面试官可能接着问。**
- 为什么余额拆成两个数？ → 提现要几分钟才完成。这段时间钱既不能再被花掉，也还没有真正离开。冻结让它不可再花，同时用户能看到「有 500 美元在路上」。
- 为什么充值不立刻加余额？ → 平台还没确认钱到了。先加余额，用户可能花掉没到账的钱，充值失败后还要追回。提现是先扣后确认，充值是先确认后加，方向相反，规则也相反。
- 为什么不做钱包间转账？ → 您划掉了。它是两个钱包行的原子改动，属于另一个问题；要做的话我会另开一轮。
**常见失分。**
- **回头讲订房支付：** 被划掉之后还花时间在它的接口上，会被记成没把范围钉住。
- **只有一个余额：** 没有冻结，提现的中间状态没有地方放，后面的冻结和释放都无从谈起。
- **充值先加钱：** 用户会花掉还没到账的钱。
- **不说难点：** 面试官不知道你看到了哪里最难，也就不知道该不该继续往下问。
