---
title: S6 · Fee anomaly detector 的 go/no-go
aliases:
  - S6
  - Anomaly detector
  - go/no-go gate
tags:
  - interview/story
  - stack/production
  - judgement
answers: [Q7, Q17, Q20, Q23]
stacks: [TS03, TS08]
status: verified
---

# S6 · Fee anomaly detector 的 go/no-go（判断力 · 说不 · 分阶段）

> [!abstract] 一句话
> 实习生离职前留下一个只在 QA 跑过的 ML 费用异常检测器。惯性是接着做；我先写了一份 State / Handoff / Prod-Cutover 评估：QA 六个合成商户 vs 生产 18,140 个、峰值一天 7.6 亿行，逐行 numpy 推理必然超时——于是拆成"什么会随离职消失 vs 什么可重建"，先保住不可再生的人工标注，再把上线切成 Phase 1（确定性规则用 SQL pushdown，几周）和 Phase 2（模型重训 + 推理重构，两三个月，**门后**），冻结 Slack 告警和 CI/CD 直到 go/no-go 给出 go。

## 1. 评估的结构（这份文档本身就是故事）

| 问题 | 我给的答案 |
|---|---|
| 系统是什么 | 三层：autoencoder（PyTorch 训练、numpy 推理）· 计划偏差特征 · 确定性一致性规则 `\|amount\| = rate × qty + fixed`；5 个数据源各一套模型与日评分 proc；部署全手工，无 CI/CD |
| 数据从哪来 | **从未见过生产**：QA 8.3 亿行 / 6 个合成商户（前两个占 97%），生产 390 亿行 / 18,140 商户 / 1,468 plan code / 15,293 (plan, description) 组合 |
| 离职会丢什么 | 代码、terraform、训练配方（seed 固定）都可重建；**唯一不可再生的是分析师的 disposition 标注**——先导出 |
| 上线要多久 | 5–8 人周编码，2–3 个月到"生产可信"；最不确定的是**推理规模**（QA 从未暴露） |
| 风险排序 | ① 推理性能 ② 精确率未知（无 ground truth，只能 shadow）③ 告警量：99.5% 阈值 × 每天数亿行 = 每天数百万条 |
| 建议 | Phase 1 只上确定性规则，纯 SQL，Snowflake 原生处理数十亿行；Phase 2 才碰 ML；两者都在 go/no-go 门后 |

## 2. 为什么是 senior 的判断

- **不按沉没成本排优先级**，按风险调整后的期望价值排。
- **把判断制度化成 gate**，不是"我觉得不值就停"：写下来、可审查、上级能独立判断。
- **先降低不确定性本身**：模糊状态先写清，再谈产出。
- 与 [[S7]] 放在一起讲"主动性"：主动造价值 vs 主动踩刹车，后者更难。

> [!warning] 证据边界
> 四个量级（834M / 39B / 6 vs 18,140 / 760M）出自我自己的评估文档，尚未从生产复核；口播用 "under a billion rows vs tens of billions"、"six merchants vs eighteen thousand"、"up to about 760 million rows on a peak day"。不点名实习生。

## 3. English · 首答（60 s）

> I inherited an ML fee-anomaly detector from a departing intern. The easy path was to keep building. Instead I wrote a go/no-go assessment. QA had six synthetic merchants and under a billion rows; production is eighteen thousand merchants, fifteen thousand plan combinations, and up to seven hundred and sixty million rows on a peak day. The serving design was a per-row numpy forward pass — that would time out on a large warehouse, and QA could never have surfaced it.
>
> So I split it: what dies when the intern leaves versus what's reproducible from code — only the analyst labels were irreplaceable, and I got those persisted before their last day. Then a phased plan: Phase 1 ships only the deterministic consistency rule as pure SQL pushdown — `|amount| = rate × qty + fixed` — which Snowflake handles at billions of rows natively; Phase 2, the autoencoder retrain and serving redesign, is two to three months and gated behind an explicit business-driver decision. I froze the Slack alerting and CI/CD work until that gate says go. Results matter; I'd rather stop a project than ship one that pages the team at 3 a.m.

## 4. 用在哪

- 回答：[[Answers#Q7]] 主动性 · [[Answers#Q17]] 模糊性 · [[Answers#Q20]] 优先级取舍 · [[Answers#Q23]] 规划
- 场景题：变慢 / 100× 数据量（逐行 → set-based）
- 技术栈：[[03-snowflake-warehouse|TS03]] · [[08-observability-oncall|TS08]]
- 相邻：[[S7]] · [[S8]]（同一项目的 terraform 事故）

## 5. 证据锚点

Confluence 3049697063；Jira DTBTTFOUND-3254 / 3255 / 3256 / 3257 / 3259 / 3260 / 3261（label `anomaly-detector`）。
