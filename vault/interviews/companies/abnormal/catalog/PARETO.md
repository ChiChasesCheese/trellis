# PARETO — 按 轮次权重 × #refs × 时效 排序（`tools/pareto.py` 输出，勿手改数字）

> 命令：`python3 tools/pareto.py catalog/RANK.md --table "总表" --focus "AI screen"`（2026-10-07 重跑：新增 cb04–cb06）。
> 宇宙很小（15 行，报道稀少），所以 80% 落在第 7 行 = 前 47%，不是教科书的 20%；**cut line 以上全部已建题**。cb04 / cb05 是 0 refs 的题型练习（覆盖 HI 开放式最常见题型与算法模式），cb06 是 File Vault take-home 同形（1 ref）。
> AI screen 是下一轮（focus 权重 1.0），其余 onsite 0.8。cb03 没有面试报道（0 refs），它的价值是团队面与 HM/deep dive 的领域语言，不进覆盖率分子。

| # | 题 | 轮次 | #refs | 最近 | score | 累计 |
|---|---|---|---:|---|---:|---:|
| 1 | 已有代码库 + 未披露 feature（insider-risk 领域库练格式） | AI screen | 5 | 2026-09 | 5.00 | 21% |
| 2 | Code review 小仓库：P0/P1 排序 + 用 AI 修 | onsite | 5 | 2026-09 | 4.00 | 38% |
| 3 | AWS incident 排查：根因、信号、止血、长期修复 | onsite | 4 | 2026-09 | 3.20 | 51% |
| 4 | 已有系统扩容：读/写扩展、瓶颈 | onsite | 4 | 2026-09 | 3.20 | 65% |
| 5 | 图片/文件去重（内存受限、哈希碰撞） | 旧流程电面 | 4 | 2025-07 | 1.92 | 73% |
| 6 | Security-events 管线：规则抑制 · enrichment 插件化 · 告警去重 | AI screen | 2 | 2026-06 | 1.60 | 80% |
| 7 | Code review 后的扩展：并发、worker、队列扩容、失败场景 | onsite | 2 | 2026-09 | 1.60 | 86% |
| 8 | File Vault take-home 同形：去重 + 并发 · 搜索 · 配额 | take-home · AI screen（迁移 | 1 | 2026-07 | 1.00 | 91% |
| 9 | 大规模照片去重服务 | 旧流程 SD | 2 | 2025-07 | 0.96 | 95% |
| 10 | 开放式安全 take-home | 旧 OA | 1 | 2025-01 | 0.48 | 97% |
| 11 | CSV session 平均时长（SRE） | SRE coding | 1 | 2025-07 | 0.48 | 99% |
| 12 | JSON Schema parsing | 旧 OA | 1 | 2024-09 | 0.32 | 100% |
| 13 | 团队领域：候选人身份欺诈（关联 · 新数据源 · 审核反馈） | AI screen（迁移） | 0 | 2026-09 | 0.00 | 100% |
| 14 | 修埋好的 bug + 推到生产可用 + 突发流量 | AI screen（题型练习） | 0 | 2026-10 | 0.00 | 100% |
| 15 | 算法型扩展：解析器 · 拓扑排序 · 图搜索 | AI screen（题型练习） | 0 | 2026-10 | 0.00 | 100% |

**15 行 · 累计 80% 出现在第 7 行（前 47%）** —— cut line 以内的题先建题库。
