# COVERAGE — 已建题对公开流出题的覆盖（`python3 tools/coverage.py`，2026-10-07）

> **分母** = `catalog/RANK.md` 12 行的 #refs 之和（独立来源数）；宇宙 = GitHub（无任何 Abnormal 列表）+ LeetCode Discuss + 1p3a 镜像 + PracHub + Glassdoor 摘要 + Blind。
> **只量得到被报道过的题**：AI screen 真实代码库只有一份报道（cb01 照它造）；cb02/cb03 与 `study/00-essentials.md` 练的是迁移，覆盖率看不见那部分。cb03 为 0 refs（团队领域，无面试报道），不进分子。
> 未建：sd03（照片去重服务，已作为 pc01 的 SD 追问讨论，不单独成题）与三道各只有 1 份报道的旧流程/SRE 题。

| 轮次 | 出现次数覆盖 | 题族覆盖 |
|---|---:|---:|
| AI screen 代码库 | 7/7 = 100% | 3/3 |
| Code review | 5/5 = 100% | 1/1 |
| Incident | 4/4 = 100% | 1/1 |
| 系统设计 | 6/8 = 75% | 2/3 |
| 旧流程 coding | 4/7 = 57% | 1/4 |
| **合计** | **26/31 = 84%** | **8/12** |

未建（按出现次数降序）：
- sd03（2）大规模照片去重服务
- pc04（1）CSV session 平均时长（SRE）
- pc03（1）开放式安全 take-home
- pc02（1）JSON Schema parsing

非编码轮题库：04_manager_deep_dive 16 · 05_team_values 10
