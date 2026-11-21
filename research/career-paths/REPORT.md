# 2026 工程方向调研：从后端 + 数据 + 测试发布出发，往哪里走

调研日期 2026-11-20。读者是一位资深路线的后端 / 数据 / 测试发布工程师，不想困在单一行业，也不想停在「可能被 AI 改写的普通后端」。
四个筛选条件：(a) 需求在增长；(b) 不容易被 AI 自动化；(c) 6–18 个月内从现有背景可达；(d) 能跨行业迁移。
规则：每个数字带 URL；找不到来源的不写。来源强弱会标注（一手 = 统计机构或论文；二手 = 媒体转述或招聘/咨询厂商）。

## 0. 先看总体：劳动力市场到底在发生什么

| 事实 | 数字 | 来源 |
|---|---|---|
| 美国软件开发岗位（含 QA）2025–35 预测增长 | 10%（全职业平均 3%）；BLS 把需求增长归因于 AI 软件开发、物联网、机器人等 | https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm |
| 软件开发招聘帖，自 2025-02 底 Claude Code 发布以来 | 约 +15%，同期美国总招聘帖 −7%；2025-05 到 2026-05 的增量中 71% 是资深岗位，37% 标题带 AI；但仍比 2020-02 低 27.5% | https://hiringlab.indeed.com/?p=20708 （Indeed Hiring Lab，2026-07-08） |
| 22–25 岁软件开发者就业 | AI Index 2026：自 2024 年起下降近 20%，年长同行人数在增长 | https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report |
| 高 AI 暴露职业里的年轻人 | 斯坦福数字经济实验室 2026-08 更新：「无普遍替代，但年轻人的 AI 就业缺口扩大到 19%」；作者强调这是描述性指标，不是因果估计，机制是少招年轻人而非裁人 | https://digitaleconomy.stanford.edu/news/canariesaug26/ |
| Anthropic 的「观察到的暴露度」 | 计算机程序员覆盖率 75%，居首；整个计算机与数学类别仅 33%；自 2022 末以来高暴露职业失业率没有系统性上升，25 岁以上无类似招聘下降 | https://www.anthropic.com/research/labor-market-impacts |
| Claude Code 对话中「自动化」占比 | 79%（Claude.ai 为 49%），2025-04 数据 | https://www.anthropic.com/research/impact-software-development |
| 开发者对 AI 输出的信任 | 46% 不信任准确性，33% 信任；87% 担心 agent 输出准确性 | https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/ |
| 经验丰富的开源开发者用 AI 工具（早期 2025 模型） | 随机对照：完成时间多 19%，而他们自己估计快 20%；作者明确说不代表所有场景 | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ |
| WEF 2025 | 2030 年前创造 1.7 亿岗位、取代 9200 万，净增 7800 万；增长最快的职位含大数据专家、金融科技工程师、AI/ML 专家、软件与应用开发者 | https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/ （数字取自搜索摘要，该页抓取被 403，未逐字核对） |

读法：整体不是「软件岗位消失」，而是**入门岗位收缩、资深岗位与 AI 相关岗位扩张**；纯写代码这一步被自动化得最快（编码类任务暴露度最高）。所以抗 AI 的判断标准应是：**越靠近「判断、验证、运行、责任」越稳，越靠近「把需求写成代码」越不稳。**

## 1. 候选方向（11 个）

评分约定：需求（D）、抗自动化（R）、可达性（C）、跨行业（T），各以 高/中/低 给出，是我的判断，依据列在条目中。

### 1.1 AI 基础设施 / ML 平台（训练与推理平台、调度、数据与特征管道）

