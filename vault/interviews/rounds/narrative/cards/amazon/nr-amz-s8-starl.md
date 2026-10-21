---
id: nr-amz-s8-starl
node: amazon.outline
type: qa
step: 23
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- **Snowflake 基础设施**仓库的发布在 **QA** 失败：`GRANT OWNERSHIP` 被拒
- 一个 reviewer 角色已持有依赖的 **USAGE** 授权

<span class="label">T</span>

- 别人被**分配**去查，我只是 **cc**；但发布被卡住

<span class="label">A</span>

- **读错误**，对上我熟悉的授权结构
- **7 分钟**贴出根因：ownership 资源没设 `outbound_privileges`
- 贴**一行修法** `outbound_privileges = "REVOKE"` + **邻近模块**核查
- **问了**能否直接推；PR 合入
- **事后**扫**全仓库**找同样的遗漏
- 标出另一模块里 **2 个**同形、还没触发的资源

<span class="label">R</span>

- QA、pre-prod、prod **同一下午**部署
- 扫描：几十个缺该参数，多数是无害 `future_*`；挖出 **2 个真实风险**，我不说它们已修

<span class="label">L</span>

- **修这一个**和**消灭这一类**是两件事
- 宁可负责「这是下一个」

<div class="sources"><b>表达 · business English</b><br>• <b><i>unblock the release</i></b> — 让发布不再被卡住<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I posted the fix quickly to unblock the release.”</span><br>• <b><i>ask for permission to push</i></b> — 先问可否直接推送<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I asked for permission to push, and the PR went in.”</span><br>• <b><i>sweep the repo</i></b> — 全仓库扫一遍<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“After the fix I swept the repo for the same omission.”</span></div>
