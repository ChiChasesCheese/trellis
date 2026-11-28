---
id: bagu-retry-1-what-to-retry
node: a.protect.retry
type: qa
step: 1
---
## Q
**重试 · 哪些错误可以重试**｜必会

面试官：「调用下游失败了，你会直接重试吗？什么样的请求、什么样的错误才应该重试？」

## A
**基本回答。** 同时满足两条才重试：错误是临时性的（超时、连接被重置、502/503/504、带 `Retry-After` 的 429），并且操作幂等（读，或带幂等键的写）。参数错误 400、没权限 401/403、余额不足这类确定性错误重试结果不会变，直接返回。
**一句话记住。** 重试像敲门：门口临时没人（临时错误）可以多敲几下；门上写着「查无此人」（确定性错误）敲一万次也一样；而且你要确定「多敲几下不会让里面的人把同一件事办两遍」（幂等）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">临时错误 且 幂等 → 重试</text>
<text x="180" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">确定性错误 → 不重试</text>
<rect x="8" y="28" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超时、连接被重置</text>
<rect x="180" y="28" width="152" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">400 参数错误</text>
<rect x="8" y="64" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">502 / 503 / 504</text>
<rect x="180" y="64" width="152" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">401 / 403 没权限</text>
<rect x="8" y="100" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">429 + Retry-After</text>
<rect x="180" y="100" width="152" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">余额不足</text>
<rect x="8" y="140" width="160" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="88" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">且操作幂等</text>
<text x="88" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读，或带幂等键的写</text>
<rect x="180" y="140" width="152" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重试结果不会变</text>
<text x="256" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接返回</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">超时不等于失败：写请求超时，</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">服务端也许已经执行了，不幂等就别重试</text>
</svg>
左边是该重试的：临时错误，且操作幂等。右边是不该重试的：重试结果不会变，直接返回。最下面强调超时不等于失败。
**讲明白。**
- **为什么要区分错误：** 临时错误过一会儿可能恢复，重试有收益；确定性错误重试一万次结果一样，只浪费资源。
- **哪些是临时错误：** 超时、连接被重置、502、503、504（网关或服务暂时不可用），以及带 `Retry-After` 的 429（让你稍后再来）。
- **哪些是确定性错误：** 参数错误 400、没权限 401 和 403、余额不足。重试结果不会变，直接返回。
- **为什么还要看幂等：** 超时不等于失败：写请求超时时服务端也许已经执行了，不幂等就重试会重复执行。所以只有读，或带幂等键的写才能重试。
- **次数要克制：** 在线同步请求 2 到 3 次；异步任务可以多，但要退避、有上限、有死信和告警。
- **总截止时间：** 整条链路设一个总截止时间（deadline），剩余时间不够就不再重试。
- **熔断器打开时：** 熔断器（失败太多时暂时停止调用下游的保护开关）打开时不重试，直接走降级。
**举个例子。** 调用第三方短信通道发验证码：
1. **返回 503（服务暂时不可用）：** 临时错误，假设通道支持按请求号去重，带同一个请求号重试就是幂等的；退避后重试。
2. **返回「手机号无效」：** 确定性错误，重试结果不会变；直接记失败，不重试。
3. **请求超时：** 不知道对方有没有发出去。带着同一个请求号重试，由对方去重；没有幂等保证就不能盲目重试，否则用户可能收到两条。
4. **已经重试了 3 次、总时间用到上限：** 不再重试，返回失败或走降级。
**容易错。**
- **一失败就重试：** 要分清临时错误和确定性错误。
- **只看错误类型不看幂等：** 临时错误的写请求，不幂等就会重复执行。
- **以为超时就是失败：** 服务端可能已经执行。
- **熔断打开了还在重试：** 白白压下游，应该直接降级。
**业务场景。** 调用第三方短信通道时对方返回 503 就退避重试；返回「手机号无效」就不重试，直接记失败，否则同一个坏号码会被反复发送。
**系统设计。** [[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：发送失败的消息怎么处理。面试官追问「哪些失败要重试，哪些直接丢弃，用户会不会收到两条」，答：临时错误退避重试，确定性错误直接丢弃记失败；重试带同一个消息 ID，通道侧去重，避免重复收到。
**可能问法。**
- 什么情况下可以重试？ → 同时满足两条：错误是临时性的（超时、连接被重置、502、503、504、带 `Retry-After` 的 429），并且操作幂等（读，或带幂等键的写）。参数错误 400、没权限 401 和 403、余额不足这类确定性错误，重试结果不会变，直接返回。
- 重试写请求安全吗？ → 要看是否幂等。超时不等于失败，写请求超时时服务端也许已经执行了，不幂等就重试会重复执行，所以写请求要带幂等键才能重试。
- 重试几次合适？ → 在线同步请求 2 到 3 次；异步任务可以多，但要退避、有上限、有死信和告警。整条链路设一个总截止时间，剩余时间不够就不再重试；熔断器打开时不重试，直接降级。