- **需求证据**：CNCF 2025 年调查（628 名受访者，2025-09）：82% 的容器用户在生产运行 Kubernetes，2023 年为 66%；66% 的 AI 采用者用它扩展推理负载。https://www.cncf.io/announcements/2026/01/20/kubernetes-established-as-the-de-facto-operating-system-for-ai-as-production-use-hits-82-in-2025-cncf-annual-cloud-native-survey/ 。Dice 10 月报告点名 ML 运维工程师与 ML 数据工程师为突出群体（无增速数字，二手）：https://www.dice.com/hiring/?p=999887277 。Veritone：2026 Q2 AI 岗位 +21.3% 至 69,539 个，AI/ML 工程师 22,056 个居首（二手招聘厂商）：https://www.veritone.com/blog/ai-job-market-q2-2026-hiring-trends/
- **AI 暴露**：偏低。工作是运行系统、容量与故障，而不是生成代码；但「按文档写配置」这类部分会被辅助。（判断；无直接测量数据）
- **技能桥**：后端服务 → 调度与资源模型（Kubernetes、队列）；数据管道 → 特征/数据平台；测试发布 → 灰度、回滚、集群升级。
- **先学**：容器与 Kubernetes 原理 → GPU 调度与批量调度 → 模型服务的伸缩与冷启动 → 成本。
- **trellis 现有领域**：`system-design`、`sysdesign`、`llm-inference`、`ml-system-design`、`kafka`、`snowflake`；拟建 `k8s`（本次大纲 `research/domains/k8s/outline.md`）。
- 评分：D 高、R 中高、C 高、T 高。

### 1.2 LLM 推理与 GPU 服务（inference engineering）

- **需求证据**：证据偏弱。岗位真实存在，要求 vLLM / SGLang / TensorRT-LLM、量化、投机解码、KV cache 管理；有标价的例子是 GPU 推理工程师岗 $184k–$287.5k（NVIDIA 岗位页，2026-07）：https://jobs.anitab.org/companies/nvidia/jobs/87705160-senior-inference-engineer-gpu-kernel-optimization 。「最难招」之说来自招聘工具厂商，且没有独立的岗位量时间序列：https://www.herohunt.ai/blog/how-to-recruit-ai-inference-engineers-2026-guide/ 。**我没找到可靠的增速数字，不下增长结论。**
- **AI 暴露**：低到中。性能优化依赖硬件与测量，但内核编写本身正被 AI 辅助。（判断）
- **技能桥**：后端延迟与容量 → 吞吐/尾延迟模型；数据 → 批处理与内存带宽直觉。门槛高：偏 C++/CUDA 与系统。
- **先学**：LLM 推理基础（prefill/decode、KV cache、连续批处理）→ 指标与基准 → 量化与并行；GPU 内核是 18 个月之外的目标。
- **trellis**：`llm-inference`（核心）、`cerebras`、`under-the-hood`、`ml-system-design`。
- 评分：D 中（证据弱）、R 高、C 中低（硬件/CUDA 门槛）、T 高。

### 1.3 AI 应用 / agent 工程

- **需求证据**：LinkedIn 2026 Jobs on the Rise：AI 工程师是美国增长最快职位，连续第二年第一；常见技能 LangChain、RAG、PyTorch：https://www.dice.com/career-advice/ai-related-jobs-top-linkedins-fastest-growing-roles-list-for-2026 ，另见 https://e.vnexpress.net/news/tech/tech-news/ai-roles-dominate-fastest-growing-jobs-in-us-5004966.html 。DataCamp：2024-01 到 2026-04 的约 200 万条去重岗位里，AI 工程师 +255%，生成式 AI 工程师 +197%：https://www.datacamp.com/resources/whitepapers/state-of-ai-careers-2026 。Levels.fyi：AI 薪酬溢价已停止增长，L3 约 1.34 倍（2024 末）降到约 1.29 倍（2026 中），样本小：https://letsdatascience.com/news/levelsfyi-tells-lds-the-ai-pay-premium-has-stopped-growing-a893d96e
- **AI 暴露**：**高**。这是最接近「被 AI 改写」的方向：门槛在降低，别人的编码 agent 也在写这类应用。竞争会随之拥挤（这是我的推断；没有直接数据）。
- **技能桥**：后端 + API 设计几乎直接可用；数据管道 → RAG 数据层。
- **先学**：LLM 基础 → 检索与评测 → 工具调用与状态管理。
- **trellis**：`ai-literacy`、`ml-system-design`、`system-design`（LLM Chat Service 题）、`python`。
- 评分：D 高、R 低中、C 高（最快）、T 高。**适合当作「附加技能」，而不是唯一定位。**

### 1.4 评测与 AI 可靠性（evals, AI reliability）

