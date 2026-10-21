# Headlands Technologies：官方信息 + 面试流程（P1-C）

> 采集日：**2026-10-14**（除另注）。可达性：**200** = 读到正文（WebFetch 会经小模型摘要，此类标 `200·摘要器`；curl 原文标 `200·原文`）；**摘要** = 只有搜索摘要；**403 / 429 / CF / 登录墙** = 正文被拒。可信度：高 = 官方/一手；中 = 一手但摘要、或带日期的聚合；低 = SEO / 自相矛盾。
> 标 `推断` 的是我自己的判断，不是来源原话。引文保持原语言。lodely / vervecopilot 未采用。
> 本文件不含任何面试官、招聘人员姓名或邮件内容。

---

## 0. 一页结论（给编排者）

| # | 结论 | 来源（见 §A） | 可信度 |
|---|---|---|---|
| 1 | 官方首页视频 Q&A 第 19 条「面试流程多久？」：「two to three weeks is probably a good timeframe … very small team … move people through the process very quickly」。这是官方唯一的流程时间陈述；没有官方的轮数、题型、通过率。 | S4（视频 19，我本地转写） | 高（转写可能有错字） |
| 2 | Java 岗官方 JD（Greenhouse，2026-06-01 首发，2026-09-21 更新）：Chicago 基础薪资 **$175k–$300k**（其余 C++/QR 岗 $200k–$300k）；职责是研究基础设施 / 分布式存储 / 性能 / 网络延迟 / 监控，**不是**交易策略；JD 明说工程师要「conducting interviews and providing candidate evaluations」。 | S2, S3 | 高 |
| 3 | 官方技术博客只有 **5 篇**（2017–2024），其中 2 篇与工程直接相关：2018 年 *OutOfLine*（C++ 缓存局部性，作者 Patrick Moran，基准约 11.8x）和 2017 年 *Quantitative Trading Summary*（系统组件 + 延迟量级：「Production systems are written in C++」）。没有 Java 相关博文。 | S5–S10 | 高（正文经摘要器） |
| 4 | 聚合器没有任何通过率 / 录取率数字。唯一量化的是 Glassdoor 汇总「31.4% positive experience、难度 3.39/5」（搜索摘要，未读到原页）。 | S22 | 低 |
| 5 | 没有找到任何 **Java** 面试面经；SWE 电话面经几乎全是 C++（队列+快照、合并多路数据流、优化 unordered_map 等）。Chi 说的「10 天 HackerRank 链接 / NDA / 一小时视频」未被任何公开来源独立证实。 | §D, §F | 中 |

---

## A. 来源台账

