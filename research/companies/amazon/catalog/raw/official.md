# Amazon 官方一手资料（amazon.jobs）

抓取日期 2026-10-15。抓取方式：`curl https://r.jina.ai/<url>`（渲染页）+ 直接 `curl` 原始 HTML 里内嵌的 JSON（折叠面板内容只在 JSON 里）。
`site:amazon.jobs` 页面没有一页叫 "How we hire / interview-process"（`/content/en/how-we-hire/interview-process` 返回 404，2026-10-15）；
真实入口是 `/content/en/how-we-hire`。`/en/software-development-interview-prep` 是纯 SPA，抓不到正文（149 bytes）。
以下标 `推断` 的是我自己的判断，其余都是页面原文或原文转述。

## 0. 官方页面地图（2026-10-15 抓取成功）

| 页面 | URL | 备注 |
|---|---|---|
| How We Hire（目录） | https://www.amazon.jobs/content/en/how-we-hire | 列出 SDE Interview Prep Course / SDE Interview Topics / SDE II / SDE II OA / SDE III / SDM ... 的子页 |
| Interview loop | https://www.amazon.jobs/content/en/how-we-hire/interview-loop | 在线 / 现场通用的流程与后勤，见 §5 |
| SDE II Interview Prep | https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep | 4 个 55 分钟面试；系统设计 + 编码四能力 + 行为面，见 §2-§4 |
| SDE III / Sr. SDE Interview Prep | https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep | 5 个 55 分钟；多一个 Low-level design 说明；技术电面含系统设计 |
| SDE Interview Topics | https://www.amazon.jobs/en/landing_pages/software-development-topics | 官方技术话题清单，见 §3 |
| University SDE OA prep | https://www.amazon.jobs/content/en/how-we-hire/university/sde-oa | 新毕业生 / 实习 OA 说明，见 §6 |
| SDE II OA prep | https://www.amazon.jobs/content/en/how-we-hire/sde-ii-oa-prep | OA 含系统设计情景题 |
| Leadership Principles | https://www.amazon.jobs/content/en/our-workplace/leadership-principles | 16 条原文，见 §1 |
| 官方视频逐字稿 | https://static.jobs.production.amazon-jobs.brightspot.cloud/6b/de/fe94b6d84b98a28ec604c5f8d1e7/transcript-system-design-interview-prep.docx 等 | 见 §4 |

没有单独的 "SDE I new grad" 面试准备页：新毕业生走 `/content/en/how-we-hire/university` + `university/sde-oa`；university 页面本身只讲 OA（见 §6）。
`推断`：SDE I / 新毕业生的 loop 官方没有单独发布结构，只能靠 SDE II / III 页面 + 官方 FAQ 视频里的一句话（见 §4 "FAQ 视频"）。

## 1. 16 条 Leadership Principles（原文，2026-10-15，https://www.amazon.jobs/content/en/our-workplace/leadership-principles）

> We use our Leadership Principles every day, whether we’re discussing ideas for new projects or deciding on the best way to solve a problem. It’s just one of the things that makes Amazon peculiar.

