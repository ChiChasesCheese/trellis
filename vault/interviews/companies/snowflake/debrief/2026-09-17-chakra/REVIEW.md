# REVIEW · Snowflake Chakra 语音筛 · 2026-09-17 16:34（人工评审）

> 输入：`transcript.md`（mlx-whisper large-v3-turbo，本机转写）· `report.md`（`analyze.py` 的数字）· 对照 `../../loop/rounds/00_ai_screen/{rubric,stories,questions}.md`。
> **录音只录到了你的麦克风**，AI 的问题没有录进来；每题的"AI 问了什么"是从你的回答反推的。
> 打分照 Chakra 的四档：3 = 有 clarity / ownership / structured reasoning / specific examples 的**具体证据**；2 = 有故事缺深度或具体性；1 = 泛泛 / 讲原理。

## 0. 一句话结论

**英语不是你这场的问题；结构和"证据词"才是。** 约 1,900 个词里 LanguageTool 只找到 6 处语法问题（每百词 0.3），填充词每百词 0.7——这两项都比大多数母语候选人干净。真正掉分的是四件事，按严重度排：

1. **每个回答都没有 headline**。你的回答全部以 "Well, so…" / "Yeah, so now…" 起头，绕 20–30 秒才到重点；Reporter 事后读 transcript 找"具体证据"，找不到第一句就是结论的句子。5 个回答超过 90 秒（最长 154 秒），AI 大概率在你讲到机制之前就切段了。
2. **JD 加权关键词几乎没说**。整场 "Java" 出现 1 次（列举语言时），"distributed" 相关 6 次但都是形容词（"it's a distributed platform"），没有一次讲到 **MERGE / idempotent / stream offset / reconciliation 的机制**。准备好的原语名（`COPY INTO`、append-only Streams、composite-key MERGE、`FULL OUTER JOIN`、trigger-status JOIN）一个都没出现；"stream" 只出现在 "shadowing"里。数字只有两个（18 months、100 billion）。
3. **几句话会被 transcript 原样记下来并伤分**："nice to meet you, the **AI officer**"、"my on-call helper… named **the cheatbot**"、"I'm pretty interested in **your feedback on me**… okay okay okay then **forget about it**"、"thank you for your help and **your tokens**"、"I was named as a **rock star**… **top 5%**"、"I don't want to be **constrained** in a single area"。前四句是失礼/失言，后两句是无证据的自夸 + 隐性抱怨。
4. **发音把关键名词转丢了**——Whisper 把 Braintree 听成 "GreenTree"、Menlo 听成 "Meadow"、cron 听成 "chronicle"、Kotlin 听成 "Kovlin"、Cortex 听成 "COCO"。Chakra 也是用 transcript 打分的，它听到的和 Whisper 听到的是同一种错。见 §4 的发音清单。

好的部分也要记下来：**AI 工具那两题（14:16、17:02）是全场最好的**——"plan → TDD → CI gates；关注 gate 不关注行数"这句是 senior 的说法；"we are the downstream of the downstream, so we don't want to make any mistake"（13:23）和 "engineer-driven, we identify the problems on our own, discovery → ADR → implementation"（21:57）也是好句子，值得进 `stories.md`。

## 1. 这场实际的形状

不是邀请邮件写的"经历 / 场景 / 协作 / 反问"四段，而是 **Ashby 那封说的 "Talent Intake"**：14 个短问题的 recruiter 式摸底，没有 applied scenarios，没有明确的 collaboration 题。从回答反推的问题序列：

| # | 时间 | AI 问的（反推） | 你答了多久 | 题库对应 |
|---|---|---|---|---|
| 1 | 06:35 | 开场寒暄 | 6 s | — |
| 2 | 07:08 | Where are you located / relocation? | 8 + 14 s | 新增 F02 |
| 3 | 07:54 | Years of experience? | 15 s | 新增 F03 |
| 4 | 08:37 | Start date / notice period? Interviewing elsewhere? | 15 s | 新增 F04 · F05 |
| 5 | 09:08 | Primary programming languages? | 48 s | 新增 F06 |
| 6 | 10:06 | Tell me about your current role | **142 s** | A01 · A06 |
| 7 | 12:42 | What share of your time is coding vs other work? | 68 s | 新增 F07 |
| 8 | 14:02 | （没听清，请它重复） | — | — |
| 9 | 14:16 | How do you use AI tools in your work? | **153 s** | A13 |
| 10 | 17:02 | How do you decide whether to trust AI-generated code? | 85 s | 新增 F08 |
| 11 | 18:41 | Walk me through a project / milestone you're proud of | **140 s** | A02 · A04 |
| 12 | 21:20 | Tell me about a time you took ownership / drove something end to end | **154 s** | C13 · A05 |
| 13 | 24:05 | Tell me about your background and why Snowflake | **112 s** | A17 |
| 14 | 26:09 | Do you have questions for us? | 20 + 60 s | E01 |

