# GitHub 先行扫描：Headlands Technologies（采集日期 2026-10-14）

> 范围：只收 **Headlands Technologies LLC**（Chicago 高频做市商，headlandstech.com）。HRT（Hudson River Trading）是另一家公司，凡仅出现 HRT 的文件一律排除（包括各 company-wise LeetCode 仓库里的 `hrt*.csv` / `Hudson River Trading/`）。
> 方法：`gh api -X GET search/repositories`、`search/code`、`search/issues`、`search/users` 共约 45 条查询（"headlands interview / technologies / headlandstech / hackerrank / phone screen / oa / quant / trading / headlands-sqrt"、`"square root of 42"`、`"Headlands Technologies" in:file / filename:README.md / extension:md` 等），再对 20 个 company-wise LeetCode 仓库逐个读完整 git tree 找 `headland`。
> 可达性：**200** = 读到正文（GitHub API 或 fastprep 页面 HTTP 200）。可信度：高 = 一手或官方 · 中 = 一手但摘要 / 聚合站标了日期与轮次 · 低 = 生成式或 SEO。
> 关键结论放前面：**GitHub 上关于 Headlands 面试真正有内容的只有一条线，perixtar（FastPrep）的题库**，38 道带阶段标签的 Headlands 题；其余全是名单、职位聚合、或明说"general-prep"的生成内容。

## 1. 来源总表

