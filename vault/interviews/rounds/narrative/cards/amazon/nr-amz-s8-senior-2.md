---
id: nr-amz-s8-senior-2
node: amazon.followups
type: qa
step: 38
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">03 senior 追问</span></p>

*"Why REVOKE and not COPY, and how did you make sure revoking the reviewer's USAGE wouldn't break something else?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对修复的副作用与影响面是否想清楚。

<span class="label">回答框架</span>

- 先说两个选项的语义：COPY 把授权复制给新所有者，REVOKE 直接撤销
- 核查谁依赖被撤销的授权：查看该角色的下游使用
- 先在 QA 验证，再逐环境放行，保持修复可重入
- 说明事实：当时我是对照邻近模块的做法选择的，没有做更深的权衡，下次会写下来

<span class="label">为什么这是最佳实践</span>

一行修复的风险常常在影响面。REVOKE 会撤销别人的访问，所以必须确认没人依赖；COPY 则会让授权扩散。最稳妥的是先在 QA 观察，再往上放。我会如实说当时的依据，并说明下次会把权衡写进 PR 描述。

<div class="sources"><b>表达 · business English</b><br>• <b><i>downstream impact</i></b> — 对下游的影响<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“REVOKE has a bigger downstream impact than COPY, so I wanted QA to prove it first.”</span><br>• <b><i>side effect</i></b> — 副作用<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I checked for side effects on the reviewer role before relying on the fix.”</span></div>
