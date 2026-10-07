# CATALOG — Abnormal AI 被报道的题（一行一题族）

> 证据：`raw/inbox.md`（门户官方，[高]）· `raw/official.md`（官网/JD/产品，O-n）· `raw/ai_screen_format.md`（F-n）· `raw/process_and_rounds.md` · `raw/questions_reported.md`（Q-n）· `raw/github_repos.md`（GitHub 优先：**无**任何 Abnormal 题库或公司标签列表；LeetCode 公司标签源三家均无 Abnormal）。
> 编排者复核（2026-10-06）：LeetCode Discuss #8335187 与 #8496901 两帖正文经 `POST leetcode.com/graphql`（`ugcArticleDiscussionArticle`）**亲自重取并逐字核对**，与 raw 文件引文一致。
> `#refs` = 独立来源数（同一候选人跨站算 1；聚合站互抄算 1；PracHub 付费标题与 1p3a 摘要疑同源，合计算 1）。置信度：HIGH 一手全文 · MED 一手摘要/编辑过的聚合 · LOW SEO。

## 一个必须先说的事实

**AI screen 的代码库与题目不公开，报道过的只有一份**：security-events 管线（collection/ingestion → enrichment（geo-ip、history、+1）→ 规则 threat level → ranking → alerts → API → DB），feature = ① 规则抑制（含 geo-ip 这类复杂条件）② 把硬编码的 enrichment 改成插件机制（Q1–Q4）。另外 5 份报道只说"已有代码库 + 一个 feature + 写测试 + 讨论扩展"，没说 feature 是什么（Q5–Q7、F-12–F-14）。
所以 80/20 在这一轮的含义是：**① 把报道过的那份代码库形态与两题做透（cb01）② 把"格式"练熟——在两个别的领域库上各做 3 张模糊 ticket（cb02 · cb03）**，靠迁移覆盖未披露的 feature。覆盖率数字只量得到 ①。

## 总表（→ `RANK.md`）

