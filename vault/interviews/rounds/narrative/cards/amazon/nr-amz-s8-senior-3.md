---
id: nr-amz-s8-senior-3
node: amazon.followups
type: qa
step: 39
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">03 senior 追问</span></p>

*"You found two risky resources and flagged them. What happens next, and how do you get someone to actually fix them?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对“发现问题之后”的推动与影响力。

<span class="label">回答框架</span>

- 先把风险写清楚：位置、触发条件、预计影响
- 开 ticket 并指定 owner，附上修法 PR 或最小改动
- 按风险排优先级：这两个形状相同、一旦触发就会卡发布
- 跟进到关闭，并复盘是否需要把检查加进 CI

<span class="label">为什么这是最佳实践</span>

标出风险只是第一步，没有 owner 的风险等于没人负责。把修法做得足够容易合入，别人才愿意接。我要诚实说明目前是标出未修，所以下一步是开 ticket、找到模块 owner 并推动合入。

<div class="sources"><b>表达 · business English</b><br>• <b><i>drive to closure</i></b> — 推动到彻底完成<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d drive the two flagged resources to closure with a ticket and an owner.”</span><br>• <b><i>make it easy to say yes</i></b> — 让别人容易同意<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d attach a ready-made PR to make it easy to say yes.”</span></div>