| ID | URL | 内容 | 可达性 | 可信度 |
|---|---|---|---|---|
| S1 | https://www.headlandstech.com/ （2026-10-14；curl + WebFetch） | 首页：公司定义、5 个办公室、21 条员工视频 Q&A 标题 | 200·原文 | 高 |
| S2 | https://www.headlandstech.com/careers/ （2026-10-14；curl 原文） | 6 个职位 + 各地福利 + 基础薪资区间 | 200·原文 | 高 |
| S3 | https://boards-api.greenhouse.io/v1/boards/headlandstechnologiesllc/jobs?content=true 与 https://job-boards.greenhouse.io/headlandstechnologiesllc/jobs/4227795009 （2026-10-14） | Greenhouse 全部职位 JSON、Java JD 全文、首发/更新时间 | 200·原文（API）+ 200·摘要器（页面） | 高 |
| S4 | https://www.headlandstech.com/videos/NN.mp4 （NN=01–03,07–14,16,17,19；2026-10-14 下载） | 官方员工视频，我用 faster-whisper small.en 本地转写 | 200（视频），转写为机器产物 | 高（来源）/ 中（转写准确度） |
| S5 | https://blog.headlandstech.com/ | 博客首页 + 存档（共 5 篇，无分页） | 200·摘要器 | 高 |
| S6 | https://blog.headlandstech.com/2017/08/03/quantitative-trading-summary/ | 见 §B | 200·摘要器 | 高 |
| S7 | https://blog.headlandstech.com/2018/06/05/successfully-starting-a-career-in-quant-research/ | 见 §B | 200·摘要器 | 高 |
| S8 | https://blog.headlandstech.com/2018/08/15/outofline-a-memory-locality-pattern-for-high-performance-c/ | 见 §B | 200·摘要器 | 高 |
| S9 | https://blog.headlandstech.com/2022/02/16/elements-of-statistical-learning-8-10/ | 见 §B | 200·摘要器 | 高 |
| S10 | https://blog.headlandstech.com/2024/05/01/opinion-rationalizing-latency-competition-in-high-frequency-trading/ | 见 §B | 200·摘要器 | 高 |
| S11 | https://en.wikipedia.org/wiki/Headlands_Technologies | 创立、创始人、历史、TD 收购、诉讼 | 200·摘要器 | 中（百科，部分条目与官网不一致，见 §C） |
| S12 | https://www.levels.fyi/companies/headlands-technologies | 员工数 150、成立 2009、营收估算 $10M–$50M | 200·摘要器 | 中 |
| S13 | https://www.levels.fyi/companies/headlands-technologies/salaries/software-engineer 与 …/salaries（页面标注更新 10/14/2026） | SWE 薪资 | 200·摘要器 | 低（样本极小，见 §E） |
| S14 | https://www.ellis.com/visa-sponsors/headlands-tech-organization-llc/salaries （页面标 "Last Updated Apr 2026"） | H-1B LCA 工资 | 200·摘要器 | 中（LCA 为申报底薪） |
| S15 | https://www.1point3acres.com/interview/company/headlands （2026-10-14；curl 原文） | 公司面经列表，第 1 页 20 条（共 3 页，只读到第 1 页） | 200·原文 | 中（仅标题与元数据） |
| S16 | 1p3a 帖子正文：/interview/thread/938472、1030839、1059121、1169914、1136321、1090391、1169644、1001711、1111077、835627、1089956、1011799 | 只见到帖子摘要；正文需登录 | 登录墙（r.jina.ai 镜像被 Cloudflare 拦：「Just a moment…」） | 中（摘要），正文无 |
| S17 | https://www.teamblind.com/post/headlands-technologies-research-developer-interview-process-pcb637t7 （帖 2024-08-20，评论 2024-08-21/22 与 2025-11-04） | Research Developer 面经评论 | 200·摘要器 | 中 |
| S18 | https://www.teamblind.com/post/headlands-interview-what-are-the-best-c-books-75wjle52 （2023-03） | C++ 备考讨论 | 200·摘要器 | 中 |
| S19 | https://www.teamblind.com/post/has-anyone-interviewed-with-headlands-technologies-llc-xueqf3d3 （2020-09-20 起，评论至 2025-11-04） | 少量流程碎片 | 200·摘要器 | 中 |
| S20 | https://www.teamblind.com/post/headlands-technologies-quantitative-researcher-k6mjefej （2022-12-16） | QR 面试一条评论 | 200·摘要器 | 中（QR，非 SWE） |
| S21 | https://www.levels.fyi/community/thread/gIZK8J/headlands-tech-nyc | NYC 工程师求评价，2 条评论 | 200·摘要器 | 低 |
| S22 | Glassdoor：fr.glassdoor.ca/Entretien/Headlands-Technologies-Entretien-E715901-RVW104113166.htm、…RVW89062704.htm、…RVW98042384.htm；www.glassdoor.com/Interview/Headlands-Technologies-Interview-Questions-E715901.htm；…Software-Engineer-Interview-Questions-EI_IE715901.0,22_KO23,40.htm | 评论正文 | WebFetch **403**；jina 镜像 CF 拦；archive.org **429**。内容仅来自 WebSearch 摘要 | 中（摘要） |
| S23 | https://www.quantt.co.uk/resources/headlands-technologies-interview （2026-08-18） | 通用化 5 阶段指南 | 200·摘要器 | 低（SEO，成立年份错成 2006，自称图示性数字） |
| S24 | https://quantvault.org/headlands-interview-process.html | 5 阶段，含 QR 新毕业 OA 结构 | 200·摘要器 | 低（SEO；无引用） |
| S25 | https://www.interviewsense.org/opportunities/headlands-tech-holdings-c-software-developer-new-grad-full-time-chicago-yqzxvb/ | C++ new grad 备考页 | 403 | — |
| S26 | https://jobright.ai/jobs/info/6a56054821f64463ad351e33 | Java Software Developer JD 镜像 | 摘要 | 中 |

---

## B. 公司与官方技术博客

### B1 公司事实

| 项 | 内容（原文 / 近似转述） | 来源 | 可信度 |
|---|---|---|---|
| 自我描述 | 「A quantitative trading firm at the forefront of finance & technology. Since 2010, we have been leading the way in designing and implementing cutting-edge quantitative trading strategies in an array of financial products on venues across the globe.」 | S1 | 高 |
| 资金 | 「We are a privately funded company and do not accept outside investors.」；视频 01：「we trade all of our own internal capital, so we don't have any external investors」 | S1, S4 | 高 |
| 办公室（官网 2026-10-14） | Chicago（110 North Wacker Drive, Floor 54）· New York（520 5th Avenue, Floor 9）· Amsterdam（World Trade Center Tower 2）· London（125 Wood Street, Floor 7）· Singapore（Asia Square Tower 1）。「trade 24/7 across diverse financial markets」 | S1 | 高 |
| 成立时间 | 官网「Since 2010」；Wikipedia「July 2009」；Levels.fyi「2009」；quantt「2006」（与他处冲突，不采信）。**不一致，待 Chi 取舍。** | S1, S11, S12, S23 | 官网高 / 其余中低 |
| 创始人 | Matthew Andresen、Jason Lehman、Neil Fitzpatrick，三人均为前 Citadel 高管（Andresen 曾任 Citadel Securities 联席 CEO；Lehman 负责全球期权做市；Fitzpatrick 曾任 Citadel Execution Services COO）。当前 CEO：Andresen。官网 bio 页 2026-10-14 已 404（其中一个子页返回 soft-404），无法从官网复核。 | S11（Wikipedia） | 中 |
| 起步 | 2009 年 7 月，10 名员工，交易股票/期权/期货，「would not manage outside money」 | S11 | 中 |
| 固收业务 | 2013 成立 Headlands Tech Global Markets LLC（电子固收，2014 起做市市政债）；2021-03 宣布 TD 收购，2021-07 完成；Headlands 继续做股票/期权/期货自营。 | S11 | 中 |
| 办公室（其他来源） | Wikipedia 另列 Austin；官网无。`推断`：Wikipedia 可能过期。2022 年租下 110 N. Wacker 约 35,000 平方英尺。 | S11 | 中 |
| 规模 | 官方未公布。第三方估计：Levels.fyi 150 人；ZoomInfo 51–200；Prospeo 101–200；quantt「reportedly 50+」（低）。无日期，均为估算。 | S12 + 搜索摘要 | 低 |
| 交易品种 | 官方只说「an array of financial products」。Levels.fyi：「exchange-traded products, including equities」；博客 2017：套利 / market taking / market making。 | S1, S12, S6 | 中 |
| 技术自述 | 官网几乎不谈技术栈；视频 01：「we build algorithms that trade in global markets … a lot of research into how markets behave, and … a lot of coding to design those algorithms and to run them efficiently」；视频 14：Chicago 24 小时有人值守 + Amsterdam / Singapore 冗余覆盖，交易周从周日芝加哥时间 16:00 到周五下午。博客 2017：「Production systems are written in C++ rather than Python, R, or Matlab」。JD：「large scale 24-hour automated trading system and research framework」。 | S1, S4, S6, S3 | 高 |
| 近期事件 | 2025-01：美国检察官指控前交易员 Richard Ho 窃取 Headlands 商业机密，Headlands 称其与 Tower Research 串通。 | S11 | 中 |