1. **Customer Obsession** — Leaders start with the customer and work backwards. They work vigorously to earn and keep customer trust. Although leaders pay attention to competitors, they obsess over customers.
2. **Ownership** — Leaders are owners. They think long term and don’t sacrifice long-term value for short-term results. They act on behalf of the entire company, beyond just their own team. They never say “that’s not my job.”
3. **Invent and Simplify** — Leaders expect and require innovation and invention from their teams and always find ways to simplify. They are externally aware, look for new ideas from everywhere, and are not limited by “not invented here.” As we do new things, we accept that we may be misunderstood for long periods of time.
4. **Are Right, A Lot** — Leaders are right a lot. They have strong judgment and good instincts. They seek diverse perspectives and work to disconfirm their beliefs.
5. **Learn and Be Curious** — Leaders are never done learning and always seek to improve themselves. They are curious about new possibilities and act to explore them.
6. **Hire and Develop the Best** — Leaders raise the performance bar with every hire and promotion. They recognize exceptional talent, and willingly move them throughout the organization. Leaders develop leaders and take seriously their role in coaching others. We work on behalf of our people to invent mechanisms for development like Career Choice.
7. **Insist on the Highest Standards** — Leaders have relentlessly high standards — many people may think these standards are unreasonably high. Leaders are continually raising the bar and drive their teams to deliver high quality products, services, and processes. Leaders ensure that defects do not get sent down the line and that problems are fixed so they stay fixed.
8. **Think Big** — Thinking small is a self-fulfilling prophecy. Leaders create and communicate a bold direction that inspires results. They think differently and look around corners for ways to serve customers.
9. **Bias for Action** — Speed matters in business. Many decisions and actions are reversible and do not need extensive study. We value calculated risk taking.
10. **Frugality** — Accomplish more with less. Constraints breed resourcefulness, self-sufficiency, and invention. There are no extra points for growing headcount, budget size, or fixed expense.
11. **Earn Trust** — Leaders listen attentively, speak candidly, and treat others respectfully. They are vocally self-critical, even when doing so is awkward or embarrassing. Leaders do not believe their or their team’s body odor smells of perfume. They benchmark themselves and their teams against the best.
12. **Dive Deep** — Leaders operate at all levels, stay connected to the details, audit frequently, and are skeptical when metrics and anecdote differ. No task is beneath them.
13. **Have Backbone; Disagree and Commit** — Leaders are obligated to respectfully challenge decisions when they disagree, even when doing so is uncomfortable or exhausting. Leaders have conviction and are tenacious. They do not compromise for the sake of social cohesion. Once a decision is determined, they commit wholly.
14. **Deliver Results** — Leaders focus on the key inputs for their business and deliver them with the right quality and in a timely fashion. Despite setbacks, they rise to the occasion and never settle.
15. **Strive to be Earth’s Best Employer** — Leaders work every day to create a safer, more productive, higher performing, more diverse, and more just work environment. They lead with empathy, have fun at work, and make it easy for others to have fun. Leaders ask themselves: Are my fellow employees growing? Are they empowered? Are they ready for what’s next? Leaders have a vision for and commitment to their employees’ personal success, whether that be at Amazon or elsewhere.
16. **Success and Scale Bring Broad Responsibility** — We started in a garage, but we’re not there anymore. We are big, we impact the world, and we are far from perfect. We must be humble and thoughtful about even the secondary effects of our actions. Our local communities, planet, and future generations need us to be better every day. We must begin each day with a determination to make better, do better, and be better for our customers, our employees, our partners, and the world at large. And we must end every day knowing we can do even more tomorrow. Leaders create more than they consume and always leave things better than how they found them.

## 2. 官方 loop 结构（按级别）

| 级别 | 流程 | 面试数量/时长 | 来源（2026-10-15） |
|---|---|---|---|
| SDE II | Application → Online Assessment → Interview Loop → Interview Outcome (within 5 business days) | "four 55-minute interviews" | https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep |
| SDE II OA | "90 minutes to complete two technical questions followed by 20 minutes of Systems Design scenarios and an 8-minute multiple choice Work Style Survey" | — | 同上 |
| SDE III / Sr. SDE | Application → Technical Phone Screening (60 min, 一位资深 leader；一半 LP，一半 coding + system design) → Loop → Outcome (5 business days) | "five 55-minute interviews" | https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep |
| 新毕业生 / 实习 OA | Coding (avg 70 min) + Workstyles (15 min) + Work Simulation (60 min) + Feedback (5 min)；"one or two parts depending on country" | 官方 OA 页：公开在线资料可用（语言文档），不可复制粘贴，print screen 会终止 | https://www.amazon.jobs/content/en/how-we-hire/university/sde-oa （时长数字来自 jugaldb 对该页的转述，页面渲染版只写 "the SDE Online Assessment (OA) is the first step"） |

Interview loop 通用说明（https://www.amazon.jobs/content/en/how-we-hire/interview-loop ，2026-10-15，原文）：
- "In our interview process, you’ll meet individually with current employees in what we call the “interview loop.” Each person will assess different aspects of your skills and experience"
- Interviewers: "You’ll likely meet with two to seven people—this may include managers, teammates, stakeholders, and a Bar Raiser (someone from another team focused on hiring quality). Treat each interviewer the same ... don’t be distracted if you see them typing—they’re taking detailed notes"
- Duration: "around 45 minutes to an hour with each interviewer."
- Location: "Your interview may be remote or in person—check your email for details."
- Check-in: "If your interview is in person, plan to arrive 15 minutes early. Bring a government-issued photo ID, such as a driver’s license or passport."
- Dress code: "Comfortable and casual is fine."
- Resume: "Interviewers will have a copy, but feel free to bring your own as well."
- Lunch: "If you’re on-site and interviewing over lunch, we’ll provide a meal."
- Remote: "you’ll use Zoom or Amazon Chime"；部分 Zoom 面试启用转录技术（需同意 Amazon AI preferences）。
- After: "You can expect to hear from us within five business days." 面后会有 feedback survey；差旅费用报销有表格。
- 行为面："we avoid brain teasers like “How many windows are in Manhattan?”"；官方示例题（verbatim）：
  - "Tell me about a time you faced a problem with multiple possible solutions. How did you decide what to do, and what was the outcome?"
  - "Describe a time when you took a risk, made a mistake, or failed. What happened, and what did you learn?"
  - "Share an example of when you took the lead on a project."
  - "What did you do to motivate a group or encourage collaboration on a team project?"
  - "How have you used data to develop a strategy or make a decision?"