| # | 来源（URL） | stars | 最近 push | 内容里关于 Headlands 的部分（题名原样） | 可达性 | 可信度 | 我们怎么用 |
|---|---|---|---|---|---|---|---|
| 1 | https://github.com/perixtar/Tech-OA-Interview-Questions（`README.md`、`formats/coding.md`、`formats/coding-page-2.md`、`formats/low-level-design.md`、`formats/system-design.md`、`question-bank/page-2.md`、`page-3.md`）| 5550 | 2026-10-14 | **38 道** Headlands 条目：31 道 Coding、4 道 Low-level design、3 道 System design（含 2 道与 Keychain / Optiver 共挂）+ 其余见 §3 完整清单。每条带"最近一次 sighting 日期"，链接到 `fastprep.io/problems/headlands-*` | 200（git clone 全仓，README 已 grep） | 中（一手候选人报告经 FastPrep 重构；日期是 `lastSeen` 不是考试日；FastPrep 自己说重构命中率约 85-90%，见 pushpa-kumar 笔记转述）| **CATALOG 主干**。阶段标签取自 fastprep 页面 `<title>`（Phone Screen / Online Assessment / Onsite Interview），见 §3。电话面试相关 = 18 道标 Phone Screen 的题 |
| 2 | https://github.com/perixtar/Tech-OA-Interview-Questions/pull/328「Sync Headlands interview questions」（2026-10-10 开，2026-10-11 合并）| （同上）| — | PR 正文："Adds five verified public Headlands Technologies coding questions"：Job Runner Chain Reports · As-Of Join · Market Order Book · Best Time to Buy and Sell Stock · Text Pattern Matching with Stars | 200 | 中 | 说明 Headlands 题库在**本月仍在更新**（新增 5 道），题目不是陈年旧货 |
| 3 | https://github.com/perixtar/quant-interview-oa-bank（`README.md`，"Headlands \| 1"）| 3 | 2026-07-31 | 只有 1 条：**Disaster Recovery**（OA，Mar 21, 2026）。README："a filtered view of FastPrep's production Firestore `problem` collection… **Last seen** is the newest ISO date in the document's `lastSeen` array"；并自述"cannot prove that an individual question was used for a quant trader or quant researcher position" | 200 | 中 | 解释 `Last seen` 的含义；确认 FastPrep 的角色标签不区分 SWE / QR。与 #1 的 Disaster Recovery 是同一条，不重复计数 |
| 4 | https://github.com/pfischer1687/headlands-sqrt | 0 | 2023-05-11 | 申请环节题：**"write a C++ program that prints out the square root of 42"**（README："my solution for the question posed for the application to Headlands Technologies"）。仓库含 `src/libs/square_root.cpp`：`std::sqrt`、`std::pow(num,0.5)`、`exp(log/2)`、`pow(10, log10/2)`、Newton-Raphson（含 epsilon/tolerance/NaN/inf 校验）+ 单测。README Keywords：Square Root · cmath · STL · pow · log · log10 · Newton-Raphson Method | 200 | 高（候选人一手；但只证明"申请题"而不是面试题）| 申请阶段（应聘前置题），**不是** HackerRank / 电话面试题。可当作"他们看重数值正确性与边界"的旁证（推断）；不进入编码题 CATALOG 主表，放"申请题"一行 |
| 5 | https://github.com/tugrul-kok/headlands-sqrt | 0 | 2026-01-25 | 同一道申请题，2026 年版："Application for Software Developer Position at Headlands Tech… your coding challenge… computes the square root of 42"。实现 4 条路径：x86 SIMD `_mm_sqrt_ss`、`constexpr` Newton-Raphson（`x_{n+1}=0.5*(x_n+a/x_n)`）、fast inverse sqrt（魔数 `0x1fbd1df5`，`std::bit_cast`）、统一入口 `std::is_constant_evaluated()`；另附 `docs/fast-sqrt-analysis.pdf`、自写 POSIX socket server | 200 | 高（候选人一手）| **独立第二次出现**：申请题在 2023 与 2026 两个周期都是 "C++ 打印 √42"。证明该申请题稳定（推断：HR/招聘表单里的固定题）|
| 6 | https://github.com/snehitvaddi/My-HeadLands-pitch-Application | 0 | 2024-11-11 | `src/app/page.tsx`："As requested in the application, I've created a C++ program that calculates and prints the square root of 42"，附代码截图与输出截图（Vercel 页） | 200 | 高（候选人一手）| 第三个独立旁证（2024-11 周期），同上 |
| 7 | https://github.com/cbasile3/headlands-application（`test.c` 6 行，`long square = sqrt(42); cout << …`）| 0 | 2026-04-28 | 同一道 √42 申请题的最简版（注意 `long` 截断成 6 是个坑，推断）| 200 | 中 | 第四个旁证；可当"别犯的错"小例子（推断）|
| 8 | https://github.com/ankitkushawaha1000/HFT（`companies/headlands-technologies/README.md`、`round-01-technical-phone-video-screen/questions.md`、`round-02-…`、`round-03-…`；`content/companies/headlands-technologies/` 为镜像副本）| 1 | 2026-07-25 | Round 1 phone/video screen（~45–60 min）三条"representative questions"：**"Implement a lock-free ring buffer in C++."** · **"What do `std::memory_order_acquire` and `std::memory_order_release` mean, and where would you use each?"** · **"Solve an algorithmic coding problem in the LeetCode-medium range."** Round 2：mutex vs lock-free 取舍、cache locality 与行情吞吐、概率 / 期望值题。Round 3："No specific Headlands final-round questions have been publicly reported"。README 自认："fewer than roughly five substantive public interview reports… very-low-confidence directional prep"；每题标 `general-prep` / `inferred`；README 声明"Optiver Focus"，面向 Senior C++ Deutsche Bank 候选人 | 200 | **低**（生成式、自标 very low confidence，不是候选人报告；pushpa-kumar 笔记也标 PRACTICE 非 REAL）| **不进 CATALOG 计数**。只作"通用 HFT C++ 预期"的弱信号（`std::memory_order`、lock-free 环形缓冲与 #1 的 SPSC channel / Fixed-Size Memory Pool 题型一致，推断）|
| 9 | https://github.com/54skyxenon/54skyxenon.github.io → `content/blog/finale-2023.md` | 0 | 2026-05-16 | 2023 秋招 new grad 周期，**一手叙述**："The most formidable contender was Headlands Technologies, reputed to put candidates through a grueling loop of 10+ interviews. I faltered after about six rounds of intense C++ questions, but at least got an Uber Eats voucher for making it to the onsite." 同文："I struggled a lot with trading firms since I needed to understand lower-level concepts better"（后去读 OSTEP 与 Kurose-Ross）| 200 | 高（一手，但无题目；岗位推断为 SWE new grad，文中未写岗位）| 唯一 GitHub 上的**流程一手信息**：onsite 阶段 ≈ 6+ 轮、C++ 偏重、低层（OS / 网络）。进 LOOP_GUIDE 的"onsite 形态"，标低置信（单源）|
| 10 | https://github.com/pushpa-kumar/placement-prep → `raw-notes/topic-algo-ds-oa.md`、`wave2-ankitkushawaha-hft.md`、`topic-concurrency-atomics.md`、`github-curated-lists.md` | — | 2026 | 二手汇总：把 #3 / #8 摘成条目。Disaster Recovery 的摘要（"Reconstruct commit histories from a corrupted log: discard malformed entries; group commits into 'repositories' via Union-Find… 'AMBIGUOUS INPUT!'… up to 10^7 log entries, 10^5 queries"）带有 FastPrep 之外没有的细节；`Status: REAL`（来自 FastPrep）与 `PRACTICE`（来自 #8）被它显式区分 | 200 | 低（二手汇总；仅用来交叉核对 #3 / #8）| 只借 Disaster Recovery 的题面摘要，用来在 fastprep 页面被付费墙截断时补全（需回到 fastprep 核对）|
| 11 | https://github.com/jraymondli/cpp → `Interviews/HackerRank.md` | — | — | 开头 "For the HackerRank assessment with **Headlands**, here's what you can expect…"，内容是泛泛的"算法 / STL / 并发 / 多线程"建议，无具体题目，行文是聊天机器人式模板 | 200 | 低（疑似 LLM 生成，无任何一手细节）| **不用**。仅登记，避免别人再点进去 |
| 12 | https://github.com/sgoel97/blog → `content/blog/quant-interview/index.md`（另有 `quant-resources`）| 0 | 2025-01-01 | "more QR-heavy firms will almost always test for programming skills through a combination of online assessments and Leetcode-style interviews. This includes firms like HRT, Headlands, and Jump Trading."；建议 Grind 75 当基准。另在一份公司清单中列出 Headlands（分档未核实） | 200 | 中（Berkeley 学生转述，QR 视角，无题目）| 旁证：Headlands 的编码考核 = OA + LeetCode 风格面试。**QR 视角，非 SWE** |
| 13 | https://github.com/YichengYang-Ethan/quant-interview-recon → `skill/quant-interview-recon/references/03-companies.md` | — | — | 只有招聘 req（"Quantitative Researcher – New Grad (Chi/NY/Ams/Lon)"）与 Greenhouse token（`headlandstechnologiesllc`）；面试证据标 `sparse` | 200 | 低（职位聚合，无面试）| 仅登记；Greenhouse board token `headlandstechnologiesllc` 可用于 JD 核对 |
| 14 | 名单 / 职位聚合类（无面试内容）：cybergeekgyan/Quant-Developers-Resources（4070★，2026-09-19）· northwesternfintech/2027QuantInternships（2527★）· quant-bobby/quant-jobs（304★，"Headlands Technologies \| Chicago, Austin, Amsterdam \| Prop Trading"）· hamza3256/quant-prep（把 Headlands 放在 tier 2，与 Citadel / Ansatz / Aquatic 同列）· mikinty/Trading-Interview-Questions（1013★，`resources/firms.md`："Headlands: Academic-driven, very high quality software"）· UBC-Trading-Group/ubctg-quant-prep · Lazar-Ilic/Lazar（`C++ 2026/01 Introductory.txt` 一句"how I would hope to do this for … Headlands Technologies… in a coding round"，内容是 bitap 字符串匹配实现，非 Headlands 报告）· ever-jobs/ever-jobs（Headlands 职位抓取插件）· SimplifyJobs/New-Grad-Positions 等 | 见左 | 见左 | 只列出名字或职位，无题 | 200 | 低 | 不用于题目；`hamza3256` 与 `mikinty` 的一句话描述可进"公司背景"（学术导向、软件质量高，推断为社区看法）|
| 15 | 公司博客被 GitHub 笔记引用：blog.headlandstech.com/2017/08/03/quantitative-trading-summary/（sgoel97、mikinty issue #6、melling/MathAndScienceNotes 均链）· blog.headlandstech.com/2018/08/15/outofline-a-memory-locality-pattern-for-high-performance-c/（CIS-1901-S24/Notes `13/README.md` 称其为"a tool called `OutOfLine`"）· blog.headlandstech.com/2024/05/01/opinion-rationalizing-latency-competition-in-high-frequency-trading/（Buildstarted/linksfordevs）| — | — | 官方博客（Max Dama 等）文章，间接证明团队关心 C++ 内存局部性与延迟 | 未抓正文（只是 GitHub 里的链接）| 高（官方）但与面试题无直接关系 | 面试前读 `OutOfLine` 那篇作 C++ 低延迟背景（推断）；URL 已登记，正文留给官方来源 agent |

