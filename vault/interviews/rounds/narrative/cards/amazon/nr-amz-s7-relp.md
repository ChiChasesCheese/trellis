---
id: nr-amz-s7-relp
node: amazon.outline
type: qa
step: 21
---
## Q
<p class="title">schema pool<span class="meta">02 提纲</span></p>

换成别的 LP 问时，强调哪一段？

## A
- **Invent and Simplify**：两秒克隆取代「等共享 schema 轮到你」；MAIN 同步到部署 SHA；别说成团队标准
- **Bias for Action**：没人派，一个下午上 V1，学到 `PUBLIC` 为什么不确定后重写；23 次直推
- **Ownership**：不在我岗位描述里，我维护它；无 ticket、有 ADR、有 Sync Failure Playbook
- **Learn and Be Curious**：学 zero-copy clone 与跨库 stream 的真实行为；微分区元数据、stream 对克隆顺序敏感
- **Frugality**：克隆花的是元数据不是存储；2 秒、不复制数据；无费用数字，别编
- **Think Big**：同一个工具让「agent 团队」工作流成为可能；on-call copilot；别夸大成「改变了团队」

<div class="sources"><b>表达 · business English</b><br>• <b><i>unblock yourself</i></b> — 自己扫清障碍<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I unblocked myself and the agents by removing the shared-schema bottleneck.”</span><br>• <b><i>tech lead of a team of agents</i></b> — agent 团队的技术负责人<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I see myself as the tech lead of a team of agents.”</span><br>• <b><i>low-cost experiment</i></b> — 低成本实验<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A clone costs metadata rather than storage, so it was a low-cost experiment to run.”</span></div>
