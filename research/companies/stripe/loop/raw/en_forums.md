# Stripe SWE 面试 Loop（OA 之后）——英文网络情报汇总（2022–2026）

> 范围：Stripe 软件工程师（New Grad / L1–L2 / Intern 为主，兼收 L3 及以上作为对照）在 HackerRank OA **之后**的全部轮次。
> 来源：Blind（teamblind.com）、LeetCode Discuss、Medium、Taro（jointaro.com）、interviewing.io、Exponent、interviewdb.io、programhelp.net、linkjob.ai、interviewfox.ai、GreatFrontend、Coditioning、Leon Consulting、IGotAnOffer、Simplify、Levels.fyi、staffengprep、codinginterview.com、oavoservice、prachub、TechPrep、Verve、FinalRound、SystemDesignHandbook、Educative、GitHub `stripe-interview` org 等。
> 采集日期：2026-09-01。共执行约 50 次搜索、抓取约 110 个页面。Glassdoor 全站被 Cloudflare 拦截（含通过代理），LeetCode/Medium 通过 r.jina.ai 代理读取。
> 约定：每条事实后面给出 `[来源编号 / URL / 帖子日期]`。英文引文只作证据、尽量短。"日期未知"表示页面未显示年份。
> 说明：Stripe 的等级体系：L1（new grad）/L2/L3 都叫 "Software Engineer"，L4+ 叫 Staff；没有 "Senior" 头衔。[Exponent guide, https://www.tryexponent.com/guides/stripe-software-engineer-interview, 2026]

---

## 0. 全局速览（先看这个）

**整体流程（2024–2026 主流报告）：**

1. 简历筛 → 2. HackerRank OA（60 min，1 题 3–4 part，仅 SWE/校招）→ 3. Recruiter 电话（30 min，有时在 OA 之前）→ 4. Technical Phone Screen / "Team Screen"（60 min，1 题 3–4 part 递进）→ 5. Virtual Onsite（新人 3 轮：Programming Exercise + Bug Squash + Integration；有经验者 5 轮：+ System Design + Behavioral/HM）→ 6. Hiring Manager Chat（校招常单独安排在 onsite 之后 3–4 个工作日）→ 7. Hiring Committee（每周开会）→ 8. Team match（若有）→ 9. Offer。

**校招 vs 社招轮次差异：**
- New grad / intern：OA → tech screen → VO 2–3 轮（coding、bug squash、integration；有时只有 coding + integration）→ HM/behavioral。**通常没有独立 system design 轮**。[LeetCode 7566910, https://leetcode.com/discuss/post/7566910/, 2026] [Blind 08mn2g87, https://www.teamblind.com/post/stripe-on-site-interviews-prep-08mn2g87, 2025-11-23] [Medium diyaag, https://medium.com/@diyaag2020/my-stripe-interview-experience-2025-2026-a-journey-to-the-final-round-19990fa6876a, 2025-11] [Exponent SD blog, https://www.tryexponent.com/blog/stripe-system-design-interview, 2026]
- L2/L3 社招：5 轮 onsite（Programming、Bug Squash、Integration、System Design、HM/Behavioral），常分两天。[Blind n4mqgn4g, https://www.teamblind.com/post/stripe-onsite-interview-experience-n4mqgn4g, 2024-04-19] [Blind cnhknchr, https://www.teamblind.com/post/share-my-stripe-interview-experience-cnhknchr, 2025-07-17]
- Staff+：把 Integration 换成 Presentation（一页纸项目总结 + 演讲）。[interviewing.io, https://interviewing.io/stripe-interview-questions]

**2025–2026 变化：**
- 2026 年新增 **AI Programming Exercise** 轮（HackerRank 内嵌 AI 聊天窗口，"lightweight Cursor"），约 30 min 编码，考察"能否指挥/验证/调试 AI 输出而不是关掉大脑"。[interviewdb AI guide, https://www.interviewdb.io/guides/stripe-ai-programming-exercise, 2026-06-09] [interviewfox, https://interviewfox.ai/interview-questions/stripe-oa-hackerrank-guide/, 2026]
- 其他轮次仍**严禁 AI**："AI use in Stripe interviews is strictly prohibited" [interviewing.io]；Stripe 员工："you can use whatever IDE you want so long as there's no AI agent in it" [Blind 1j2ckbta, https://www.teamblind.com/post/need-help-regarding-stripe-interview-1j2ckbta, 2025-12-22]。
- 2024 起 Stripe 加快题库轮换频率，因为发现候选人"答题速度和流利度过于惊人，像是见过原题"，内部人建议"表现自然一点"。[interviewdb insider, https://www.interviewdb.io/guides/insights-on-stripe-interviews-from-an-insider]
- 校招 OA 通过率约 13%（2025-11，16 名美国候选人样本）；Taro 统计 new grad 岗 pass rate 13%，SWE 岗 11%。[InterviewCoder, https://www.interviewcoder.co/blog/stripe-software-engineer-interview] [Taro, https://www.jointaro.com/interviews/companies/stripe/experiences/software-engineer-new-grad-united-states-november-5-2025-no-offer-neutral-d8d78bbd/, 2025-11-05]

---

## 1. Recruiter Screen（HR 电话）

**格式/时长：** 30 分钟（IGotAnOffer 说 30–45），非技术闲聊。有些地区（印度）是 OA 先于 recruiter call。[interviewing.io] [IGotAnOffer, https://igotanoffer.com/en/advice/stripe-interview-process] [FinalRound, https://www.finalroundai.com/blog/stripe-interview-process]

**内容：** 背景、动机、对 Stripe 价值主张的理解、职业目标、想做的方向（Product Eng vs Infra Eng）。Stripe 是"hybrid hiring model"——你面的是具体 org（Product 或 Infrastructure），但面试官来自全公司。[interviewing.io]

**常见问题（据报道）：**
- "What do you know about Stripe?" / "What about Stripe makes you want to work here?" [Prepfully, https://prepfully.com/interview-guides/stripe-software-engineer]
- 30–60 秒自我介绍 + 1–2 个能讲深的项目 + 为什么 Stripe（要具体，"API-first, developer-focused mission"）。[Exponent guide]

**建议（来自 interviewing.io 的前 Stripe 面试官）：** "not reveal your salary expectations or where you are in the process with other companies"。[interviewing.io]

**第二次 recruiter call：** 过了 phone screen 后还有一个 30 min 的信息型电话，专门讲 onsite 各轮怎么考、发 prep doc 和各语言的 sample repo（让你提前配好 IDE/debugger）。[interviewing.io] [Blind mrsi2qqr, https://www.teamblind.com/post/any-example-for-stripe-onsite-bug-squash-and-integration-mrsi2qqr, 2022-01-28："Recruiter should have sent you a doc... sample repository in your preferred language"]

**Stripe 官方 prep repo：** GitHub org `stripe-interview` 下有 `python-interview-prep`、`java-interview-prep`、`javascript-interview-prep`、`ruby-interview-prep`、`cpp-interview-prep`、`csharp-interview-prep`、`scala-interview-prep`、`android-kotlin-interview-prep`、`react-native-interview-prep`、`ml-python-interview-prep`，描述为 "A sample repo to get setup to interview in JavaScript at Stripe"。[https://github.com/stripe-interview]（这些 repo 暗示了 Stripe 支持的面试语言集合。）

---

## 2. Hiring Manager Chat / HM Round / Behavioral / "Experience & Goals"

### 2.1 在流程中的位置
- **校招/实习：** 通常是最后一轮，在 VO 技术轮之后 3–4 个工作日单独安排，30–45 min。[Blind rmvygjeb, https://www.teamblind.com/post/new-grad-offer-likelihood-rmvygjeb, 2023-11-21："Manager chat: Occurred 3-4 business days later"] [Medium azn7u1, https://medium.com/@azn7u1/stripe-intern-oa-vo-experience-960450b750d4, 2025-11-14："Round 4: Behavioral Interview, HR-conducted"]
- **社招：** 是 onsite 5 轮之一，45–60 min，由 hiring manager 或 "Leveler"（相当于 Amazon Bar Raiser）主持。[interviewing.io] [Exponent guide]
- **有时在 tech screen 之前：** 一位班加罗尔 backend 候选人（2024-06）是 HM 直接联系他，先做 HM call（经历+leadership+motivation，并讲解整个流程），再做 screening。[LeetCode 5341224, https://leetcode.com/discuss/interview-experience/5341224/Stripe-or-Backend-Engineer-or-Bangalore-or-Jun-2024-or-Reject/, 2024-06]
- **前端：** 这一轮叫 "Experience and Goals"，兼做 HM 面试，pre-team-matching 从这里开始。[GreatFrontend, https://www.greatfrontend.com/interviews/company/stripe/questions-guides]
- **重要：** "Unlike Amazon, you won't be asked behavioral questions in other rounds, just like this one." 行为面只集中在这一轮。[interviewing.io]
- 有候选人报告 onsite 里"本来以为有 bug bash，结果换成了 HM screen"（team specific）。[Blind x7beaq87, https://www.teamblind.com/post/stripe-onsite-x7beaq87, 2025-04-02] [Blind sfaggc1a, https://www.teamblind.com/post/stripe-frontend-onsite-sfaggc1a, 2024-11-11]
- 也有报告 onsite 同时有一个 30 min 的 **PM 主持的 behavioral**（聊 conflicts 和 good work experiences）+ 另一个 HM 轮。[Blind x7beaq87, 2025-04-02]

### 2.2 评分依据：Stripe Operating Principles
六条：**Users first / Create with craft and beauty / Move with urgency and focus / Collaborate without ego / Obsess over talent / Stay curious**。"Interviewers use them as an active evaluation framework"，面试官写 feedback 时会对照这些原则。[Exponent guide] [interviewing.io："Evaluation Framework: Aligned with Stripe's Operating Principles (analogous to Amazon's Leadership Principles)"]

Exponent 给的对应关系：
- Users first → 是否考虑下游影响
- Craft and beauty → 代码质量与细节
- Urgency and focus → 快速推进最重要的事
- Collaboration without ego → 争论、分享 credit、从错误中学习
- Obsess over talent → 提高标准
- Curiosity → 主动学不熟的东西

### 2.3 具体被问到的问题（实录）
- "Why Stripe?"；5 年职业规划；面试官当场翻 LinkedIn 问"毕业后 3–4 个月空窗期"、"为什么你每次升职后就跳槽"。[rampatra blog, https://blog.rampatra.com/stripe-interview-for-software-engineer, 2020-01（都柏林，较旧但结构未变）]
- New grad HM："Focused on teamwork, past work, ownership, and how I approach problems." [LeetCode 7566910, 2026]
- 实习 HM（班加罗尔 2025-11）：聊之前的 Amazon 实习、deadline 管理、任务拆解、团队合作、ownership、沟通、错误处理；"round was brief and direct"；候选人因网络故障+沟通 gap 被拒。[Medium diyaag, 2025-11]
- 社招 HM："asked a few tough behavioral questions that I felt I got stumped on"，包括**喜欢多大的团队、你的 engineering philosophy**。[Blind x7beaq87, 2025-04-02]
- Prepfully 列出的样题："What is something you would have done differently in a project?"、"Describe disagreement with team decision and your response"、"Share mistake and what you learned"。[Prepfully]
- linkjob 2026 记录（约 1 小时）：学习新技术的经历、如何回应批评、自动化测试工具熟悉度、分析能力例子、与 Stripe 价值观契合度。[linkjob SWE, https://www.linkjob.ai/interview-questions/stripe-software-engineer-interview/, 2026-02-12]
- programhelp 5 轮 VO 的 HM 轮：项目 deep dive，强调 personal initiative 和 teamwork，"准备 2–3 个项目故事"。[programhelp VO, https://programhelp.net/en/vo/stripe-vo-interview-5rounds-experience-guide/, 2025-08-07]
- Verve 汇总的行为题（23–30 号）：难的技术 trade-off 项目、和同事有分歧、为什么离开现职、为什么 Stripe、超出职责范围的 ownership、紧约束下 ship、如何快速上手新代码库、主动发现并修问题。[Verve, https://www.vervecopilot.com/blog/how-does-stripe-leetcode-really-work-and-how-to-prepare]
- Simplify（校招指南）："A real filter, not a formality"；准备具体的 "why Stripe / why payments"、协作故事、艰难决策故事、接受反馈的例子；反问 "What does success look like in the first six months?"；要熟悉自己实习的细节。[Simplify, https://simplify.jobs/blog/stripe-new-grad-swe-job, 2026]

### 2.4 HM 轮的"权重"
- Stripe 员工："they want all thumbs up or it's gonna be a rejection"，一个 lukewarm 的面试官就会被拒，"most managers won't pull rank on that part of the Stripe culture"。[Blind VPdSosJJ, https://www.teamblind.com/post/Stripe-interview-loop-rejection-VPdSosJJ, 2024-02-01]
- 但 interviewing.io 说：panel 写完 feedback 后开会，多数靠 consensus，"in cases where consensus isn't possible, the hiring manager has final say"。[interviewing.io]
- 校招 HM 后被拒："It took me about a week and half before I was rejected. They told me it was extremely close and went with someone with a bit more experience." [Blind k4acvawb, https://www.teamblind.com/post/stripe-new-grad-interview-with-manager-k4acvawb, 2021-10-14]
- 一位 Amazon 6.5 YOE 候选人 5 轮中 manager 轮"manager acknowledged good team fit"，SD 被夸 "You did very well"，仍因 bug squash 没做完被拒。[Blind umo0fobx, https://www.teamblind.com/post/onsite-experience-at-stripe-umo0fobx, 2021-06-19]

---

## 3. Technical Phone Screen（"Team Screen" / "Pre-onsite" / "Code pair"）

### 3.1 格式
- **时长：** 60 min，其中 45 min 编码 + 15 min 聊 Stripe/提问。[LeetCode 7566910, 2026："solve 4 parts within 45 minutes, followed by a 15-minute discussion"] [Medium diyaag, 2025-10："60 minutes (45 coding + 15 buffer)"] [Blind nqzaykah, https://www.teamblind.com/post/chances-with-stripe-screen-nqzaykah, 2025-10-27："They'll give you 35-45 mins to solve and rest for questions"]
- **平台：** Zoom + CoderPad 或 **自己的 IDE 共享屏幕**（候选人可选）；HackerRank 也有报告。[interviewing.io] [Blind a18jdcfu, https://www.teamblind.com/post/stripe-swe-phone-screen-how-to-prepare-a18jdcfu, 2024-02-19："Conducted on CoderPad"] [Glassdoor 摘要（通过搜索引擎片段）："60 minutes long, conducted over Hackerrank or your personal IDE"]
- **语言：** 任意。Stripe 员工："Language doesn't matter for the initial phone screen use whatever you're most comfortable with." [Blind 1gfdplee, https://www.teamblind.com/post/stripe-interview-language-1gfdplee, 2021-02-28]（但同帖一位自称 HM 的人说 PHP 会直接拒；后续轮次因为要给你代码，语言受限。）
- **题型：** 一道题 3–4 个 part 递进，"parts are connected"，做完一部分才给下一部分。**不是 LeetCode**："there will not be request response stuff in phone screening, it is meant to test your basic programming skills"（Stripe 面试官 Loki-b）。[Blind mdtk4bmj, https://www.teamblind.com/post/stripe-phone-screen-interview-mdtk4bmj, 2024-06-15]
- Stripe 员工 jughead69："There is no Leetcode. It's all practical programming problems. Read in this JSON, transform it/do something interesting with it, etc." [Blind jcnxxpsh, https://www.teamblind.com/post/stripe-phone-screen-interview-jcnxxpsh, 2025-09-28]
- **测试：** 需要自己构造输入并写测试；没有自动测例。"a lot of time got wasted because I expected automated test case execution rather than being required to generate the input on your own and write your own test cases." [LeetCode 6696304, https://leetcode.com/discuss/post/6696304/, 2025-04-28]
- **通过线：** 语言相关。"language-dependent minimum parts: 3 for Python, 2 for C++/Java"（另一人说"Minimum number of parts varies from question to question"）。[Blind 5d7673dy, https://www.teamblind.com/post/stripe-interview-prep-5d7673dy, 2025-11-03] Stripe 员工在另一帖："It could be 2 required to pass. It's hard to know without the question." [Blind nqzaykah, 2025-10-27] 常见现象：面试官做完第 2 part 就停下来转 Q&A，"There are usually 4 parts but interviewers may stop after the 2nd part"。[Blind nqzaykah]
- **prep 材料：** Stripe 发的材料强调 "quality over speed"，但候选人投入太多时间打磨代码反而挂。[Blind VPdSosJJ, 2024-02-01]

### 3.2 面试官看什么（据报道）
- "Clean, idiomatic code, with tests for all edge cases"；沟通思路是必须的。[Blind rptglpyd, https://www.teamblind.com/post/stripe-phone-screen-interview-rptglpyd, 2021-05]
- "Optimal algorithm does not matter"；主要是数组/哈希表；"The challenge is more in translating business rules in the question into good code quickly"。[Blind a18jdcfu, 2024-02-19]
- 阅读理解："programming problem, but overly verbose to check your reading comprehension"；"worse than leetcode imo... solve all the parts, test the code, explain"。[Blind b34ftqso, https://www.teamblind.com/post/stripe-phone-screen-interview-b34ftqso, 2023-08-15]
- 面试官指导："Focus on writing readable, clean and maintainable code, not just optimization." [Medium diyaag, 2025-10]
- "Stripe cares about being able to produce working code fast. Time complexity or performance is only an afterthought." 候选人追求 O(n log n) 排序解法，事后认为应该直接写 O(n²)。[Taro intern SF, https://www.jointaro.com/interviews/companies/stripe/experiences/software-engineering-intern-san-francisco-ca-september-1-2024-no-offer-positive-dd9f3cf6/, 2024-09-01]
- 反例（面试官不一致）：Taro 2025-10 一位拿到 offer 的候选人抱怨面试官"repeatedly asked me to revise variable names for readability"、要求大量 typecasting/interfaces，与"speed and efficiency"矛盾。[Taro SWE, https://www.jointaro.com/interviews/companies/stripe/experiences/software-engineer-october-20-2025-declined-offer-negative-88c270a4/, 2025-10-20]
- Blind 上多名候选人"做完所有 part + 单测，还剩 15 分钟"仍被拒，认为 rubric 不稳定；有人做 3/4 不写测试却过了（"attributing success to likability"）。[Blind 1ofokxcp, https://www.teamblind.com/post/stripe-phone-screen-rejected-1ofokxcp, 2021-11-30]
- Stripe 内部人：题库对每题定义了 passing band 和 rubric，但"most people don't decide pass or fail based on the rubrics"，面试官各有风格；打动面试官的四点："High code quality / Fast completion speed / Simple and clear description of thought process / Humble attitude"。[interviewdb insider]

### 3.3 Phone screen 题目实录（尽量完整）

**P1. Accept-Language header 解析**（多次报告，2022–2024）
- Part 1："Write a function that receives two arguments: an Accept-Language header value as a string and a set of supported languages, and returns the list of language tags that will work for the request." 按客户端偏好顺序返回被支持的语言。例：`"en-US, fr-CA, fr-FR"` + supported `["fr-FR","en-US"]` → `["en-US","fr-FR"]`；`"fr-CA, fr-FR"` + `["en-US","fr-FR"]` → `["fr-FR"]`。[LeetCode 4742657, https://leetcode.com/discuss/post/4742657/stripe-phone-screen-by-anonymous_user-ehvf/, 2024-02-17]
- 后续 part（Glassdoor 题目标题）："accept-language parser with **region/language/wildcard filtering**"——即 Part 2 只给语言（`fr`）时匹配所有 `fr-*` 地区；Part 3 支持 `*` 通配匹配剩余所有支持语言；（社区解法里）Part 4 支持 `q=` 权重排序。[Glassdoor QTN_4729735, https://www.glassdoor.com/Interview/Phone-interview-How-do-you-build-an-accept-language-parser-with-region-language-wildcard-filtering-QTN_4729735.htm，日期未知] [staffengprep 列为 "HTTP Accept-Language header", https://staffengprep.com/companies/stripe/]
- Blind 2023 描述为 "request filtering or internationalization"。[Blind b34ftqso, 2023-08]

**P2. Currency Conversion（汇率图）**（多次报告）
- 输入形如 `"AUD:USD:0.7,AUD:JPY:100,USD:CAD:1.2"`。Part 1：写函数返回 fromCurrency→toCurrency 的 **direct** 汇率。Part 2：经过中间货币的转换（AUD→USD→CAD）。Part 3：多条路径时求**最优汇率**。[staffengprep] [codinginterview.com, https://www.codinginterview.com/guide/stripe-interview-questions/ 列为 "Evaluate Division"]
- interviewing.io 版本：rates `['USD','GBP',0.77]` 数组 + queries `[['USD','CHN'],...]`，无法转换返回 `-1.0`，需支持双向（A→B 存在则 B→A 可算）。例：rates USD-JPY 100, JPY-CHN 20, CHN-THAI 200；queries USD→CHN=1000.0，JPY→THAI=4000.0，USD→AUD=-1.0。[interviewing.io currency-conversion, https://interviewing.io/questions/currency-conversion]
- linkjob 2026 也遇到（"Graph search problem modeling currencies as nodes and exchange rates as weighted edges"）。[linkjob SWE, 2026-02-12]

**P3. Closing Time / Minimum Penalty for a Shop**（2022 senior 电面；2022-03 L2 电面；interviewdb 2026 仍在题库）
- Part 1：给日志字符串（每小时 `Y`/`N`）和 closing time，算 penalty："+1 for each N before closing (customer absent while open)"、"+1 for each Y after closing (customer present while closed)"。
- Part 2：枚举所有 closing time 找 penalty 最小的（最早）时刻。
- Part 3：嵌套多店日志 `"BEGIN BEGIN BEGIN Y Y N Y END Y Y N N END Y N Y N END"`，用栈解析 BEGIN/END，对每家店跑 Part 2，按开店顺序输出。[LeetCode 2585038, https://leetcode.com/discuss/post/2585038/stripe-phone-screen-senior-se-reject-by-rypom/, 2022-09-16] [Kotlin 解法 gist, https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1]
- Blind 2022-03 post-mortem 描述同一题："1a: parse the string... counting something based on the integer; 1b: find the 'best' integer; 2a: given a bunch of bad input that you gotta clean up, find all the 'strings' contained within"；做完 3/4，两天后拒。[Blind bj5ehdwf, https://www.teamblind.com/post/stripe-phone-screen-post-mortem-bj5ehdwf, 2022-03-14]
- 对应 LeetCode 2483。多名候选人"跨年份遇到相同题"；有人全做完仍被拒。[LeetCode 2585038 评论]

**P4. Bracket / Brace Expansion（"Expansion"）**（2024-06 班加罗尔 backend；interviewdb "Expansion" 2026 仍活跃；hackerprep "last seen within 4 months"）
- 解析花括号内逗号分隔 token，生成所有组合（带前后缀）。例：`"/2022/{jan,feb,march}/report"` → 3 个字符串；`"over{crowd,eager,bold,fond}ness"` → 4 个；`"read.txt{,.bak}"` → 2 个。
- Follow-up：处理不完整/不匹配的括号、少于 2 个 token、无括号（原样返回）；后续 part 可能是嵌套括号。候选人只做完第一个 follow-up，一周后拒："they usually have 2-3 follow up questions"。[LeetCode 5341224, 2024-06] [hackerprep, https://hackerprep.io/company/stripe/bracket-expansion（付费）] [codinginterview.com "Brace Expansion" 按字典序返回]

**P5. Shipping route cost（运费路径）**（约 2024-10）
- 输入 `"US,UK,UPS,5:US,CA,FedEx,3:CA,UK,DHL,7"`。Part 1：直达运费（US→UK=5）。Part 2：经一个中转（US→CA→UK 合计）。（评论区讨论 Part 3 可能是最小成本/Dijkstra，但建议"do it directly"别过度工程）。候选人抱怨面试官"arrogant and not engaged"。[LeetCode 5883672, https://leetcode.com/discuss/interview-question/5883672/, 约 2024-10]

**P6. 交易风控四段题（Data Validation / Fraud Reports）**（2025-11-30，programhelp 转 LeetCode）
- Part 1 数据完整性：从 CSV 读 6 个字段，验证"all fields are non-empty"。
- Part 2 风控规则：金额须在业务定义范围内；支付方式不能在 blocked list；违反则标 suspicious。
- Part 3 用户行为匹配：与历史行为（消费国家、时间范围、金额区间）比对，"at least 50% of the behavioral attributes"匹配，否则 SUSPICIOUS。
- Part 4 智能错误报告：按优先级输出"up to two error codes"或 "OK"，并"maintain column alignment for readability"。[LeetCode 7384225, https://leetcode.com/discuss/post/7384225/stripe-phone-screen-4-part-interview-exp-dhoy/, 2025-11-30]（interviewdb 题库里 "Data Validation" 2 周前、"Fraud Reports" 1 个月前仍有报告，[https://www.interviewdb.io/question/stripe, 2026-07]）

**P7. Invoice reconciliation（发票对账）**（2025-04，L2 backend 班加罗尔）
- payment 字符串 `"payment5,1000,Paying off: invoiceC"`（id、USD minor units 金额、memo）；invoices 列表 `["invoiceA,2024-01-01,100","invoiceB,2024-02-01,200","invoiceC,2023-01-30,1000"]`（id、due date、amount）。Part 1：解析并找到 memo 中提到的 invoice，输出 `"payment5 pays off 1000 for invoiceC due on 2023-01-30"`。
- 2026-02 评论补充 follow-up：金额匹配多张发票时返回**到期日最早**的那张。[LeetCode 6696304, 2025-04-28]
- Glassdoor 片段（另一报告）："Stripe's Invoicing product phone screen involved problems about creating and sending invoices to customers, with multi-part requirements around payment allocation and due dates"。

**P8. User deduplication / similarity score（"Collusion"/linked users）**（2025 末）
- 用户记录 (id, name, email, company)，按字段加权算相似度，总分 ≥ threshold 视为同一人。Follow-up 1：找直接及 1 跳间接关联用户。Follow-up 2：无限跳数的连通分量。[linkjob technical, https://www.linkjob.ai/interview-questions/stripe-technical-interview/, 2025-12-08]（interviewdb 有 "Collusion" 标为 OA，题库共用。）

**P9. Accounting / tiered pricing（实习 tech screen 2025）**
- Part 1：订单 + 运费算总价。Part 2：阶梯定价，"unit price decreases as quantity increases"。Part 3：两种计费模型（incremental vs fixed-pricing）。[linkjob intern, https://www.linkjob.ai/interview-questions/stripe-intern-interview/, 2025]

**P10. Transaction string processing + 规则阻断（实习 tech screen 2024）**
- Part 1：把交易字符串处理成可读格式。Part 2：应用"在特定时间阻断某些交易"的规则，返回最终状态。[Taro intern SF, 2024-09-01]

**P11. Transactions + rules（"三题递进，交易与规则，每题要写测试"）**
- Glassdoor 摘要："3 questions building upon each other about transactions and rules, with a need to create test cases for each question"。[Glassdoor SWE list 搜索片段, https://www.glassdoor.com/Interview/Stripe-Software-Engineer-Interview-Questions-EI_IE671932.0,6_KO7,24.htm]

**P12. CSV 校验四段题（Exponent 收录的 tech screen）**
- 1) 解析带 header 的 CSV；校验无连续逗号。2) 校验行值非空；按条件输出某些列。3) 跨列校验（某列的值须存在于另一列）。4) 检测循环依赖（建图找环）。[Exponent guide]

**P13. Card Parsing / Credit Card Number（interviewdb 2026 活跃）**
- Part 1：把卡号除后 4 位外替换成 `x`。Part 2：按品牌校验（Visa 13–16 位以 4 开头；AmEx 15 位以 34/37 开头；Mastercard 16 位特定首位）。Part 3：Luhn 校验。[staffengprep "Valid Credit Card Number (Redaction)"] [interviewdb "Card Parsing"/"Credit Card Number" 2 周前有报告]

**P14. Min/Max record with comparator（2020 都柏林电面）**
- Part 1：取最小值记录；Part 2：按参数返回 min 或 max；Part 3：用 comparator；Part 4：处理 ties。[rampatra, 2020-01]

**P15. 其他电面题名（interviewdb 题库，2026-07，无详细描述）**
- "Factory Cost"（1 个月前）、"Chat Billing"（标 OA）、"Deployment"（标 OA）。[https://www.interviewdb.io/question/stripe]

**P16. Numeronym 校验**（FinalRound 标 "Final Round"；Exponent 列为 coding 轮样题）
- 校验 `i18n` 这类缩写是否合法：首尾字母、中间数字等于省略字符数；进阶：给定词典判断展开是否有效。[FinalRound, https://www.finalroundai.com/interview-questions/stripe-tech-numeronyms-validation] [Exponent guide]

### 3.4 电面挂点
- 时间不够：Java 冗长语法（getter/setter/构造器）吃掉时间。[Blind n4mqgn4g, 2024-04]
- 期待自动测例、没自己构造输入。[LeetCode 6696304, 2025-04]
- 追求最优复杂度而非先写能跑的代码。[Taro 2024-09]
- 需要面试官多次帮助（"required help from the interviewer at least 3 times"）。[Blind sy0bj6e3, 2018]
- 完成度不够：只做到第一个 follow-up。[LeetCode 5341224, 2024-06]
- 校招 2025-11 被拒后反馈："Focus on strengthening LeetCode fundamentals"，题目本身"realistically doable"，"standard array access"。[Taro new grad, 2025-11-05]

---

## 4. Onsite — Bug Squash（"Bug Bash" / Debugging）

### 4.1 格式
- 45–60 min（有报告 50 min）。给一个**真实开源项目的 fork**（私有 GitHub repo，pin 到某版本）+ Stripe 加的一个失败单测（或 GitHub-issue 风格的描述），在**自己的 IDE** 里 clone、跑测试、定位并修复。[Coditioning, https://www.coditioning.com/blog/804/stripe-swe-bug-squash-interview] [GreatFrontend] [Blind bekekkqf, https://www.teamblind.com/post/stripe-onsite-interview-bekekkqf, 2023-08-23："They gave me a cloned version of a repo and a test case that fails"]
- Stripe 员工："Our bug squashes use real open source bugs. We do write tests to help reproduce those bugs, but everything else is real." [Blind hkzsddkz, https://www.teamblind.com/post/why-isnt-stripes-bug-squash-debugging-interview-style-more-widely-used-hkzsddkz，日期未知]
- interviewing.io 版本："a generic version of a real Stripe bug"。[interviewing.io]
- 一个或多个 bug：多数报告 1 个主 bug + 修完后的 follow-up 改动；也有"expected 4 bugs"（senior）、"2 bugs"（JS）、"第三个 bug 前面试官就结束了"。[Blind gyamarmf, https://www.teamblind.com/post/stripe-bug-squash-interview-gyamarmf, 2025-10/11] [Blind t3w1kp3c, https://www.teamblind.com/post/stripe-javascript-bug-squash-t3w1kp3c, 2024-04-05] [Blind cnhknchr, 2025-07-17]
- 2020 都柏林（线下）：镜像笔记本、两位工程师旁观，clone 知名开源项目，修一个真实 GitHub bug。[rampatra, 2020-01]
- 前端候选人：面试官想看你"open the dev tools, throw breakpoints, and look at the call stack"。[Blind 8lewehei, https://www.teamblind.com/post/stripe-on-site-interviews-prep-8lewehei, 2025-11-23]
- 环境：Node 需要 `npm i`；Python 有人遇到 2.7 vs 3.7 环境问题；Java 有人 JDK 版本不兼容浪费时间。[Blind bekekkqf] [Blind hkzsddkz] [linkjob integration]

### 4.2 被报告的 repo / 库（按语言）
| 语言 | Repo / 库 | 来源 |
|---|---|---|
| Python | **requests**（一位候选人遇到 BytesIO 相关 bug；另一人说"fix a bug in an HTTP library"） | [Blind hkzsddkz] [Blind bxonqpkp, https://www.teamblind.com/post/stripe-on-site-bug-squash-and-integration-in-javascript-bxonqpkp, 2022-02-22] |
| Python | **Mako**（模板引擎；"Python + Mako; no hints"；bug 涉及 path handling validation、AST node traversal edge cases） | [programhelp VO, 2025-08-07] [linkjob technical, 2025-12-08] [staffengprep "Mako parser bug squash"] |
| Python | **YAML parser**、**HTML template parser**（staffengprep 付费题名） | [staffengprep] |
| Java | **Jackson**（jackson-core / jackson-databind / jackson-annotations，传闻） | [Blind nyhsknza, https://www.teamblind.com/post/stripe-bug-squash-tips-nyhsknza, 2021-02-22] |
| Java | **SnakeYAML**（"boolean and CSV parsing failures"） | [linkjob technical, 2025-12-08] |
| JavaScript | **Express**（"a widely used http package to create services in Node.js"，NDA 不能明说）、**Day.js** | [Blind t3w1kp3c, 2024-04] [GreatFrontend] |
| Ruby | **Sass**（Ruby 版）；另一人只说 "bug squash in Ruby... extremely hard" | [GreatFrontend] [Blind bxonqpkp] |
| 通用 | Exponent 收录的 bug 类型：missing directory-path check；missing visitor function for an AST node type → runtime error；unguarded read-modify-write race condition | [Exponent guide] [linkjob SWE 2026："Identified race condition in read-modify-write sequence"] |

**注：** 用户提到的 sinatra / jq / flask / redis-py / lodash 在英文来源中**没有**作为实际面试 repo 被证实；lodash/axios/express 只是候选人自行练习注入 bug 的 repo。[Blind bqug02mq, https://www.teamblind.com/post/stripe-onsite-interview-bug-squash-bqug02mq, 2025-09-11]

### 4.3 评分标准（Stripe 员工与指南）
- Stripe 员工（2022）："under <10% of candidates can crack the Python bug squash"；"solving the bug isn't the primary objective"；"you don't get extra credit for finding the bug, and you aren't dinged for not finding it, but you do get credit for showing independent debugging capability"；用 debugger、别钻兔子洞。[Blind bxonqpkp, 2022-02-23]
- Stripe 员工（2025）："We're looking for good communicators. That's made very clear in the instructions. You need to be able to express your thought process and solve the bugs methodologically." [Blind gyamarmf, 2025-11]
- Stripe 员工（2024）："They are great because you don't need to waste time preparing for them. Just do your normal work. The bug squash can be very hard depending on language." [Blind zlayqkxr, https://www.teamblind.com/post/stripe-bug-squash-integration-interviews-zlayqkxr, 2024-09-15]
- interviewing.io："approach the problem thoughtfully and test different approaches, rather than just barreling into something and hitting a wall"。
- Coditioning 分级期望：Intern/New grad → "Calm code reading and clarifying questions"；Mid → "Reproduce → isolate → fix → validate without excessive trial-and-error"；Senior → 加回归测试、可维护性讨论、相关失败面审计。强信号：先复现再改代码、证据驱动假设、最小且有理由的修复、加回归测试、协作清楚。[Coditioning]
- Leon 的"强表现"范文："Candidate read the entry point before touching the code. Set a breakpoint early, formed a clear hypothesis, verified it, then applied a targeted fix." [Leon, https://leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide/]
- Blind 候选人复盘："Stripe doesn't focus solely on the number of bugs fixed but emphasizes how candidates approach debugging and arrive at fixes"：一位候选人修复方案条件写错没生效，面试官仍满意。[Blind 0n7yfwy5, https://www.teamblind.com/post/stripe-interview-experience-software-engineer-0n7yfwy5, 约 2025-01]
- 一位 L3 候选人"took nearly the full time to locate the bug, emphasized verbalizing thoughts throughout, and received light guidance before completing the fix"，最终拿到 offer。[Blind bqug02mq, 2025-09]

### 4.4 挂点 / 教训（实录）
- "Couldn't even get close to the bug" 尽管用了 debugger/inspection 工具（L2, 2022）→ 最终去了 Apple。[Blind iNE4wxOA, https://www.teamblind.com/post/Stripe-interview-review-iNE4wxOA, 2022-04-02]
- Meta 候选人（2025-04）："solving only one bug with interviewer assistance"，问题：不理解这个库是干什么的、误解异常含义、在错误位置浪费时间、"fixating on stack trace tops"，最后发现是"a simple one liner"。评论：可以用自己的 VSCode；"this was so easy, I just had to calm down a bit"。[Blind 0vofunvv, https://www.teamblind.com/post/bombed-stripe-bug-squash-interview-0vofunvv, 2025-04-09]
- Google 候选人（senior，2025）：期待解 4 个 bug，做对 2 个、3 个部分；主要反馈是**没有充分读文档**导致调试时间过长。[Blind gyamarmf]
- JS 候选人（2023）：只用 console.log，用满时间没修好，止步该轮；建议提前学 debugger。[Blind bekekkqf, 2023-08-23]
- Google 候选人（JS，2024）："really really hard"，没找到 bug。[Blind t3w1kp3c]
- 2021 Python 候选人：不熟悉那个库，找不到核心问题。Pinterest 评论给的方法："Put print statements everywhere down the stack. Start at the unit test that's failing, locate where the data is off, and then dig deeper into the call stack to find where the data that's wrong is being generated." [Blind dqk1zngt, https://www.teamblind.com/post/tips-for-stripe-bug-squash-round-dqk1zngt, 2022-04-11]
- 15+ 年 Python 老手仍挂：Python 2.7 vs 3.7 环境、不熟 BytesIO、时间压力、"lightbulb"式设计；另一人被 race condition 吃掉大部分时间。[Blind hkzsddkz]
- C++ 候选人（2025-04）："didn't have the best experience in bug squash and integration rounds"，建议不同轮次允许换语言。[Blind fs65z4cm, https://www.teamblind.com/post/stripe-onsite-experience-offer-chances-fs65z4cm, 2025-04-11]
- 校招 2026：被给"large, complex codebase"，在面试官指导下修好，但自认这是最弱一轮（"weakness in advanced Java debugging"），最终拒。[LeetCode 7566910, 2026]
- InterviewCoder 总结的三大失败原因："trying to understand the entire codebase rather than following stack traces, searching in wrong places when fixes are minimal, and debugger failures with no fallback plan"。[InterviewCoder]

### 4.5 备考建议（汇总）
- 用 recruiter 发的 sample repo **提前跑通 IDE + debugger + 测试运行**（VS Code JS debug terminal / PyCharm / IntelliJ）。[Blind vwunpzkn, https://www.teamblind.com/post/stripe-onsite-interview-vwunpzkn, 2023-12-23] [Blind mrsi2qqr, 2022-01-29]
- 自己 clone 热门开源库（express/axios/lodash/requests 等）注入 bug 计时练习；至少 4 次 45 min 练习，其中一次不用 debugger。[Blind bqug02mq, 2025-09] [InterviewCoder 4 周计划]
- 先读 README/文档，理解库的用途；从失败测试出发看栈，别从栈顶死抠。[Blind gyamarmf] [Blind 0vofunvv]
- 语言选择：高层语言（Python/JS）更快；C++/Java 会被样板拖慢。[Blind jfsq2wjb, https://www.teamblind.com/post/bug-squash-for-stripe-infrastructure-interview-jfsq2wjb, 2024-09-01]

---

## 5. Onsite — Integration（API 集成轮）

### 5.1 格式
- 45–60 min，"open-book"：给私有 GitHub repo（含 README、boilerplate、示例数据、API 文档），本地 clone、配置环境，按 4–5 个递进 part 实现功能；**可以自由上网查文档/语法**，但不能用 AI。[Medium diyaag, 2025-11："Private GitHub repository, API documentation, full internet access"] [InterviewCoder] [Exponent guide]
- 面试官描述（Stripe 员工 guanaco）："make sure you move quickly through the exercise"，优先 "correctness (working solution) in the limited time"，**一般不要求写单测**。[Blind vwunpzkn, 2023-12-21]
- 2020 都柏林版本：Java，"Read file containing array of request data and make HTTP POST calls with this data and print out the response"，期望全部 200 OK；读文件方法已给、HTTP 库已在依赖里、需自己查在线文档；30 min 做完。[rampatra, 2020-01]
- 2021 候选人转述："they give you some project with boilerplate code that you will be integrating with some api (rest, http, json) with tests etc."。[Blind wyagomik, https://www.teamblind.com/post/stripe-onsite-interview-wyagomik, 2020-11-16]
- interviewing.io："You'll be asked to use the Stripe API here, and it will be based on real-world integrations they've seen their merchant customers create"；Staff 及以上没有这轮；面 Integrations org 的也跳过。[interviewing.io]
- 题库不固定：Stripe 员工："It is not fixed. There is a question bank and interviewers may favour a question but I have never used bikemap so far."；"Every language has a few questions. There's no round which has just 1 question in the bank."；"If you can do bikemap then you should be able to do the other ones too." [Blind h8lemeaq, https://www.teamblind.com/post/is-stripe-integration-always-bikemap-for-java-h8lemeaq, 03-25（年份未显示，约 2025）]

### 5.2 BikeMap（最常见的 integration 题，2023–2026 多次报告）
完整五段（oavoservice 2026-06-07 + linkjob 2025-12 + 1point3acres 标题）：
1. **GeoJSON 解析**：`ride-simple.json`（约 500 个 GPS 点，FeatureCollection → features → geometry → coordinates），提取前 10 个坐标，输出 `lat,lng`（注意 GeoJSON 内部是 `[lng, lat]`）；要求文件路径可配置、异常处理。
2. **HTTP POST 取地图**：向给定 URL POST JSON body（坐标），服务器返回 PNG，保存到本地（二进制 `wb`）；要正确设置 headers、处理网络错误后再写文件。
3. **staticmap 渲染**：用 `staticmap` 库把骑行路线画成连线导出图片（CoordinateLine、render）。
4. **地标标注 + 最近点查询**：在图上标 landmarks，计算每个 landmark 到路线的最小距离，找最近的；提到 O(n·m) 暴力 vs KD-tree 会加分。
5. **生产化特性**：批处理、缓存、CLI 模块化——"Few candidates reach this section; completion is not expected"。
[oavoservice, https://oavoservice.com/en/articles/stripe-integration-bikemap-geojson-http-staticmap-nearest-landmark, 2026-06-07] [linkjob technical, 2025-12-08："You're given bicycle ride JSON data and need to send HTTP requests to REST API rendering maps... the problem is long and the time is tight"（setup 后只剩 30–40 min）] [1point3acres 英文标题 "Integration Exercise: BikeMap API Integration", https://www.1point3acres.com/interview/problems/bba4944f-e065-4b5f-91be-f3564b9fd691]
- linkjob 2025 另一版本："reading three JSON files, converting them into dictionaries, and performing bidirectional ETL operations"，完成 3.9/5，第三问输出没显示但面试官"did not count it against me"；JDK 不兼容拖慢；建议用 Python。[linkjob integration, https://www.linkjob.ai/interview-questions/stripe-integration-round/, 2025-12-06]
- 实习版："BikeMap task requiring cloning a repository, call a given API, and store the response. Focused on POST requests."[linkjob intern, 2025]
- prachub 把 "Design ledger and bikemap integration" 作为 onsite 设计题合并收录（2025-07-29）。[https://prachub.com/interview-questions/design-ledger-and-bikemap-integration]

### 5.3 其他被报告的 integration 任务
- "Call specified API and store results in database"：按 README 配环境、.env 管密钥、API/DB 异常处理、事务一致性。[programhelp VO, 2025-08-07]
- 实习 2025：Sub-task A 文件操作+数据抽取（要读库文档）；Sub-task B 调外部 API、处理响应、调试不熟的工具。[Medium diyaag, 2025-11]
- 实习 2025："Writing some POST request code against existing APIs, with many steps"，做完 4 part 超时。[Medium azn7u1, 2025-11-14]
- 实习 2024（JS）："Debugging existing code, API integration, documentation reading under time pressure"。[Medium mitali, https://medium.com/@mitali.dixit04/software-engineer-intern-stripe-interview-experience-5eaf5a0e395c, 2024-10]
- 2024-04 L3：Part 1 十分钟做完，Part 2 需要修 API server 报错，面试官帮忙解释；被拒理由之一是"seeking clarification on Part 2 suggested insufficient independent problem-solving"。[Blind n4mqgn4g, 2024-04-19]
- 2025-01 L2 印度（Java）：调 import error 花时间，"json and string mismatch" 导致输出不对。[Blind 8grkgwt1, https://www.teamblind.com/post/stripe-interview-8grkgwt1, 2025-01-06]
- Exponent 收录类型：读多个 JSON 文件互转格式；clone repo → 调指定 API → 存响应；从本地文件抽字段 → 调外部 API → 把响应合并进输出；对 payments 风格 API 实现功能并提取特定字段。有候选人说这轮"more like design than coding"。[Exponent guide]
- linkjob 2026 coding 轮记录（可能是 integration）："Make an HTTP request to a mock payment API, handle errors, and parse the response"。[linkjob coding, https://www.linkjob.ai/interview-questions/stripe-coding-interview, 2026-02]
- Simplify 转述校招 VO："transaction reconciliation script handling pagination, rate limits, and idempotency"。[Simplify, 2026]
- Verve 汇总的 API-style 题：Build small HTTP client（无框架）；Compare API responses from two endpoints（normalize JSON，报差异）；Idempotent request handler（每个唯一请求只处理一次）；Debug failing webhook handler（特定 content type 静默失败）。[Verve]
- 前端版：读本地 JSON 渲染进现有 UI；接 `fetch` 到后端；处理二进制（Blob/ArrayBuffer/Uint8Array）；`URL.createObjectURL` 生成可下载文件。[GreatFrontend]

**注：** 用户提到的"flaky payments API with retries/idempotency"在英文一手报告中**没有**直接对应；只有 Leon/Simplify 等指南把 pagination、idempotency key、429 + Retry-After 退避、malformed response 防御解析列为"四大边界情况"。[Leon]

### 5.4 评分 / 通过线
- 完成度：2/5、"1.5/5 ran out of time"、"2.5 of 5 with hints"、"3 of 5"、"3.9/5" 等都有；社区共识："you can not finish integration or poor bug squash but probably not both... soft no"。[Blind iNE4wxOA, 2022-04] [Blind ncjsazmm, https://www.teamblind.com/post/stripe-offer-chances-ncjsazmm, 2022-05-11] [Blind VPdSosJJ, 2024-02]
- Google 候选人（2025-12）："very easy api calling but it is easy for everyone so you pretty much have to be perfect"。[Blind 1j2ckbta, 2025-12-22]
- 印度 Core Infra offer（2023-07，7.5 YOE）：做完 2/3 part，口头解释 Part 3 被接受；但**因 Part 3 没实现被降到 high-end L2**（原本期望 55 LPA，最终 95 LPA 包）。[Blind vvjmavis, https://www.teamblind.com/post/stripe-interview-experience-vvjmavis, 2023-07]
- 2021 建议："send http requests, read/write files and parse json"，至少做完 4 part 中 2–3 个。[Blind ezcaontf, https://www.teamblind.com/post/stripe-onsite-interview-tips-ezcaontf, 2021-09-18]
- Exponent 评分点：高效浏览陌生代码、按文档正确用 API、端到端实现、API 方法选择合理、清晰推理并吸收反馈。[Exponent guide]
- Leon 评分点：文档使用、边界覆盖、API ergonomics、production-readiness；失败模式：假设 REST 约定不读文档、只取分页第一页、无限重试无退避、支付流程静默失败。[Leon]
- 时间分配模板（extrabrain）：0–5 读题确认假设；5–15 跑通项目定位代码；15–35 happy path；35–48 错误处理边界；48–55 清理测试；55–60 总结。[extrabrain, https://extrabrain.app/interview-questions/stripe-integration-round-extrabrain/]

### 5.5 允许的库/工具
- 语言自选（与 bug squash 通常同一语言）；HTTP 库随意（Python `requests`、Java 已配依赖、Node fetch/axios）；可用 Postman；可查网页文档。[Blind mrsi2qqr, 2022-03] [rampatra] [Medium diyaag]
- 面试官不要求单测。[Blind vwunpzkn]
- 禁 AI 助手（Copilot/ChatGPT/Gemini/TabNine）。[GreatFrontend] [Blind 1j2ckbta]

---

## 6. Onsite — Coding / "Programming Exercise" / "Advanced Programming"

### 6.1 格式
- 45–60 min，与 phone screen 同类型但**更长、更多 part**，多为"读 JSON/测试数据，按逐步加码的需求实现"；有时需要 clone 一个 GitHub repo 在本地做。[Blind x7beaq87, 2025-04："Not leet code style but build off of some JSON/test data with different requirements added on"] [Blind cnhknchr, 2025-07："cloned a GitHub repository and solved 2 parts"] [Medium azn7u1, 2025-11："Similar to phone interview but required built-in libraries"]
- 平台：CoderPad 或本地 IDE；有报告在 HackerRank（2024-04 L3："finish two parts in hackerrank"）。[Blind n4mqgn4g]
- interviewing.io："less algorithms and data structures heavy than the LeetCode-style"，评分：决策理由、时间/空间复杂度分析、集成影响；主题 Hash Maps / Search / Parsing / Arrays / Strings。[interviewing.io]
- 校招 2026："Multi-part problems; I solved two parts along with follow-up questions on edge cases (45 minutes)"。[LeetCode 7566910]
- Stripe 员工在 2025-10 帖子："Stripe usually wants two parts"（L2）。[Blind 8grkgwt1 评论, 2025-01]

### 6.2 题目实录
**C1. Subscription / Email 通知调度（校招 & 实习，2025–2026 多次）**
- Part 1：按 plan 日期发邮件（welcome、expiration notices）。Part 2：根据用户输入处理 plan 变更。Part 3：续费/延期。[linkjob intern, 2025]
- "2026 Java NG VO - Email Subscription"：灵活的 `send_schedule` 结构，处理多种触发类型。[linkjob technical, 2025-12-08]
- Simplify 转述："notification scheduling system with subscription lifecycle management"。[Simplify, 2026]

**C2. Transaction processing / 余额（实习 VO 2026）**
- Part 1：从交易列表算每个用户的非零余额。Part 2：识别余额不足被拒的交易 + 剩余余额。Part 3a：平台借款机制，跟踪最大 reserve borrowed。（75+ 分钟的题量）[linkjob technical, 2025-12-08]
- Glassdoor 片段："output the names of users with a non-zero balance and their corresponding balances given a series of transactions"。

**C3. Account Balance / 清账（programhelp VO 2025-08）**
- 实现用户间转账系统使"all account balances end up at 0"；follow-up：最少交易数策略（greedy vs DFS）；审计考虑（日志、验证、追踪、异常检测）。对应 LeetCode "Optimal Account Balancing"。[programhelp VO, 2025-08-07] [codinginterview.com 列 "Optimal account balancing"]

**C4. AccountScheduler（2025 末 VO coding）**
- 实现接口判断 account 在时刻 t 是否可用，维护 `locked_until` 字典。Follow-up 1：`acquire(account_id, duration)` 锁定一段时间。Follow-up 2：不指定 account_id 时按 **LRU** 自动选最久未用的可用账户。[linkjob technical, 2025-12-08]

**C5. 可疑用户检测 / sliding window（programhelp VO 2025-09）**
- "Given a list of credit card transactions (user_id, amount, timestamp), detect suspicious users who have more than 3 transactions in a 1-minute window."（先 O(n²) 再 hashmap+滑窗 O(n)）。[Medium programhelp, https://medium.com/@neat_lava_bear_388/stripe-vo-interview-experience-interview-experience-coding-system-design-behavioral-a7bf34b1abcb, 2025-09-10]

**C6. CSV 交易统计（2026-02）**
- "Read a CSV file of transactions, filter by status, and output the total per user."（有人直接用 pandas）；以及"Refactor a messy codebase for readability and write automated tests"。[linkjob coding, 2026-02] [linkjob SWE, 2026-02-12]

**C7. Recurring Payment Scheduler（2026）**
- 设计任务：数据建模、触发逻辑、可扩展性、容错。[linkjob SWE, 2026-02-12]

**C8. interviewing.io 列出的 coding 轮样题**
- "How would you build a simple version of Identity Access Management?"
- "How would you blur credit card numbers from logs?"
- "Design a rate limiter in any programming language"（Prepfully 也列 "Design a rate limiter from scratch"、"Ensure personally identifiable information access control"）。[interviewing.io] [Prepfully]

**C9. Exponent 列出的类型**
- Validate numeronyms；parse transaction logs into per-user balances；implement stateful structures (caches, rate limiters)。[Exponent guide]

**C10. 2020 都柏林 Programming Exercise**："Algorithm-based coding from scratch, LeetCode Easy level"，15–20 min 做完。[rampatra]

**C11. AI Programming Exercise 的题（2026 新增轮，见 §9）**："given a list of transactions and a list of rules, where each rule says whether to accept or block a transaction followed by an if condition"；从关键词/字符串匹配升级到 AND/OR 布尔逻辑，每段递进。[interviewdb AI guide, 2026-06-09]

### 6.3 反馈实录
- 2024-04 L3 反馈："clean code practices with function decomposition"，但 Java 样板拖慢；两 part 完成、第二 part 有 bug 未修 → 被列为拒因之一（"Programming exercise performance suffered despite problem simplicity"）。[Blind n4mqgn4g]
- 2025-01 L2（Java）：只做完 part 1，"output has some extra commas"。[Blind 8grkgwt1]
- 2025-04：3/4 完成，第 4 口头。[Blind x7beaq87]
- 2021：面试官指出一个潜在 bug，改后"more accurate and cleaner"。[Blind umo0fobx]
- Taro 2025-10：面试官反复要求改变量名可读性。[Taro SWE]

---

## 7. Onsite — System Design（"Design 1"）

### 7.1 谁有这轮、格式
- **New grad / intern 一般没有**（3 轮 VO 中不含）；L2 及以上有；Exponent："new grads typically skip"，设计思维体现在 integration 轮。[Exponent guide] [Exponent SD blog] [Blind 1j2ckbta, 2025-12（London SDE1-2 岗"No system design round noted"）]
- 但**个别 L2/校招报告有**：2025-04 一位候选人 onsite 含 45 min SD；2025-03 Toronto "Money as a Service" 团队 SWE 有 "Design 1"。[Blind x7beaq87] [Blind ps7pgzwy, https://www.teamblind.com/post/stripe-onsite-design-1-interview-ps7pgzwy, 2025-03-18]
- 时长 45 min（多次确认）到 60 min；工具 **Whimsical**（Stripe 推荐，可用任意白板工具）或自己的画图工具共享屏幕。[Blind ps7pgzwy] [Blind x7beaq87] [interviewing.io] [Exponent SD blog]
- 题面形式："a big paragraph of details on a system to design"，需求"not clearly communicated by the writing or interviewer which I found wasted a lot of time"。[Blind ps7pgzwy, 2025-04-01]
- interviewdb 内部人：L2 的设计要求宽松，"as long as the candidate isn't completely clueless or without ideas, I would pass them"；L3 要求数据驱动设计、多场景论证、多语言多数据库熟悉度。[interviewdb insider]

### 7.2 被报告的题
| 题 | 细节 | 来源 |
|---|---|---|
| **Webhook 投递系统** | "Design a system that receives an internal event, finds the merchant's configured webhook URLs, and delivers the HTTP POST request to their servers." 10k events/s，高可靠。10 min 画完架构后 45 min 压力测试：①商户 endpoint 全部 500 怎么办；②商户 B 大促、服务器 accept 后 hang 30s 超时——商户 C 怎么不受影响（noisy neighbor）；③商户给任意 URL，如何防止利用 webhook 扫内网（SSRF）+ DNS rebinding；④商户 D 要 exactly-once 怎么保证。候选人被拒，反馈"insufficient reasoning about failure modes"。面试官 Staff，在 Stripe 4 年。 | [Medium emily, https://medium.com/@emilyhustlenyc/every-question-i-was-asked-in-stripes-system-design-interview-f6f19c2e62d6, 2026-05-20] |
| **Ledger service** | 要具体接口而非架构图：交易/余额表数据模型、API 接口带样例 I/O、状态管理（pending/completed/failed）、幂等设计。"Make systems 'really work' with concrete implementations rather than abstract frameworks." | [programhelp VO, 2025-08-07] |
| **Ledger（prachub 版）** | 双记账、不可变可审计（反冲而非修改）、幂等写（at-least-once 网络下 exactly-once 效果）、线性一致写；高写吞吐水平扩展、余额点查含 point-in-time；多 AZ、备份、加密；API：建账户、转账、holds/releases、reversals、余额查询、交易列表。 | [prachub, 2025-07-29] |
| **Payment Refund Service** | 高并发、幂等、最终一致；MQ、重试、幂等键、日志监控、DLQ。 | [Medium programhelp, 2025-09-10] |
| **Idempotent Payment System** | "Preventing duplicate charges" 为核心，(user_id, order_id) 唯一索引、状态迁移、并发控制、可观测性。 | [linkjob SWE, 2026-02-12] |
| **Monitoring service（like Datadog / SignalFx）** | 2020 都柏林；先 5–7 min 澄清再端到端设计。 | [rampatra] |
| **Exponent 汇总的 Stripe 报告题** | Ledger/bookkeeping service；APIs for transactions and transaction logs；redesign an internal authorization system across services；rate limiter；metrics service；distributed LRU cache；application performance monitoring system。 | [Exponent SD blog] |
| **staffengprep 题名** | Design ledger API；Design metrics counter system；（付费）Design merchant webhook；identity management system；feature flighting system；TopK system。 | [staffengprep] |
| **Prepfully 题名** | Database design for products；Frontend/backend for logging system；Webhook delivery architecture；Notification system for high traffic。 | [Prepfully] |
| **techinterview.org 题名** | Design Stripe's payment processing system（幂等、exactly-once、fraud、多币种、对账）；Distributed rate limiting（token bucket vs sliding window、Redis）；Stripe Radar fraud detection；Timeout handling "Was payment processed or not?"（saga、幂等键）。 | [techinterview.org, https://www.techinterview.org/post/3233460268/..., 更新 2026-07-05] |
| **ophyai 的 "API Design" 轮题** | Design a subscription billing API；refunds API；marketplace payouts API；payment split API。评分：资源建模与 HTTP 语义、错误处理与幂等、版本化与向后兼容、DX、分页。（注：ophyai 把 Integration 描述成 "API Design" 轮，与一手报告不完全一致。） | [ophyai, https://ophyai.com/blog/company-guides/stripe-interview-guide, 更新 2026-07-29] |
| **前端 Full Stack Design（HackerRank）** | TypeScript interface 数据建模 → 带校验和后端调用的函数 → React 组件白板（state/callbacks）。 | [GreatFrontend] |

### 7.3 评分维度
- Exponent 四维：Problem Framing / API & Data-Model Design / Failure-Mode & Scale Reasoning / Separation of Concerns（快路径 enforcement vs 慢路径 management）；"Stripe weighs API design heavily"。[Exponent SD blog] [Exponent guide]
- interviewing.io：架构决策、技术选型、可扩展性、可靠性、可用性、数据库选择、缓存策略。
- 一手反馈："insufficient reasoning about failure modes"（拒）；"You did very well"（该候选人仍因其他轮被拒）；"bombed it... misalignment with interviewer expectations"（L2 拒，2025-07）；Google 候选人"received a hire on Bug Squash but was rejected overall due to system design performance"（2025-12）。[Medium emily] [Blind umo0fobx] [Blind cnhknchr] [Blind 1j2ckbta]
- 2025-04 候选人：30 min 就讲完、面试官只有澄清问题没有 concerns，最终仍拒。[Blind n4mqgn4g]

---

## 8. 最终 HM / Behavioral（见 §2，此处补充 offer/level 相关）

- 校招 HM 后等待："reviewing feedback on a rolling basis"，一周以上无消息属正常。[Blind k4acvawb, 2021-10]
- Recruiter 邮件写 "walk you through next steps" 通常是好消息（该候选人拿到 offer；manager chat 周四 → 次周三收到邮件）。拒信一般是邮件，有的 recruiter 也会打电话。[Blind gwmegqab, https://www.teamblind.com/post/does-stripe-call-to-reject-gwmegqab, 2021-10-06]
- 2024-02：周三上午面完，周五上午拒，"no explicit feedback"。[Blind VPdSosJJ]
- 2025-07 L2 拒因（recruiter 原话）：团队想要 "a stronger candidate in technical, design and communication"。[Blind cnhknchr]
- 2025-04 拒："generic recruiter email with no specific feedback"（4/2 面，4/8 拒）。[Blind x7beaq87]
- Stripe 员工：正面的面试官反馈"uncommon and a great sign"；反馈至少 48 小时内；定级看 YOE 和 references。[Blind umo0fobx 评论, 2021-06]

---

## 9. 2026 新增：AI Programming Exercise 轮

- 位置：onsite loop 内，"recently added"（文章 2026-06-09）。有候选人报告 onsite 是 "2 technical rounds including integration and AI programming rounds"。[interviewdb AI guide] [ophyai]
- 平台：HackerRank 特殊环境，内嵌 AI 聊天窗口，"kind of like a lightweight Cursor"；可以让 AI 读 README、出计划、写代码、加测试、调试。
- 时长：编码约 30 min（手写几乎不可能完成）。
- 题目：交易 + 规则（accept/block + if 条件），从字符串匹配到 AND/OR 布尔逻辑，多段递进。
- 评分："whether you can use AI effectively without turning your brain off"——理解 spec、正确引导 AI、批判性 review 生成代码、**自己写测试**、发现 AI 过度工程/漏边界。interviewfox 版本："scores how you use it on architecture, testing, and optimization"。[interviewdb AI guide] [interviewfox, 2026]
- 推荐流程：AI 总结 README → 一起过实现计划 → AI 生成代码 → 自己写测例 → 调试并确认理解。[interviewdb AI guide]
- 与其他轮的关系：其余轮次仍禁 AI（IDE 不能带 AI agent）。[Blind 1j2ckbta, 2025-12] [GreatFrontend]

---

## 流程与时间线

### 各阶段时长（汇总）
| 阶段 | 报告的时长/等待 | 来源 |
|---|---|---|
| 申请 → OA 邀请 | 4–5 天（2026） | [interviewfox] |
| OA → 结果 | 2 小时（2025-11 实习）；3–5 个工作日（指南） | [Medium azn7u1] [lodely] |
| OA → tech screen 排期 | 约 1 周（节假日可到 3 周） | [interviewfox] |
| Tech screen → 结果 | 次日（实习 2025）；1–3 天；约 5 天 | [Medium azn7u1] [Blind 1hirauis, https://www.teamblind.com/post/finished-phone-screen-at-stripe-1hirauis, 2021-07] |
| Tech screen → onsite | 2–3 周（可自己要求更多准备时间） | [Leon timeline, https://leonstaff.com/blogs/stripe-interview-response-time-2025/] [linkjob intern] |
| Onsite → 决定 | 2 天（拒）；5–10 个工作日；2 周以上 = "maybe" 池等 team match/committee | [Blind VPdSosJJ] [Leon timeline] |
| 端到端 | 4–8 周（Exponent/Leon）；6 周、内推可 2 周（interviewing.io）；校招 1–3 个月（Simplify：9 月 OA → 11 月 screen → 12 月 onsite/HM） | |
| Tech screen → offer | 约 3 周（linkjob 2025） | [linkjob integration] |
| 实习 2024（班加罗尔） | 8/22 recruiter 联系 → 8/28 HackerRank → 9/9 coding 60 min → 9/18 进终面 → 10/7 两轮连面 → 10/16 拒 | [Medium mitali] |
| 实习 2025（班加罗尔） | 9 月中 OA → 10 月初 tech screen → VO 两轮 → 11 月初 HM → 拒 | [Medium diyaag] |
| 校招 2024–25（美国） | 10 月开始：OA → code screen → 3 小时 onsite → HM chat → 圣诞前"等 returning intern 决定后再看 headcount" → 1 月初被告知 "they filled headcount" | [Blind t6bahgt3, https://www.teamblind.com/post/stripe-swe-new-grad-headcount-t6bahgt3, 2025-01-14] |

### Onsite 形式
- 全部虚拟（Zoom），社招 5 轮常分 2 天；校招 3 轮可连排 3 小时。[Blind n4mqgn4g] [Blind t6bahgt3] [interviewing.io "5 hours total"]
- 2020 都柏林是线下 6 小时含午餐。[rampatra]

### Hiring Committee / 决策
- 全体 panel 写书面 feedback（Leon 说打 1–4 分）→ 开会讨论 → 多数 consensus，否则 HM 决定。[interviewing.io] [Leon]
- Hiring committee **每周**开会；references 之后只剩 committee，"if you are rejected after the reference calls... there's literally no other reason other than committee rejected you"（Stripe 员工）。[Blind cnclye1l, https://www.teamblind.com/post/stripe-decision-delays-cnclye1l，日期未知（L3，12 月中 references，1 个月后拒）]
- "all thumbs up or it's gonna be a rejection"。[Blind VPdSosJJ]

### Team match
- 有候选人 committee 通过但原团队拒，recruiter 说会匹配其他团队；另一人"got matched to another team at L2 after about a month"。[Blind h0j2kuo1, https://www.teamblind.com/post/stripe-team-matching-issue-h0j2kuo1, 2022-09-29]
- IGotAnOffer：team matching = 与 2–4 位 HM 各 30 min 聊。[IGotAnOffer]
- Leon：通过但等 team 的可能在池里 2–6 周，headcount 变动可能撤回。[Leon timeline]
- interviewing.io："hiring managers at Stripe are encouraged to share all good candidates with other teams"。

### 定级 / 降级
- 定级在面试后决定（"they level you after the interview"）。[Blind sfaggc1a]
- Integration 没做完 Part 3 → 从预期 L3 降到 high-end L2。[Blind vvjmavis]
- Staff 候选人讲不清业务影响会被降级。[interviewing.io]

### Cooldown（拒后再申请）
- Stripe 员工 ×2（2021-10）："6 months"（初筛 code pair 被拒）。[Blind c7vzbrvh, https://www.teamblind.com/post/cool-off-period-to-reapply-at-stripe-c7vzbrvh, 2021-10-12]
- Stripe 员工（2021-02）："12 months is what we recommend"。[Blind yiPKLXYS, https://www.teamblind.com/post/Stripe-interview-cool-off-period-yiPKLXYS, 2021-02-05]
- interviewfox（2026）："fixed 12-month period"；4dayweek："six to twelve months"。[interviewfox] [4dayweek, https://4dayweek.io/interview-process/stripe-software-engineer]
- 结论：一线消息 6 个月（早期轮）/ 12 个月（推荐），2026 指南倾向 12 个月。

### 校招 Offer / 薪酬
- 美国 L1（levels.fyi，2026）：中位 TC ≈ $209,973；均值 $212,925 = base $147,042 + stock $40,250 + bonus $25,633；区间 $190K–$260K。2024/25 典型包：~$140k base + ~$65k/yr RSU + ~$20k sign-on + perf bonus，首年常超 $220k。[levels.fyi, https://www.levels.fyi/companies/stripe/salaries/software-engineer/levels/l1] [InterviewCoder salary guide]
- 2025-04 一位美国 onsite 候选人的 offer 预期：180K base + 股权不确定。[Blind x7beaq87]
- 班加罗尔 L1 new grad（2025-10 offer）：base 29L + sign-on 4.4L + RSU 22L/yr（1 年 cliff 后季度 vest）+ 10% bonus ≈ 59L；可选全现金或混合。[LeetCode 7352963, https://leetcode.com/discuss/post/7352963/, 2025-11-16]
- 印度 L2 high-end（2023-07，7.5 YOE）：base 50L + bonus 10L + stock 35L = 95 LPA。[Blind vvjmavis]
- Exponent 各级 TC（2026 年中）：L1 ~$209K / L2 ~$278K / L3 ~$437K / L4 ~$719–744K / L5 ~$1.08M；股权一年 vest、9 个月 refresh。[Exponent guide]
- 实习生没有 RSU。[Blind 6ab5ozmg, https://www.teamblind.com/post/stripe-new-grad-interview-6ab5ozmg, 2021-10-22]
- 校招 headcount 受 returning intern 影响，可能面完等到 1 月被告知没 HC。[Blind t6bahgt3]
- Stripe 2025-01 裁 300 人后无裁员，2026-07 有 400+ 岗位。[Simplify]

### 远程 / 地点
- 面试全程远程；Simplify 提到校招落点多为 payments/infra 团队，Glassdoor 工程师 WLB 分数偏低。[Simplify]

---

## 题目总表

| 题目 | 轮次 | 描述 | 来源数 | URLs |
|---|---|---|---|---|
| Accept-Language parser | Phone screen | 解析 header 返回按偏好排序的受支持语言；后续 part：仅语言匹配地区、`*` 通配、（q 权重） | 4 | leetcode.com/discuss/post/4742657/ ; glassdoor QTN_4729735 ; teamblind b34ftqso ; staffengprep.com/companies/stripe/ |
| Currency Conversion | Phone screen / coding | 字符串汇率表→直达汇率→多跳→最优路径；无法转换返回 -1 | 4 | staffengprep ; interviewing.io/questions/currency-conversion ; codinginterview.com ; linkjob.ai/.../stripe-software-engineer-interview/ |
| Closing Time / Min Penalty for a Shop | Phone screen | Y/N 日志算 penalty→最优关门时间→BEGIN/END 嵌套多店 | 5 | leetcode.com/discuss/post/2585038/ ; teamblind bj5ehdwf ; gist pkafel ; interviewdb.io/question/stripe ; codinginterview.com |
| Bracket / Brace Expansion | Phone screen | `{a,b}` 展开所有组合；边界：不匹配括号、单 token、无括号 | 4 | leetcode 5341224 ; hackerprep.io/company/stripe/bracket-expansion ; interviewdb "Expansion" ; codinginterview.com |
| Shipping route cost | Phone screen | `"US,UK,UPS,5:..."` 直达运费→一次中转 | 1 | leetcode.com/discuss/interview-question/5883672/ |
| 交易风控四段（Data Validation / Fraud Reports） | Phone screen | CSV 非空校验→金额范围/黑名单→50% 行为匹配→最多两个错误码对齐输出 | 2 | leetcode.com/discuss/post/7384225/ ; interviewdb.io/question/stripe |
| Invoice reconciliation | Phone screen | payment memo 找 invoice，输出对账语句；多匹配取最早到期 | 1 | leetcode.com/discuss/post/6696304/ |
| User dedup / similarity（Collusion） | Phone screen | 加权相似度≥阈值判同人→1 跳→连通分量 | 2 | linkjob.ai/.../stripe-technical-interview/ ; interviewdb "Collusion" |
| Tiered pricing / accounting | Phone screen（实习） | 订单+运费→阶梯单价→两种计费模型 | 1 | linkjob.ai/.../stripe-intern-interview/ |
| Transaction strings + 时间规则阻断 | Phone screen（实习） | 格式化交易→按时间规则阻断→最终状态 | 1 | jointaro.com ...intern-san-francisco...2024 |
| Transactions + rules（3 题递进） | Phone screen | 交易与规则，每题写测试 | 1 | glassdoor EI_IE671932.0,6_KO7,24 |
| CSV validation 四段 | Phone screen | 解析→非空/条件输出→跨列校验→循环依赖 | 1 | tryexponent.com/guides/stripe-software-engineer-interview |
| Card Parsing / Credit Card Number | Phone screen | 打码后 4 位→品牌规则→Luhn | 2 | staffengprep ; interviewdb |
| Min/Max with comparator | Phone screen | 取最小→参数化 min/max→comparator→ties | 1 | blog.rampatra.com/stripe-interview-for-software-engineer |
| Factory Cost / Chat Billing / Deployment | Phone/OA | 仅题名 | 1 | interviewdb.io/question/stripe |
| Numeronym validation | Coding/Final | 校验 i18n 式缩写 | 2 | finalroundai.com/...numeronyms-validation ; tryexponent |
| Subscription / Email 通知调度 | Onsite coding（校招/实习） | 按 plan 日期发邮件→plan 变更→续费；send_schedule 多触发类型 | 3 | linkjob intern ; linkjob technical ; simplify.jobs |
| Transaction balances + 拒绝 + 平台借款 | Onsite coding（实习 2026） | 非零余额→余额不足拒绝→借款上限 | 1 | linkjob.ai/.../stripe-technical-interview/ |
| Account Balance 清账（Optimal Account Balancing） | Onsite coding | 转账使余额归零→最少交易→审计 | 2 | programhelp.net/en/vo/... ; codinginterview.com |
| AccountScheduler | Onsite coding | 时刻 t 可用性→acquire 锁定→LRU 自动选账户 | 1 | linkjob technical |
| 1 分钟 >3 笔可疑用户 | VO coding | 滑窗+hashmap | 1 | medium.com/@neat_lava_bear_388/... |
| CSV per-user total / refactor+tests | Coding | 读 CSV 按状态过滤汇总；重构+自动化测试 | 1 | linkjob.ai/.../stripe-coding-interview |
| Recurring Payment Scheduler | Coding | 数据建模、触发、扩展、容错 | 1 | linkjob SWE 2026 |
| IAM / blur card numbers / rate limiter | Coding | interviewing.io 样题 | 2 | interviewing.io/stripe-interview-questions ; prepfully.com |
| Transactions + rules（AI 轮） | AI Programming Exercise | accept/block 规则解析，字符串→AND/OR | 2 | interviewdb.io/guides/stripe-ai-programming-exercise ; interviewfox.ai |
| BikeMap | Integration | GeoJSON 解析→POST 取 PNG→staticmap 渲染→地标最近点→生产化 | 6 | oavoservice.com ; linkjob integration ; linkjob technical ; teamblind h8lemeaq ; 1point3acres ; prachub |
| Call API + store in DB | Integration | README 配环境、.env、异常、事务 | 1 | programhelp VO |
| 读文件→POST→打印响应（Java） | Integration | 2020 都柏林 | 1 | rampatra |
| 文件抽字段→调外部 API→合并输出 | Integration | 实习 2025 | 2 | medium diyaag ; tryexponent |
| Reconciliation script（分页/限流/幂等） | Integration（校招） | Simplify 转述 | 1 | simplify.jobs/blog/stripe-new-grad-swe-job |
| requests（BytesIO bug） | Bug squash（Python） | 真实历史 bug | 2 | teamblind hkzsddkz ; teamblind bxonqpkp |
| Mako | Bug squash（Python） | path handling、AST 遍历边界 | 3 | programhelp VO ; linkjob technical ; staffengprep |
| YAML parser / HTML template parser | Bug squash（Python） | 题名 | 1 | staffengprep |
| Jackson | Bug squash（Java） | 传闻 | 1 | teamblind nyhsknza |
| SnakeYAML | Bug squash（Java） | boolean/CSV 解析失败 | 1 | linkjob technical |
| Express / Day.js | Bug squash（JS） | | 2 | teamblind t3w1kp3c ; greatfrontend.com |
| Sass | Bug squash（Ruby） | | 1 | greatfrontend.com |
| Webhook delivery system | System design | 10k/s、500 处理、noisy neighbor、SSRF、exactly-once | 3 | medium emily ; staffengprep ; prepfully |
| Ledger service / API | System design | 双记账、幂等、状态机、具体接口 | 4 | programhelp VO ; prachub ; staffengprep ; tryexponent SD blog |
| Payment refund service | System design | 幂等、MQ、DLQ | 1 | medium programhelp |
| Idempotent payment system | System design | 防重复扣款 | 2 | linkjob SWE ; techinterview.org |
| Monitoring / metrics / APM | System design | Datadog-like；metrics counter | 3 | rampatra ; staffengprep ; tryexponent SD blog |
| Rate limiter | System design / coding | | 3 | tryexponent SD blog ; interviewing.io ; techinterview.org |
| Authorization / identity / feature flag / TopK / distributed LRU | System design | 题名 | 2 | tryexponent SD blog ; staffengprep |
| Subscription billing / refunds / payouts / payment split API | "API design" | ophyai 汇总 | 1 | ophyai.com |
| Notification system / logging system / product DB | System design | Prepfully 题名 | 1 | prepfully.com |
| UI component（品牌样式） | Phone screen（前端） | 2018 | 1 | teamblind sy0bj6e3 |
| Contact Form / Data Merging / Data Selection / Data Table | 前端 coding | GreatFrontend 12 题 | 1 | greatfrontend.com |

---

## 面试官评分维度（据报道）

**通用（所有技术轮）**
1. **代码质量 > 最优复杂度**："Correctness and readability outrank optimization at every stage"；"Time and space complexity carry little weight"。[Exponent] [Blind a18jdcfu] [Taro 2024]
2. **速度**：多 part 题必须推进；"Speed comes from reading and typing quickly"；Stripe 内部人把"Fast completion speed"列为第二关键。[Exponent] [interviewdb insider]
3. **阅读理解 / 问题提取**："pulling a clean problem from a wall of text"。[Exponent] [Blind b34ftqso]
4. **测试意识**：自己构造输入、写测例、自验证。[Blind rptglpyd] [LeetCode 6696304]
5. **沟通**：边做边讲；"Simple and clear description of thought process"；bug squash "We're looking for good communicators"。[Blind gyamarmf] [interviewdb insider]
6. **独立性**：过多求助被记为负面（"seeking clarification on Part 2 suggested insufficient independent problem-solving"）。[Blind n4mqgn4g]
7. **谦逊态度**："Humble attitude" 列为第四关键。[interviewdb insider]
8. **反 AI / 反背题**：题库轮换、面试官警惕"太熟练"。[interviewdb insider]

**Bug squash**：复现 → 假设 → 用 debugger 验证 → 最小修复；方法论 > 修复数量；读文档；不乱改。[Coditioning] [Leon] [Blind bxonqpkp]

**Integration**：正确性优先、快速推进、按文档用 API、错误处理、代码组织；不要求单测；完成 3–4/5 且解释清楚可竞争。[Blind vwunpzkn] [oavoservice] [Leon]

**System design**：先澄清需求；API/数据模型；失败模式推理（这是最常见拒因）；trade-off；具体接口而非抽象框架。[Exponent SD blog] [Medium emily] [programhelp VO]

**Behavioral/HM**：对照六条 Operating Principles 写 feedback；要具体例子和 trade-off，避免过度排练；"why Stripe/why payments" 要具体。[Exponent] [Simplify]

**决策机制**：全员书面 feedback（1–4 分）→ 周会 → consensus / HM 拍板；一个 lukewarm 即拒。[interviewing.io] [Leon] [Blind VPdSosJJ]

---

## 常见挂点

1. **语言拖慢**：Java/C++ 样板代码让 coding/integration 做不完；多位候选人事后建议 Python/JS。[Blind n4mqgn4g] [Blind fs65z4cm] [Blind jfsq2wjb] [Medium mitali] [oavoservice："Python saves more than half the development time"]
2. **环境问题**：JDK 版本、import error、Python 2/3、repo 访问权限，吃掉 5–10 分钟甚至更多。[linkjob integration] [Blind 8grkgwt1] [Blind hkzsddkz] [Blind umo0fobx]
3. **Bug squash 不熟 debugger / 只用 print**：用满时间找不到 bug。[Blind bekekkqf] [Blind iNE4wxOA] [Blind t3w1kp3c]
4. **Bug squash 不读文档、盯栈顶、试图理解整个库**。[Blind gyamarmf] [Blind 0vofunvv] [InterviewCoder]
5. **Integration 需要提示 / 只做 1–2 part**："soft no"；两轮都弱基本必拒。[Blind rmvygjeb] [Blind ncjsazmm] [Blind VPdSosJJ]
6. **追求最优解 / 过度工程**：Taro 实习生 O(n log n) 排序；Blind 建议"do it directly"。[Taro 2024] [LeetCode 5883672 评论]
7. **投入过多时间打磨代码**："prep materials emphasized quality over speed... proved insufficient"。[Blind VPdSosJJ]
8. **System design 失败模式推理不足**：webhook 题被拒；L2 "bombed" SD；Google 候选人 SD 拒。[Medium emily] [Blind cnhknchr] [Blind 1j2ckbta]
9. **沟通 / 非母语 + 技术故障**：实习 HM 轮网络故障+沟通 gap → 拒；Taro 反馈 "communication and problem fit"。[Medium diyaag] [interviewfox]
10. **面试官不一致 / 主观**：全做完+单测仍拒；做 3/4 无测试却过；面试官"arrogant and not engaged"。[Blind 1ofokxcp] [LeetCode 5883672] [Taro 2025-10]
11. **Headcount / 时间点**：校招面完等 returning intern 决定，1 月被告知 HC 满。[Blind t6bahgt3]
12. **只准备 LeetCode**：Meta/Google 背景候选人低估 Stripe 的"实践"取向；反之 2025-11 校招被拒反馈却是"strengthen LeetCode fundamentals"（说明基础数组/哈希操作要熟）。[Blind a18jdcfu] [Taro new grad 2025-11]
13. **一轮 lukewarm 即拒**：Stripe 文化不 pull rank。[Blind VPdSosJJ]

---

## 附：各来源一句话可信度备注
- **Blind 上自称 Stripe 员工的评论**（bxonqpkp、gyamarmf、zlayqkxr、mdtk4bmj、jcnxxpsh、1j2ckbta、hkzsddkz、h8lemeaq、c7vzbrvh、yiPKLXYS、VPdSosJJ、cnclye1l、1gfdplee）：一手，但匿名。
- **interviewing.io 指南**：由前 Stripe 面试官撰写，结构最可信（但偏社招/staff 视角）。
- **LeetCode/Medium/Taro 个人经历**：一手题目复述，年份明确。
- **linkjob / programhelp / oavoservice / interviewfox / interviewdb**：付费辅导/题库站，题目细节多但含营销；programhelp 与 1point3acres 中文圈同源。
- **Exponent / Leon / InterviewCoder / TechPrep / Verve / ophyai / techinterview.org / codinginterview.com / FinalRound / Prepfully / IGotAnOffer / Simplify / 4dayweek**：二手汇总指南，部分题目（如 "Two Sum with transaction amounts"、"SQL 题"、"LeetCode medium 两轮 coding"）与一手报告不符，仅作参考。
- **未能访问**：Glassdoor 全部页面（Cloudflare）；LeetCode 5740845（需登录）；interviewdb 的 integration/bug-squash 题页（内容未加载）；hackerprep（付费）；designgurus（付费）。