### B2 博客：全部 5 篇（blog.headlandstech.com，存档页：/2024/05/、/2022/02/、/2018/08/、/2018/06/、/2017/08/ 各 1 篇，无分页，2026-10-14 读取）

| # | 标题 | 发布日期（更新日期） | URL | 作者 | 技术内容一行摘要 |
|---|---|---|---|---|---|
| 1 | Opinion: Rationalizing Latency Competition in High-Frequency Trading | 2024-05-01（更新 2025-01-15） | https://blog.headlandstech.com/2024/05/01/opinion-rationalizing-latency-competition-in-high-frequency-trading/ | Max Dama（Quantitative Researcher） | 观点文：延迟竞争降低价差——把做市报价建模成空头期权、延迟相当于到期时间，Black-Scholes 下到期时间减半期权价格降约 30%（文中算出 29%）；亚毫秒级反馈回路、HFT 作为市场「优化层」、非赢者通吃；文中提到交易所处理需数十微秒，纳秒级优化主要影响周边生态。非工程文，面试偶尔可聊。 |
| 2 | Elements of Statistical Learning. 8/10 | 2022-02-16 | https://blog.headlandstech.com/2022/02/16/elements-of-statistical-learning-8-10/ | Max Dama | 给新 quant 的书评：无条件推荐第 1、2、3、7 章；4、8、16、9/10/15、11、13/14 章有保留；5、6、12、17、18 章可跳过。与 SWE 无关。 |
| 3 | OutOfLine – A Memory-Locality Pattern for High Performance C++ | 2018-08-15（更新 2018-08-28） | https://blog.headlandstech.com/2018/08/15/outofline-a-memory-locality-pattern-for-high-performance-c/ | Patrick Moran | **最贴近工程面试**：热路径只访问 4 字节 `fd`，但带 `std::string` 的对象约 40 字节，冷数据白占缓存行。用 CRTP 基类 `OutOfLine<Fast, Cold>` + 静态全局 map（按对象地址索引）把冷数据移出对象，保留 RAII；API 含 `cold()`、`TwoPhaseInit`、`init_cold_data()`、`release_cold_data()`；拷贝被 delete，移动时重新关联。基准（作者称 contrived）：冷数据内联 34,684,547 ns；丢弃冷数据 2,938,327 ns；OutOfLine 2,947,645 ns，约 11.8x（作者说「~10x」）。实现约 29 行。 |
| 4 | Successfully Starting a Career in Quant Research | 2018-06-05（更新 2022-09-12） | https://blog.headlandstech.com/2018/06/05/successfully-starting-a-career-in-quant-research/ | Max Dama | 入职前向雇主问的 7 个结构性问题（面试是否考脑筋急转弯 / 扑克 / 心算；竞业是否超过 2 年，「standard term is about 18 months」；是否限制看源码；研究员是否兼任值班交易员；能否看到 PnL；是否人工日内调参；同事是否直接竞争）。透露其价值观：偏好研究驱动、不靠心算。 |
| 5 | Quantitative Trading Summary | 2017-08-03（更新 2025-01-15） | https://blog.headlandstech.com/2017/08/03/quantitative-trading-summary/ | Max Dama | 量化公司的组织与软件组件：实盘链路 = market data parser → strategy → order gateway；配套 = monitoring GUI、drop copy、market data capture、启动脚本；离线 = 参数优化、production reconciliation、backtesting simulator（tick 数据可达每天数百 GB）、画图。延迟量级：慢软件系统收数据到发单约 30 µs；交易所包间隔约 10–1,000 µs；撮合响应约 100 µs–5 ms；NY–Chicago 微波约 4 ms vs 光纤约 7 ms。技术备注：C++ 生产、co-location、Linux 调优（processor affinity、NUMA）、时钟同步为基线。 |

`推断`（备考价值）：#3 和 #5 是面试官（工程师，JD 说工程师参与面试）最可能引用的内容：缓存行/对象布局、热冷数据分离、RAII、延迟量级。Java 岗面试直接引用 C++ 博客的概率不高，但「布局 / 缓存 / 分配」这类问题是同一思路。博客页数据经小模型摘要，正文细节（尤其 #3 的基准数字）请 Chi 打开原文复核。

---

## C. 官方职位：Software Engineer / Java