- STAR：Situation / Task / Action / Result；"It’s helpful to use “I” instead of “we.”"；"not every story has to be a success"；"We don’t expect perfect answers or rehearsed scripts"。
- "Why Amazon?" 是常见问题（页面原话 "“Why Amazon?” is a common question."）。

行为面细节（SDE II / SDE III 页，2026-10-15）："A significant portion of the conversation will focus on how you’ve demonstrated our Leadership Principles ... We won’t ask brain teasers ... Each interviewer will typically ask two or three behavioral-based questions about successes or challenges and how you handled them using our Leadership Principles." 以及 "different interviewers will be assigned to evaluate" LP 与 technical competencies。

## 3. 官方技术话题（SDE Interview Topics，2026-10-15）

https://www.amazon.jobs/en/landing_pages/software-development-topics ：
- "Most technical interviews require you to perform coding and system design white boarding exercises."
- 话题清单（10 项，原文顺序）：Programming language / Data structures / Algorithms / Coding / **Object-oriented design** / **Databases** / **Distributed computing** / Operating systems / Internet topics / General machine learning and artificial intelligence。
- "Your interviewers won’t be evaluating your ability to memorize all of the details for each of these topics. They’ll be looking for your ability to apply what you know to solve problems efficiently and effectively. We recommend reviewing computer science fundamentals and practicing coding outside of an integrated development environment."
- "Interviewing for a software engineer role that requires at least two years of experience? Prepare for your interview [-> SDE prep]"，即该话题页把 "<2 年" 和 "≥2 年" 分流；SDE II 页的 coding/system design 面板对 "at least two years" 适用。

## 4. 官方"技术能力"措辞（SDE II 页内嵌 JSON，2026-10-15）

来源：https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep （折叠面板 "Coding resources"）。四个能力 = 编码三项 + 系统设计；页面原话
"Be prepared for three separate interviews evaluating logical and maintainable code, problem-solving, and data structures and algorithms."
与 Seattle SDE-2 候选人的复述一致："Technical Competencies : Problem solving, DSA, Logical and maintainable code and system design"（LeetCode Discuss 6472834，2025-02-26，https://leetcode.com/discuss/post/6472834/ 的 topic id；见 forums.md）。

### 4.1 Data structures and algorithms（原文）
"Most of the work we do involves storing and providing access to data in efficient ways. This requires a strong background in data structures. You’ll need to understand the inner workings of common data structures and be able to compare and contrast their usage in various applications. You’ll be expected to know the runtimes for common operations as well as how they use memory. Understand data structures you encounter in core libraries, e.g. trees, hash maps, lists, arrays, and queues. Your interview will not be focused on rote memorization of algorithms. However, having a good understanding of the most common algorithms will make solving some of the questions easier. Review common algorithms such as traversals, divide and conquer, and breadth-first search vs. depth-first search, and understand the trade-offs for each. Knowing the runtimes, theoretical limitations, and basic implementation strategies of different classes of algorithms is more important than memorizing the specific details of any given algorithm."

### 4.2 Problem solving（原文）
"This competency assesses your ability to take something complex, break it down, identify a solution, and translate that solution into working code. These questions will most likely have an ambiguous problem statement. ... you will need to ask clarifying questions ... Split your time three ways: 1. Uncover requirements and consider evolution of the situation. 2. Implement a first pass of the design and cover all requirements. 3. Enhance the solution. When you’re satisfied you’ve met the original requirements, seek more requirements to show how your solution evolves when requirements change."