| ID | 题族 | 轮次 | 最近 | #refs | 置信度 | 来源 | 本 kit |
|---|---|---|---|---:|---|---|---|
| cb01 | **Security-events 管线扩展**：规则抑制（geo-ip 等复杂条件，多租户 API）· 硬编码 enrichment → 插件机制（客户不碰平台代码）· +告警去重（reconstructed） | AI screen | 2026-06 | 2 | MED-HIGH | Q1/Q2 LC #8335187（全文）· Q3/Q4 PracHub 标题 + 1p3a 1181621 摘要（同源，算 1） | `loop/rounds/01_ai_screen/cb01_sentinel/` t1 t2 t3 · **原题复刻 `REAL_QUESTION.md` + `start cb01 real`** |
| cb02 | **已有代码库 + 未披露 feature + 测试 + 扩展讨论**（格式本身；领域未知 → 以 insider-risk 领域库练） | AI screen | 2026-09 | 5 | MED | Q5 #8496901 · Q6 #8387564 · Q7 PracHub a2857641b5 · PracHub 874b1387d9 · Glassdoor Sr SWE 2026-06（"coding exercise with AI assistant"） | `cb02_insiderwatch/` t1 t2 t3 |
| cb03 | **团队真实领域**：候选人身份欺诈（Infiltration Prevention）——关联引擎、新 ATS 数据源、审核反馈 | AI screen（迁移练习）· 团队面 | 2026-09 | 0 | — | 无面试报道；领域来自 JD 与产品页 O-1/O-4（官方） | `cb03_vetting/` t1 t2 t3 |
| cb04 | **修埋好的 bug + 推到生产可用**：跨租户、吞异常、竞态、时区、非幂等 release；开放的 production-ready；同一封邮件的突发报告 | AI screen（题型练习） | 2026-10 | 0 | — | 无 Abnormal 报道；题型来自 HI 开放式题（Schedulr · Transcribe · Fileshare · LinkLock）与 `raw/ai_round_sweep_2026-10-07.md` 题型地图 | `cb04_quarantine/` t1 t2 t3 |
| cb05 | **算法型扩展**：规则表达式解析器 · 检测器依赖拓扑排序 · 被盗账号影响面 BFS | AI screen（题型练习） | 2026-10 | 0 | — | 无 Abnormal 报道；模式来自 HI Patterns；印度路径 OA 有图题（sweep S-2，类比） | `cb05_rulelang/` t1 t2 t3 |
| cb06 | **File Vault take-home 同形**：内容去重（含并发）· 搜索过滤 · 配额 + 统计 + 限流；要求录屏讲 GenAI 用法 | take-home（旧流程）· AI screen（迁移） | 2026-07 | 1 | MED | sweep S-1（GitHub 模板 + 候选人仓库，`gh api search/repositories -f q="abnormal file vault"` 40 个） | `cb06_filevault/` t1 t2 t3 |
| cr01 | **Code review 一个小仓库**：找问题、P0/P1 排序、给具体修法（+ 用 AI 修） | onsite | 2026-09 | 5 | MED | Q12 #8496901 · Glassdoor 2026-04（"Code review & fix implementation with AI"）· Glassdoor Sr SWE 2026-06（"take-home code review"）· PracHub（"PR or code-review discussion"）· Q14 1p3a 1148780（2025-10，预发 link） | `loop/rounds/03_code_review/cr01_*` |
| sd02 | **Code review 之后的扩展**：并发/并行、worker 扩容、消息队列扩容、吞吐、瓶颈、失败场景（"beyond add more workers"） | onsite | 2026-09 | 2 | MED | Q13 #8496901 · Q14 1p3a 1148780（同轮 code review + SD） | `loop/rounds/03_code_review/cr01_*/followups.md` + `sd02` |
| ic01 | **AWS 环境里排查一个线上 incident**：哪里坏了 · 根因怎么找 · 看哪些 logs/metrics · 立即止血 · 长期修复 | onsite | 2026-09 | 4 | MED | Q8 #8496901 · Q9 #8387564 · Glassdoor 2026-04（"System design & Incident handling"）· PracHub（"incident-management-style"） | `loop/rounds/02_incident_sd/ic01_*`、`ic02_*` |
| sd01 | **给一个已有系统，怎么扩容**：读扩展、写扩展、瓶颈、流量增长下的行为 | onsite | 2026-09 | 4 | MED | Q10 #8496901 · Q11 #8387564 · Glassdoor 2026-04 · PracHub | `loop/rounds/02_incident_sd/sd01_*` |
| pc01 | **图片/文件去重**（内存受限、哈希、哈希碰撞、`os.walk`、写 main）（旧流程电面） | 旧流程电面 | 2025-07 | 4 | MED | Q16 1p3a 1059585 / 1072363 / 1074077 / 1137132（四帖摘要）· PracHub "duplicate-file removal"（2025-07，疑同源不另计） | `loop/rounds/06_legacy_coding/pc01_*` |
| sd03 | **大规模照片去重服务**（旧流程 SD） | 旧流程 SD | 2025-07 | 2 | MED-LOW | PracHub "scalable photo deduplication service"（2025-07）· 1p3a 1072363（"最后问 system design"） | `pc01` 的 followups §SD |
| pc02 | JSON Schema parsing（旧 OA） | 旧 OA | 2024-09 | 1 | MED | Q25 Glassdoor | 未建（旧流程，单一来源） |
| pc03 | 开放式安全 take-home（2 天） | 旧 OA | 2025-01 | 1 | MED | Q26 LC #6347241 | 未建（新流程已取消 take-home 的 SWE II 路径；Singapore 等地区仍有 take-home） |
| pc04 | CSV session → 每用户平均时长（SRE，CodeSignal） | SRE coding | 2025-07 | 1 | MED | Q28 LC #6939818 | 未建（SRE 岗位） |

## 非编码轮（题库，不进 RANK）

| 轮 | 证据 | 本 kit |
|---|---|---|
| Manager / behavioral（过往项目、技术决策、挑战、影响、情景题；"why Abnormal"；"how do you use AI"） | Q17–Q21 · O-14 · O-15 | `loop/rounds/04_manager_deep_dive/` |
| 额外的 technical deep dive（"lacked sufficient judgment"） | Q22 | 同上，§judgment |
| Team Interviews（跨职能，价值观 VOICE、协作） | O-10 · O-14 | `loop/rounds/05_team_values/` |

## 不入库

- Scoutify 19 题（自述"inferred from open roles"，面向销售/SE）。PracHub/InterviewQuery 通用指南的"可能会问"清单（编辑撰写，非报道）。
- "Fourth Round Video"：任何渠道无对应原文（raw/process_and_rounds.md §1.6），不建。
