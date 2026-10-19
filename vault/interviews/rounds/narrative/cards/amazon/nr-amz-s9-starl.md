---
id: nr-amz-s9-starl
node: amazon.outline
type: qa
step: 26
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 大型 marketplace 商户报告约 **$4M** Amex 出款"不见了"
- 开了**正式事故频道**

<span class="label">T</span>

- 指挥点名我是**三位 fix owner 之一**
- 我的任务：判断这是**违约**还是预期延迟，并修真正的原因

<span class="label">A</span>

- 资深同事对美国 aggregated-Amex SLA **没有背景**，**让我来答**
- 我说明 **T+7 是内部管线 SLA**，且我们**只在 Amex 结算到我们之后才出款**
- 这就分开了**预期延迟**和**真实回归**，终止了「是否违约」的争论
- 指挥追到 **6 月 23 日**为 **EU 合规**做的 effective-date 改动，把 US 出款推后约**一天**
- revert 最快；我主张在 table function 里加 **region 条件**，EU 和 US 语义相互独立
- 小组选了它；**两位同事部署**了修复

<span class="label">R</span>

- 事故**三天内关闭**
- 我的份额：**SLA 判定**和**修复方向**；部署是同事做的

<span class="label">L</span>

- 多 owner 事故里，拿下自己是**权威**的那一块，**直白**地说
- 争取**稳健**的修法，而不是最快的

<div class="sources"><b>表达 · business English</b><br>• <b><i>draw the line</i></b> — 划清边界<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I drew the line between the internal pipeline SLA and Amex settlement timing.”</span><br>• <b><i>take the call</i></b> — 拿主意、做判断<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“On the SLA question I took the call because I was the one with the context.”</span><br>• <b><i>robust over fast</i></b> — 宁稳不图快<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I argued for robust over fast: a region condition rather than a revert.”</span></div>
