# Headlands Technologies — 论坛面经台账（P1-B）

> 采集日 **2026-10-14**（所有「抓取日」均为此日）。范围：Headlands Technologies（芝加哥 HFT，**不是** Hudson River Trading）的软件工程师面经；QR/QT 单列在 §3，仅作对照。
> 可达性：**200** = 读到正文 · **摘要** = 只读到搜索摘要 / 镜像预览 / 站内公开摘要 · **403 / CF / 登录墙** = 正文被拒。可信度：[高] 一手 · [中] 一手但只有摘要，或带日期的聚合 · [低] SEO。lodely / vervecopilot 未引用。
>
> **关键限制（先读）**：一亩三分地（1p3a）几乎所有 Headlands 帖子的正文都在**登录墙**后（`/interview/thread/<tid>` 返回 "Please log in to view interview details"；`/bbs/thread-*` 是 Cloudflare 挑战，r.jina.ai 与 m. 镜像同样被挡）。我没有绕过登录。本文件里 1p3a 的内容来自三条**公开**路径，逐行标注：
> - **[L]** 公司列表页 `https://www.1point3acres.com/interview/company/headlands` 的 SSR 数据（共 56 帖，含 tid、发帖日期、标题、岗位类别），分页走站点自己的 `trpc.1point3acres.com/trpc/interview.getInterviewThreadList`；
> - **[S]** 同站公开摘要 `interview.getTranslation`（一句话英文摘要，站方生成，非原文）；
> - **[P]** 帖子正文的公开预览（搜索引擎索引 + Telegram 镜像频道 `https://t.me/s/usinterview?q=%23headlands` 抓到的 22 条，含帖子开头 ~100 字原文，Chinese 原文引用）。
> 凡是 [S] 的表述都是摘要转述，不是逐字题面；凡标 `推断` 是我自己的判断。

## 0. 一眼结论（SWE 视角）

1. **一小时技术视频电话**（Chi 即将面的那一轮）有**逐字级**证据的只有两处：Blind 2024-08-22「1 小时 Zoom，先要求不用公式求 1..n 之和，再加优化追问；第二题优化 C++ `unordered_map`（股票代码）；36 小时内被拒」（#B1），以及 Glassdoor 首轮视频「如何识别并删除大型代码库里的无用代码」（#G3）。1p3a 的同类帖子（#A1–#A20）有题目名但正文被锁。
2. **题型家族稳定**：①递归求和 / 尾递归 / 溢出 / 栈（3 个独立来源，2021–2024）；②订单 / 股票交易事件处理（订单区间最大重叠 + 撤单、Put/Delete 订单 API、market order book）（5 个来源，2024–2026）；③流式数据结构（带 `get_mean` 的 queue + snapshot、合并多路数据流 + 多线程非阻塞、merge k sorted）（3 个来源，2024–2026）；④买卖股票 DP（1p3a×2 + WSO，2023–2025，**独立来源**）；⑤C++ 语言深度（为什么快、C++11/14/17/20、IPC / 共享内存、智能指针、unordered_map）。
3. **HackerRank 测试**：2020–2026 反复是同一道「job runner / job chain」CSV 题（`job_id, run_time_seconds, next_job_id`，输出每条链的首尾 id、个数、总时长 hh:mm:ss、平均时长；非法输入要报错），**至少 8 个来源**；2024-11 出现并查集 + 异常变体，2025-10 出现「disaster recovery」变体，2026-09 QR/Research Developer 版整体换成 4 段（统计 MCQ + OLS + C++ 滑窗均值 + 2 道 LC）。语言：多数帖强调**只能 C++**，但 2026-08 一帖说「不是 C++ 也会考这题」，1187591 摘要说「C++、Python 或 Java 均可」。**没有任何来源明确提到 "Java"**（Chi 选 Java，需向招聘方确认；见缺口）。
4. **形式**：电话 / 视频 33 分钟（初级工程师，含简历 + BQ）到 1 小时；结果标题带「挂」的占多数；onsite 有「2 电话 + 6 onsite + 1 加面」（#A10）和「3 小时 final：2 技术 + 1 BQ」（#W1）。

## 1. SWE 面经逐条（按阶段优先级：电话 / 视频 > HackerRank > onsite）

字段：日期 = 发帖 / 提交日；角色（SWE=码农类 General）；阶段；语言；题目（原文引用用 `「」`；[S] 为摘要转述）；时长；结果；来源；可达性 / 可信度。

### 1.1 技术电话 / 视频面（最优先）