## 2. 没找到什么（负面结果也是结果）

| 查询 / 仓库 | 结果 |
|---|---|
| `search/repositories` "headlands interview / technologies / headlandstech / hackerrank / phone screen / oa / quant / trading" | **0 个仓库**。只有 `headlands-sqrt` 系列（#4–#7）与无关的地理 / 农业 "headland" 仓库 |
| 20 个 company-wise LeetCode 仓库逐个读完整 git tree 搜 `headland`：krishnadey30/LeetCode-Questions-CompanyWise（20277★）· liquidslr/leetcode-company-wise-problems（31474★，原名 interview-company-wise-problems）· snehasishroy/leetcode-companywise-interview-questions（8377★）· hxu296/leetcode-company-wise-problems-2022（11384★）· MysteryVaibhav/leetcode_company_wise_questions · jobream/Leetcode-Company-Wise-Problems · ayush-that/codejeet · udayrajsawhney/Leetcode · pratikn0708/… · md-akhlak/… · harlleybastos/leetcode-premium-questions · farneet-singh/… · Kali-Prem/… · mohitkumhar/companywise-dsa-interview-question · themysterysolver/PLACEMENT-QUESTIONS · geekygirl8/lc_cc · zinader/… · Hariharan76/tob_interview · chindsch/… · ADHIL48/… | **全部没有 Headlands 文件**。它们只有 HRT（`hrt_alltime.csv`、`Hudson River Trading/`、`hrt/`、`companies/HRT.csv`），已按规则排除。结论：**LeetCode 公司标签路线对 Headlands 无效**，不要跑 `lc_company.py Headlands` 期待有数据 |
| 其它量化面试库：SoYuCry/awesome-quant-interview（784★）· QuantBrainteasers/awesome-quant-interview-prep · mikinty/Trading-Interview-Questions · meagmohit/mlquant-interview-question-bank · andyhu4023/Quant-Interview-Question-Bank · quant-robby/… | 代码搜索与目录检查均无 Headlands 面试内容（只有 mikinty 的一句公司描述）。这些库多是脑筋急转弯 / 概率，非公司分类 |
| `search/issues`（"headlands technologies interview / tech interview / hackerrank / headlandstech"）| 只命中 perixtar PR #328、ankitkushawaha1000/HFT PR #3（"Add companies/ directory… 34 HFT and top…"）、mikinty issue #6（博客链接）、两个求职追踪仓库。无候选人讨论串 |
| `search/code` 的 "Headlands" 高噪音命中（`ever-jobs`、`Jiang6082/QJS`、`ipverse/as-ip-blocks`、各类 Greenhouse 公司表）| 全是职位 / ATS 聚合或 ASN 表，已忽略 |