### C1 当前在招（Greenhouse 板，2026-10-14；板 slug 为 `headlandstechnologiesllc`，**不是** `headlandstech`——`boards.greenhouse.io/headlandstech` 301 到 `job-boards.greenhouse.io/headlandstech` 后返回 404）

共 8 个：C++ Software Developer（4227758009，2026-05-11 首发）· C++ Software Developer - New Grad（4336806009，2026-09-16；Amsterdam / Chicago）· FPGA Engineer（4228114009，2026-06-10）· **Java Software Developer（4227795009，首发 2026-06-01，更新 2026-09-21；Amsterdam / Chicago / London / New York）** · Legal & Compliance Associate（Singapore，4273272009）· Opportunistic Applications（4237953009）· Quantitative Researcher（4194144009）· Quantitative Researcher – New Grad（4227566009）。均为 `https://job-boards.greenhouse.io/headlandstechnologiesllc/jobs/<id>`。页面要求「apply to only one job」。（来源 S2, S3；高）

### C2 Java Software Developer JD（S3，Greenhouse API 原文，高）

**Scope**：「work in close collaboration with the research, systems, and operations teams to design, engineer, implement, and maintain the Firm's software written in Java … key role in designing and constructing the Firm's software infrastructure to support new and existing lines of business. You will expand the Firm's proprietary research platform to improve performance and support new exchanges, products and functionality.」

**Qualifications（原文）**
- Preferred degree in any computing related area；in lieu of this, extensive professional software development experience
- Well-versed in the fundamentals of software engineering
- Genuine interest in solving technical problems, along with a strong ability to implement solutions
- Low ego, able to work both in a collaborative team setting and autonomously
- Committed to designing and implementing fully automated, scalable, and maintainable solutions with extensive testing
- Comfortable operating at various levels of abstraction, from individual machines to large scale distributed systems
- Strong knowledge of the details of computing all throughout the technical stack
- Superior ability to write, refactor, and debug programs in Java
- Good knowledge of networking and storage systems
- Plus：C++ 经验或知识；Linux；交易行业经验

**Day to Day（原文）**：Maintain and extend core research infrastructure · Design, implement, and maintain distributed storage systems with various performance and reliability requirements · Address performance limitations within our own software, open-source libraries and applications, Linux, etc. · Investigate new technologies to improve stability, scalability, and performance of a distributed computing farm · Develop and improve monitoring and proactive detection capabilities · Perform basic data analysis to support decision making and better plan for future growth · Improve networking communication between different components of the system to achieve optimal latency and throughput · Communicate with stakeholders across teams … · Conduct code reviews of other developers, researchers and operations team members · **Participate in the recruitment process by conducting interviews and providing candidate evaluations**

**JD 中没有**：面试流程、时间线、薪资（Greenhouse 页面本身无薪资；API `pay_input_ranges` 为空）。薪资在官网 careers 页，见 §E。（高）

### C3 同期 C++ Software Developer JD 的差异（S3 页面，200·摘要器；高）

职责额外包含：exchange connectivity、low-level networking protocols、「Optimizing latency and throughput using profiling, lock-free data structures」、策略实现、模拟与生产对账。要求「Superior ability to write in C++, or experience with other statically-typed imperative programming language」。`推断`：Java 岗更偏研究平台与基础设施（存储、计算集群、监控），而非交易热路径，但仍强调性能与网络。

### C4 旧版/镜像

jobright.ai 的 Java Software Developer 镜像（S26）内容与官方一致，并标注「可能提供 H1B 担保」（聚合器标签，未证实）。（摘要，中）

---

## D. 面试流程

### D1 官方陈述

| 陈述 | 来源 | 可信度 |
|---|---|---|
| 视频 19「How long does the interview process take?」（我转写，约 50 秒）：「Depending on the candidates availability, two to three weeks is probably a good timeframe. One of the really nice things about being a very small team is that we are able to move people through the process very quickly and we are able to communicate updates very quickly … big tech companies of the world where they're waiting for months at a time to hear back. So we do our best to keep timelines short in terms of recruiting …」 | S4 | 高 |
| 官方 careers 页 / JD **没有**描述轮数、题型或评分标准。只说工程师会面试并写评价。 | S2, S3 | 高 |
| 官网「What makes a candidate stick out?」（视频 03，转写）：见 §G。 | S4 | 高 |

### D2 聚合器：流程骨架（按来源列，不合并）

