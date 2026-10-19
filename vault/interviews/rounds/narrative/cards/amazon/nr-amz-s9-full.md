---
id: nr-amz-s9-full
node: amazon.full
type: qa
step: 9
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：一家大型 marketplace 商户报告约 400 万美元的 Amex 出款“不见了”，团队开了正式事故频道，指挥点名我是三位 fix owner 之一。因为钱是商户的，所以先要判断这是真违约还是预期内的延迟。
- 问题：一位资深同事对美国 aggregated-Amex 的 SLA 没有背景，直接让我来答。如果不先把这件事说清，大家会一直争“是不是违约”，真正的原因就没人去查。
- 我做了什么（SLA）：我说明 T+7 是我们内部管线的 SLA，而且我们只在 Amex 把钱结算到我们账户之后才出款。这样预期延迟和真实回归就分开了，违约之争随之结束，指挥才能去追真正的原因。
- 我做了什么（修法）：指挥追到 6 月 23 日为 EU 合规做的一次 effective-date 改动，把美国出款日推后了约一天。revert 最快，但会把 EU 合规改动一起撤掉，所以我主张在 table function 里加 region 条件，让 EU 和 US 语义相互独立。小组选了这个方案，由两位同事部署。
- 结果与学到：事故三天内关闭（07-06 到 07-09）。我的份额是 SLA 判定和修复方向，部署是同事做的。学到的是：多 owner 事故里，拿下自己是权威的那一块并直白地说清楚，并且争取稳健的修法而不是最快的。

<span class="label">英文口述（60–90 秒）</span>

A large marketplace merchant reported roughly four million dollars of Amex payouts missing, and a formal incident channel spun up. The incident commander named me one of three engineers who own the fix. I made two contributions. First, the SLA: a senior teammate said he didn't have context on US aggregated-Amex SLAs and deferred to me. I established that T+7 is our internal pipeline SLA and that we only disburse after Amex settles funds to us, which separated expected latency from the real regression and ended the argument about whether we had breached anything. Second, the regression: an effective-date change we made for EU compliance had shifted US disbursement dates by about a day. Reverting was the fast option, but I argued for the robust one, a region conditional in the table function so EU and US keep independent semantics. The group chose it, two teammates deployed it, and the incident closed in three days.

<div class="sources"><b>表达 · business English</b><br>• <b><i>defer to someone</i></b> — 把判断交给更懂的人<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A senior teammate deferred to me on the US aggregated-Amex SLA.”</span><br>• <b><i>separate signal from noise</i></b> — 把真信号和噪音分开<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Naming the T+7 SLA separated signal from noise: expected latency versus a real regression.”</span><br>• <b><i>owner of the fix</i></b> — 修复的负责人<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The incident commander named me one of three owners of the fix.”</span></div>
