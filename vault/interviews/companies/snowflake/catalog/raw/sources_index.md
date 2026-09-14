# 来源台账（system_design.md / bq_hm_recruiter.md / process_and_jd.md 共用）

> 采集日期：2026-09-13（全部条目同一天完成，未标注则均为此日期）。可达性：**200** = 直接读到正文内容；
> **摘要** = WebFetch/WebSearch 只返回摘要或页面骨架，正文本身不可达（如 403/410）；**403/410/关闭** = 请
> 求被拒或职位已下线（但内容仍可能通过其它渠道读到，见备注）。可信度沿用三份文件里的 [高]/[中]/[低] 体
> 系：官方页面与一手候选人叙述记 [高]；聚合/培训站转述记 [中] 或 [低]；lodely、vervecopilot 一律不采信
> （本次调研未检索到这两个域名，符合仓库规矩）。

## 官方来源（careers.snowflake.com）

| URL | 内容 | 可达性 | 可信度 |
|---|---|---|---|
| https://careers.snowflake.com/us/en/generalsoftwareengineeringprogram | GenSWE 项目说明、FAQ、4 步流程、在招职位入口 | 200 | 高 |
| https://careers.snowflake.com/us/en/gethired | 官方 4 阶段 Hiring Process | 200 | 高 |
| https://careers.snowflake.com/us/en/job/SNCOUSDD524B932E4E4E3B84B44684A46E9148EXTERNALENUS3EB872AF0AB149868F72E7321FCD1538/Software-Engineer-Backend | GenSWE "Software Engineer - Backend" JD 原始链接（当前仍链接在 GenSWE 页面上，但直接抓取显示 "已关闭" 骨架页，正文需经 builtin/zapply 镜像读取） | 骨架页，无正文 | 高（职位存在性），正文见镜像 |
| https://careers.snowflake.com/us/en/job/SNCOUSAD1534302339458586FEB7D4B2D4E21DEXTERNALENUSC592250A60414C40AA821D947E3494DA/Backend-Software-Engineer-AI-Platform-for-User-Experiences | Backend SWE, AI Platform for User Experiences (Bellevue) | 410 | 中（仅标题/搜索摘要确认存在） |
| https://careers.snowflake.com/us/en/job/SNCOUS1765E102554A42B1A2389D13DEB3F1FBEXTERNALENUSDB1375F0EA5D404AB640259F94DBC995/Software-Engineer-Database-Engineering | Software Engineer - Database Engineering | 骨架页，无正文 | 高（正文见 builtin 镜像） |
| https://careers.snowflake.com/us/en/job/SNCOUS9DCE815D980E4D35B97907BBE70BB19DEXTERNALENUSEB080F6142F24BEC91D39C0466EA5918/Staff-Software-Engineer-Query-Processing-Snowtrail | Staff SWE - Query Processing (Snowtrail) | 骨架页，无正文 | 中（未获正文，未使用其内容） |
| https://careers.snowflake.com/us/en/job/SNCOUSF69D55B7C8D04019ABEE0DDECF8FC2AEEXTERNALENUS74466B259CC84E9BB60B234C539C455C/Software-Engineer | 通用 "Software Engineer" 岗 | 410 | 未使用（未获正文） |
| https://careers.snowflake.com/us/en/database-engineering | Database Engineering 团队介绍（Menlo Park/Bellevue/Berlin） | 200（复用 C §3.1，本次未重新抓取） | 高 |

## 招聘聚合镜像（保留官方 JD 逐字文本的第三方站点）

| URL | 内容 | 可达性 | 可信度 |
|---|---|---|---|
| https://zapply.jobs/jobs/c2382f97-dcee-4d0e-85e7-eb7e8b27562c/ | Software Engineer - Backend（GenSWE），标注 Posted 2026-08-21，**当前在招** | 200 | 高 |
| https://builtin.com/job/software-engineer-backend/4472801 | 同一职位的另一镜像，标 "Reposted One Month Ago"，内容与 zapply 一致 | 200 | 高（交叉核实） |
| https://builtin.com/job/software-engineer-database-engineering/4472390 | Software Engineer - Database Engineering，标注 2026-05-22 移除 | 200 | 高（官方文本快照） |
| https://builtin.com/job/senior-software-engineer-query-processing-snowtrail/4471461 | Senior SWE - Query Processing (SnowTrail)，标注 2025-10-13 移除 | 200 | 高 |
| https://builtin.com/job/software-engineer-backend-apps-collaboration/4588620 | SWE Backend - Apps & Collaboration，标注 2025-05-08 移除 | 200 | 高 |
| https://builtin.com/job/software-engineer-snowtrail/7767539 | Software Engineer - SnowTrail，标注 2026-01-06 移除 | 200 | 高 |
| https://builtin.com/job/software-engineer-billing-platform/4472400 | Software Engineer - Billing Platform，标注 2025-06-03 移除 | 200 | 高 |
| https://haystackapp.io/jobs/458b1230-bd05-4702-921e-049b95bc37bc | Senior SWE, AI Platform for User Experiences | 404 | 未使用 |

## Blind（teamblind.com，浏览器 UA 直连可读正文/摘要）