| # | 日期 | 角色 / 地点 | 阶段 | 语言 | 题目（原文 / 摘要） | 时长 | 结果 | 来源 URL | 可达性 / 可信度 |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 2026-03-23 | SWE 全职，跳槽 | 技术电面 | C++ | [P]「面试官反应很快 喜欢讨论C++相关的技术知识一共两问 第一问是实现一个queue 和三个函数 push pop 和 get_mean get_mean就是所有里面数据的mean 第二问是实现一个带有sn…」（预览截断；[S]：queue systems with snapshots, problem-solving and clarifications） | — | 未知 | https://www.1point3acres.com/interview/thread/1169914 ；预览镜像 https://t.me/s/usinterview/27677 | 摘要（正文登录墙）/ 中 |
| A2 | 2025-11-11 | SWE 全职，猎头联系 | 第一轮技术电面 | C++ | [P]「第一轮电面，这家公司保持了oa的风格，就是题目长+难。…面完感觉它家是招c++ linguist。red flag：没有performance review，comp不透明。」[S]：debugging and bitwise operations with C++ in a code framework | — | 帖内标签 Negative / Hard（搜索引擎转述）；结果未知 | https://www.1point3acres.com/interview/thread/1154043 ；https://t.me/s/usinterview/26257 | 摘要 / 中 |
| A3 | 2025-12-02 | SWE 全职，跳槽 | 技术电面 | — | [S]「thoroughly review all stock trading related LeetCode problems… DP-based coding question requiring detailed state tracking」；正文「本内容被作者隐藏」 | — | 未知 | https://www.1point3acres.com/interview/thread/1156658 ；https://t.me/s/usinterview/26518 | 摘要 / 中 |
| A4 | 2025-07-09 | Junior Engineer（NG），SWE | 技术电面 | — | [P]「一个Junior Engineer…问了33分钟简历和bq然后一道不是很难的ood，trading相关直接挂」[S]：resume, behavioral, an easy trading-related OOD question | **33 分钟（简历 + BQ）+ 一道 OOD** | 被拒 | https://www.1point3acres.com/interview/thread/1136321 | 摘要 / 中 |
| A5 | 2025-06-24 | SWE 全职，跳槽 | 先过 OA，再技术电面 | — | [S]「processing order intervals to find maximum overlaps and handling order cancellations by buy/sell sides」；[P]「先是过了一个OA…面试小哥还是很nice的」 | — | 标题「店面挂经」= 挂 | https://www.1point3acres.com/interview/thread/1134455 ；https://t.me/s/usinterview/23873 | 摘要 / 中 |
| A6 | 2024-10-04 | SWE 全职，跳槽 | 技术电面 | C++ | [S]「coding in C++ to merge multiple data streams, including a multithreaded non-blocking follow-up」；正文「本内容被作者隐藏」；17 条回复 | — | 标题「挂经」= 挂 | https://www.1point3acres.com/interview/thread/1089956 ；https://t.me/s/usinterview/19732 | 摘要 / 中 |
| A7 | 2024-06-11 | SWE 全职，跳槽 | **两次**技术电面 | — | [P]「两次电面，第一次感觉答得不好，花了很多时间修compile error。第二次感觉顺利一些。依然挂了。」[S]：merge k sorted list and streaming problems | 2 轮 | 挂 | https://www.1point3acres.com/interview/thread/1071034 ；https://t.me/s/usinterview/18592 | 摘要 / 中 |
| A8 | 2024-05-26 | SWE 全职，跳槽 | 技术电面 | C++ / Python | [P]「店面题目难度不算大，但没有太详细得准备再加上当天状态不是很好，发挥不行。第二天收到fail的消息。店面内容：c++/Python的区别，会问得比较详细。在哪种情…」[S]：smart pointers, a trading events coding challenge | — | 次日被拒 | https://www.1point3acres.com/interview/thread/1068621 ；https://t.me/s/usinterview/18477 | 摘要 / 中 |
| A9 | 2024-05-10 | SWE 全职，跳槽 | 技术电面 | — | [P]「1. You have to implement 4 APIs, to place orders - Put(unique_id,quantity) -> put the order in a sequence - Delete(unique_id,quantity) -> delete an existi…」[S]：API design and memory management | — | 未知 | https://www.1point3acres.com/interview/thread/1066045 ；https://t.me/s/usinterview/18290 | 摘要 / 中 |
| A10 | 2024-04-05 | SWE 全职；有数年 trading 经历 | **免 OA**：2 轮电话 + 6 轮 onsite + 1 轮加面 | — | [P]「headlands recuirter来联系，就面了一下，没怎么准备。免OA面了2轮phone + 6轮onsite+1轮加面，最后不move forward。」题目正文被锁 | 共 9 轮 | 不 move forward | https://www.1point3acres.com/interview/thread/1059121 ；https://t.me/s/usinterview/17956 | 摘要 / 中 |
| A11 | 2025-01-08 | SWE 全职，跳槽 | 第二轮电面 | — | [S]：second-round SWE phone screen, compared with other hedge funds（题目不可见） | — | 进入第二轮 | https://www.1point3acres.com/interview/thread/1106014 | 摘要 / 低（仅摘要） |
| A12 | 2023-11-30 | SWE（US SDE） | 技术电面 | — | [S]：coding question + cross-time-zone collaboration（题目不可见） | — | 未知 | https://www.1point3acres.com/interview/thread/1030839 | 摘要 / 低 |
| A13 | 2023-08-24 | SWE（C++）| OA + 技术电面 | C++ | [P]「求加米…OA就是地里那道，只有100分钟，时间挺紧，推荐提前把逻辑或者pseudo code准备好再开始。他们大概想要看起来很clean，well structured，容易maintain」；电面题（搜索引擎转述原文）：「为什么C++比别的语言快？follow up：为什么C++比别的需要compile的语言也快？」[S]：language features, shared memory, system design | OA 100 分钟 | 挂 | https://www.1point3acres.com/interview/thread/1011799 ；https://t.me/s/usinterview/16248 | 摘要 / 中 |
| A14 | 2023-08-10 | SWE | 技术电面 | — | [P]「问题：Given n, write a function sum up 1 to n recursively? Follow-ups: [隐藏]」[S]：handling overflows, recursion optimizations | — | 未知 | https://www.1point3acres.com/interview/thread/1009358 ；https://t.me/s/usinterview/16195 | 摘要 / 中 |
| A15 | 2023-06-28 | SDE 全职（本科） | 第一轮电面 | — | [S]：interview rounds, system design and algorithm focus, recruiter insights；预览称准备方向是项目经历 + 可能的算法 | — | 一轮游 / 挂 | https://www.1point3acres.com/interview/thread/1001963 ；https://www.1point3acres.com/bbs/thread-1001963-1-1.html（CF） | 摘要 / 低 |
| A16 | 2023-03-09 | SWE 全职 | 第一轮电面 | C++ | [S]：C++ versions, IPC methods, classic buy stock algorithm problem with follow-up | — | 未知 | https://www.1point3acres.com/interview/thread/974931 | 摘要 / 中 |
| A17 | 2022-11-10 | SWE 全职（Quant 公司） | 技术电面 | — | [S]：tail recursion and ticker hashing techniques；「Positive interview with an encouraging senior interviewer」 | — | 未知 | https://www.1point3acres.com/interview/thread/944714 | 摘要 / 中 |
| A18 | 2022-10-19 | SWE 全职 | OA + 电面 | — | [S]：test cases, system design, interprocess communication topics | — | 未知 | https://www.1point3acres.com/interview/thread/938472 | 摘要 / 低 |
| A19 | 2022-02-15 | SWE 全职，芝加哥 | 技术电面 | C++ / Java | [S]：Chicago-based quant trading firm requiring proficiency in **C++ and Java** | — | 未知 | https://www.1point3acres.com/interview/thread/851894 | 摘要 / 低（唯一提到 Java 的 1p3a 摘要） |
| A20 | 2021-02-11 | SWE，芝加哥办公室 | 第一轮电面 | C++ | [S]：C++ basics, recursion, error handling, optimization techniques | — | 未知 | https://www.1point3acres.com/interview/thread/715829 | 摘要 / 低 |