## 3. 题目 / 主题完整清单（每项带来源）

### 3.1 FastPrep 题库中的 Headlands 条目（来源 #1，经 perixtar README / formats / question-bank 校验；#3 重复 Disaster Recovery）

阶段取自对应 fastprep 页面 `<title>`（2026-10-14 抓取，全部 HTTP 200）。日期 = FastPrep `lastSeen` 最新日期（**不是**题目出现的确切月份，见 #3 的说明）。一句话描述取自页面 meta description（只有前约 160 字符，完整题面在 fastprep 页面，部分可能受限，需人工打开）。

#### A. 标 Phone Screen（电话 / 视频技术面，与 Chi 的一小时视频通话最相关）共 18 道

| 题名（原样） | 阶段标签 | 最近 sighting | 题面线索 | fastprep URL |
|---|---|---|---|---|
| Market Order Book | Phone Screen | Jun 25, 2026 | "Implement a finite in-memory order book for one instrument. Process the operations in o…" | https://www.fastprep.io/problems/headlands-market-order-book |
| Gradient Descent on a Sinusoidal Objective | Phone Screen | Apr 09, 2026 | "Use gradient descent to seek a minimum of f(x) = x*x - 2*x + 1…" | https://www.fastprep.io/problems/headlands-gradient-descent-sinusoidal-objective |
| Pearson Correlation Coefficient | Phone Screen | Apr 09, 2026 | "Given two equal-length arrays x and y of paired observations, calculate t…" | https://www.fastprep.io/problems/headlands-pearson-correlation |
| Top K Frequent Elements | Phone Screen | Apr 09, 2026 | "Given an integer array nums and k, return its k most frequent distinct values. Or…" | https://www.fastprep.io/problems/headlands-top-k-frequent-elements |
| Queue Mean Queries | Phone Screen | Mar 23, 2026 | "Process a sequence of operations on an initially empty first-in, first-out queue of in…" | https://www.fastprep.io/problems/headlands-queue-mean |
| Queue Mean from Corrective Snapshots | Phone Screen | Mar 23, 2026 | "A FIFO queue starts empty. Ordinary events belong to one logical his…" | https://www.fastprep.io/problems/headlands-snapshot-queue-mean |
| CPU Register Bitwise Operations | Phone Screen | Nov 11, 2025 | "Simulate one unsigned 32-bit register. You receive its initial nonnegativ…" | https://www.fastprep.io/problems/headlands-cpu-register-bitwise-operations |
| Merge K Sorted Sequences | Phone Screen | Oct 04, 2024 | "Given sequences, an array of integer sequences, merge all their entries into one…" | https://www.fastprep.io/problems/headlands-merge-k-sorted-sequences |
| Top Trade Events by Notional | Phone Screen | May 26, 2024 | "You are given parallel arrays tickers, prices and volumes describing trade e…" | https://www.fastprep.io/problems/headlands-top-trade-events-by-notional |
| Fixed-Size Memory Pool | Phone Screen | May 10, 2024 | "Implement a pool containing capacity equal-size blocks. Blocks are represented by…" | https://www.fastprep.io/problems/headlands-fixed-size-memory-pool |
| Order Sequence Prefix Counts and Quantities | Phone Screen | May 10, 2024 | "Maintain an insertion-ordered sequence of active orders. Each…" | https://www.fastprep.io/problems/headlands-order-sequence-prefix-aggregates |
| Best Time to Buy and Sell Stock | **Phone Screen & Onsite** | Apr 05, 2024（PR #328 在 2026-10 重新同步）| "prices[i] is th…"（LC 121）| https://www.fastprep.io/problems/headlands-best-time-to-buy-and-sell-stock |
| Custom Stack with Bottom Increment | Phone Screen | Apr 05, 2024 | "Maintain an initially empty stack that can hold at most maxSize intege…"（LC 1381）| https://www.fastprep.io/problems/headlands-custom-stack |
| Limit Order Matching | Phone Screen | Apr 05, 2024 | "Process the finite orders batch in arrival order. Every row is [side,price,quantity]…" | https://www.fastprep.io/problems/headlands-limit-order-matching |
| Checked Recursive Sum | Phone Screen | Aug 10, 2023 | "Given a nonnegative integer n, compute the sum of every integer from 1 through n. T…"（疑为溢出 / 递归深度检查，推断）| https://www.fastprep.io/problems/headlands-checked-recursive-sum |
| Decode a Run-Length Stream | Phone Screen | Jun 03, 2023 | "Decode the run-length stream in encoded. Each record consists of a positive de…" | https://www.fastprep.io/problems/headlands-stream-decoder |
| Numeric Wildcard Dictionary Matching | Phone Screen | Jun 09, 2019 | "You are given a dictionary words and a query batch patterns. Match e…" | https://www.fastprep.io/problems/headlands-numeric-wildcard-dictionary-matching |
| Text Pattern Matching with Stars | Phone Screen | Jan 21, 2017（PR #328 在 2026-10 重新同步）| "You are given a lowercase string text and a pattern pattern containing l…" | https://www.fastprep.io/problems/headlands-text-pattern-matching |

