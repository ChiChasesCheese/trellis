# 官方来源：LEaD 项目、JD、Miami 技术组织、官方面试建议

> 采集日期：2026-09-21。方法：WebFetch/WebSearch。**[高]** = mlp.com 官方页 / 官方 JD 镜像逐字；**[中]** = 媒体（efinancialcareers）；**[低]** = SEO 站。

## 1. LEaD = Learning Engineering and Data（官方页）

- 官方定义：**"provides early career software engineers with the opportunity to accelerate their career growth at the intersection of finance and technology in Miami. Software engineers with 2+ years of experience who are interested in learning about technology in finance and the various parts of Millennium's business are invited to apply."** — https://www.mlp.com/life-at-millennium/millenniums-learning-engineering-and-data-lead-program/ **[高]**
- 结构：**"LEaD engineers work alongside technology leadership and mentors on high impact projects that span various teams and technical fields, and also participate in a robust training curriculum focused on developing both hard and soft skills. At the end of the program, LEaD engineers transition into one of Millennium's four technology divisions."**（同上）**[高]**
- 时长：**12–18 个月轮岗**（"an enriching 12-18 month rotational program aimed at accelerating the growth of early career software engineers based in Miami"，LinkedIn 公司帖 + JD 镜像；官方项目页本身没写月数）**[高，JD 原文]**
- 历史："Since its launch in **April 2023** … LEaD's new entrants are grouped into **cohorts** … first cohort began completing the program in **Summer 2024** … preparing to welcome **5th cohort in Summer 2025**"；已扩展出 **LEaD interns**（跟随在岗 LEaD 工程师的轮岗、课堂式学习）；LEaD 工程师带实习生练 people management。— https://www.mlp.com/life-at-millennium/2-years-later-unlocking-potential-with-lead-millenniums-learning-engineering-and-data-program/（2025-05）**[高]**
- 负责人：**Steve Johnson, Head of LEaD**（此前 Head of Risk Technology & Portfolio Visualization；2018-02 从 Citadel 加入，前 Director of Front Office Technology）。引语："our LEaD engineers engage directly with technology leaders on high-impact projects while honing both technical and leadership skills." **[高]**
- Steve 的 "Level Up Your Financial IQ"（https://www.mlp.com/life-at-millennium/level-up-your-financial-iq-with-steve/）给 LEaD 候选人的 5 条：① 每天读一篇金融市场文章 ② 啃一本金融技术书 ③ **用 Python 写并回测一个简单交易策略** ④ 用 ChatGPT 学市场与策略 ⑤ 保持好奇、多问。**[高]** → Chi 的 Quant-Stroller 恰好是第 ③ 条的放大版，是最贴合 LEaD 口径的项目。
- 参与者引语：Shreya Gupta Sharma："LEaD at Millennium has given me insight into a range of departments…"；另一位："There is such a diverse set of technologies that people are using. Each team has their own varied use cases." **[高]**
- **"four technology divisions" 官方没有点名。** 技术页只给出领导头衔：Global Head of Fixed Income, Commodities and **Core Technology**；Global Head of Equities, Quantitative Strategies and **Shared Services Technology**；**Head of Technology, Miami**；CIO Vlad Torgovnik。— https://www.mlp.com/people/technology/ **[高]**（分部名称 = 推断，见 `../../01-company-brief.md`）

## 2. JD 原文（REQ-27753 / 同题历史 req 镜像）

官方页 https://career.mlp.com/careers/job/755953879362 只渲染元数据（Miami · REQ-27753 · Information Technology · IT LEad Program · Onsite）。正文取自镜像：

- Glassdoor 职位镜像（jl=1010000638587）："Millennium is a large global alternative investment manager with a strong commitment to leveraging innovations in technology and data. As a member of the Miami-based Learning Engineering and Data (LEaD) program, LEaD engineers can expect to get comprehensive training and work alongside technology mentors and leaders to develop and maintain applications and tools spanning **front-office, middle-office and back-office functions** in a dynamic and fast paced environment … exposure to investment teams and technologists in different parts of Millennium's organization … The technology teams are looking for Software Engineers with **C++, Python or Java** to design, implement, and maintain systems supporting technology business functions." Glassdoor 估薪 **$90K–$141K**（估算，非官方）。**[高，JD 逐字；估薪低]**
- jobright 镜像（同题较新版本，含 AI/ML 段）：
  - Responsibilities：collaborate on requirements/specs；**backend distributed system development**；**apply AI/ML techniques including deep learning, NLP, and large language models to solve business problems**。
  - Required：**2–5 years** with C++/Python/Java；**Pandas, NumPy**；**FastAPI / Boost / Spring Boot**；Unix/Linux + Windows；design patterns；analytical/mathematical；communication in fast-paced settings。
  - Preferred：BS/MS in CS/Math/Stats；**experience building LLM-powered products**；**ML/data pipeline architecture**；**distributed messaging systems**；**Docker/Kubernetes**、**AWS/GCP**；relational + non-relational DBs。
  - Level: Entry to Mid；H1B: likely sponsor（jobright 推断）。**[高（JD 段落）/ 中（jobright 标签）]**