### 1.2 Blind / Glassdoor / WSO / 其他（电话 / 视频 / onsite）

| # | 日期 | 角色 / 地点 | 阶段 | 语言 | 题目（原文 / 摘要） | 时长 | 结果 | 来源 URL | 可达性 / 可信度 |
|---|---|---|---|---|---|---|---|---|---|
| B1 | 2024-08-22（评论日） | Research Developer / 软件岗（OP 3 YOE，评论者为 Google 员工） | OA → **1 小时 Zoom（工程师）** | C++（隐含） | OA「a known LeetCode question」（评论称 LeetCode 论坛有 "headlands oa" 帖）。Zoom：「started with summing natural numbers without the formula, then added optimization variants. A second question covered optimizing a C++ unordered_map for stock tickers.」 | **1 小时** | **36 小时内被拒**（评论者称赞回复快） | https://www.teamblind.com/post/headlands-technologies-research-developer-interview-process-pcb637t7 | 200（WebFetch 摘要转述，非逐字）/ 中 |
| B1b | 同上（2024-08-22） | 另一评论者（G-Research 标签），初级 C++ | OA + 3 轮算法，未 onsite | C++ | 「junior C++ role last year… online assessment and three algorithm rounds but no onsite」；评论位于 Headlands 帖内，是否指 Headlands `推断`（未明说） | — | 无 onsite | 同上 | 200 / 低 |
| B2 | 2023-02-18 | 未写（标签 Google） | HackerRank → 两次 1-on-1 → onsite | — | OP 问「leetcode or cpp trivia」→ OP 答「Both」；Jump Trading 评论者称自己的流程「A lot of questions about background」+ 少量 SWE 题 | — | 未报告 | https://www.teamblind.com/post/headlands-onsite-8hporjad | 200（WebFetch 转述）/ 中 |
| B3 | 2020-09-20 | 未写 | HackerRank（猎头联系）→ 电话 | — | 无题目；OP 2020-10-16 回复「被拒」；2022-12 / 2023-02 / 2023-04 评论者称自己也是「一电后排第二电」 | — | OP 被拒 | https://www.teamblind.com/post/has-anyone-interviewed-with-headlands-technologies-llc-xueqf3d3 | 200（转述）/ 中 |
| G1 | 日期未显示（RVW104113166，≈2026） | Software Engineer，芝加哥 | HackerRank | C++ | 「Interviewed. very hard. It was a 2 hour hacker rank and the question was very challenging. make sure you study c++ before hand. otherwise you'll not be prepared.」Question 1：「Solve this C++ question in under 2 hours」 | **2 小时** | 无 offer；体验 positive、难度 difficult | https://fr.glassdoor.ca/Entretien/Headlands-Technologies-Entretien-E715901-RVW104113166.htm | 200（经 r.jina.ai；www.glassdoor.com 403/CF）/ 高 |
| G2 | **2026-02** | 未写，**Amsterdam** | C++ HackerRank OA → 1-on-1 Zoom（developer 或 researcher）→ 后续轮 | C++ | 「The process starts with a C++ HackerRank online assessment, followed by a 1-on-1 Zoom interview with a developer or researcher. The OA problems are medium-to-hard difficulty. Later rounds covered algorithms, OS concepts, concurrency, and open-ended systems questions.」Question 1：「dp on trees problem, making market order book in c++」 | 全程 3 周 | 无 offer；neutral / average | https://fr.glassdoor.ca/Entretien/Headlands-Technologies-Entretien-E715901-RVW89062704.htm（正文经同页镜像读到：RVW104113166 页内含此条） | 200 / 高 |
| G3 | 日期未显示（RVW98042384） | Software Engineer | **第一轮视频电话** | — | 「The first round of the interview was conducted via video call. … how I would identify and remove unused code from a company's codebase.」Question 1：「removing unused or dead code in a large company's codebase」；评论称该题偏窄、HFT 公司很少删代码 | — | 无 offer；negative / difficult | https://fr.glassdoor.ch/Entretien/Headlands-Technologies-Entretien-E715901-RVW98042384.htm | 200（经 r.jina.ai 的 .ch 域）/ 高 |
| G4 | 2026（月未知，搜索摘要） | 高级 C++ 岗（搜索工具转述） | HackerRank | C++ | 「2 hours, 1 question … wording very intentionally convoluted … roughly a LeetCode hard, with malformed input」；另一条：「100 minute hackerrank question … rejected without feedback」；另一条：算法约 5 分钟可解，但「read the input from STDIN and … STDOUT」解析耗时 | 100–120 分钟 | 拒 | https://www.glassdoor.com/Interview/Headlands-Technologies-Software-Engineer-Interview-Questions-EI_IE715901.0,22_KO23,40.htm | **摘要**（www/.co.uk/.com.hk 均 403 / CF；以上为 WebSearch 转述）/ 低 |
| W1 | 2025-03（提交 2025-04-02） | SWE Generalist，Chicago | OA（LeetCode 题）→ 1-on-1 行为面（兼 company fit）→ **3 小时 final：2 轮技术 + 1 轮行为** | — | 「Leetcode hard, best time to buy and sell stock」 | <1 个月 | No Offer | https://www.wallstreetoasis.com/company/headlands-technologies-llc/interview | 200（经 r.jina.ai）/ 高 |
| W2 | 2020-09（提交 2020-11-24） | SWE new grad，Chicago | 仅 C++ 在线测试 → 较难电话面（系统设计 + C++ 经验） | C++ | 「Differences between C++ 11, 14, 17, and 20」 | <1 个月 | No Offer | https://www.wallstreetoasis.com/company/headlands-technologies-llc/interview（子页 …/interview/swe-new-grad） | 200 / 高 |
| W3 | 2020-03（提交 2020-04-05） | quant researcher（DC），仅作 OA 题面参照 | HackerRank，1 题 / 100 分钟，**必须 C++** | C++ | 「Given a list of jobs that are chained, generate all the job chains. Each line of the input is in the following format: job_id, run_time_in_seconds, next_job_id (this field is 0 for the the last job in the chain). You are asked to output a section for each job chain, in the following format: start_job_id, last_job_id, num of jobs: job chain run time, in hh:mm:ss format, average job time in ths chain. There are only 2 test cases in the OA, so you have to come up with test cases on your own.」 | 100 分钟 | 2 天后被拒（测试全过未知） | https://www.wallstreetoasis.com/company/headlands-technologies-llc/interview | 200 / 高 |
| W4 | 2020-02-28 | quant researcher（WSO 论坛） | HackerRank，仅 C++ | C++ | 回复：「The algorithm part is a medium to hard leetcode question. 100 min. Given a csv file, each row being (start_job, time, next_job), Your job is to detect if the input data is an union of single linked list; then compute the total time to finish all jobs, the total number of jobs, average time per job. Read the csv file, run an algorithm, writing output.」 | 100 分钟 | — | https://www.wallstreetoasis.com/forum/hedge-fund/headlands-tech-interview-online-assessment | 200（经 r.jina.ai；直连 403）/ 中 |
| T1 | 2020-03（GitHub gist，最后更新 2025-03-25） | 题解，非面经 | HackerRank 同一道 job-chain 题 | C++ | 代码按 `next_job_id` 串链，输出首尾 job、个数、总时长与平均时长（HH:MM:SS）；非法行或不在链中的 job → 输出 "Malformed Input" 并 exit -1 | — | — | https://gist.github.com/tobyjbanks/d9c3b05c26f0dc55df309a96c800a19b | 200 / 中（作者自述，非官方题面） |

