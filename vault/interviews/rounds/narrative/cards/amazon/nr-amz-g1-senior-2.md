---
id: nr-amz-g1-senior-2
node: amazon.followups
type: qa
step: 78
---
## Q
<p class="title">一个自信的错数字<span class="meta">03 senior 追问</span></p>

*"If this were a customer-facing product with millions of readers, what would you change?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能否把个人规模的做法扩展到生产规模。

<span class="label">回答框架</span>

- 先说把复算脚本放进 CI，不通过就不能发布
- 再说抽样加分级：高影响内容（数字、安全）强制校验，低影响内容抽检
- 最后说发布后的反馈通道：读者纠错入口，并把每次纠错变成新规则

<span class="label">为什么这是最佳实践</span>

规模变大后，靠人记得去复算不可行，必须变成发布前的自动闸门。同时发布后也要有纠错通道，因为任何闸门都有盲区。事前预防加事后反馈，才是完整的闭环。

<div class="sources"><b>表达 · business English</b><br>• <b><i>release gate</i></b> — 发布闸门<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d make the recompute script a release gate in CI.”</span><br>• <b><i>feedback loop</i></b> — 反馈回路<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Reader corrections would feed back into new rules.”</span></div>
