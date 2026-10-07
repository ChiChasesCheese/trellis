# RANK — 技术题一张表（28 法则打分的输入）

> 由 `CATALOG.md` 总表汇总。跑：`python3 tools/pareto.py catalog/RANK.md --table "总表" --focus "AI screen"`
> 输出写进 `PARETO.md`（不手抄数字）。

## 总表

| ID | 题 | 轮次 | 最近 | #refs | 置信度 |
|---|---|---|---|---:|---|
| cb01 | Security-events 管线：规则抑制 · enrichment 插件化 · 告警去重 | AI screen | 2026-06 | 2 | MED-HIGH |
| cb02 | 已有代码库 + 未披露 feature（insider-risk 领域库练格式） | AI screen | 2026-09 | 5 | MED |
| cb03 | 团队领域：候选人身份欺诈（关联 · 新数据源 · 审核反馈） | AI screen（迁移） | 2026-09 | 0 | — |
| cb04 | 修埋好的 bug + 推到生产可用 + 突发流量 | AI screen（题型练习） | 2026-10 | 0 | — |
| cb05 | 算法型扩展：解析器 · 拓扑排序 · 图搜索 | AI screen（题型练习） | 2026-10 | 0 | — |
| cb06 | File Vault take-home 同形：去重 + 并发 · 搜索 · 配额 | take-home · AI screen（迁移） | 2026-07 | 1 | MED |
| cr01 | Code review 小仓库：P0/P1 排序 + 用 AI 修 | onsite | 2026-09 | 5 | MED |
| sd02 | Code review 后的扩展：并发、worker、队列扩容、失败场景 | onsite | 2026-09 | 2 | MED |
| ic01 | AWS incident 排查：根因、信号、止血、长期修复 | onsite | 2026-09 | 4 | MED |
| sd01 | 已有系统扩容：读/写扩展、瓶颈 | onsite | 2026-09 | 4 | MED |
| pc01 | 图片/文件去重（内存受限、哈希碰撞） | 旧流程电面 | 2025-07 | 4 | MED |
| sd03 | 大规模照片去重服务 | 旧流程 SD | 2025-07 | 2 | MED-LOW |
| pc02 | JSON Schema parsing | 旧 OA | 2024-09 | 1 | MED |
| pc03 | 开放式安全 take-home | 旧 OA | 2025-01 | 1 | MED |
| pc04 | CSV session 平均时长（SRE） | SRE coding | 2025-07 | 1 | MED |