#### B. 标 Online Assessment（HackerRank 一类）共 8 道（As-Of Join 同时标 Onsite）

| 题名（原样） | 阶段标签 | 最近 sighting | 题面线索 | fastprep URL |
|---|---|---|---|---|
| Array Interval Sums | Online Assessment | Oct 11, 2026 | "You are given an integer array nums and an array of interval queries queries. Ea…" | https://www.fastprep.io/problems/headlands-array-interval-sums |
| Minimum Changes for Distinct Adjacent Characters | Online Assessment | Sep 13, 2026 | "You are given a string s. In one operation, you may…" | https://www.fastprep.io/problems/headlands-minimum-changes-no-equal-adjacent-characters |
| Sliding-Window Means with IEEE Special Values | Online Assessment | Sep 13, 2026 | "You are given an integer array valueBits and an intege…"（位模式解释为浮点，NaN/Inf 处理，推断）| https://www.fastprep.io/problems/headlands-sliding-window-means-ieee-floats |
| Job Runner Chain Reports | Online Assessment | Aug 17, 2026 | "You receive a CSV-like job log in lines. The first line must be exactly #jo…" | https://www.fastprep.io/problems/headlands-job-runner |
| As-Of Join | **Online Assessment & Onsite** | Aug 13, 2026 | "You are given two timestamp-sorted tables, leftRows and rightRows. E…" | https://www.fastprep.io/problems/headlands-asof-join |
| Disaster Recovery | Online Assessment | Mar 21, 2026 | "Your company has been using an archaic repository management system and is switchi…"；pushpa-kumar 摘要：并查集 + 范围查询，10^7 条日志、10^5 次查询、`AMBIGUOUS INPUT!`（来源 #10，二手）| https://www.fastprep.io/problems/headlands-disaster-recovery |
| Exclusive Function Execution Times | Online Assessment | Jan 01, 2024 | "A single-threaded CPU runs function calls. A new call pauses the…"（LC 636）| https://www.fastprep.io/problems/headlands-exclusive-function-execution-times |
| Earliest Dependency Schedule | Online Assessment | Oct 13, 2023 | "There are N jobs with indices from 0 through N - 1. Job i takes duratio…"（DAG 最早完成时间）| https://www.fastprep.io/problems/headlands-dependency-job-schedule |

