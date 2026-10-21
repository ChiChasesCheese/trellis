---
id: nr-amz-s4-full
node: amazon.full
type: qa
step: 4
---
## Q
<p class="title">澳洲 Amex 退款费<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：一位 PM 通过正式 help 流程升级：澳洲商户看不到 Amex 退款费。这个问题在三个团队之间弹了约 50 条回复，最后作为熟悉该领域的人被路由到我。
- 问题：线程里大家在争是谁的问题，没人拿出一份所有人都能核对的证据。我 own 的是答案，不是工单。
- 我做了什么：我不查组织架构，直接拉数据。六个月内按国家统计退款费行数：美国约 108 万行、英国 294 行、澳洲 0 行，涉及约 150 个澳洲商户。根因在配置：所有澳洲商户的 fee_refund_policy 都是 partial，而退款费逻辑只在 full 时触发。我还证明了这早于平台迁移，不是我们引入的回归。
- 结果：我把结论连同原始查询写出来，让 PM 和另一个团队自己复跑，线程当天结束，并转成一张正式的功能票，要在 Snowglobe 里建 REFUND_FEE 计算管线。线程里还冒出第二个不相关的费用种类，我如实说 not sure yet，给出分层假设，资深同事确认了。
- 为什么这样做 / 学到：当分歧其实来自知识不对称，就给所有人同一份证据，不争归属。宁可说 not sure yet 并给出计划，也不乱猜。

<span class="label">英文口述（60–90 秒）</span>

A product manager escalated through our formal help process: Australian merchants weren't seeing Amex refund fees. It bounced across three teams for about fifty replies before it was routed to me as the person who knows that domain. I pulled the data instead of the org chart. Over six months there were more than a million refund-fee rows in the US and zero in Australia, across about a hundred and fifty merchants. The root cause was configuration, not code: every Australian merchant's pricing schedule had the refund policy set to partial, and the refund-fee logic only fires on full. I also showed it predated our platform migration, so it wasn't a regression we introduced. I wrote it up with the exact query so the PM and the other team could re-run it themselves. It ended the thread the same day and became a tracked feature to build the refund-fee pipeline properly. In the same thread a second, unrelated fee kind came up; I said I wasn't sure, laid out a layered hypothesis, and a senior engineer confirmed it. I'd rather say 'not sure yet' with a plan than guess.

<div class="sources"><b>表达 · business English</b><br>• <b><i>get routed to someone</i></b> — 被转到某人手上<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The thread was routed to me as the person who knows that domain.”</span><br>• <b><i>cut through the noise</i></b> — 穿透噪音抓住关键<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“One query cut through fifty replies of noise and put everyone on the same facts.”</span><br>• <b><i>predates the migration</i></b> — 早于这次迁移就存在<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I showed the behavior predates the migration, so it wasn&#x27;t a regression we introduced.”</span></div>