| URL | 内容 | 可达性 | 可信度 |
|---|---|---|---|
| https://www.teamblind.com/post/snowflake-ic1ic2-system-design-interview-1dd4vqt7 | IC1/IC2 SD：SQL engine as cron job；面试官沉默 | 200 | 高 |
| https://www.teamblind.com/post/snowflake-onsite-tips-wzrlktbi | ex-Google IC2："电面不计分，onsite 每轮要 Hire" | 200（复用 P） | 高 |
| https://www.teamblind.com/post/expertise-round-in-snowflake-3tbrdamq | Expertise 轮问答（2024-02-04，Senior L64） | 200 | 高 |
| https://www.teamblind.com/post/snowflake-expertise-interview-xcavd10l | IC3 Expertise 轮一手报告（40 min 项目深挖） | 200（复用 P） | 高 |
| https://www.teamblind.com/post/passed-all-rounds-at-snowflake-then-silence-z4cg3oq0 | IC1 全轮通过后 team matching 阶段石沉大海 | 200 | 高 |
| https://www.teamblind.com/post/snowflake-interview-rejected-for-no-reason-gsuxeszj | 两轮 coding 后无 onsite 直接拒 | 200（复用 P） | 高 |
| https://www.teamblind.com/post/snowflake-downlevel-txc5g5ub | Down-level 讨论 | 摘要 | 中 |
| https://www.teamblind.com/post/snowflake-swe-intern-fall-2025-team-matching-losing-hope-bkgoqjdw | 实习 team matching 焦虑帖（仅标题确认存在） | 摘要 | 中 |
| https://www.teamblind.com/post/snowflake-system-design-and-leetcode-questions-a83swi3f | SD 与 LC 题目综合帖（仅标题/摘要） | 摘要 | 中 |
| https://www.teamblind.com/post/how-is-gen-swe-interview-at-snowflake-ouhoegc5 | GenSWE 提问帖（复用 P，无回复内容） | 摘要 | 高（帖子存在）/无内容 |
| https://www.teamblind.com/post/snowflake-chakra-ai-wg7wd28k | Chakra AI 讨论（复用 P） | 200（复用 P） | 高 |
| https://www.teamblind.com/company/Snowflake/posts/snowflake-interview | Snowflake 面经列表页 | 摘要 | 中 |

## 1point3acres（正文 403，经 Telegram 镜像 `t.me/s/usinterview?q=snowflake` 或搜索摘要读到）

| URL | 内容 | 可达性 | 可信度 |
|---|---|---|---|
| https://t.me/s/usinterview?q=snowflake | Telegram 镜像搜索，命中 8 条以上 2026 年 Snowflake 面经摘要（本文件主要新证据来源） | 200 | 高（镜像内容为一手面经的转述摘要） |
| https://www.1point3acres.com/bbs/thread-1179343-1-1.html | "Snowflake Store Interview"：两轮 coding，第二轮开场 15 min behavioral | 403，经 Telegram 读摘要 | 高 |
| https://www.1point3acres.com/bbs/thread-1179486-1-1.html | 2026-06 SDE 电面：LC1751 变体 | 403，经 Telegram 读摘要（复用 P） | 高 |
| https://www.1point3acres.com/bbs/thread-1179571-1-1.html | Happy Number + Design user password storage | 403，经 Telegram 读摘要（复用 P） | 高 |
| https://www.1point3acres.com/bbs/thread-1180916-1-1.html | IC2 mid-level onsite：coding+behavioral+SD（Jira ticket automation 系统设计，"very unique"） | 403，经 Telegram 读摘要 | 高 |
| https://www.1point3acres.com/bbs/thread-1181800-1-1.html | AI Screening（HR 类问题，复用 P） | 403，经 Telegram 读摘要（复用 P） | 高 |
| https://www.1point3acres.com/bbs/thread-1185571-1-1.html | "Snowflake OA ai 面试"：20 min BQ+项目（复用 P） | 403，经 Telegram 读摘要（复用 P） | 高 |
| https://www.1point3acres.com/bbs/thread-1185881-1-1.html | Queue class → cloud queue service（复用 P） | 403，经 Telegram 读摘要（复用 P） | 高 |
| https://www.1point3acres.com/bbs/thread-1186357-1-1.html | Fullstack 电面：Kanban 板 coding + SQL notebook SD | 403，经 Telegram 读摘要 | 高 |
| https://www.1point3acres.com/bbs/thread-1186534-1-1.html | HR Screening（Infrastructure Role） | 403，经 Telegram 读摘要 | 高（细节有限） |
| https://www.1point3acres.com/bbs/thread-1187965-1-1.html | 电面两轮 back-to-back：coding + SQL notebook SD（复用 P） | 403，经 Telegram 读摘要（复用 P） | 高 |
| https://www.1point3acres.com/bbs/thread-1188432-1-1.html | IC1 Store Interview：两轮 coding | 403，经 Telegram 读摘要 | 高（细节有限） |
| https://www.1point3acres.com/bbs/thread-1091322-1-1.html | "snowflake system design 大汇总" | 403（直连与经既往镜像均未获正文，复用 P 的失败记录） | medium（复用 P，仅存在性确认） |
| https://www.1point3acres.com/bbs/thread-978440-1-1.html | "雪花店面系統設計" | 403（本次新尝试直连，仍失败） | 未获内容 |
| https://www.1point3acres.com/bbs/thread-1049039-1-1.html | "雪花店面挂经" | 403（本次新尝试直连，仍失败） | 未获内容 |
| https://www.1point3acres.com/interview/problems/company/snowflake | 1p3a 问题库页（144 题），含多个 SD 题标题/摘要 | 200（问题库页可读，区别于论坛帖） | 中 |
| https://www.1point3acres.com/interview/post/7100158 | "Design a Distributed KV Store" | 摘要 | 中 |
| https://www.1point3acres.com/interview/problems/post/7100062 | "Durable Key-Value Store Serialization" | 摘要 | 中 |
| https://www.1point3acres.com/interview/company/snowflake | Snowflake 面经索引（Dynamic Blacklist Filter System 等标题，复用 P） | 摘要（复用 P） | medium |

