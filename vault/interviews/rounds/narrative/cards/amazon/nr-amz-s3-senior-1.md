---
id: nr-amz-s3-senior-1
node: amazon.followups
type: qa
step: 12
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">03 senior 追问</span></p>

*"How would you decide whether to backfill the missing fees, and who needs to be involved?"*

## A
<span class="label">面试官在探</span> 面试官在探：你在账务场景下如何处理已经产生的错误状态，而不是只修代码。

<span class="label">回答框架</span>

- 先量化：缺失的笔数和金额，以及是否已经被下游消费
- 再判断：灰度阶段影响小，可能不需要，但这个判断要有数据和负责人确认
- 再说方法：fix forward，必要时 backfill，已被消费的状态用更正分录而不是回滚
- 最后说协作：财务和出款方要知情，并确认补录口径

<span class="label">为什么这是最佳实践</span>

账务里的错误状态一旦被下游消费就不能当没发生，所以用更正分录补上才有可追溯的历史。是否 backfill 取决于量级和已有影响，需要数据支撑并让相关方确认，而不是工程师单方面决定。这里我没有声称自己做了 backfill，说的是方法。

<div class="sources"><b>表达 · business English</b><br>• <b><i>correcting entry</i></b> — 更正分录<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“If the wrong state was already consumed downstream, I would post a correcting entry, not roll back.”</span><br>• <b><i>loop in finance</i></b> — 拉财务一起确认<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Before any backfill I would loop in finance to agree on the amounts.”</span></div>
