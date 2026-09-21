# 01 · 公司与项目简报（Millennium · LEaD Program · Miami）

> 全部数字与引语的出处在 `catalog/raw/official_lead.md`；未标来源的句子是推断并已注明。

## 1. Millennium 是什么（60 s 口径）

- **多策略、多经理（multi-manager / pod）对冲基金**，1989 年 Israel "Izzy" Englander 创立，纽约总部，AUM 约 **$79B**（LinkedIn 公司页 2026）。几百个独立交易团队（pod）各自做策略，公司层面做**统一的风险管理、基础设施与技术平台**——技术团队既服务 pod（前台）也服务中后台。
- 技术组织（官方技术页头衔推断的四条线）：**Core Technology**（固收/商品线下）· **Shared Services Technology**（股票/量化线下）· **Miami 技术中心**（Head of Technology, Miami：Olga Naumovich，ex-Goldman CDO）· 企业技术（DevOps/QA/支持）。**"四个技术分部"官方没有点名**——反问时可以直接问这个。
- 技术栈（一手）：C++（低延迟、交易基础设施）· **Java**（Miami equities algo）· **Python**（研究、数据、AI）· kdb+/q（行情）· Kafka · Terraform/K8s · 云（AWS/GCP）· "proprietary AI infrastructure and agentic tools"，日处理 900K+ 数据文件（技术页）。
- 文化关键词（官方 + 一手）：**autonomy、personal accountability、"choose the tools that suit the challenge"**、快、卷（1p3a 1158922）。

## 2. LEaD = Learning Engineering and Data

| 项 | 事实 | 来源 |
|---|---|---|
| 定位 | Miami 早期职业 SWE 加速项目，"intersection of finance and technology" | 官方 |
| 门槛 | **2+ 年经验**（JD：2–5 年）；C++/Python/Java 任一 | 官方 / JD |
| 时长 | **12–18 个月轮岗**，cohort 制（2023-04 启动，2025 夏第 5 期） | JD / 官方文章 |
| 内容 | 与技术 leadership、mentor 做跨团队高影响项目 + 硬/软技能课程；结束时进四个技术分部之一 | 官方 |
| 业务面 | "applications and tools spanning **front-office, middle-office and back-office** functions" | JD |
| 技术面（新版 JD） | backend distributed systems + **AI/ML（deep learning、NLP、LLM）解决业务问题**；Pandas/NumPy；FastAPI/Boost/Spring Boot；优先 LLM 产品经验、ML/data pipeline、messaging、Docker/K8s、AWS/GCP、SQL/NoSQL | JD（jobright 镜像） |
| 负责人 | Steve Johnson（Head of LEaD；ex-Citadel 前台技术总监；曾任 Millennium 风险技术 & 组合可视化负责人） | 官方 |
| 薪酬 | Miami 轮岗 new-grad offer 一例 ≈ $210K TC（Blind）；levels.fyi Miami SWE 中位 $209K；全现金 | 中 |
| 规模 | Miami 技术人员 ~200（2023）；LEaD cohort 人数未公开 | 媒体 |

**Steve Johnson 给 LEaD 候选人的五条**（官方）：每天读一篇市场文章 · 啃一本金融技术书 · **用 Python 写并回测一个简单交易策略** · 用 ChatGPT 学市场 · 保持好奇多问。→ Chi 的 **Quant-Stroller** 正是第 3 条的完整版：这是 R1 项目段的首选。

## 3. 为什么 Chi 能进这个通道而不是其它四个 req

- SWE ×2 / Cloud / Infra&Data 四个 req 都是**具体团队的社招岗**，简历筛看"对口年限 + 栈"，1.5 YOE 直接被批处理拒。
- LEaD 明写 **2–5 YOE + 想学金融技术 + AI/ML/LLM 优先**：简历上 Quant-Stroller（回测、DuckDB、PyTorch、FastAPI）、AikiCard/Aiki（OpenAI API 产品）、PayPal（Snowflake/PostgreSQL、$600B+ 管线、on-call）三块都命中。**面试里要把这三块和 JD 的词一一对上**（见 `fit.md`）。

## 4. 对 Chi 的风险点（诚实）

1. **1.5 年 vs "2+ 年"**：JD 写 2–5 年；实习 4 个月可以算进"经验"但要说清。回答 "how many years" 时说 "about a year and a half full-time at PayPal plus a summer internship there — two years of production work on the same payments platform"。
2. **Java/C++ 只是简历列表**：Miami 有 Java 团队；口头 Java 基础（HashMap、集合、并发原语）要能答；C++ 不主动提。
3. **金融知识**：LEaD 看 "interest in finance"，不考定价公式；但要能讲清 Quant-Stroller 里的 Sharpe / 交易成本 / 因子风险这几个词是什么意思（`study/20-cards/finance_vocab.md`）。
4. **Onsite Miami**：JD 写 Onsite；relocation 意愿要直接说 yes。
