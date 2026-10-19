---
id: nr-amz-s6-senior-4
node: amazon.followups
type: qa
step: 30
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">03 senior 追问</span></p>

*"What would you do differently, and how do you prevent handoffs like this from becoming a risk in the first place?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能否从一次个案抽出组织层面的机制。

<span class="label">回答框架</span>

- 承认问题：一个人带着关键标注和只在 QA 跑过的代码离开
- 提议实习项目的 exit checklist：标注导出、环境说明、生产准备度评估
- 要求任何 ML 项目在立项时写下生产规模假设
- 更早做评估，而不是在最后一周才发现

<span class="label">为什么这是最佳实践</span>

这件事的根因是项目没有生产准备度的检查点，不是某个人的失误。把评估前移到立项时，并把不可再生的资产（标注）列进离职清单，才能让下一次不依赖我临时发现。下次我会更早发起评估，而不是等到离职前。

<div class="sources"><b>表达 · business English</b><br>• <b><i>handoff checklist</i></b> — 交接清单<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d add irreplaceable assets like labels to the handoff checklist.”</span><br>• <b><i>production readiness review</i></b> — 生产准备度评审<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A production readiness review at kickoff would have surfaced the scale gap earlier.”</span></div>