## 2. 逐题评审

打分列：**Chakra 档 / 我认为它会记下的证据**。改写都是 English、≤ 60 s、照 `stories.md` 的骨架。

### Q2 · 地点（07:08）— 2

说了 "San Jose, 20 miles from your Menlo Park headquarters"（好，具体）；但 "Meadow Park"、"the one in San Francisco if you have"（Snowflake 没有 SF 办公室——JD 是 Menlo Park / Bellevue）、"anyways, open to all" 松。
> "I'm in San Jose, about twenty miles from Menlo Park, so Menlo Park is my preference. I'm open to Bellevue as well."

### Q3 · 年限（07:54）— 2

"roughly two years, more specifically 18 months since January 2025"——两个数打架（2025-01 到现在是 20 个月），而且漏了实习。
> "About two years on the same team — I interned there in 2024 and joined full-time in January 2025."

### Q4 · 时间线 / 是否在面别家（08:37）— 1

"that'll be enough for me and my team"（前半句没录到，语义断）；"I'm **not actively interviewing** any company, just casually looking forward to new opportunities"——对 recruiter 来说这句降低你的紧迫度和市场价值，且 "casually" 不像 senior。
> "I could start in early November after a standard notice period. I'm in conversations with a small number of platform teams, and Snowflake is the one I'm most interested in."

### Q5 · 主力语言（09:08）— 2

结构好："Java, Kotlin, Ruby on Rails, and SQL — I put SQL last but it's the most important in my day-to-day"，这是一个 headline。但后半段 "migrate every computation logic into an all-in-one data warehouse hosted in Snowglobe" 把公司内部名当成了产品名，AI 听不懂 "Snowglobe"。**Java 只在这里出现了一次**——JD 4/6 点名 Java，应该多说一句 Java 在你系统里的位置。
> "Java and SQL, in that order of volume but the reverse order of importance. Our platform is database-first: the business logic — fee calculation, settlement — lives in Snowflake SQL, stored procedures and tasks; Java 17 with Gradle and Flyway does orchestration, testing and deployment. I've also written Kotlin gRPC services and worked in a Rails payout system."

### Q6 · 现在的角色（10:06，142 s）— 2

**问题**：(a) 开头 "main owner and the builder of the Snowglobe platform" 好，但接着 "it sounds like a data warehouse but actually it's a distributed platform… it can be hosted anywhere to achieve the availability and consistency" 是空话，而且技术上站不住（Snowflake 不是"hosted anywhere"，AI 若追问 CAP 你没准备）；(b) "build it from zero to one and migrate funding, pricing and reporting into this warehouse" 是三个系统级的 overclaim，一追问 "which of those did you personally migrate" 就要收回；(c) "Snowflake SQL is not a very high-level programming language but in essence it can be expressive enough" 花了 20 秒讲一句没有信息的话；(d) 结尾 "Yeah, that's pretty much about it" 是在告诉打分器"我没有 learning"。
**它会记下的证据**：stored procedures、tasks、DAG、"ledger every row"、shadowing / parity。
> 用 `playbook.md` §2 的 60 秒自我介绍替换整段：三件事（Amex pipeline · quality-check framework · interchange migration）+ schema pool + hook。每件事一句机制、一个量级。

### Q7 · coding 占比（12:42）— 2（接近 3）

"60% coding including design, 40% business and meetings… data contracts in sync… **we are the downstream of the downstream**, we take care of fee calculation and disbursement, and we don't want to make any mistake" ——这是全场最有"senior 味"的段落之一，只是缺一个具体例子。
> 加一句："For example, the trigger-status handshake I built is literally a data contract: downstream teams join on a `Completed` status row before they read a day's data."