### 1.3 SWE HackerRank / OA（1p3a，正文被锁；[S] 摘要 + [P] 预览）

| # | 日期 | 角色 | 语言 | 题目（摘要 / 预览原文） | 时长 | 结果 | 来源 URL | 可达性 / 可信度 |
|---|---|---|---|---|---|---|---|---|
| O1 | 2026-08-17 | SWE 全职，跳槽 | **非 C++ 也考** | [P]「考的job runnner， 参考这篇。不是c++也会考这题。花时间准然后做题，test全过提交，过了一周邮件通知拒了。感觉是先oa再看简历」[S]：job runner test, preparation, rejection timeline | — | 一周后被拒（测试全过） | https://www.1point3acres.com/interview/thread/1186508 ；https://t.me/s/usinterview/29380 | 摘要 / 中 |
| O2 | 2026-03-21 | SWE 全职，跳槽 | — | [S]：SWE FT OA at the hedge fund（无题目） | — | — | https://www.1point3acres.com/interview/thread/1169644 | 摘要 / 低 |
| O3 | 2025-10-30 | SWE 全职，跳槽 | — | [S]「most difficult full-time software engineer online assessment … a complex disaster recovery problem requiring extensive input handling」 | — | — | https://www.1point3acres.com/interview/thread/1152383 | 摘要 / 中 |
| O4 | 2025-02-07 | SWE 全职，跳槽 | — | [S]：test format and problem types（无题目） | — | — | https://www.1point3acres.com/interview/thread/1111077 | 摘要 / 低 |
| O5 | 2024-11-03 | Software Developer（站内归类金工） | C++ | [P]「OA出了地里没有的新题，需要写个并查集和处理异常case。…Sample1：6 id 8 timestamp 200 quicksort.cpp …」[S]：disjoint set algorithms and exception handling | — | — | https://www.1point3acres.com/interview/thread/1095582 ；https://t.me/s/usinterview/20210 | 摘要 / 中 |
| O6 | 2024-01-01 | SWE 全职 | **一定要用 C++** | [P]「Test cases都pass了，也不知道为啥挂了 就一道题，在图里啦」（题在图片中） | — | 全过仍挂 | https://www.1point3acres.com/interview/thread/1036062 ；https://t.me/s/usinterview/17160 | 摘要 / 中 |
| O7 | 2023-08-24（并入 A13） | SWE（C++） | C++ | OA「就是地里那道，只有100分钟…」 | 100 分钟 | — | 见 A13 | — |
| O8 | 2023-07-14 | SDE 全职 | — | [S]「Exact Repeat」：题目未变，注意 clean code 与边界 | — | — | https://www.1point3acres.com/interview/thread/1004587 | 摘要 / 低 |
| O9 | 2023-06-26 | SDE 全职 | C++ | [S]：test format, real questions, C++ coding, error-handling advice | — | — | https://www.1point3acres.com/interview/thread/1001711 | 摘要 / 低 |
| O10 | 2023-05-23 | SWE | — | [S]：input validation and graph traversal precautions | — | — | https://www.1point3acres.com/interview/thread/996155 | 摘要 / 低 |
| O11 | 2023-04-19 / 2023-03-28 | SWE / 其他 | — | [S]：「main focus areas … best data structures」（989188）；test case details + 结果更新（982411） | — | — | https://www.1point3acres.com/interview/thread/989188 ；https://www.1point3acres.com/interview/thread/982411 | 摘要 / 低 |
| O12 | 2022-11-09 | NG（站内归类 6） | — | [S]「Job Chain Metrics Problem … building and reporting job chain metrics from job runtimes, emphasizing output formatting challenges」 | — | — | https://www.1point3acres.com/interview/thread/944240 | 摘要 / 中 |
| O13 | 2022-08-21 | SWE（C++ NG） | C++ | [S]：strict testcases and common input pitfalls | — | — | https://www.1point3acres.com/interview/thread/921628 | 摘要 / 低 |
| O14 | 2022-01-04 / 2021-09-18 | SWE 全职 | C++ | [S]：835627 problem-solving and data structures；799106 "Headlands Tech Coding Test - C++" | — | — | https://www.1point3acres.com/interview/thread/835627 ；https://www.1point3acres.com/interview/thread/799106 | 摘要 / 低 |
| O15 | 2022-03-30（QR，OA 题面参照） | Quant Finance | — | [S]「Job Runner challenge … distributed computing job chains. Includes input/output formats and error handling guidelines」；搜索转述原文：「解析CSV格式作业日志、按链汇总、格式错误报错；测试用例只有题目中给的两个例子；需为不符合格式的输入做较多边界检查」 | — | 通过（搜索转述：结果=通过） | https://www.1point3acres.com/interview/thread/876489 （旧 URL https://www.1point3acres.com/bbs/thread-876489-1-1.html） | 摘要 / 中 |
| O16 | 旧帖（2019–2021，日期未取到） | SWE / Developer | C++ | 搜索转述：「Headlands Tech Developer Test-C++ 100 minutes on HackerRank 还是那个job runner/chains那道题」；另一贴「独立环，多个parent，多个children等边界情况是讨论的重点」 | 100 分钟 | — | https://www.1point3acres.com/bbs/interview/headlands-engineering-638585.html （CF） | 摘要 / 低 |

