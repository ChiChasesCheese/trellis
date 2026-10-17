# GitHub 先行检索（2026-10-15）

方法：`gh api -X GET search/repositories`（12 组查询：amazon sde 1 interview / amazon new grad loop / amazon sde new grad interview experience /
amazon leadership principles stories / amazon leadership principles interview STAR / amazon onsite interview questions / amazon interview questions
list leetcode / aws sde interview / amazon sde1 onsite 2025 / amazon bar raiser / amazon OOD low level design interview / amazon interview experience 2025）
+ `search/code`（"amazon new grad onsite loop"、"SDE1 amazon loop bar raiser"、"亚麻 面经 system design AWS SDE2"、
"Amazon AWS SDE2 system design DynamoDB interview"、"amazon system design interview S3 design key-value store AWS onsite"）。
`search/code` 对长查询多次 503 "too many shards failed"，用短查询重试。

结论先行：**GitHub 上没有一个 star 过百的 Amazon SDE I 面经仓库**。最高的 `kianis4/AmazonPrep`（47 star）是通用备考指南。
真正有价值的一手信息来自三类：(a) 汇总 Reddit/LeetCode Discuss 的聚合仓库（`kevin3010/FAANGQuestionsOnReddit`、`jugaldb/faang-interview-prep`、
`atomeocean/job-compass`）；(b) 个人博客/仓库里的单篇面经（`jenishk20/personal-site`）；(c) 一份把 1point3acres/LeetCode 面经翻成中文的站点源码（`job-compass`）。

## 1. 可用度高（含 2025-2026 具体面经，URL 可回溯）

| 仓库 / 文件 | 内容 | 日期 | 可信度 | 备注 |
|---|---|---|---|---|
| `kevin3010/FAANGQuestionsOnReddit` -> `Amazon/README.md`、`Amazon/LP/README.md` | 把 r/leetcode 的 Amazon 帖按日期汇总，每条带 Reddit 原帖链接；覆盖 2025-04-20 ... 2025-07-24，共 54 个日期块（脚本计数）（SDE1/SDE2/L5） | 2025-04..07 | high（原帖链接齐全） | https://github.com/kevin3010/FAANGQuestionsOnReddit/blob/main/Amazon/README.md ；Reddit 本身 403，全靠这个聚合 |
| `jugaldb/faang-interview-prep` -> `docs/companies/amazon.md` | "Updated October 2026"；新毕业 loop 结构（OA 70+15+60+5 分钟；loop 3-4 轮；常见 2026 四轮=1-2 DSA + 1 LLD + 1 HM(GenAI 讨论 up to 30 分钟 + DSA) + 1 BR）；"Reported in 2025 to 2026 interviews" 表，每条带 LeetCode Discuss 帖链接 | 2026-10 | high（我回抓并核对了其中 8 条原帖（8520348, 8535500, 8500377, 7584467, 8293563, 8471051, 7578011, 8468910），一致） | https://github.com/jugaldb/faang-interview-prep/blob/main/docs/companies/amazon.md 。注：其中 "L4 design interview covers object oriented design instead of large scale systems" 引自 Hello Interview（二手） |
| `atomeocean/job-compass` -> `docs/zhHans/interview-experience/amazon/*.md`（顶层 15 个 + onsite/ 2 个 + online-assessment/ 2 个，另有 index） | 中文面经站点的源码；每篇有 `ReferenceSource` 指向 1point3acres / LeetCode / 小红书原帖 | 2025-10..2026-10 | medium-high（有来源帖，但转述过） | https://github.com/atomeocean/job-compass/tree/main/docs/zhHans/interview-experience/amazon ；1point3acres 原帖自身需登录（Cloudflare），此处是唯一可读的镜像 |
| `jenishk20/personal-site` -> `src/content/writing/four-rounds-at-amazon-seattle-hq.md` | AWS S3 Glacier SDE1 Seattle 现场，4 轮（BR 全 LP；GenAI+滑窗；LP+括号匹配栈；LP+Rate limiter LLD in C++），2026-08，拒。同内容在 LeetCode Discuss 8535500 | 2026-09-22 | high（当事人自述，双平台） | https://github.com/jenishk20/personal-site/blob/main/src/content/writing/four-rounds-at-amazon-seattle-hq.md |
| `ombharatiya/FAANG-Coding-Interview-Questions` -> `FAANG-Recent-Questions.md` | "Last updated October 2026"；声明 "AI-assisted repository debugging now appears in the SDE OA for some roles and regions ... Live coding rounds still ban AI" | 2026-10 | medium（二手聚合，Amazon 段落按主题列题，无 loop 结构） | https://github.com/ombharatiya/FAANG-Coding-Interview-Questions/blob/main/FAANG-Recent-Questions.md |
| `ombharatiya/AI-Engineer-Interview-Questions` -> `14-company-interview-questions/amazon.md` | Amazon AWS/AGI AI engineer 视角；"System design is at genuine extreme scale: multi-tenancy, throttling, cell-based isolation, and operational excellence are native vocabulary" | 2026-10 | low-medium（AI 工程岗，不是 SDE I；仅作 AWS 设计语言参考） | https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/14-company-interview-questions/amazon.md |
| `nem0z/amazon-loop` | AWS Dublin SDE1 面试题：实现 "top K most bought product"，bonus 只统计最近一小时 | 2024-11-16 | medium（仓库自述；超出 2025-01 窗口） | https://github.com/nem0z/amazon-loop |