- **需求证据**：**没有找到专门追踪该岗位的数据**。能确认的只有它作为职责出现在描述中（构建测试以判定模型是否可靠）：https://www.pymnts.com/?p=3961580 。Dice 报告称「负责任 AI」技能同比增长 495%（二手摘要，指技能出现次数而非岗位）：https://www.hrdive.com/news/dice-report-tech-hiring-AI/824902/ 。
- **AI 暴露**：低到中。判定「对不对、够不够好」要领域判断与责任；但评测里的「用 LLM 打分」部分自身在自动化。
- **技能桥**：**这是现有背景最强的桥**：测试设计、回归、基线、统计、发布门禁 → 评测集、漂移监控、上线闸门。
- **先学**：评测方法学（数据集构造、指标、LLM-as-judge 的偏差）→ 线上监控 → 红队。
- **trellis**：`test-release`、`ai-literacy`、`ml-system-design`、`llm-inference`（指标与正确性）。
- 评分：D 中（证据缺）、R 中高、C 高、T 高。

### 1.5 平台工程 / 开发者效率（platform engineering, developer productivity）

- **需求证据**：DORA 2025（近 5000 名受访者，2025-06–07）：平台采用接近普及（Google 公告写 90%，报告摘要写 94%，两者不一致，原因未查清）；InfoQ 转述 76% 有专职平台团队；报告称高质量内部平台与 AI 收益直接相关：https://blog.google/technology/developers/dora-report-2025/ ，https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025 。Gartner 预测（2023）：到 2026 年 80% 的软件工程组织建立平台团队，2024 年措辞改为「大型组织」：https://www.gartner.com/en/newsroom/press-releases/2023-11-28-gartner-hype-cycle-shows-ai-practices-and-platform-engineering-will-reach-mainstream-adoption-in-software-engineering-in-two-to-five-years 。预测不是观测，只作参考。
- **AI 暴露**：中。模板与脚手架会被自动化，但「决定组织的黄金路径和约束」是判断工作。
- **技能桥**：后端 + CI/CD + 发布 → 内部平台；测试发布经验直接对应交付流水线。
- **先学**：Kubernetes 与 GitOps → 策略即代码 → 可观测性（OpenTelemetry）→ 度量（DORA）。
- **trellis**：`test-release`、`cdn-content`（交付、金丝雀）、`system-design`（基础设施）、拟建 `k8s`。
- 评分：D 中高、R 中、C 高、T 高。

### 1.6 SRE / 可靠性工程

- **需求证据**：弱。没有找到权威 2026 年度调查；多数是职业博客与厂商文章，信号是「稳定、工作内容在变」，常规事件响应正在被自动化：https://www.careerexplorer.com/careers/site-reliability-engineer/ai-impact/ （二手）。**不引用任何增速数字。**
- **AI 暴露**：中。AIOps 减少「每个系统所需人数」，但复杂系统增多；责任与取舍难外包。
- **技能桥**：后端 + 发布经验 + 事故复盘。
- **先学**：SLO 与错误预算、容量、事故管理、Linux 与网络排错、Kubernetes 故障模式。
- **trellis**：`system-design`（可靠性）、`sysdesign`（Linux 排错）、`test-release`、拟建 `k8s`（事故章节）。
- 评分：D 中、R 中、C 高、T 高。

### 1.7 AI 数据基础设施（数据平台、流处理、向量/特征存储、数据质量）

- **需求证据**：WEF 把大数据专家列入增长最快职位（见 §0，摘要来源）；Dice 点名 ML 数据工程师为突出群体（无数字，二手）。BLS 的数据库管理员与架构师类别 2025–35 仅 +4%，其中数据库架构师 +9%、管理员 0%：https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm —— 说明传统 DBA 不增长，增长在架构与平台一侧。
- **AI 暴露**：中。管道代码会被辅助，数据建模、质量与治理更稳。
- **技能桥**：数据管道经验直接延伸；侧重「面向模型的数据」。
- **先学**：流批一体、数据质量与血缘、向量检索、成本。
- **trellis**：`kafka`、`snowflake`、`ml-system-design`、`under-the-hood`。
- 评分：D 中高、R 中、C 高、T 高。

### 1.8 安全工程（含 AI 安全）