| 来源 | 描述 | 日期 | 可信度 |
|---|---|---|---|
| Glassdoor（Amsterdam，搜索摘要） | 「starts with a C++ HackerRank online assessment, followed by a 1-on-1 Zoom interview with a developer or researcher. The OA problems are medium-to-hard difficulty」；后续轮覆盖 algorithms、OS concepts、concurrency、open-ended systems questions | 报告日 2026-02（搜索摘要自述） | 中（摘要） |
| Glassdoor（Chicago，搜索摘要） | 「2 hour hacker rank」「very challenging」「make sure you study c++ before hand」，流程约 3 周；另一条：问题约 LC Med-Hard，但 I/O 解析与校验吃掉时间 | 日期不详 | 中（摘要） |
| Glassdoor（Chicago，搜索摘要） | 2025-09：先 C++ 编程挑战，然后「one hour long zoom interview one on one with a researcher」（QR 方向） | 2025-09 | 中（摘要） |
| Glassdoor（搜索摘要） | 2023 一条：onsite 前「relentless escalating coding pre-screening」，称面试官态度差，单一轶事 | 2023 | 低 |
| Glassdoor 汇总（搜索摘要） | 「31.4% positive experience」、难度 3.39/5 | 搜索摘要 2026-10-14 | 低（未见原页） |
| Glassdoor 另一条（搜索摘要） | 一位候选人写「the question was under NDA, but expect LC Medium」；一个视频首轮问了「removing dead code」 | 日期不详 | 低（摘要的转述） |
| Blind（评论，Google 员工，2024-08-21/22） | OA → **一小时视频**，对方为工程师；第一题「summing natural numbers」基础题，面试官不断加优化追问；第二题「design an optimized hash map for stock tickers」；「refreshing compared to big tech」；**36 小时内收到拒信**。另有 HRT 员工称混合 math / coding / ML；另一位 Google 员工称被问 C++。G-Research 员工：「multiple algorithm rounds before an onsite」。 | 2024-08 | 中 |
| Blind（2023-03） | 前 Goldman quant 候选人：首轮是 OA，只有一道 C++ 题；发帖人称 Headlands 问 `malloc` vs `new`、`std::copy` vs `memcpy` 等深层 C++ 题；「Headlands … pays higher than Citadel, JaneStreet」（原帖断言，未证实） | 2023-03 | 低–中 |
| Blind（2020–2025 评论） | 常见路径：HackerRank → 电话面（Phone screen），多人称有「second phone screen」；一人 2020-10 电话面后被拒 | 2020-09 至 2025-11 | 低–中 |
| Blind（2022-12，QR） | 「Headlands is small, so interviews depend heavily on what each interviewer chooses to discuss」 | 2022-12 | 低–中 |
| Levels.fyi 社区（NYC 工程师） | 一位面过被拒的 TPM：「super high」的招聘标准，团队小 | 日期不详 | 低 |
| quantt.co.uk（SEO） | 「three to five rounds over three to six weeks」：CV + OA（2–3 题）→ 1–2 次 45–60 分钟电话面 → 3–5 节 final（芝加哥现场或虚拟）→ offer「within one to two weeks」；通过率「Not reported」；文内自称数字为图示性、可能过期 | 2026-08-18 | 低 |
| quantvault.org（SEO） | 5 阶段：recruiter → OA → probability & mental math（45–60 min）→ statistics & modeling（45–60 min）→ onsite；其中 OA 结构 70 分钟（10 道基础统计选择题 10 min + 4 道统计简答 24 min + 1 道 C++ 20 min + 2 道编程 16 min）是 **QR new grad 版**，声称 2026-09 报告；「Headlands has no trading game」 | 2026-09 | 低；**QR，不适用 SWE** |
| Chi 口述（任务说明，非来源） | Chi 提供的路径：HackerRank 链接 10 天、NDA、一小时技术视频。公开来源**均未**证实链接有效期或 NDA 时点。 | — | — |

### D3 1point3acres：Headlands 面经列表（S15，2026-10-14 读取，第 1 页共 20 条；还有第 2、3 页未读）

> 表中最后两列为列表页的两个未标注数字；从 HTML 看，前者是点赞图标、后者是评论图标（`推断`：点赞数 / 评论数）。正文均需登录（S16），此处只有标题、角色、日期。

| # | 标题 | 日期 | 角色标签 | 赞 / 评论 |
|---|---|---|---|---|
| 1 | Headlands Technology Full Time QR OA | 2026/10/11 | Fulltime · Quant Finance · NewGrad | 0 / 1 |
| 2 | Headlands Tech Phone Screen Interview Report for Quant Finance Intern | 2026/9/14 | Intern · Quant Finance | 1 / 1 |
| 3 | headlands Research Developer Online Assessment Experience | 2026/9/14 | Fulltime · Quant Finance · JobHopper | 3 / 0 |
| 4 | headlands Online Assessment Details for Fulltime Position | 2026/8/27 | Fulltime · Other · NewGrad | 1 / 2 |
| 5 | headlands Online Assessment for Software Engineer Position | 2026/8/17 | Fulltime · **SWE** · JobHopper | 0 / 1 |
| 6 | Interview Experience and Online Assessment for Headlands FPGA Engineer Position | 2026/4/6 | Fulltime · EE/Semiconductor | 0 / 1 |
| 7 | headlands Software Engineer Tech Phone Interview Experience | 2026/3/24 | Fulltime · **SWE** · JobHopper | 1 / 4 |
| 8 | headlands Online Assessment for Software Engineer Fulltime Position | 2026/3/21 | Fulltime · **SWE** · JobHopper | 1 / 2 |
| 9 | Headlands Technical Phone Screen for Software Engineer: Stock Trading Questions | 2025/12/3 | Fulltime · **SWE** · JobHopper | 1 / 2 |
| 10 | Headlands Technical Phone Screen for Software Engineer Position | 2025/11/11 | Fulltime · **SWE** · JobHopper | 3 / 0 |
| 11 | Headlands Fulltime Quantitative Researcher Phone Interview Experience | 2025/11/10 | Fulltime · Quant Finance | 2 / 0 |
| 12 | Headlands Online Assessment: Challenging Disaster Recovery Problem | 2025/10/30 | Fulltime · **SWE** · JobHopper | 0 / 2 |
| 13 | headlands Intern Tech Phone Screen Coding Interview for Quant Finance | 2025/10/23 | Intern · Quant Finance | 0 / 2 |
| 14 | headlands Quant Finance Intern Tech Phone Screen Interview Experience | 2025/10/23 | Intern · Quant Finance | 0 / 0 |
| 15 | headlands Interview Experience and Behavioral Question Focus | 2025/9/28 | Fulltime · Quant Finance | 0 / 0 |
| 16 | Headlands Junior Engineer Technical Phone Screen Experience | 2025/7/9 | Fulltime · **SWE** · NewGrad | 0 / 3 |
| 17 | Headlands Tech Phone Screen: Order Interval Overlap and Cancellation Problem | 2025/6/25 | Fulltime · **SWE** · JobHopper | 0 / 0 |
| 18 | Headlands Technical Phone Screen Has 17 Hackerrank Questions in 70 Minutes | 2025/4/18 | Fulltime · Quant Finance · NewGrad | 1 / 15 |
| 19 | Headlands Technology Quantitative Research Video Interview Experience | 2025/3/8 | Fulltime · Quant Finance · NewGrad | 1 / 4 |
| 20 | Headlands Technologies Online Fulltime SDE Test | 2025/2/8 | Fulltime · **SWE** · JobHopper | 0 / 1 |

