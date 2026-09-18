# 06 · Expertise / 项目深挖

> 事实层在 `../../loop/LOOP_GUIDE.md` §7；题库 `../../loop/rounds/06_project_deep_dive/`；素材 [[Core]]、`resume-evidence-map/01、02`。

## 这轮到底考什么（一句话）

**每个决策的 why、被否方案、系统属性。** 一手（Blind IC3）："pick a project and deep dive into it for good 40 mins"，追问 "why/how I made the decisions… technical architecture, approach and external libraries"，并延伸到 availability / fault tolerance。早期职业：coding 轮前 15–20 min + onsite 一轮 resume。

## 准备两个 15 分钟版本

**[[S1]] · AMEX GRRCN 管线**（主讲，Snowflake-native，面试官最有共鸣）

| 分钟 | 内容 |
|---|---|
| 0–2 | 一句话 + 数字：Amex 专有定宽结算文件 → fee → 出款；2025 年 ~22M 笔 / $138.6B；18 个月生产；我从 stub 设计到 EU 扩展 |
| 2–6 | 架构口述：S3 → staging（整行一列）→ 6 条 append-only stream 按 record type 分流 → proc 解析 + TRY_CAST + MERGE → UDTF 合并 → fee task → Funding |
| 6–11 | 三个决策 × 被否方案：① Snowflake-native vs Airflow / Ruby 续命 ② 按类型分流 vs 单流全扫 / 外部解析服务 ③ 幂等 MERGE + 急停 flag vs 手工回滚 |
| 11–14 | 失败模式与监控：半截文件、重复投递、stream 过期、summary 对账不一致即停；TASK_HISTORY + Streamlit + Datadog |
| 14–15 | 重做清单：商户粒度质量门从第一天做；下游聚合改 Dynamic Tables |

**[[S5]] · Net settlement 迁移**（备用，决策与验证最强）

| 分钟 | 内容 |
|---|---|
| 0–2 | $450M/月 float → Fiserv 净额 T+1；我拥有 pricing 侧；$55B+ TPV 前提 |
| 2–6 | interchange 取数 Trans View → Settle View；CDC backfill 三级时间兜底 |
| 6–11 | shadow-run vs flip-and-monitor；商户灰度 vs 全量；模板化 vs 一次性脚本 |
| 11–14 | 13.7M 行 day-level 对账 0.224%，每类差异解释完才切；toggle 回滚路径 |
| 14–15 | 重做：更早 handshake；差异自动分类 |

## 练法

1. 对着 `../../loop/rounds/06_project_deep_dive/questions.md` 抽 3 题，每题 5 分钟（`mock.py bq expertise -n 3 -m 5`）。
2. 每个决策做"三层自检"：why → alternatives → now。第二层讲不出就是挂点。
3. 录音，对 `rubric.md` 五维打分。

## 红线

- 只用已确认数字（138.6B / 21.96M / 13.7M / 0.224% / $55B / $450M）；不说 $600B。
- 不编 PR review 与 1:1 细节。
- 被问到不知道的内部细节，说"that was owned by the Funding team; what I owned was…"。