## 聚合/培训站（不含 lodely/vervecopilot；按可信度分级使用）

| URL | 内容 | 可达性 | 可信度 |
|---|---|---|---|
| https://staffengprep.com/companies/snowflake/ | SD 题族归类：KV store/Quota/Dedup/Scheduler/2PC/Rate Limiter/Event Subscription | 200 | 中（细节具体，与一手题面吻合，上调） |
| https://prachub.com/companies/snowflake/categories/system-design | SD 题库（19+ 条，含做题人数/日期） | 200 | 低-中（AI 题库聚合站，部分题面与一手印证） |
| https://prachub.com/interview-guide/snowflake-software-engineer-interview-guide | 综合面试指南（复用 P） | 200（复用 P） | low-medium |
| https://www.fastprep.io/problems/snowflake-sliding-window-rate-limiter | Sliding-window rate limiter，标注 Snowflake Onsite | 200 | 中 |
| https://www.tryexponent.com/blog/snowflake-interview-process | Snowflake 面试流程综述（含 Senior Tech Talk、Expertise 轮描述） | 200 | 中 |
| https://www.tryexponent.com/guides/snowflake-software-engineer-interview | SWE 面试指南 | 200 | 中 |
| https://spacecomplexity.ai/blog/snowflake-behavioral-interview-questions | 行为面试问题 × 价值观映射（复用 P） | 200（复用 P） | low-medium |
| https://customcareer.miami.edu/blog/2026/05/14/get-a-job-at-snowflake-interview-process-and-top-questions/ | Exponent 博客镜像，行为面试问题列表（复用 P） | 200（复用 P） | medium |
| https://www.systemdesignhandbook.com/guides/snowflake-system-design-interview/ | SD 风格综述（"低级细节/精确分片 key"） | 摘要 | 低-中 |
| https://algo.monster/interview-guides/snowflake | 综合面试指南 | 摘要 | 低-中 |
| https://interviewing.io/snowflake-interview-questions | 综合面试指南 | 摘要 | 中 |
| https://leonstaff.com/blogs/snowflake-interview-process/ | 时间线（电面后 3-5 天，onsite 后 1-2 周，复用 P） | 200（复用 P） | low |
| https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ | OA 题目/SD 题目汇总（复用 P） | 200（复用 P） | low |
| https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic1 | IC1 薪酬 | 200 | 高（数据随时间波动） |
| https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic2 | IC2 薪酬 | 200 | 高（数据随时间波动） |
| https://www.levels.fyi/companies/snowflake/salaries/software-engineer/title/backend-software-engineer | Backend SWE title 薪酬区间 | 200 | 高 |

## 未采信 / 明确排除

- **lodely.com、vervecopilot.com**：本次调研的全部 WebSearch 结果均未出现这两个域名，符合仓库"AI 题目
  农场，一律不采信"的规矩，无需额外过滤动作。
- **Glassdoor**：未在本次检索中主动抓取（P/C 已记录其详情页 403，本文件未重复尝试，直接沿用既有结论）。
- **Medium 个别文章**（如 Snowflake 失败复盘文 `medium.com/@workwithalam/...`）：出现在搜索结果标题中但
  本次未展开抓取正文，未纳入引用，仅记录标题供后续人工判断是否值得补采：
  https://medium.com/@workwithalam/%EF%B8%8F-the-snowflake-interview-that-i-failed-and-made-me-a-better-engineer-3de0f8097156

## 复用来源（原采集日期同为 2026-09-13，来自本仓库既有文件，未重新抓取）

以下 URL 在 `../../raw/process_research.md` 与 `../../raw/company_research.md` 中已有完整记录，本次
三份新文件中引用时均标注"复用 P/C"，此处不重复列出可达性/可信度（详见原文件）：Ashby/HackerRank 邮件相
关背景、Chakra 官方页面（chakra.sh / YC launch / hackerrank.com 说明）、8 条官方价值观 PDF、levels.fyi
早期职业 offer 明细、Snowflake 工程博客（Execution Anchor / FoundationDB / Dynamic Tables 等）。