### 4.3 Logical and maintainable（原文，对应 LLD/OOD 的官方依据）
"This competency measures your ability to produce code that is easy to maintain, read, and understand. It also evaluates how you organize your methods and classes to ensure a clear separation of concerns. We want to see you name variables, methods, and classes so future developers with no knowledge of the code can understand how they work, evolve the logic, investigate, and debug. Your test names should describe business and technical requirements, and your test code should be consistent with your test names." 要点：write maintainable, readable, reusable code; "Make code extendable and avoid single functions that do everything"; "Use functions, classes, and inheritance to break the solution into logical components"; "Ensure code is reasonably easy to maintain as traffic/load increases"；"Write syntactically correct code, no pseudo code. Start with a working solution and enhance as you go."；语言清单：C, C++, C++14, C#, Go, Java7, Java8, JavaScript, Kotlin, Objective-C, PyPy2, PyPy3, Python2, Python3, Ruby, Scala, Swift。
`推断`：这个 competency 就是 Reddit/LeetCode 上说的 "LLD round / Logical & Maintainable round / OOD"；官方不用 "LLD" 称呼它，SDE III 页才单列 "Low-level design" 面板。

### 4.4 Best practices（编码页）
"Big O Notation: You’ll be asked to determine time/space complexity in almost all your interview questions, and how to optimize your code for better time/space complexity." "Think out loud. Explain your approach before coding ..." "The most important thing a SDE does at Amazon is write scalable, robust, and well-tested code. These are the main evaluation criteria. Also check for edge cases and validate that no bad input can slip through." "Expect to be asked to write syntactically correct code—no pseudo code."（官方推荐 Livecode 练习）；SDE III 页编码 Objectives：Efficiency / Reliability / Robustness / Portability / Maintainability / Readability。

### 4.5 System design（SDE II + SDE III 页原文）
- "At Amazon, designing software systems is unique due to our size and speed of change. **Expect at least one question on software systems design.**"
- Objectives（SDE II/III 页）：Practicality / Accuracy / Efficiency / Reliability / Optimization / Scalability。
- "Scaling is a critical part of software design at Amazon ... you may want to research scalability concepts and technology, such as caching, load balancing, non-relational databases, microservices, and sharding. You’ll need an understanding of distributed systems, SOA, and n-tiered software architecture."
- HLD 面板："This is an ambiguous problem to be solved in one line. We expect you to clarify requirements and abstract out systems and design to bring customer value ... Think about how you can split your system into five to seven high-level blocks ... use meaningful abstractions (for example, load balancers, horizontally scaled app servers, NOSQL DB, message queue, rate limiters, etc.). ... identify the data model or develop an object-oriented design or an API contract for one of the sub-systems. ... Your interviewer might ask you to create classes to represent users’ follows with actual functionality, or they may ask you to expose API endpoints ..." 官方示例实体：users, Tweets, follows, favorites, photos, videos。
- Question tips："Who are you designing for? Why? ... What happens if we become hyper-popular? What does twice the growth look like? Or ten times the growth? ... Ensure your design is addressing operations and resilience in addition to solving your customer’s problem. Consider key business and technical metrics, bottlenecks, failure points, redundancy, and log access for system debugging. If there are multiple viable system designs, compare their trade-offs, select one, and justify your decision." "**We are looking for broad comprehension of system design and expertise in one area.** If you’re asked to delve into an unfamiliar topic, let your interviewer know and suggest exploring a familiar topic instead."
- 官方 resource links（SDE II/III 页）：HackerRank "Distributed System Problems"（https://www.hackerrank.com/domains/distributed-systems/client-server/page:1）、GitHub `donnemartin/system-design-primer#index-of-system-design-topics`、书 *Scalability Rules: 50 Principles for Scaling Websites*、Educative "Grokking the Low Level Design Interview Using OOD Principles"（标题页面写作 "Design Library Management System, Parking Lot, and Others"）。**官方参考书目里没有 DDIA。**
- 官方视频逐字稿（下载自 static.jobs.production.amazon-jobs.brightspot.cloud，2026-10-15）：
  1. System Design Interview Prep（一位 SDM）：示例题 "designing an online bookstore"。流程："don't jump into solving the problem ... ask questions about the scale about the performance about whether it needs an API ... make this a conversation"；示例规模 "six million users"、"500 transactions per second"；"focus on your strengths ... if you're a back-end or a database person ... start talking about the database"；然后实体 -> API (POST /books, JSON) -> 服务拆分 (order/payment/book/search) -> 前端。（https://static.jobs.production.amazon-jobs.brightspot.cloud/6b/de/fe94b6d84b98a28ec604c5f8d1e7/transcript-system-design-interview-prep.docx）
  2. High-Level Design（Prep series Episode 3，Senior SDE）："evaluating the candidate’s skill on designing a large system. The end result should be an architecture diagram of overall system and sequence diagrams ... in just 30 to 40 minutes ... Use generic terms as much as possible, and rely on specific technologies as less ... interviewers are probably familiar with popular AWS products ... one major mistake ... forgetting about availability, storing everything in memory in a single host ... when talking of persistence think about what kind of storage systems ... even within a database explain the type of database like a DBMS, NoSQL, Graph DB ... candidates asking about some esoteric features from these databases ... I usually ask them to design that part in detail ... not understanding basic network stack ... if you are going to rely on something like Leader election it would be better if you know how it works, but at the very least be aware of its limitations ... make sure auxiliary systems are covered as well like data (BI/Analytics), monitoring (alerts, pagers), billing, reports". （https://static.jobs.production.amazon-jobs.brightspot.cloud/21/34/6a49615b4b70bc4d4a3a00796335/transcript-episode-3-prep-series-senior-software-development-engineer.docx）
  3. Low-Level Design（Episode 2，Senior SDE）："you come up with a detailed design of the system ... sufficiently detailed and complete that if it is given to a team of junior engineers they are able to implement it correctly ... a clean set of APIs, the entities ... sub-components ... this round expects you to go deep so be prepared to come up with class-level diagrams and if needed, code up the critical section. For the class design, think what design patterns may be applicable ... be vocal about trade-offs and assumptions ... Do not limit yourself to an abstract high level block diagram". （https://static.jobs.production.amazon-jobs.brightspot.cloud/55/5b/fd0caeeb4cc2b3c283fb3208a53e/transcript-episode-2-prep-series-senior-software-development-engineer.docx）
  4. **SDE Interview FAQs（官方，回答 "系统设计是偏架构还是偏 OOD"）**：“If you are applying for more senior positions you can expect to design a more complex system, possibly with lots of components where the interactions between those components and the scalability of the system are very important. But if you are applying for a more entry-level position you can expect to dive deep into a single component, identify the main abstractions of that component and we will possibly be asked to design an object-oriented model for those abstractions.” 同一视频另有：不必写能编译的 IDE 代码但要 "syntactically correct code that's readable"；“you will not really have time to write unit tests though after you finish coding you will be asked to validate your code with an example”；可以用任何语言；“starting with a brute force solution then optimize”。（https://static.jobs.production.amazon-jobs.brightspot.cloud/7d/ef/5e9012d545ba95aa2892723617e3/transcript-sde-interview-faqs.docx）

