---
id: nr-amz-s1-full
node: amazon.full
type: qa
step: 1
---
## Q
<p class="title">Amex 结算管线<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：Braintree 的费用平台跑在 Snowflake 上。Visa 和 Mastercard 能从收单方拿到近实时视图，但 Amex 是闭环网络，每天只丢一个定宽文件过来，所以文件确认结算之前，Amex 交易不能入账。因为这个限制，Amex 必须单独做一条管线。
- 问题：我接手时只有前任留下的一张表的 stub。我是这条管线从设计文档到生产的 owner，输出要喂给费用计算和出款，所以它一旦出错就会直接影响钱，必须从设计上就假定会出错。
- 我做了什么：每种记录类型一条 append-only stream，共六条，各有独立 offset，这样互相不阻塞；每个阶段用复合键 MERGE，这样重发文件或重跑任务都不会重复计数；两个校验函数把所有对不上的记录写进 error log 而不是丢掉；再用一个 feature flag 当 kill switch，一条 UPDATE 就能停，不用发版。
- 结果：我一直在 on-call，真实故障出现后又补了十几个加固 PR。前六个月处理了约 2200 万笔 Amex 交易，在生产跑了 18 个月，管线本身也是我任期内最大的 PR，约 1800 行。
- 为什么这样做 / 学到：钱的管线不可能假设不出错，所以我选择让它坏的时候留下记录而不是悄悄丢数据，这是我最自豪的设计。

<span class="label">英文口述（60–90 秒）</span>

The project I'm proudest of is the American Express settlement pipeline on our Snowflake-based fee platform at Braintree. Amex is a closed-loop network: instead of near-real-time views from our acquirer, it sends one fixed-width reconciliation file a day, so we can't book an Amex transaction until that file confirms it settled. I inherited a stub with a single table and owned the pipeline from the design doc through eighteen months of production. I made three design calls. First, six append-only streams, one per record type, so each has its own offset and none blocks the others. Second, a composite-key MERGE at every stage, so a re-delivered file or a re-run task can't double-count. Third, two validation functions that send every mismatch to an error log instead of dropping it, plus a single feature flag that doubles as a kill switch, so I could stop it with one UPDATE and no deploy. Because I was on-call for it, I shipped about a dozen hardening PRs after real failures. It processed about twenty-two million Amex transactions in its first six months, and it's the largest change I've merged, around 1,800 lines. The part I'm proudest of: when it breaks, it records the problem instead of losing data.

<div class="sources"><b>表达 · business English</b><br>• <b><i>own something end to end</i></b> — 从头到尾全权负责<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I owned the Amex pipeline end to end, from the design doc through eighteen months of production.”</span><br>• <b><i>closed-loop</i></b> — 闭环（网络自己同时是发卡方和收单方）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Amex is a closed-loop network, so we only learn a transaction settled when its daily file arrives.”</span><br>• <b><i>never silently drop</i></b> — 绝不悄悄丢数据<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“My rule was that the pipeline never silently drops a record; every mismatch goes to an error log.”</span></div>