#### C. 标 Onsite Interview（仅 onsite）共 5 道

| 题名（原样） | 阶段标签 | 最近 sighting | 题面线索 | fastprep URL |
|---|---|---|---|---|
| Triggered Order Event Filter | Onsite Interview | Oct 07, 2024 | "You receive orders in arrival order. Each row is [price, side], where si…" | https://www.fastprep.io/problems/headlands-triggered-order-filter |
| Best Time to Buy and Sell Stock II | Onsite Interview | Apr 05, 2024 | "prices[i] is the price of one share on day i. Starting with no sha…"（LC 122）| https://www.fastprep.io/problems/headlands-best-time-to-buy-and-sell-stock-ii |
| House Robber | Onsite Interview | Apr 05, 2024 | "nums[i] is the amount available at position i along a linear street. Choose positions to…"（LC 198）| https://www.fastprep.io/problems/headlands-house-robber |
| Merge Intervals | Onsite Interview | Apr 05, 2024 | "closed integer intervals intervals[i] = [start, end]. Merge every group…"（LC 56）| https://www.fastprep.io/problems/headlands-merge-intervals |
| Net Position Calculation from API Snapshots | Onsite Interview | Apr 05, 2024 | "Calculate the final signed share quantity for each symbol…" | https://www.fastprep.io/problems/headlands-net-position-calculation |

