---
id: nr-amz-r1-senior-4
node: amazon.followups
type: qa
step: 65
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">03 senior 追问</span></p>

*"If a team of ten researchers started using this platform, what would break first and what would you change?"*

## A
<span class="label">面试官在探</span> 面试官在探：你从个人项目走向团队平台的规模化思维

<span class="label">回答框架</span>

- 先找最先出问题的点：共享数据的一致性和账本的写入冲突、环境不可复现
- 再说约束：要有 point-in-time 数据的唯一来源和版本，实验要可复现
- 然后说治理：关卡要变成所有人都绕不开的流水线，而不是个人习惯
- 最后说文档和接口稳定性：窄接口让别人能自助接入

<span class="label">为什么这是最佳实践</span>

单人项目靠自律，团队则必须靠机制。把关卡放进共享流水线、让数据版本固定且可复现，别人才无法绕过校验；窄接口降低接入成本，所以扩展性主要来自已有的分层，而不是重写。这只是我下一步会做的设计，目前它是个人项目。

<div class="sources"><b>表达 · business English</b><br>• <b><i>single source of truth</i></b> — 唯一可信的数据来源<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“With ten researchers I&#x27;d need a single source of truth for the data.”</span><br>• <b><i>make the right thing the easy thing</i></b> — 让正确的做法成为最省力的做法<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d make the right thing the easy thing by putting the gates into the shared pipeline.”</span></div>