### 1.4 聚合站（带日期的二手，仅作交叉印证）

| # | 日期 | 内容 | 来源 URL | 可达性 / 可信度 |
|---|---|---|---|---|
| X1 | 2026-09（页内标 "seen" 月份） | QuantVault 把 Headlands 的 56 题标了「最近一次报告月」：Streaming Queue with Mean and Snapshots（2026-03）· Maximum Concurrent Orders in an Interval（2025-06）· As-Of Join on a Timestamped Table（2024-10）· Merge K Sorted Streams with Bounded Concurrency（2024-06）· Top K Tickers by Notional（2024-05）· Order Management API with Sublinear Queries（2024-05）· Find the First Failing Transaction（2023-08）· Recursive Sum 1 to N with Overflow and Stack Limits（2023-08）· Mutable Default Arguments in Python（2022-11）· Job Runner（2022-03）。**题面是站方改写，单题页面已是乱码 / 付费墙**；月份与 A1/A5/A6/A7/A9/A14 对得上 `推断`（它们是这些 1p3a 帖的二次加工，**不算独立来源**） | https://quantvault.org/headlands-interview-questions.html | 200 / 中（只取标题 + 月份） |
| X2 | 2026-09-19 | PracHub 转载 1p3a #1189414（Research Developer OA，2026-08）：10 道统计 MCQ；4 道 OLS / Sharpe / 最小化 E[\|x−c\|]；**C++：给 float 数组与窗口 k，求每个滑窗均值，处理 inf / −inf / nan**；2 道 medium LC（其一：最少改几个字符使相邻字符都不同）；并写明「两年前的 OA 还是 C++ 手动解析输入字符串 + 时间戳 + Kahn 算法算依赖图」 | https://prachub.com/interview-experiences/headlands-research-developer-interview-experience-a-four-part-online-assessment-on-stats-ols-and-cplusplus | 200 / 中（与 1p3a 同源，不独立） |
| X3 | 2026-09-06 | PracHub 备考文：只有 5 道通用练习题，无 Headlands 真题；引用 "Wall Street Oasis March 2025 SWE" = 本文 W1 | https://prachub.com/resources/headlands-technologies-swe-intern-2027-c-algorithms-and-trading-systems-interviews | 200 / 低（SEO 式） |
| X4 | 2026-09-04 / 2026-08-18 | techinterview.org、quantt.co.uk、quantvault 流程页：「3–5 轮、3–6 周；电话 45–60 分钟；final 3–5 场」。**示例题是泛化的 "representative phrasings"，无出处，不采信**，仅记录其流程描述 | https://www.techinterview.org/post/3233477385/headlands-technologies-quant-interview/?format=md ；https://www.quantt.co.uk/resources/headlands-technologies-interview ；https://quantvault.org/headlands-interview-process.html | 200 / 低 |

