# Amazon kit — 进度断点

> 分支 `amazon-kit`（从 main 切出）。编排：主会话，子代理 sonnet ≤ 3。规则 `AGENT_RULES.md`。

## 现状（2026-10-15）

岗位：Software Development Engineer, AWS Data Services – 2026 (US)，job 10414316，**SDE I**，Seattle。
Onsite：西雅图现场，约 10/20–21（由 10/19 去、10/22 回的机票推断；recruiter 邮件在 NYU 邮箱，主会话读不到）。
Chi 的要求：教科书模式；编码用 Python。

## 阶段

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P1 | 流程调研 `catalog/raw/{github_repos,official,forums}.md`（110 条面经） | ✅ | 主会话审 |
| P2 | LP 故事库 `lp/`（15 故事 × 16 LP）+ GenAI 轮 `lp/genai/` | ✅ | `python3 lp/coverage.py`；引用 commit 核对存在 |
| P3 | 编码 `coding/`（16 模式、81 题） | ✅ | `python3 -I coding/run_all.py` ALL PASS |
| P4 | 系统设计 `sd/` + LLD `lld/`（senior 标准） | ✅ | lld/code 全 OK；18 条凭记忆项核对（11 对 6 改） |
| P5 | LOOP_GUIDE · README | ✅ | — |

## 下一步（Chi）

1. 统一简历 $600B / net settlement 口径（README「面试前必须处理」）。
2. 按 `lp/drill.md` 补【待 Chi 补】，先补 matrix 里的单点风险 LP。
3. 按 LOOP_GUIDE §6 的 5 天表走；面完写 debrief 回填 `catalog/raw/`。