## 2. 通用/低可信（读过，不引用事实）

| 仓库 | 判断 |
|---|---|
| `kianis4/AmazonPrep`（47 star，2025-01-11） | 目录：Amazon Leetcode Questions / Behavioural Prep / Leadership Principles / Phone Interview Prep / Technical Prep。通用备考笔记，无近期 loop 事实 |
| `dlgi71/amazon-interview-prep`（2026-10-10） | SEO 型长文，OA1 "debugging and logical reasoning" 描述是旧版 OA（与 2026 的 AI-assisted repo debugging 不符）。不引用 |
| `mhemanthsai-dev/amazon-sde-preparation`、`Unseencoderz/SDE-1-Interview-Master-Sheet`、`kidskoding/faang-dsa`、`serdardoruk/Amazon-Online-Assessment-Python-Solutions`（2020） | 题单/解法，无 loop 结构信息 |
| `wanyingng/alyssa`、`andresgars92/amazon-loop-simulator`、`geledek/ace-the-amazon-interview`、`bballdave025/star-capsules-agi` | LP/STAR 辅导工具，AI 工具，不含面经 |
| `gauravpatil97886/GoForge` -> `interview-prep/company-amazon.md` | "Expect 2-3 LP questions per round, taking 20-25 minutes of each hour"；"system design (x1, SDE2+)"；无引用来源，当作通用说法 |
| `kitahara-saneyuki/LCPython` -> `amazon_onsite.md`、`ZhiyongJing/algorithm`、`lingduoduo/Leetcode` | 2019-2022 年旧面经，窗口外 |
| `humancto/interview-buddy-hub`、`sreenu-dev/Resume`、`urmzd/openlearn` 等 | 生成式/模板内容，不引用 |

## 3. 用到的辅助源（GitHub 找到，内容实际在别处）

- 聚合仓库给出的 LeetCode Discuss 帖子 -> 通过 LeetCode GraphQL（`ugcArticleDiscussionArticle(topicId)`）和 `r.jina.ai` 取全文，见 forums.md。
- `job-compass` 给出的 1point3acres 帖子 ID（thread-1184612、thread-1182648、thread-1182406、thread-1182063、thread-1191311、thread-1181449、thread-1184465、thread-1182725）-> 直接抓 1point3acres 返回 Cloudflare "Just a moment" / "Please log in"（2026-10-15）；`m.1point3acres.com` 被 r.jina.ai 拒（422 domain），web.archive.org 匿名 403。**只能经 job-compass 镜像读**。

## 4. 空白（GitHub 没有的）

- 没有任何 GitHub 仓库按 "AWS Data Services / RDS / Aurora / DynamoDB / Redshift / Glue / EMR / Kinesis / OpenSearch / Lake Formation 团队" 汇总面试题。
  `search/code` 对 "Amazon AWS SDE2 system design DynamoDB interview" 只回通用 prep 仓库；对团队名检索 LeetCode Discuss 也只得到零散帖（见 forums.md §AWS 数据团队）。
- 没有仓库发布过 SDE I 的 "no system design" 官方依据；该说法只出现在候选人帖（见 forums.md 回答节）。