## 2. 题目汇总（按题型归并，#refs = 独立来源数；同一帖被多处转载只算 1）

| 题型 | 内容（尽量逐字） | 出现的报告 | #refs | 阶段 | 最近 |
|---|---|---|---|---|---|
| **Q1 递归求 1..n 之和 / 不用公式 / 溢出 / 栈 / 尾递归** | 「Given n, write a function sum up 1 to n recursively? Follow-ups: …」；「summing natural numbers without the formula, then added optimization variants」；[S] handling overflows, recursion optimizations, tail recursion | A14（1p3a 2023-08）· A17（1p3a 2022-11，tail recursion）· B1（Blind 2024-08）· A20（1p3a 2021-02，recursion + error handling，较弱） | **3–4** | 电话 / 视频第一题 | 2024-08 |
| **Q2 `unordered_map` / 股票代码哈希优化** | 「optimizing a C++ unordered_map for stock tickers」；[S] ticker hashing | B1（Blind 2024-08）· A17（1p3a 2022-11） | **2** | 电话 / 视频第二题 | 2024-08 |
| **Q3 订单 / 交易事件处理（order book 家族）** | 订单区间最大重叠 + 按买卖方处理撤单（A5）；Put / Delete(unique_id, quantity) 等 4 个 API（A9）；trading events coding challenge（A8）；trading 相关 OOD（A4）；「dp on trees problem, making market order book in c++」（G2） | A5 · A9 · A8 · A4 · G2 | **5** | 电话 / 视频 | 2026-02 |
| **Q4 买卖股票 DP** | 「best time to buy and sell stock」（W1，LeetCode hard 指带约束的变体 `推断`）；[S]「stock trading related LeetCode problems … DP … detailed state tracking」（A3）；[S] classic buy stock algorithm + follow-up（A16） | A3（1p3a 2025-12）· A16（1p3a 2023-03）· W1（WSO 2025-03） | **3（互相独立）** | 电话 + 3h final | 2025-12 |
| **Q5 流式数据结构** | 「实现一个queue 和三个函数 push pop 和 get_mean … 第二问是实现一个带有 sn[apshot]…」（A1）；merge multiple data streams（C++）+ multithreaded non-blocking follow-up（A6）；merge k sorted lists / streaming（A7） | A1 · A6 · A7 | **3** | 电话 | 2026-03 |
| **Q6 C++ 语言深度** | 「为什么C++比别的语言快？follow up：为什么C++比别的需要compile的语言也快？」（A13）；C++ vs Python 区别 + smart pointers（A8）；「Differences between C++ 11, 14, 17, and 20」（W2）+ IPC（A16）；IPC / 共享内存 / system design（A13, A18）；OS concepts, concurrency（G2）；debugging + bitwise in a code framework（A2）；compile error 现场修（A7） | A13 · A8 · W2 · A16 · A18 · G2 · A2 · A7 | **≥6** | 电话 / 后续轮 | 2026-02 |
| **Q7 如何识别并删除大型代码库里的无用代码** | 「removing unused or dead code in a large company's codebase」（第一轮视频） | G3 | **1** | 首轮视频 | 日期未显示 |
| **Q8 HackerRank：job runner / job chain CSV** | 输入每行 `job_id, run_time_in_seconds, next_job_id`（0 = 链尾）；输出每条链：首 job、尾 job、个数、总时长 hh:mm:ss、平均时长；检测数据是否是若干单链表的并；格式错误 → 报错 / "Malformed Input"；公开用例只有 2 个，边界（环、多 parent、多 children）要自己造 | W3 · W4 · T1 · O15 · O12 · O13/O9（C++ OA）· O8（原题未变）· O16 · O1（2026-08 仍考） | **≥8** | HackerRank，100–120 分钟，1 题 | **2026-08** |
| **Q8b 变体** | 并查集 + 异常 case（O5，2024-11）；disaster recovery，大量输入处理（O3，2025-10）；手写解析输入 + 时间戳 + Kahn 拓扑（X2 提及的「两年前」版本）；2026-08 QR / RD 版换成 4 段（统计 MCQ + OLS + C++ 滑窗均值含 inf / nan + LC） | O5 · O3 · X2 | 各 1 | HackerRank | 2026-09 |
| **Q9 HackerRank 题量 / 时长** | 1 题 / 100 分钟（2020、2023）· 1 题 / 120 分钟、只能 C++（2024-11）· 「17 题 / 70 分钟」（1124806，QR 新卒帖，2025-04）· 2 小时 1 题，题面刻意绕、近 LC Hard（G1, G4） | W3 · A13 · 1097225 · 1124806 · G1 · G4 | — | HackerRank | 2026 |
| **Q10 其他** | 带 sublinear 查询的订单管理 API（A9）；as-of join、top-K tickers by notional（仅 X1 标题，无一手来源，**不采信**） | — | — | — | — |

