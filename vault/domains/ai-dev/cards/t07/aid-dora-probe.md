---
id: aid-dora-probe
node: t07.dora-ai-assisted-software-development-report
type: qa
step: 2
tags: [考点]
---
## Q
**DORA · 放大器怎么用**｜考点 · 追问

两个团队同时上线 agent。A：CI 15 分钟、测试覆盖好、小步合并；B：CI 要两小时、测试不稳定、每周一次大发布。按"放大器"的结论，一个季度后各会怎样？该先投资什么？

## A
| | A | B |
|---|---|---|
| 变更量增加 | 被快速反馈消化 | 排队、堆积，一次发布含大量未验证改动 |
| 缺陷 | 在 CI 里被拦 | 流到下游，不稳定放大 |
| 预期结果 | 吞吐上升且稳定性可控 | 吞吐可能上升，**稳定性下降** |

**B 该先做：** 不是买更多 agent 席位，而是修基础——让测试稳定、CI 变快、发布变小。这正是报告的发现："没有强自动化测试、成熟版本控制、快速反馈，更多变更导致不稳定"。

**追问：** 这个判断有什么不能保证？DORA 是相关性调查，不是随机实验；能说"一致"，不能说"因果已证明"。

<details class="pt" markdown="1"><summary>出处</summary>

DORA《2025 State of AI-assisted Software Development》（Google Cloud 博客）

</details>