## 5. Bar Raiser（官方措辞）
- 官方 loop 页只有一句定义："a Bar Raiser (someone from another team focused on hiring quality)"（2026-10-15）。官方没有发布 "veto" 字样；veto 权来自 Hello Interview / 候选人转述（见 forums.md / github_repos.md，标二手）。
- 候选人 2026 的 Bar Raiser 描述（LeetCode Discuss 8420230，2026-07-25 SDE2 Prime Video Bangalore）："strictly a senior engineer (SDE3+) with 10+ years ... always from outside your hiring team ... no fixed structure"（二手）。

## 6. University / 新毕业生 OA（官方，2026-10-15）
https://www.amazon.jobs/content/en/how-we-hire/university/sde-oa ：
- "The SDE Online Assessment (OA) is the first step in the hiring process for our full-time and internship SDE roles ... No Amazon-specific knowledge is needed."
- "During the Coding Assessment, you’re allowed to use publicly accessible online resources (e.g., the Java Developer Kit or Standard Template Library). Don’t access sites that require a login or are private repositories. Your browser usage is logged."
- "Don’t use the print screen functionality, because your session will be terminated ... Avoid copying and pasting."
- "Manage your time: If you get stuck on a problem, move to the next one and revisit questions as needed."
- 同页指向 "Software Development Topics page" 与 "Leadership Principles"。
- 同页没有出现 loop 结构；SDE I 的 loop 结构见 forums.md 的 2025-2026 候选人汇总。

## 7. 抓取失败/受限记录（Rule 3）
- `https://www.amazon.jobs/content/en/how-we-hire/interview-process`、`/sde-interview-prep`、`/sde-interview-topics`、`/sde-interview-prep-course`：404 "no longer available"（2026-10-15）。
- `https://www.amazon.jobs/en/software-development-interview-prep`：SPA，jina 只回 149 bytes。
- `/content/en/how-we-hire/assessments`：jina 返回空文件，没重试镜像。