### Q9 · AI 工具（14:16，153 s）— 2

内容其实是全场最独特的（多 agent 并行 + 自建 on-call 助手），但：(a) "this is a long story as well, because, well, anyways" 开头浪费 8 秒；(b) 工具名 "COCO"（应是 Snowflake Cortex Code？）AI 听不懂；(c) **"named after my name, which is the cheatbot"** —— "cheat" 在面试 transcript 里是一个会被单独标红的词，改名；(d) "I'm not sure whether this one is related to your topic" 自我否定；(e) 153 秒太长，AI 可能在 "rate limit" 那段就切了。
> "Two layers. Day to day I run Claude Code, Codex and Cursor in parallel — each has its own usage limit, so I built a schema pool of zero-copy Snowflake clones so several agent sessions can run migrations and integration tests at the same time without colliding. On top of that I built an on-call copilot: it polls Slack, PagerDuty and Datadog, opens the right agent session with that context, and drafts the reply as a Slack draft I review and send. Teams next to ours adopted it. The principle: I'm the tech lead of a team of agents, and I still own every diff."

### Q10 · 信任 AI 代码（17:02，85 s）— 3

"Step one: a detailed plan from me and the agent. Step two: TDD in every phase. Final gate: CI and monitoring… **focus on the gates and thresholds of quality, not the lines of code**." 结构清楚、有原则句。唯一缺的是 ownership 一句。
> 结尾加："And in a system that moves money I read every line that touches a fee calculation myself — the agent drafts, I own correctness."

### Q11 · 里程碑项目（18:41，140 s）— 2

**问题**：(a) 前 30 秒讲 net settlement 背景（"T plus 30 means we charge fees next month"）——含混，且不是你要讲的项目；(b) "my tech lead and my staff engineer are all on sabbatical PTO so I had to take care of all of this" ——ownership 是真的，但这句听起来像"没人管所以我做"，改成主动承接；(c) 机制部分 "file uploading to S3 → parse → make it unique → split into tables using **the chronicle task triggers** and stored procedures → shadowing" 方向对但没有一个准确的原语名：没有 Streams、没有 MERGE、没有 idempotent、没有 good-funds model；(d) **"over 100 billion… with no bugs, no accidents"** ——"no bugs" 是任何 senior 都不会说的话（你自己的 S3 就是这个管线下游的事故），AI 若追问 "what broke" 就自相矛盾。
**它会记下的证据**：S3、parse files、tasks、stored procedures、shadowing、100 billion、"I built from scratch"。
> 用 `stories.md` §S1 的 90 秒首答。必说四点：good-funds model → `COPY INTO` + six append-only Streams + composite-key `MERGE` + two validation table functions with `FULL OUTER JOIN` → idempotent at every stage → "what I'd change: config-driven parser"。把 "no bugs" 换成 "and when something did break — a late file, a reject flag — the pipeline recorded it instead of dropping it, which is the design decision I'm proudest of."

### Q12 · Ownership / 质量门（21:20，154 s）— 2

**问题**：(a) "I am now the main on-call handler and also the closest membership with our engineers and managers" 语义不清（closest relationship?）；(b) "**GreenTree** which is on par with Stripe" —— Braintree 发音被听成 GreenTree，而且和 Stripe 比是给自己加压；(c) "engineer-driven instead of product-manager driven… discovery tickets, ADR, PRD all on my own" **好**；(d) 质量门框架讲了 60 秒只有 "centralized quality gate framework… hard gate to anyone who wants to contribute"，没有机制（config table、executor、trigger-status、downstream JOIN）、没有数字（8 subject areas）、没有 ADR 那段 senior 的自我纠错。
> 用 `stories.md` §S2 的 90 秒首答，把 "hard gate" 具体化成 "readiness became a JOIN condition in the consumer's SQL, not a Slack message"。

### Q13 · 背景 / 为什么 Snowflake（24:05，112 s）— 1