**过线（cut line，手工归类，未用脚本计数，待 orchestrator 复核）**：Q1 / Q3 / Q4 / Q5 / Q6 / Q8 六类涵盖了本表里所有「有题目线索」的 SWE 电话 / 视频 / OA 报告；六类之外只有 Q7（1 次）、Q8b 变体与题面不可见的帖子。

## 3. QR / QT / 其他岗位（只列索引，不展开；来源 = 1p3a 公司列表 [L]+[S]）

| tid | 日期 | 标题 | 类别 | URL |
|---|---|---|---|---|
| 1192691 | 2026-10-11 | Headlands Technology Full Time QR OA | QR | https://www.1point3acres.com/interview/thread/1192691 |
| 1189518 | 2026-09-14 | QR 27 NG 面筋（实习，OA + tech phone screen） | QR 实习 | https://www.1point3acres.com/interview/thread/1189518 |
| 1189414 | 2026-09-13 | [头地] Research Developer OA | QR / RD | https://www.1point3acres.com/interview/thread/1189414 |
| 1187591 | 2026-08-27 | 头地 OA（概率 + 统计 + C++/Python/Java 编码） | 其他 | https://www.1point3acres.com/interview/thread/1187591 |
| 1171822 | 2026-04-06 | FPGA 岗 OA | FPGA | https://www.1point3acres.com/interview/thread/1171822 |
| 1153784 | 2025-11-09 | Quantitative Researcher 电面 | QR | https://www.1point3acres.com/interview/thread/1153784 |
| 1151303 / 1151304 | 2025-10-23 | Quant 实习 tech phone（假设检验、OLS、STL、C++） | QR 实习 | https://www.1point3acres.com/interview/thread/1151303 |
| 1147809 | 2025-09-28 | 体验不好的面试（大量 BQ + 简历） | QR | https://www.1point3acres.com/interview/thread/1147809 |
| 1124806 | 2025-04-18 | 新 hackerrank 17 题 / 70 分钟 | QR 新卒 | https://www.1point3acres.com/interview/thread/1124806 |
| 1116577, 1105729, 1104233, 1097225, 1090391, 1089532, 1022231, 995755, 941778, 929474, 674051 | 2022–2025 | QR / QT 的 OA、HR、电面、8 轮 onsite | QR | 同模式 `/interview/thread/<tid>` |