- ziprecruiter / talentify 旧 req（REQ-16650，2023）同题；talentify 页已 404。

**JD → Chi 的映射**（备考用）：Python ✅ · Pandas/NumPy ✅（Quant-Stroller）· FastAPI ✅ · Spring Boot（实习 Kotlin/Spring）✅ · LLM-powered products ✅（AikiCard / Aiki，OpenAI API）· ML/data pipeline ✅（DuckDB/Parquet point-in-time data plane）· messaging（Kafka 实习）✅ · Docker/K8s ✅ · AWS ✅（DVA-C02）· C++/Java：简历列了，**准备被问 Java 基础**（HashMap 冲突处理是一手电面题）。

## 3. Miami 技术组织（媒体，**[中]**）

- efinancialcareers 2023-04-17 "The top 10 technologists at Millennium in Miami"：Miami **"nearly 200 tech staff"**；Head of Technology Miami = **Olga Naumovich**（ex-Goldman MD/CDO，2022-09 加入）；Head of Trading UI Vladimir Korostyshevskiy；Global Head of Support/DevOps/QA (Corporate Tech) Stanley Mak；Lead Software Architect Michael Scrivo（20 年）；equities algo dev in **Java**（Kenneth Collins）；Senior DevOps **Kafka** specialist（Ivan Varela）；CI/CD/Terraform（Luisel Rios）。→ Miami 栈里 **Java、Kafka、Terraform、K8s** 都有一手证据。
- efinancialcareers 2022-07：Miami 23 个技术岗在招（前端、C++）；一名 12 YOE 技术人员 $240k base（levels.fyi 转述）；Izzy Englander 投资人信提到 Miami 技术中心。
- 公司：多策略对冲基金，1989 年 Izzy Englander 创立，AUM 约 **$79B**（LinkedIn 公司页 2026 口径）/ 约 $70B（techinterview.org 2026-04 口径）；约 320 个 pod（techinterview.org，**[低]**）；办公室 NYC 总部、London、HK、Singapore、Tokyo、Tel Aviv、Greenwich、Dubai、**Miami**、Bengaluru、Dublin。

## 4. 官方"Level Up Your Tech Interview"（mlp.com，**[高]**）

- John Talarico（Talent Acquisition）："Demonstrate your **abstract reasoning skills and creativity**" · "Bring examples of **ownership and initiative**" · "Show how you can **work together in a team** to solve problems" · "Contribute your individual strength to make a collective impact"。— https://www.mlp.com/life-at-millennium/level-up-your-tech-interview-with-john/
- Abhinav Srivastava（Head of HR, Millennium India）："Brush up on your **fundamentals**" · "be prepared to **talk through code live**" · "Stay updated with **industry trends**" · "how you **handle feedback**"。— https://www.mlp.com/life-at-millennium/level-up-your-tech-interview-with-abinav/
- 学生页（campusjobs）：流程 "screening, assessments, and technical plus behavioral interviews … vary by role"；**不公布题数、时长、分数线**（PracHub 引用）。

## 5. 薪酬（LEaD / Miami 早期职业）

| 数字 | 口径 | 来源 | 置信度 |
|---|---|---|---|
| **≈ $210K TC** | "new grad offer in Miami with a rotational program focused on AI/ML and LLM projects" —— 与 LEaD JD 描述一致 | Blind（搜索摘要，原帖 403） | 中 |
| "roughly around what MSFT is paying you right now for your YOE" | Blind 帖 "Millenium LEaD program"（j0mxzge4）回复；"Lead is relatively new and is strictly Miami office" | Blind 摘要 | 中 |
| $209K 中位（SWE）· 最高 $355K；Senior $272K | levels.fyi Miami-Ft. Lauderdale，2026-07-02 更新 | levels.fyi 摘要（页面本体空返回） | 中 |
| $90K–$141K | Glassdoor 对该 JD 的估薪（极可能只是 base 估算，且偏低） | Glassdoor | 低 |
| 全现金、无股票；"pays ~20% above peers" | Blind 多帖共识 | 摘要 | 中 |
| 印度：SWE 2 YOE base ₹40L + ₹10L bonus（2024-08）；应届 ₹50L + ₹15L + ₹5L JB | LeetCode Discuss 7307279 | 高（一手，但印度） |

结论：**LEaD 在 Miami 的合理预期 = $200K 上下 TC（base 大头 + 现金 bonus）**；谈薪时不报数字，只说 "in line with the program's band for my experience"。
