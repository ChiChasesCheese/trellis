---
id: bagu-timeout-unknown-1-not-failure
node: a.idem.timeout-unknown
type: qa
step: 1
---
## Q
**超时未知 · 超时不等于失败**｜必会

面试官：「调用渠道扣款接口超时了，到底扣了没有？你怎么办？」

## A
**基本回答。** 不知道。超时只表示没收到响应，不表示失败。不能直接当失败回滚，也不能盲目再扣；先查询对方的最终状态，再用同一个幂等键重试，最后靠对账兜底。
**一句话记住。** 超时像寄出一封挂号信一直没收到回执：信可能根本没寄到，也可能已经寄到、回执在路上丢了。你不能因为没回执就认定对方没收到。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<rect x="20" y="6" width="80" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我方</text>
<rect x="240" y="6" width="80" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道</text>
<line x1="60" y1="32" x2="60" y2="128" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="280" y1="32" x2="280" y2="128" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="60" y1="56" x2="280" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,56.0 273.0,59.2 273.0,52.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣款请求 R1</text>
<rect x="226" y="66" width="106" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="279" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道已扣款</text>
<line x1="280" y1="116" x2="60" y2="116" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="60.0,116.0 67.0,112.8 67.0,119.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="170" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢了或太慢</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">等到超时：不知道扣没扣</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">不能直接回滚，也不能盲目再扣</text>
</svg>
我方发出扣款请求 R1，渠道真的执行了扣款（右边高亮框），但响应在回来的路上丢了（虚线）。我方等到超时，只知道「没收到回复」，无法区分是没扣还是扣了。
**讲明白。**
- **超时和失败不一样：**失败是对方明确返回了错误，结果确定；超时只是没收到响应，结果未知。
- **请求可能已经执行：**请求有可能已经到达并执行了，只是响应在回来的路上丢了，或者太慢超过了我们的等待时间。
- **直接回滚的后果：**把超时当失败回滚订单，如果渠道其实扣了款，就变成用户被扣钱但订单失败。
- **盲目重扣的后果：**把超时当失败再发一次扣款，渠道其实已经扣过，就重复扣款了。
- **当成功也不对：**把超时当成功，又可能漏单（实际没扣到钱）。所以要标成未知状态，查询或对账后才进入终态。
- **正确的三步：**先查询对方的最终状态，再用同一个幂等键重试，最后靠对账兜底。
**举个例子。** 用户支付 100 元，我方请求渠道，请求号 R1，3 秒后超时：
1. **可能性一：**请求根本没到渠道，渠道没扣款。
2. **可能性二：**请求到了、扣款成功，响应在回来的路上丢了。
3. **可能性三：**请求到了，渠道还在处理，响应只是慢了。
4. **怎么办：**这三种情况从我方看起来一模一样，所以不能猜。订单标成「处理中」，用 R1 去查渠道，再决定下一步。
**容易错。**
- **以为超时就是失败：**超时结果未知，可能已经扣款成功。
- **以为失败了重发一次就好：**如果第一次其实成功了，重发就是重复扣款，要用同一个幂等键。
- **以为超时就是成功：**也可能请求根本没送到，当成功会漏单。
**业务场景。** 调渠道扣款超时，订单卡在处理中；不能直接回滚也不能盲目再扣，要用请求号查询并重试。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：画出调用渠道的时序后，面试官问「渠道调用超时怎么办」，答未知状态、查询、同键重试、对账。
**相关题。** 练习题 idempotent-transfer
**可能问法。**
- RPC 超时了到底成功没？ → 不知道。请求可能已经到达并执行，只是响应在回来的路上丢了或慢了。先按请求号查询对方的最终状态，再用同一个幂等键重试，最后靠对账兜底。
- 超时能直接重试吗？ → 不能盲目重试：写操作可能已经执行，直接重扣会重复扣款。要用同一个幂等键重试，让对方识别成同一笔，或者先查询最终状态再决定。
- 超时和失败的区别？ → 失败是对方明确返回了错误，结果确定；超时只是没收到响应，结果未知。把超时当失败回滚，会出现用户被扣钱但订单失败；当成功又可能漏单。所以要标成未知状态，查询或对账后才进入终态。
