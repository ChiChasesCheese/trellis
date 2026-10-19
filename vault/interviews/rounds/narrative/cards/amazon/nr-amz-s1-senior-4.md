---
id: nr-amz-s1-senior-4
node: amazon.followups
type: qa
step: 5
---
## Q
<p class="title">Amex 结算管线<span class="meta">03 senior 追问</span></p>

*"How would you hand this pipeline to another team so it does not depend on you?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能不能让自己建的东西脱离个人，变成团队可运维的资产。

<span class="label">回答框架</span>

- 先说文档：设计文档、runbook，区分哪些告警是下一轮会自愈的噪音
- 再说可观测：监控页和告警让别人不用读代码也能判断状态
- 再说演练：让别人在我旁观下处理一次真实告警
- 最后说验证：看别人能否在不问我的情况下接入或排查

<span class="label">为什么这是最佳实践</span>

一条管线只有在别人不问你也能运维和扩展时才算交付完成。runbook 把你脑子里的经验固化下来，监控让状态可见，演练则检验这两样是否真的管用。这样 on-call 才不会永远只有一个人。

<div class="sources"><b>表达 · business English</b><br>• <b><i>bus factor</i></b> — 巴士系数（多少人离开会让项目停摆）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I would raise the bus factor by getting a teammate to handle a real alert from my runbook.”</span><br>• <b><i>runbook</i></b> — 运维手册<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The runbook separates noisy errors that self-heal from the ones that need a human.”</span></div>