#### D. Low-level design（4）与 System design（3）

| 题名（原样） | 类型 | 最近 sighting | 题面线索 | URL |
|---|---|---|---|---|
| Concurrent Sorted-Stream Merger | Low-level design | Oct 04, 2024 | "incremental sorted merging through a supplied unsafe blocking client, with bounded overlapping background reads…" | https://www.fastprep.io/low-level-design/concurrent-sorted-stream-merger |
| Shared-Memory Single-Writer Single-Reader Channel | Low-level design | Aug 24, 2023 | "bounded shared-memory message channel between two processes, with safe record ownership, FIFO delivery and explicit full, empty and drained…" | https://www.fastprep.io/low-level-design/shared-memory-spsc-channel |
| Asynchronous TCP Message Channel | Low-level design | Mar 09, 2023 | "bounded message API over one TCP session, with local circular buffers, partial-I/O framing…" | https://www.fastprep.io/low-level-design/asynchronous-tcp-message-channel |
| Design an Incremental Lattice Coverage Tracker | Low-level design | Apr 17, 2018 | "accepts geometric segments and maintains an exact distinct-point count as the input grows to millions of additions" | https://www.fastprep.io/low-level-design/lattice-segment-coverage-tracker |
| Design a Future-Time Job Scheduler（标 "Keychain / Headlands Technologies"）| System design | Oct 05, 2026 | "durable one-time jobs… within a bounded delay after its requested time" | https://www.fastprep.io/system-design/future-time-job-scheduler |
| Design a Low-Latency Electronic Trading System（标 "Optiver / Headlands Technologies"）| System design | Oct 29, 2025 | "Ingest market data, validate strategy order intents, route orders to exchanges, and reconcile executions" | https://www.fastprep.io/system-design/low-latency-electronic-trading-system |
| Design Distributed Unused-Code Analysis | System design | Jun 28, 2023 | "Analyze a fixed company-wide code snapshot and produce explainable unused-code candidates…" | https://www.fastprep.io/system-design/distributed-unused-code-analysis |

行数核对（脚本 `ex.py` 对 perixtar 仓库去重得出）：唯一题名 38 = 电话面试 18 + OA 8（含 As-Of Join）+ 仅 onsite 5 + LLD 4 + SD 3。

### 3.2 主题层面的提炼（`推断` = 我的归纳，不是来源原文）

| 主题 | 出现的题 | 来源 |
|---|---|---|
| 订单簿 / 撮合 / 订单事件处理（电话面试里最集中的一类）| Market Order Book · Limit Order Matching · Triggered Order Event Filter · Order Sequence Prefix Counts and Quantities · Top Trade Events by Notional · Net Position Calculation from API Snapshots | #1，推断（题型归类）|
| 滚动统计 / 队列均值 / 数值稳定性 | Queue Mean Queries · Queue Mean from Corrective Snapshots · Sliding-Window Means with IEEE Special Values · Pearson Correlation Coefficient · Gradient Descent on a Sinusoidal Objective | #1，推断 |
| 低层 / C++ 系统题 | Fixed-Size Memory Pool · CPU Register Bitwise Operations · Shared-Memory SPSC Channel · Asynchronous TCP Message Channel · Concurrent Sorted-Stream Merger | #1；ankitkushawaha1000/HFT 的 `lock-free ring buffer`、`std::memory_order_acquire/release` 与之同向（#8，低置信）|
| 经典 LeetCode 原题（电话面试 / onsite 都出现）| Best Time to Buy and Sell Stock(121) · Best Time … II(122) · House Robber(198) · Merge Intervals(56) · Top K Frequent Elements(347) · Custom Stack with Bottom Increment(1381) · Exclusive Function Execution Times(636) · Merge K Sorted Sequences | #1（题名原样；LC 编号为我标注，推断）；#2 PR 点名 Best Time + Text Pattern Matching 为新同步 |
| 字符串 / 模式匹配 | Text Pattern Matching with Stars · Numeric Wildcard Dictionary Matching · Decode a Run-Length Stream · Minimum Changes for Distinct Adjacent Characters | #1 |
| 日志 / 数据管道风格 OA | Job Runner Chain Reports（CSV 式日志）· As-Of Join · Disaster Recovery · Earliest Dependency Schedule · Array Interval Sums | #1 |
| 应聘前置题 | "C++ 程序打印 √42" | #4 #5 #6 #7（四个独立仓库，2023-05 / 2024-11 / 2026-01 / 2026-04）|
| onsite 形态 | "grueling loop of 10+ interviews… about six rounds of intense C++ questions" | #9（单源）|
| 通用预期（低置信）| lock-free ring buffer · `std::memory_order_acquire/release` · mutex vs lock-free · cache locality · 概率 / 期望值 | #8（生成式 `general-prep`，不当作报道）|

