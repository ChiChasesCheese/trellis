---
id: nr-amz-s8-full
node: amazon.full
type: qa
step: 8
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：我们 Snowflake 基础设施仓库的一次发布在 QA 失败了：对一个数据库的 GRANT OWNERSHIP 被拒绝，因为一个 reviewer 角色已经持有依赖它的 USAGE 授权。被分配去调查的是别人，我只是被 cc。
- 行动：我读了错误信息，对上我熟悉的授权结构，7 分钟后贴出根因：ownership 资源没设 outbound_privileges，所以 Terraform 想转移所有权却没有先撤销依赖授权。我同时贴了一行修法 outbound_privileges = "REVOKE"，以及对相邻模块的核查。
- 推进：我问了一句能不能直接推，PR 合入后，QA、预生产、生产在同一个下午都部署完了。
- 事后：火灭了之后我扫了整个仓库。79 个 ownership 资源里有 42 个缺这个参数，多数是无害的 future_* 授权，但另一个模块 scheme_fees 里有 2 个和出事的形状完全一样、还没触发的资源，我把它们标了出来。
- 学到：修这一个和消灭这一类是两件事。我宁可负责“这是下一个”，也不只管已经响了的那一个。

<span class="label">英文口述（60–90 秒）</span>

A release of our Snowflake infrastructure repo failed in QA. GRANT OWNERSHIP on a database was rejected because a reviewer role already held a dependent USAGE grant. Someone else was assigned to investigate; I was cc'd. Seven minutes later I'd posted the root cause: the ownership resource didn't set outbound_privileges, so Terraform tried to transfer ownership without revoking dependents. I posted the one-line fix, outbound_privileges equals REVOKE, and a check of the neighboring modules. I asked whether I could push, the PR went in, and QA, pre-prod and prod deployed that afternoon. The part I care about is what came after. I scanned the whole repo: out of seventy-nine ownership resources, forty-two lack the parameter. Most are future grants where it's harmless, but two in another module are the exact same shape as the one that broke, and haven't fired yet. I flagged them. I'd rather own here's the next one than only the one that paged.

<div class="sources"><b>表达 · business English</b><br>• <b><i>root-cause under pressure</i></b> — 压力下定位根因<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I root-caused the grant failure under pressure in about seven minutes.”</span><br>• <b><i>the next landmine</i></b> — 下一个隐患<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“After the fix I flagged the next landmine before it went off.”</span><br>• <b><i>time-box</i></b> — 给排查限定时间<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Under pressure, time-box each hypothesis so you don&#x27;t tunnel on one.”</span></div>