- **需求证据**：BLS 信息安全分析师 2025–35 +21%，中位年薪 $129,180，年均约 14,100 个岗位空缺：https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm 。ISC2 2025（16,029 受访者）：41% 认为 AI 是关键技能，云安全 36%；88% 经历过技能短缺造成的重大后果；ISC2 没有发布全球缺口数字：https://www.isc2.org/Insights/2025/12/ISC2-publishes-2025-cybersecurity-workforce-study 。**反向信号**：CyberSN 统计 2026-01 至 09 美国安全岗位帖 235,786 条，同比 −26.4%，安全工程师岗 −32.3%，但 AI 安全工程师帖 2,409 条（+268.3%，约占总数 1%）：https://www.esecurityplanet.com/cybersecurity/news-us-cybersecurity-job-postings-decline-ai-roles/ 。Glassdoor 称 2026 Q1 安全岗位 +11%（经 Gizmodo 转述，与上面冲突，数据源不同）。SANS 追踪：近 100 个 AI 红队岗位、约 430 个 AI 治理合规岗位：https://www.cybersecuritydive.com/news/ai-security-jobs-hiring-sans-tracker/833465/
- **AI 暴露**：中；攻防双方都在用 AI，判断与责任不外包。
- **技能桥**：后端与测试 → 应用安全、供应链安全；发布经验 → 安全门禁。
- **先学**：应用与云安全基础、Kubernetes 安全（CKS 课纲）、供应链（SBOM/签名）、LLM 应用威胁模型。
- **trellis**：`system-design`（安全章节）、`test-release`、拟建 `k8s`（安全章节）；目前无专门安全领域。
- 评分：D 中（总量下降、AI 子方向上升）、R 中高、C 中、T 高。

### 1.9 分布式数据库 / 存储引擎

- **需求证据**：**没有找到按岗位的增长数据**（BLS 的数据库类别见 1.7 只能当旁证）。不下增长结论。
- **AI 暴露**：低。正确性、一致性与性能的底层工作。（判断）
- **技能桥**：后端 + 数据 → 事务、索引、复制；门槛是系统编程与大量深度阅读，18 个月内转成引擎开发者的难度高；更现实的是「懂内部机制的使用者/平台工程师」。
- **先学**：存储引擎（LSM / B 树）、复制与共识、事务隔离。
- **trellis**：`under-the-hood`、`snowflake`、`kafka`、`sysdesign`。
- 评分：D 不明、R 高、C 低中、T 高。

### 1.10 边缘 / 嵌入式 / 机器人软件

- **需求证据**：BLS 软件开发页只泛泛提到机器人、物联网是需求驱动因素；**没有找到该子方向的岗位量数据**。
- **AI 暴露**：低到中（物理世界、硬件在环调试难以自动化，这一条是判断）。
- **技能桥**：从纯后端转入较远：需要 C/C++/Rust、实时与硬件知识。测试经验可迁移到硬件在环测试。
- **先学**：不建议作为 6–18 个月的目标；若有兴趣，先做仿真与测试方向。
- **trellis**：无直接领域；`code-core`、`low-level-design` 有一点帮助。
- 评分：D 不明、R 高、C 低、T 中。

### 1.11 AI 系统的测试与发布 / 质量

- **需求证据**：BLS 把软件 QA 分析师与测试员放在软件开发页，该职业中位年薪 $104,300（低于开发者 $135,980），页面没有单独给出 QA 的增长百分比：https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm 。传统「手工/脚本测试」暴露度高；与 1.4 同源的「AI 系统质量与发布门禁」是升级方向。
- **AI 暴露**：传统测试高；「为非确定性系统设计验证与发布策略」中。
- **技能桥**：直接。把测试发布升级为评测 + 渐进发布 + 回滚 + 线上监控。
- **先学**：非确定性系统的测试方法、评测集、灰度与影子流量、事故复盘。
- **trellis**：`test-release`（核心）、`cerebras`、`cdn-content`。
- 评分：D 中、R 中、C 最高、T 高。**与 1.4 合并成一条路线更合理。**

## 2. 汇总表

