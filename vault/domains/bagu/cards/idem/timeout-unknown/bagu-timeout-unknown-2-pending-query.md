---
id: bagu-timeout-unknown-2-pending-query
node: a.idem.timeout-unknown
type: qa
step: 2
---
## Q
**超时未知 · 处理中状态与主动查询**｜必会

面试官：「订单为什么要进入「处理中」状态？怎么查询对方的最终状态？」

## A
**基本回答。** 不要判成功或失败，订单进入「处理中」（未知）状态；用同一个幂等键或请求号查询。查到成功就推进，查到失败就释放，还在处理就稍后再查。
**一句话记住。** 处理中就像快递的「运输中」状态：既不是签收也不是退回，你不去催，也不重新下单，只是按时间去查物流。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<rect x="60" y="6" width="220" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 先落库：尝试记录 + 请求号</text>
<line x1="170" y1="34" x2="170" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,54.0 166.8,47.0 173.2,47.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="54" width="140" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理中（未知）</text>
<line x1="140" y1="84" x2="90" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,116.0 94.2,109.5 97.6,114.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="200" y1="84" x2="250" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,116.0 242.4,114.9 245.8,109.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="116" width="160" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="88" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查到成功 → 推进订单</text>
<rect x="176" y="116" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查到失败 → 释放</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仍在处理：5秒、30秒、2分钟、10分钟、1小时</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">再查，次数有上限，超限转对账</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户看到：处理中，请勿重复支付</text>
</svg>
发请求之前先把尝试记录落库（带稳定的请求号），超时后订单停在「处理中」。后台再用请求号去查渠道，查到哪种结果就往哪边走；还没出结果就按退避间隔再查，次数用完转对账。
**讲明白。**
- **发请求前先落库：**先持久化带稳定请求号的尝试记录，再发请求。如果请求发到一半我方崩了，重启后能看到这条记录，知道有一笔需要去查，不会凭空丢掉。
- **订单进入处理中：**不判成功也不判失败，这是一个正式的中间状态，对用户展示「处理中，请勿重复支付」。
- **怎么查最终状态：**用同一个幂等键或请求号调用渠道的查询接口，查到成功就推进订单，查到失败就释放资源，仍在处理就稍后再查。
- **按退避间隔轮询：**如 5 秒、30 秒、2 分钟、10 分钟、1 小时，次数有上限，超限转对账。
- **渠道切换的陷阱：**A 渠道超时并不代表没成功，如果直接改走 B 渠道，A 其实已经扣款，用户就被扣两次。
- **一单一活跃尝试：**同一个订单同一时间只能有一个进行中的尝试（可以用部分唯一索引，或一张只存活跃尝试、订单号唯一的表）。切换渠道前必须先终结旧尝试：查到失败，或者成功后撤销，才能发起新的。
**举个例子。** 用户充值 100 元，请求号 P-77：
1. **发请求前：**先写一条尝试记录 P-77，状态是「已发起」。
2. **请求超时：**状态改成「处理中」，App 显示「处理中，请勿重复支付」。
3. **5 秒后第一次查询：**渠道回答「仍在处理」，30 秒后再查。
4. **30 秒后第二次查询：**渠道回答「成功」，订单推进到已支付，入账并通知用户。
**容易错。**
- **超时就直接换渠道重试：**旧渠道可能已经扣款，会重复扣两次，要先终结旧尝试。
- **发请求之后才记录：**崩溃时这条请求就找不回来了，要先落库再发。
- **一直无限轮询：**要有退避间隔和次数上限，超限转对账或人工。
**业务场景。** 充值超时，App 显示「处理中」；后台按请求号每隔一段时间查渠道，查到成功后再入账并通知用户。
**系统设计。** [[links.tt-wallet-ledger-service|钱包与复式账本服务（余额、冻结、转账、多币种）]]：充值状态机里面试官问「中间状态有哪些」，答 PENDING/UNKNOWN 及查询推进。
**相关题。** 练习题 digital-wallet
**可能问法。**
- 超时后订单是什么状态？ → 不要判成功或失败，订单进入「处理中」（未知）状态。发请求之前先持久化带稳定请求号的尝试记录，崩溃后才能恢复。对用户展示「处理中，请勿重复支付」，由后台去查最终结果。
- 怎么查最终状态？ → 用同一个幂等键或请求号调用渠道的查询接口。查到成功就推进订单，查到失败就释放，仍在处理就稍后再查。按退避间隔轮询，如 5 秒、30 秒、2 分钟、10 分钟、1 小时，次数有上限，超限转对账。
- 渠道切换为什么危险？ → A 渠道超时并不代表没成功，如果直接改走 B 渠道，A 其实已扣款，用户就被扣两次。所以要保证一单一活跃尝试（部分唯一索引），切换前先终结旧尝试：查到失败或成功撤销后，才能发起新的。