计数：20 条里 **SWE 标签 9 条**（#5、7、8、9、10、12、16、17、20），QR / 其他 / FPGA 11 条。（可信度：标题与日期高，内容无）

### D4 1p3a：可见的 SWE 帖摘要（线程页只露摘要，正文登录墙；中）

| 线程 | 页面摘要（原样转述） | 对应列表行（`推断`，按标题匹配） |
|---|---|---|
| https://www.1point3acres.com/interview/thread/1169914 | C++ 与「implementing a queue system with snapshots」；强调 problem-solving 与 asking clarifying questions | #7（2026/3/24） |
| https://www.1point3acres.com/interview/thread/1089956 | 电话面：用 C++ 合并多路数据流（merge multiple data streams），追问多线程、non-blocking | 无法对应列表行 |
| https://www.1point3acres.com/interview/thread/1011799 | C++ 电话面：language features、shared memory、system design | 无法对应 |
| https://www.1point3acres.com/interview/thread/1136321 | 初级工程师岗电话面，**33 分钟**：简历、行为题、一道与交易相关的简单 OOD 题 | #16（2025/7/9） |
| https://www.1point3acres.com/interview/thread/1059121 | 「covering two technical phone screens, six onsite rounds, and an additional interview round」（SDE 全职） | 日期不详 |
| https://www.1point3acres.com/interview/thread/938472 | OA 和电话面：test cases、system design、interprocess communication | 日期不详 |
| https://www.1point3acres.com/interview/thread/1030839 | SDE 电话面：流程、一道编码题、跨时区协作 | 日期不详 |
| https://www.1point3acres.com/interview/thread/1169644 | SWE 全职 OA | #8（2026/3/21） |
| https://www.1point3acres.com/interview/thread/1001711、1111077、835627 | 各为 SDE OA 帖（C++ coding、错误处理建议；数据结构与 fintech 场景） | 日期不详 |
| https://www.1point3acres.com/interview/thread/1090391 | 「Quantitative Finance Onsite Interview Experience (8 Rounds)」 | QR 方向，**不用于 SWE** |

### D5 阶段、轮数、时长汇总表（SWE 方向；缺的格子如实留空）

| 阶段 | 形式 | 时长 | 出处 | 可信度 |
|---|---|---|---|---|
| 投递 | Greenhouse，只能投一个职位；表单问 offer 截止日、通知期、搬迁、签证 | — | S2, S3 | 高 |
| HackerRank OA | C++/Java/Python 版本（Chi 的信息）；聚合器多说 C++；Chicago「2 小时、一道很难」；也有「17 题 / 70 分钟」（QR new grad，1p3a #18，仅标题）；有「Disaster Recovery」题（#12，仅标题） | 70 分钟 / 2 小时（两个不同报告）；10 天有效期**未证实** | S15, S22 | 中–低 |
| NDA | 无公开来源 | — | — | — |
| 技术视频面（Chi 要面的） | 与一位工程师一对一，Zoom；题目「基础题 + 不断加优化追问」，或 C++ 队列快照、合并数据流、优化 hash map；另一帖 33 分钟（junior） | 1 小时（Blind）；33 分钟（1p3a #16 摘要） | S17, S16 | 中 |
| 第二次电话面 | 多个 Blind 评论提及 | 未知 | S19 | 低 |
| Onsite / final | 1p3a SDE 帖：「six onsite rounds, and an additional interview round」；QR 帖：8 轮；quantt（SEO）：3–5 节。官方未说明。 | 未知 | S16, S23 | 低 |
| Offer 时间 | 官方：整个流程 2–3 周；Blind 一例：电话面后 36 小时给拒信；Glassdoor Chicago：约 3 周 | — | S4, S17, S22 | 高 / 中 / 中 |

### D6 通过率 / 选择性数字（原样）

| 数字 | 来源 | 注 |
|---|---|---|
| Glassdoor「31.4% positive experience」，难度「3.39 out of 5」 | S22 搜索摘要（2026-10-14 检索） | 未读到原页；样本量未知；**不是通过率** |
| quantt：「Pass rates: Not reported」 | S23 | 自己说没有 |
| quantvault：「The page gives no pass rates」 | S24 | 没有 |
| 1p3a 的两个数字是点赞 / 评论，不是通过率 | S15 | — |
| 无任何一手的 OA 通过率、电话面通过率 | — | **没有找到。** 以任何「X%」引用都是编的。 |