**问题**：(a) "I'm not sure whether this is a little bit off topic" 开头；(b) 本科土木 → CS 转行的叙事本身可以是亮点（goal-oriented），但接着 "**rock star of the organization**"、"**annual review exceptional, top 5%**"、"I've already proved that I have the ability and talent to build amazing infrastructure" ——三连自夸而无一个可引用的证据，Reporter 只会记 "vague"；(c) "**I don't want to be constrained** in a single area" 会被读成对现公司的抱怨；(d) 最后 20 秒的 why-Snowflake 其实对："my day-to-day work involves a lot of Snowflake and I hope to get involved in the development of this product" —— 应该是整段的第一句。
> "The short version: I've spent two years as one of the heaviest users of exactly the primitives your backend teams build — Streams, Tasks, MERGE semantics, task DAGs, warehouse cost — inside a platform that moves real money. I know where they're great and where they hurt: stream staleness is silent, task observability is thin. I want to move from consuming those primitives to building them. On background: I came to CS from a construction-management degree, which is why I'm comfortable owning a system end to end rather than a slice of it."

### Q14 · 反问（26:09 + 27:14）— 1

第一问 "do you have any specific preference over the qualification of candidates" 尚可；第二段 "given that you are an AI interviewer, I'm pretty interested in your feedback on me… **okay okay okay then forget about it**"（AI 显然拒绝了）→ 7.9 秒沉默 → "what is the thing that you value most from an engineer that has already worked from another company" ——句子本身勉强，但前面的尴尬和沉默都在 transcript 里。收尾 "thank you so much for your help and **your tokens**" 是对 AI 开玩笑，人看记录会皱眉。
> 用 `playbook.md` §6 的两问一表态，收尾用 §8 的三个关键词。对 AI 只问流程类问题；不要求它评价你。

## 3. 三个横向问题的练法

**A. Headline first（最重要，一周能改）。** 每题第一句必须是结论或定位。练法：`python3 loop/mock.py bq ai -n 8 -m 1`，每题只允许说**两句话**：第一句 headline，第二句一个机制或数字。录音，听自己是不是以 "Well, so…" 开头；是就重来。这一周不练长答案，只练前两句。

**B. 证据词说出口。** 从 `CARD.md` 挑 15 个词做成一张单独的卡：`MERGE` · `append-only stream` · `idempotent` · `composite key` · `FULL OUTER JOIN` · `COPY INTO` · `trigger status` · `JOIN on Completed` · `feature toggle` · `shadow run` · `reconciliation` · `Java 17` · `Flyway` · `zero-copy clone` · `micro-partition`。每个故事讲完自查：至少 3 个词说出口了没有。

**C. 删掉五类句子。** (1) 自我否定："I'm not sure whether this is related / off topic"；(2) 无证据自夸："rock star / top 5% / amazing"；(3) 绝对化："no bugs, no accidents"；(4) 对 AI 的玩笑和请求："your tokens"、"your feedback on me"；(5) 隐性抱怨："constrained"、"my tech lead is on sabbatical so I had to"。替代物都在 `stories.md` 里。

## 4. 发音清单（转写把它们听成了别的词——AI 也会）

| 你说的 | 被听成 | 练法 |
|---|---|---|
| Braintree | GreenTree | /ˈbreɪn.triː/，"brain" + "tree"，重音在前 |
| Menlo (Park) | Meadow | /ˈmen.loʊ/，"men" + "low" |
| cron (task) | chronicle | /krɒn/ 一个音节；或直接说 "scheduled task" |
| Kotlin | Kovlin | /ˈkɒt.lɪn/，t 要出来 |
| Cortex Code（如果你说的是它） | COCO | 说全名 "Snowflake Cortex Code" |
| Snowglobe | （听对了，但 AI 不知道它是什么） | 第一次出现时解释："our internal Snowflake-native settlement platform" |
| anyways | anyways | 改 "anyway"，或直接删 |

另外三处语法（LanguageTool）：`I've already have` → `I've already had` / `I have`；`100 billion total transaction amount` → `in transaction volume`；`sessions information` → `session information`。就这些，别在语法上花时间。

## 5. 回写到 kit

- `02-process.md` 末尾「亲历」：这轮是 14 问的 intake，不是四段式；无场景题；AI 拒绝给反馈；总时长 23 分钟（对话窗口）。
- `loop/rounds/00_ai_screen/questions.md` 新增 F 段（亲历 8 题）→ `build_bank.py`。
- `stories.md` 收进两句好话："we are the downstream of the downstream" · "engineer-driven: we identify the problem, write the discovery and the ADR, then implement"。
- 下一场（recruiter call）前：只练 §3 A/B，两天。
