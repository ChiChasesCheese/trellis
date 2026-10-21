---
id: nr-amz-s9-senior-3
node: amazon.followups
type: qa
step: 44
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">03 senior 追问</span></p>

*"What would you put in place so that an effective-date change can't silently shift payout dates again?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能不能把一次事故变成系统性的预防，而不是只修这一个点。

<span class="label">回答框架</span>

- 改动层面：任何 effective-date 变更都要在每个受影响区域做测试，比较前后出款日
- 监控层面：对出款日与 SLA 的偏差设告警，在商户发现之前先发现
- 文档层面：把 T+7 内部 SLA 与上游到账的边界写进 runbook，下次不依赖某个人的记忆
- 流程层面：合规类改动评审时明确问一句“对其他区域的影响是什么”

<span class="label">为什么这是最佳实践</span>

这次问题能拖到商户来报，说明改动没有按区域验证、也没有基于 SLA 的告警。预防要分层：测试在改动进入前挡住，告警在改动进入后兜底，文档把只存在于个别人脑中的 SLA 变成团队共识。这些是我会推动的下一步，需要和团队确认哪些已经落地。

<div class="sources"><b>表达 · business English</b><br>• <b><i>guardrail</i></b> — 护栏<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d add a guardrail that compares payout dates per region before any effective-date change ships.”</span><br>• <b><i>detect before the customer does</i></b> — 赶在客户之前发现<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The goal is to detect it before the merchant does.”</span></div>