## 4. 来源可达性台账

| 来源 | 路径 / 结果 | 备注 |
|---|---|---|
| 1p3a `/interview/company/headlands` | 直连 200（带普通 UA），含 SSR 列表；分页走 `trpc.1point3acres.com/trpc/…getInterviewThreadList`，共 56 帖 | [L] 列表 + 日期可靠 |
| 1p3a `/interview/thread/<tid>` | 200 但正文「Please log in」；`getTranslation` 公开摘要可读；`getEnglishMessage`、`getExternalInterviewThreadDetail` 返回 401 | 未绕过登录 |
| 1p3a `/bbs/thread-*`、`/bbs/tag/*`、`/bbs/interview/*` | 直连 403（Cloudflare 挑战）；r.jina.ai 同样被挑战；web.archive.org 429；m.1point3acres.com 空响应 | 靠 Telegram 镜像 `t.me/s/usinterview` 取开头预览 |
| Telegram `t.me/s/usinterview?q=…` | 200，22 条 Headlands 预览（2023-08 至 2026-09） | 预览为原帖前 ~100 字，被作者隐藏的部分显示为「本内容被作者隐藏」 |
| Glassdoor `www/.co.uk/.com.hk/.ca/.sg` | 403 / CF（含 r.jina.ai）；`fr.glassdoor.ca` 与 `fr.glassdoor.ch` 经 r.jina.ai 可读到 3 条评论 | G1–G3 来自此路径 |
| Blind | 3 个帖 WebFetch 200（转述） | 评论被折叠 / 需登录看全 |
| WSO `/company/…/interview` 与论坛帖 | 直连 403；r.jina.ai 200 | W1–W4 |
| LeetCode Discuss | 站内搜索无 "Headlands" 结果（WebSearch 无命中；LeetCode 本身拒抓） | Blind 评论称有 "headlands oa" 帖，未找到 |
| Reddit | WebSearch 域名被封；`old.reddit.com` 经 r.jina.ai 403；未取到任何 r/cscareerquestions / r/quant / r/csMajors 帖 | |
| QuantNet | 搜索无 Headlands 帖 | |
| PracHub | 公司页 5 题（统计 / 编码 / ML / SWE 基础，多为 QR 方向），无 SWE 电面真题 | X2、X3 |
| tradermath.org | 页面无 Headlands 标签，不采信 | |

## 缺口（Chi 需要手动打开的 URL）

1. **一小时视频电话的题目全文**（最有价值）：登录 1p3a 后打开 https://www.1point3acres.com/interview/thread/1169914 （2026-03，queue + get_mean + snapshot）、https://www.1point3acres.com/interview/thread/1154043 （2025-11，debugging + 位运算）、https://www.1point3acres.com/interview/thread/1156658 （2025-12，股票 DP）、https://www.1point3acres.com/interview/thread/1134455 （2025-06，订单区间重叠 + 撤单）、https://www.1point3acres.com/interview/thread/1089956 （2024-10，合并多路数据流 + 多线程）、https://www.1point3acres.com/interview/thread/1068621 与 https://www.1point3acres.com/interview/thread/1066045 （2024-05，C++ vs Python / 智能指针 / 订单 API）。这些帖的预览显示正文有「被作者隐藏」段，需要积分或回复才可见。
2. **Java 是否可用于 HackerRank / 电面**：全部来源里只有 A19 摘要（2022-02，"C++ and Java"）和 1187591 摘要（C++/Python/Java）提到 Java；多数来源称 HackerRank「只能 C++」。请向招聘方确认电面语言，再决定是否准备 C++ 版本。
3. **Glassdoor 全部评论**：浏览器打开 https://www.glassdoor.com/Interview/Headlands-Technologies-Interview-Questions-E715901.htm 和 https://www.glassdoor.com/Interview/Headlands-Technologies-Software-Engineer-Interview-Questions-EI_IE715901.0,22_KO23,40.htm （全站 403 / CF，仅 3 条经镜像读到；搜索摘要显示总数约 57 条）。
4. **Blind 折叠评论**：https://www.teamblind.com/post/headlands-technologies-research-developer-interview-process-pcb637t7 和 https://www.teamblind.com/post/has-anyone-interviewed-with-headlands-technologies-llc-xueqf3d3 登录后展开回复；Blind 搜索 "Headlands" 还可能有更多帖。
5. **LeetCode Discuss**："headlands oa" 帖（Blind 评论提及）未找到；请在 LeetCode Discuss 站内搜索。
6. **Reddit / QuantNet / WSO 论坛其余帖**：本环境无法访问 Reddit；建议手工搜 `site:reddit.com "Headlands Technologies" interview`。
7. **日期缺失**：Glassdoor G1、G3 页面不显示日期（G2 为 2026-02）；A12、A15、A18 仅有发帖日，无面试月份。
8. **1p3a 列表第 2–3 页的 36 个旧帖**（2021–2024）只拿到 [S] 摘要；其中 SWE 的 OA 帖（O8–O14）都没有题面。
