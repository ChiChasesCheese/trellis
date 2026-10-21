---
id: nr-amz-s7-followups
node: amazon.followups
type: qa
step: 31
---
## Q
<p class="title">schema pool<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **Why GitHub Deployments API, not tags?**
    - 打了 **tag 没部署**；Deployments API 记录**生产环境实际部署**的 SHA
- **Why is a clone 2 seconds?**
    - **不可变微分区** + **元数据指针**，不拷数据
- **What broke in V1?**
    - `PUBLIC` 的状态取决于**谁最后跑了什么迁移**，不可预测
- **How do cross-database streams break?**
    - 先克隆 APP_DB 再 REPL_DB 会让依赖 REPL 表的 **stream 失效**
    - 固定顺序**先 REPL 后 APP**；`MAIN_STAGING → MAIN` 交换后**自动扫描修复**
- **How do you trust AI-generated code?**
    - **plan with the agent → TDD every phase → CI + monitoring gates**；看 **gates 和 thresholds**，不看行数
    - money code 里我读**每一个 diff**
- **Why direct-push to main?**
    - **个人仓库**，不影响团队代码；诚实说明
- **Who uses it?**
    - 见待补；on-call copilot 是相邻团队采用（人数无记录）

<div class="sources"><b>表达 · business English</b><br>• <b><i>source of truth for what&#x27;s deployed</i></b> — “当前部署了什么”的权威来源<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The Deployments API is the source of truth for what&#x27;s deployed, not a release tag.”</span><br>• <b><i>gates and thresholds</i></b> — 关卡与阈值<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“To trust AI code I look at the gates and thresholds, not lines of code.”</span><br>• <b><i>own every diff</i></b> — 对每一处改动负责<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“In money code I read and own every diff.”</span></div>
