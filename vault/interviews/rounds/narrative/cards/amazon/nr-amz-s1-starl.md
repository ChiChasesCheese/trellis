---
id: nr-amz-s1-starl
node: amazon.outline
type: qa
step: 2
---
## Q
<p class="title">Amex 结算管线<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- **Braintree** 费用平台，跑在 **Snowflake** 上；Visa / Mastercard 走收单方近实时视图
- **Amex** 是闭环：**每天一个定宽文件**，文件确认结算前不能入账

<span class="label">T</span>

- 我 **owner** 整条管线，从设计文档到生产；接手时只有**一张表的 stub**
- 输出喂给**费用计算和出款**

<span class="label">A</span>

- 设计 **6 条 append-only stream**，每种记录类型一条，各有独立 **offset**，互不阻塞
- 每个阶段用**复合键 MERGE**，重发文件不会 **double-count**
- 两个**校验函数**，所有不匹配进 **error log**，不丢弃
- 一个 **feature flag** 当 **kill switch**，一条 `UPDATE`，无需发布
- 一直 **on-call**，真实故障后上了**十几个加固 PR**

<span class="label">R</span>

- 前六个月 **~22M** 笔 Amex 交易；生产 **18 个月**
- 任期内最大 PR，**~1,800 行**

<span class="label">L</span>

- 坏了的时候，它**记录问题而不是丢数据**

<div class="sources"><b>表达 · business English</b><br>• <b><i>idempotent</i></b> — 幂等（重复执行结果不变）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The composite-key MERGE makes every stage idempotent, so a re-delivered file can&#x27;t double-count.”</span><br>• <b><i>kill switch</i></b> — 紧急停止开关<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“One feature flag doubles as a kill switch: a single UPDATE stops the pipeline without a deploy.”</span><br>• <b><i>fail safe</i></b> — 出错时落在安全状态<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I designed it to fail safe: bad rows land in an error log instead of vanishing.”</span></div>
