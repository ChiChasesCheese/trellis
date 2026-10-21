---
id: nr-amz-s8-hook
node: amazon.outline
type: qa
step: 22
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**A release failed in QA; I was only cc'd, posted the root cause and fix seven minutes later, then scanned the whole repo and flagged the next two failures.**

<span class="label">适用 LP</span>

- 主：**Bias for Action**、**Dive Deep**
- 副：Ownership、Insist on the Highest Standards、Earn Trust、Deliver Results

<span class="label">数字</span>

- **7 分钟**：从被 cc 到贴出根因 + 修法 + 邻近模块核查
- QA → pre-prod → prod **同天**部署
- 事后全仓库扫描：**79** 个 ownership 资源，**42** 个缺 `outbound_privileges`
- 多数是无害的 `future_*` 变体；`scheme_fees` 模块里 **2 个**与出事的形状完全相同、尚未触发
- 不要说 "the only resource in the whole repo missing it"，不成立。说：「I checked the neighboring modules that day; afterwards I scanned the whole repo and found dozens missing it, mostly harmless future grants, but two real ones in another module that haven't fired yet.」

<div class="sources"><b>表达 · business English</b><br>• <b><i>root cause</i></b> — 根本原因<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Seven minutes in, I&#x27;d posted the root cause in the thread.”</span><br>• <b><i>cc&#x27;d</i></b> — 被抄送（没有被分配）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I was only cc&#x27;d, but the release was blocked, so I looked anyway.”</span><br>• <b><i>same shape</i></b> — 形态完全相同<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Two resources in another module were the same shape as the one that broke.”</span></div>