---

## E. 薪资

| 来源 | 数据 | 日期 | 可信度 |
|---|---|---|---|
| **官方 careers 页**（S2，curl 原文） | 基础薪资：**Java Developer，Chicago：$175k–$300k**；C++ Developer、C++ New Grad、Quantitative Researcher、QR New Grad（Chicago / New York）：$200k–$300k；FPGA Engineer（Chicago / New York）：$225k–$300k。Amsterdam / London：未列。Java 岗没有 New York 的福利/薪资区块（页面只有 Amsterdam / Chicago / London）。仅 base，未说明奖金。 | 2026-10-14 | 高 |
| 官方福利（S2，Chicago / New York） | 医疗（PPO / HDHP）day 1、牙科视力、HSA 公司注资、401(k) 含 employer match、公司付寿险、免费餐 + 餐补、健身房、月度 tech stipend、EAP 等 | 2026-10-14 | 高 |
| Ellis H-1B LCA（S14，页面标「Last Updated Apr 2026」） | Headlands Tech Organization LLC：Software Developer 9 条 $120k–$200k，中位 $200k；Software Engineer 3 条 $150k–$180k；Research Developer 28 条 $110k–$265k，中位 $200k；FPGA 3 条 $200k；Chicago 43 条中位 $200k；总中位 $200,000，平均 $177,717。页面内部计数不一致（9 vs 46），LCA 是申报底薪，不含奖金。 | 2026（Apr） | 中 |
| Levels.fyi（S13，页面标 10/14/2026） | Software Engineer：中位总包 $100K，均值 $119,313，最高 $147,253；中位包是「Mobile Software Engineer, New York, NY，L3，0 年经验，base $100K，stock $0，bonus $0」；页面无数据点数量，提交表为空。公司页（S12）无薪资汇总。 | 2026-10-14 | 低：样本极小，与官方区间（$175k–$300k base）明显矛盾，`推断`为极少数提交，不应用于谈薪 |
| Blind（2024-08 评论） | 发帖人称 3 YoE、TC 210k；多人质疑；一人说 Headlands「pays around 100k」 | 2024-08 | 低 |
| Blind（2023-03 发帖人断言） | Headlands 付得「higher than Citadel, JaneStreet」 | 2023-03 | 低 |

---

## F. 与 Chi 当前阶段（HackerRank 通过 → 一小时视频面）直接相关的证据

1. **谁面**：官方 JD 说工程师做面试并写评价；Blind 与 Glassdoor 均说是 developer（或 researcher）一对一 Zoom。（高 / 中）
2. **题型（公开线索，均为 C++ 方向，未找到 Java 版）**：
   - 基础题（求自然数和）+ 面试官连续加优化追问（Blind 2024-08）；
   - 为股票代码设计优化的 hash map / 优化版 `unordered_map`，追问 hash 冲突和内存开销（Blind 2024-08 + 搜索摘要）；
   - C++：带快照的队列系统（1p3a #7 摘要）；合并多路数据流 + 多线程 non-blocking 追问（1p3a 1089956 摘要）；
   - 订单区间重叠与撤单（1p3a #17 标题）；股票交易相关题（#9 标题）；
   - junior 电话面 33 分钟：简历 + 行为题 + 简单交易相关 OOD（1p3a #16 摘要）；
   - 重 C++ 细节：`malloc` vs `new`、`std::copy` vs `memcpy`（Blind 2023-03，低）。
3. **评价风格**：Blind「面试官想聊什么就聊什么」（QR，2022-12）；「refreshing compared to big tech」「36 小时内拒信」。`推断`：电话面当场反馈快，节奏短；题目是「一道简单题逐步加深」而非多道独立题。
4. **与 JD 的对应** `推断`：Java 岗 JD 强调 distributed storage、networking、Linux、性能瓶颈、监控——电话面若偏 Java，可能会涉及并发、内存/GC、IO、数据结构实现，而不是纯算法；但这只是由 JD 推出，**没有任何面经支持**。
5. **没有找到**：任何 Java 面试面经；NDA 说明；HackerRank 链接有效期。

---

## G. 文化 / 价值观 / 他们找什么

> 官网无「价值观」栏目。以下全部来自官网首页视频 Q&A（S4，我用 faster-whisper small.en 在本机转写；说话人未标名；引文可能有听写错误，取意可靠），及 JD / 首页文字。