| 方向 | 需求 | 抗自动化 | 6–18 月可达 | 跨行业 | 证据强度 |
|---|---|---|---|---|---|
| 1.1 AI 基础设施 / ML 平台 | 高 | 中高 | 高 | 高 | 中（CNCF 一手；岗位增速二手） |
| 1.2 推理与 GPU 服务 | 中 | 高 | 中低 | 高 | 弱 |
| 1.3 AI 应用 / agent | 高 | 低中 | 高 | 高 | 中（LinkedIn、DataCamp；但竞争证据缺） |
| 1.4 评测与 AI 可靠性 | 中 | 中高 | 高 | 高 | 弱（无专项数据） |
| 1.5 平台工程 | 中高 | 中 | 高 | 高 | 中（DORA 一手） |
| 1.6 SRE | 中 | 中 | 高 | 高 | 弱 |
| 1.7 AI 数据基础设施 | 中高 | 中 | 高 | 高 | 中 |
| 1.8 安全（含 AI 安全） | 中 | 中高 | 中 | 高 | 中（BLS、ISC2 一手；岗位量有冲突） |
| 1.9 分布式数据库 / 存储 | 不明 | 高 | 低中 | 高 | 弱 |
| 1.10 边缘 / 机器人 | 不明 | 高 | 低 | 中 | 弱 |
| 1.11 AI 系统测试发布 | 中 | 中 | 最高 | 高 | 弱 |

## 3. 推荐排序（Top 4）

1. **AI 基础设施与推理平台（1.1，把 1.2 作为深入选项）。** 理由：唯一同时有一手需求数据（CNCF 82% 生产使用、AI 推理负载占多数）和可达性高的方向；工作靠近「运行与责任」，离「写代码」远；Kubernetes 与调度知识跨行业可迁移。先建 `k8s` 领域，再接 `llm-inference`。
2. **评测、测试发布与 AI 系统质量（1.4 + 1.11 合并）。** 理由：这是现有背景的最短桥，6 个月内能做出东西；风险是需求数据缺失，需要用面试与岗位描述自行验证。可与第 1 条并行：「会运行 AI 系统，又会证明它可靠」。
3. **平台工程 / 可靠性（1.5 + 1.6）。** 理由：DORA 一手数据显示平台采用近乎普及，且与 AI 收益相关；同一份 Kubernetes、GitOps、可观测性知识服务它。风险：SRE 一侧的增长证据弱，常规事件响应在自动化。
4. **AI 安全 / 供应链安全（1.8 的子集），或 AI 应用工程（1.3）二选一。** 安全：总岗位下降而 AI 安全岗从小基数高速增长，抗自动化好，但可达性中等。AI 应用：最快上手、需求最高，但抗自动化最弱，只建议作为叠加技能。

## 4. 诚实的不确定性

- **岗位增速多为二手**：Dice、Veritone、CyberSN、DataCamp、LinkUp 都是厂商或媒体转述的统计，口径、数据源不同，且彼此矛盾（如安全岗位 CyberSN −26.4% 对 Glassdoor +11%）。
- **「AI 岗位 +100%」多是从小基数起算**（如 AI 安全工程师帖约占总帖 1%）；增速不等于机会量。
- **AI 暴露度的测量目前基于任务覆盖率，不是实际失业**：Anthropic 自己写明自 2022 末以来高暴露职业失业没有系统性上升；斯坦福的 19% 是描述性、不是因果，机制是少招年轻人。对资深者的直接冲击证据很少，AI Index 反而显示年长开发者人数在增长（斯坦福数字经济实验室 / AI Index，见 §0）。
- **METR 结果来自 2025 初的模型，且只有 16 名开发者、246 个任务**：不要外推到现在的 agent 工具。
- **推理工程、分布式数据库、机器人三项没有找到可靠需求数据**，评分只能是判断。
- **薪酬数据**（Levels.fyi 的 AI 溢价）样本小、媒体转述，只作方向。
- **没有找到**：LinkedIn 或 Indeed 的细分岗位（评测工程师、ML 平台工程师）招聘量；Stanford AI Index 劳动章节里软件开发岗位量的原始数字（只看到摘要）；WEF 报告的各职位百分比增速（页面 403）。
- **可达性是按「通用后端 + 数据 + 测试发布」背景的判断，不是数据**；6–18 个月是否足够，取决于每周投入与是否有实战项目。

## 5. 与 trellis 的对应与下一步

- 新建 `k8s`（本次已出大纲）直接服务第 1、3 条；`test-release` + `llm-inference` + `ai-literacy` 服务第 2 条。
- 目前没有专门的安全领域与平台工程领域；若选第 3/4 条，评审后再决定是否单独建。
- 建议核实顺序：先用目标岗位的真实 JD（20 份左右）做一次技能频次统计，比继续读二手报告更有价值。
