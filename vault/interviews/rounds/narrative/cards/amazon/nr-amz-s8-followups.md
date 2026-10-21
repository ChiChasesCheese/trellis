---
id: nr-amz-s8-followups
node: amazon.followups
type: qa
step: 36
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **How did you get to the root cause in 7 minutes?**
    - 对整个仓库的 **grant 结构**有全局图景；错误信息指向**依赖授权**；provider 有对应参数
- **Why REVOKE and not COPY?**
    - COPY 会把授权复制给新所有者；其余见待补
- **What are the risks of this fix?**
    - Terraform **无事务**，修复必须可重入
    - REVOKE 会撤销 reviewer 角色的 **USAGE**，要确认它是否依赖
- **Why didn't you fix the two risky ones?**
    - 见待补
- **How would you prevent this class?**
    - 全仓库 **lint / policy check**，前移到 **plan 阶段**；尚未落地，别说成已有
- **Why the scan?**
    - 「修完这一次」和「消灭这一类」是**两件事**
- **Terraform pitfalls?**
    - **重命名资源**默认删了重建（`moved` block / `state mv`）；危险变更**拆小、可重入**

<div class="sources"><b>表达 · business English</b><br>• <b><i>re-entrant</i></b> — 可重入，中途失败后能安全重跑<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Terraform has no transactions, so the fix has to be re-entrant.”</span><br>• <b><i>shift left</i></b> — 把检查前移到更早阶段<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A policy check at plan time would shift left the detection of this class.”</span><br>• <b><i>dependent grant</i></b> — 依赖的授权<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Before transferring ownership we have to revoke or account for each dependent grant.”</span></div>
