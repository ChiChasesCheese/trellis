---
id: nr-amz-s7-senior-2
node: amazon.followups
type: qa
step: 33
---
## Q
<p class="title">schema pool<span class="meta">03 senior 追问</span></p>

*"What are the failure modes of a clone-based pool, and how would you keep it reliable as more people use it?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对共享基础设施的可靠性、泄漏和并发边界是否有思考。

<span class="label">回答框架</span>

- 先列失败模式：槽位泄漏、同步到一半失败、MAIN 与生产漂移、克隆顺序引发的 stream 失效
- 再说防护：借用设租期、超时自动回收、同步失败有 playbook
- 监控：槽位使用率、同步新鲜度、克隆耗时
- 容量：槽位数量与并发会话数的关系，以及耗尽时的退让策略

<span class="label">为什么这是最佳实践</span>

共享工具的可靠性取决于怎么失败，而不是怎么成功。租期与自动回收防止泄漏，同步新鲜度监控防止测试在过期结构上通过，Sync Failure Playbook 让别人不依赖我也能恢复。这些是个人工具变成团队工具之前必须补的。

<div class="sources"><b>表达 · business English</b><br>• <b><i>blast radius</i></b> — 影响范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Isolated clones keep the blast radius of a bad migration to one session.”</span><br>• <b><i>lease and reclaim</i></b> — 租借并回收<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d add a lease and reclaim so abandoned slots free themselves.”</span></div>