| 主题 | 原话（转写，节选） | 视频 | 可信度 |
|---|---|---|---|
| 首页定位 | 「Our people are at the core of everything we do. We hire the best minds and empower them to take bold action towards solving some of the world's hardest quantitative problems.」 | S1 | 高 |
| 什么样的人突出 | 「You kind of need to be good at everything, so you need to be smart, you need to be prolific, you need to be knowledgeable about a lot of different areas from math, statistics, computer science, trading systems … so we're always trying to find people that complement each other … we try to hire people that are different.」 | 03 | 高 / 转写 |
| 工程师要多少金融知识 | 「Very little. I think for what we do, you'll pick it up on the job. … having deep technical knowledge on the FPGA side, on the software side as well. That's sort of the most important thing … It's really having the problem solving ability that's foundational」 | 17 | 高 / 转写 |
| 什么人不适合 | 「If you want the kind of job where you kind of work nine to five and then don't think about work at all, it's probably not a good fit … If you want to be told exactly what to do your entire career … After a few years here, you're generally expected to have independent ideas and the occasional substantial insight.」 | 07 | 高 / 转写 |
| 与 Big Tech 的区别 | 「faster iteration cycle than my previous job in the Big Tech … I can kind of see what its impact on production within weeks. Whereas previously in the Big Tech, the rollout cycle could be months or even years.」 | 16 | 高 / 转写 |
| 成功的人 | 「we like to find entrepreneurs that are ever curious and looking to take their career to the next level」（说话人讲了小时候自建游戏服务器并托管到机房的故事；「at least half of the group grew up gaming … upgrading their computer … curious why it was slow」） | 12 | 高 / 转写 |
| 激励机制 | 「at a lot of other trading firms, incentives are team-based … Here, that's not an issue. One strategy cannibalizes another. Doesn't matter because we're incentivized based on just our performance and the firm's performance.」 | 08 | 高 / 转写 |
| 内部氛围 | 「no political games … everybody's very focused on just doing what's best for Headlands」；扁平：「You can walk into anyone's office including … any of the partners … such a flat hierarchy … everyone's ideas are treated pretty equally」 | 09, 13 | 高 / 转写 |
| 上手周期 | 「everything's open internally and our system is pretty complex … we have to teach them the entire way that we do everything … maybe like even a year or two to get somebody up to speed.」 | 10 | 高 / 转写 |
| 公司做什么 | 「we trade all of our own internal capital … we build algorithms that trade in global markets」；「We have no clients」 | 01, 11 | 高 / 转写 |
| 为什么现在加入 | 「We are a dominant player in many of the markets that we trade. There's so much left to do. There's new asset classes, there's new geographies … we've built so much infrastructure that can be horizontally scaled」 | 02 | 高 / 转写 |
| 24 小时运营 | 交易周从芝加哥时间周日 16:00 到周五下午；Chicago 全天有人，Amsterdam、Singapore 冗余；「how comfortable would you be on a commercial airliner if it was on autopilot but there were no pilots in the cockpit」 | 14 | 高 / 转写 |
| JD 价值词 | 「Low ego」「collaborative」「Committed to designing and implementing fully automated, scalable, and maintainable solutions with extensive testing」「Genuine interest in solving technical problems」 | S3 | 高 |
| 博客价值观 | 「Attention to detail, hard work, trading intuition, and strong programming skills」（2017）；偏好研究驱动 > 脑筋急转弯（2018） | S6, S7 | 高（摘要器） |

`推断`：面试中展示「低自我、能独立推进、对性能/系统细节好奇、能把简单题越挖越深」比展示金融知识更贴合官方口径。

---

## 缺口（我没拿到的 + Chi 该手动打开的 URL）

1. **1p3a 帖子正文**（Cloudflare / 登录墙；jina 镜像同样被拦）：Chi 登录后依次打开  
   - https://www.1point3acres.com/interview/company/headlands （读第 2、3 页；我只读了第 1 页的 20 条）  
   - https://www.1point3acres.com/interview/thread/1169914（SWE 电话面：队列 + 快照）、/1089956（合并数据流）、/1011799（C++ 特性 / 共享内存 / system design）、/1136321（junior 33 分钟）、/1059121（两次电话面 + 6 轮 onsite + 额外一轮）、/938472、/1030839  
   - 列表 #5、#9、#10、#12、#17、#20（SWE 标签）的帖子 URL 我没拿到（列表页靠 JS 点击，HTML 无链接）。
2. **Glassdoor 原文**（WebFetch 403、jina CF、archive.org 429）：打开 https://www.glassdoor.com/Interview/Headlands-Technologies-Software-Engineer-Interview-Questions-EI_IE715901.0,22_KO23,40.htm 与 https://www.glassdoor.com/Interview/Headlands-Technologies-Interview-Questions-E715901.htm ，核对 31.4% / 3.39、流程天数、各条的日期与地点。本文所有 Glassdoor 内容均为搜索摘要。
3. **Java 专属面经**：全网没找到。可去 Blind 搜 "Headlands Java"、LeetCode Discuss、Reddit（本次未搜 Reddit 与 LeetCode Discuss 原站）。
4. **Chi 口述的流程细节**（10 天链接、NDA、一小时视频）没有任何公开来源证实，只能以 Chi 收到的通知为准。
5. **创始人官方 bio**：headlandstech.com/about/<name> 全部 404（2026-10-14），创始人与 CEO 信息只有 Wikipedia 与搜索摘要。成立年份冲突（官网 2010 / Wikipedia 2009）未解。
6. **视频未转写**：04、05、06、15（量化研究员的一天）、18（新研究多久）、20、21（福利）未处理。完整清单：https://www.headlandstech.com/ 的 21 条员工视频。已转写的 14 条建议 Chi 抽看 19、03、07、10 原视频验证转写。
7. **博客正文均经摘要器**，尤其 OutOfLine 的基准数字与「29 行」请对照原文：https://blog.headlandstech.com/2018/08/15/outofline-a-memory-locality-pattern-for-high-performance-c/ 。
8. **Levels.fyi 数据**可靠性很低（见 §E），不要拿来谈薪；官方区间与 H-1B LCA 更可信。
9. **未搜索**：Reddit（r/cscareerquestions、r/quant）、LeetCode Discuss、GitHub 上的 Headlands 面经仓库（编排者说由其它 agent 负责 GitHub）。