### 3.3 交叉校验与限度

- **独立性**：#1 的 38 条全部来自同一个聚合器（FastPrep），所以它们是**一个来源的 38 个条目**，不是 38 个独立来源；`#refs` 在 CATALOG 里应记为 1（FastPrep），除非别的 agent 在论坛上找到同题。#4–#7 是 4 个独立候选人，但只证明申请题。
- **阶段标签可靠性**：标签来自 fastprep 页面标题，由其审核流程打的；我无法验证 "Phone Screen" 对应 SWE 还是 QR 岗位（#3 README 明说角色字段不区分）。Chi 的情形是 SWE + 一小时视频通话，所以 18 道 Phone Screen 题是最强候选，但**不要假设会原题重现**；更合理的用法是按题型（订单簿、滚动统计、位运算、内存池、LC 中等）备考。
- **付费 / 截断**：fastprep 页面 meta 描述只有前约 160 字符，完整题面和解答可能需登录或付费，本次没尝试登录。

## 缺口（我没能触达、Chi 该手动打开的 URL）

| 缺口 | 该打开的 URL | 原因 |
|---|---|---|
| 38 道题的完整题面 / 测试用例 / 难度 | 每道题的 fastprep URL（§3.1 表格），优先 18 道 Phone Screen 题；首选 https://www.fastprep.io/problems/headlands-market-order-book 与 https://www.fastprep.io/problems/headlands-queue-mean | meta 描述被截断，完整内容可能在页内但需浏览器渲染 / 登录；本次只读 `<title>` 与 meta |
| 各题"来自哪个候选人 / 哪个岗位"的原始报告 | FastPrep 自己的 Discord（perixtar README 里的 invite）；或 1point3acres / Glassdoor 的 Headlands 页面（由其它 agent 负责）| GitHub 上没有原始报告；FastPrep 只给 `lastSeen` |
| ankitkushawaha1000/HFT 的数据索引 | https://github.com/ankitkushawaha1000/HFT/blob/main/data/content-index.json | 判断其 Headlands 条目是否有未列入的 sources（我只读了 4 个 md）；预期仍是 general-prep |
| 54skyxenon 的 Headlands 轮次细节 | https://github.com/54skyxenon/54skyxenon.github.io/blob/main/content/blog/finale-2023.md（同作者其它博文 `recruiting-2022.md`、`interviewing.md` 未见 Headlands 命中）；若需细节可在其站点留言 | 只有一段话，没有题目与岗位 |
| 申请题的官方表述 | https://www.headlandstech.com/careers/ 与 Greenhouse board https://job-boards.greenhouse.io/headlandstechnologiesllc | √42 题的出处文字应在申请表单里；本次未登录申请流程 |
| `search/code` 总命中数大于单页上限的查询（如 "Headlands Technologies" in:file 共 496 条）| 在 GitHub 网页端按语言 Markdown 过滤再翻页：https://github.com/search?q=%22Headlands+Technologies%22+interview&type=code | API 每个查询最多取前 100 条；已用多种措辞交叉，但长尾可能漏 |
