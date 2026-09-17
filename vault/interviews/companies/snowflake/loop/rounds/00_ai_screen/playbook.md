# playbook · Chakra 20 分钟逐分钟剧本（Snowflake · GenSWE / Software Engineer - Backend）

> 通用机制与操作清单在 `../../../../../core/playbooks/ai-voice-screen.md`（先读一遍）。本文件只做一件事：**把 20 分钟按邀请邮件的四段拆成逐分钟脚本，每段配好英文口述稿**。面试是英文；稿子是英文，注释是中文。
> 打分铁律：Reporter 只读 transcript，每条 expectation 要有「clarity / ownership / structured reasoning / specific examples」的**具体证据**；theoretical = Not Met；没说到 = 0；JD 的 **must-have 加权**。所以每段都要**说出原语名、决定、量级、"I decided / I designed / I owned"**，并主动命中 JD 关键词：**SQL · distributed systems · Java · database internals · large-scale production**。
> 故事全文与追问版在 `stories.md`；题库在 `questions.md` / `bank.json`；场景题在 `scenarios.md`；考前卡在 `CARD.md`。

## 0. 一句话定位（贴在摄像头旁的卡片第一行）

> **Backend engineer who owns a Snowflake-native settlement and fee-calculation platform end to end — tens of millions of transactions, billions of dollars a year — and now wants to build the primitives I've been consuming.**

三个关键词，收尾时再说一遍：**ownership · correctness at scale · Snowflake-native**。

## 1. 时间表

| 分钟 | 段（邮件原文） | 主答 | 备用追问 |
|---|---|---|---|
| 0–1 | 开场 | 听议程；可问 "How many sections and roughly how long each?" | — |
| 1–6 | Your experience and role-related background | 自我介绍 60 s → 项目深挖 **S1** 90 s | S1 追问版 ×6（`stories.md`） |
| 6–11 | Applied scenarios relevant to your role | 通用开场句 → Clarify → 3 步 → 最接近的真实例子 → trade-off（`scenarios.md`） | 每题 60–90 s |
| 11–16 | Collaboration and decision-making | **S5** 决策 90 s；**S4** 跨团队 60 s；**S6** 说不 60 s（按它问的挑） | S2 ADR / S9 事故 / S8 unblock 作备用 |
| 16–19 | Questions you may have for us | 2 个它能答的 + 1 句表态（§6） | — |
| 19–20 | 收尾 | 三个关键词 + 感谢 | — |

它会按 allotted duration 主动切段。**任何一段被切走都不要恋战**——没讲完的关键词下一段找机会补一句。看到 **Thinking** 闭嘴等；**Listening** 才开口。沉默用 "Let me think about that for a second — the key decision there was…" 填。

## 2. 段一 · 自我介绍（60 秒，English）

> I'm a backend engineer at PayPal on the Braintree Pricing & Settlement team. For the last two years I've been the primary owner of our settlement and fee-calculation platform — internally it's called Snowglobe. It's built natively on Snowflake: Streams, Tasks, stored procedures and table functions carry the business logic, with **Java 17 and Gradle** for orchestration, testing and Flyway deployments. It's a **database-first system** — the correctness of a lot of money lives in SQL I wrote.
>
> Three things sum up my work. First, I designed and built the end-to-end American Express settlement pipeline — file ingestion through fee calculation to payout — which processes tens of millions of transactions a year. Second, I built the team's config-driven **quality-check and trigger-status framework**: the handshake every downstream consumer now joins on before reading a day's data, rolled out across eight subject areas. Third, I owned the migration of our interchange source of truth to the acquirer's settlement view — shadow-validated with the production query itself before it went behind a feature toggle.
>
> On the side, I built a zero-copy-clone **schema pool** so multiple engineers — and multiple AI coding-agent sessions — can run migrations and integration tests in parallel without colliding.
>
> Before that I did my master's in CS at NYU and interned on the same team, building Kafka-based transaction-event processing. I'm interested in Snowflake because I've spent two years as a very heavy user of exactly the primitives your backend teams build, and I want to work on the platform side of that.

中文注释：
- 四个 JD 关键词已经在里面：**SQL / Java / database-first / large-scale**。distributed systems 在 S1/S5 里补（idempotency、handshake、exactly-once by design）。
- 最后一句是 hook，引它去问「你用 Snowflake 做了什么」——这正是最强的地方。
- 如果它开场就要 "recent project"，跳过第二段直接进 S1。

## 3. 段一 · 项目深挖 S1（90 秒首答 + 追问版）

首答全文和六条追问（"what was yours / why streams not Airflow / how do you know it's correct / what broke / what would you change / how does it relate to Snowflake"）见 `stories.md` §S1。首答的**四个必说点**：

1. 为什么 Amex 不能乐观入账 → **good-funds model** + pending 表（domain 判断力）
2. 原语名：`COPY INTO` · append-only **Streams** · `MERGE` on composite key · UDTF with `FULL OUTER JOIN` · Task `AFTER A, B`（database internals）
3. 幂等从哪来：文件级 dedup + 每级 `MERGE` 键（distributed-systems 语义）
4. "What I'd change"：offset 配置表 + 通用解析 UDTF（senior 的自我批评）

## 4. 段二 · Applied scenarios

见 `scenarios.md`（12 题）。通用开场句先说：*"Let me structure this: first what I'd want to know, then how I'd approach it, then the closest thing I've actually done."* 没做过就说没做过 + 最接近的真实经验 + 方法。

## 5. 段三 · 协作与决策（三选二，按它问的挑）

- **技术决策 + trade-off** → S5（静态拆分 vs 更聪明的 fallback；同源验证；deploy ≠ release）
- **跨团队 / 分歧** → S4（用同一条查询结束 50 条回复的争论）或 S9（事故里给 SLA 定论、主张 region conditional 而非 revert）
- **说不 / 推迟投入** → S6（go/no-go 门 + 分阶段）
- **说服团队改方案** → S2 ADR（四方案 + strictest-wins 论证 + 容量分析）
- **压力下 unblock** → S8（7 分钟 RCA + 主动指出未爆的同类风险）
- **带人 / 影响别人** → 见 §7 "Mentoring" 的说法

每个故事的最后一句必须是 learning 或 principle：**fail loudly · same SQL for validation and production · deploy ≠ release · config over code · strictest wins**。

## 6. 段四 · 反问（对 AI，它只能答流程类）

1. "What are the next steps after this screen, and roughly when would I hear back?"
2. "Which areas does this screen weight most heavily for the backend role?"
3. 表态（不是问题，是给 transcript 留证据）："One thing I'd like to explore with the team next round is how the Streams, Tasks and Dynamic Tables scheduling side is organized, and whether metering and billing is an area where an engineer can own something end to end — that's the shape of work I've been doing."

更多见 `../../../06-questions-to-ask.md`。

## 7. 危险追问与答法

| 追问                                           | 答法                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Your resume says $600B+ annual volume"      | "That's the platform-level annual volume the pipeline sits inside. The pipeline I personally own processes tens of millions of Amex transactions a year — billions of dollars — and that's the number I'd stand behind in detail."                                                                                                                                                                                    |
| "How much of the repo is yours?"             | "Roughly ninety PRs over two years; the two largest changes in the repo's recent history — the Amex pipeline and the quality-check framework — are mine. I'd rather be measured by what the pipelines process than by commit count."                                                                                                                                                                                  |
| "Did the merchant-level quality check ship?" | "The framework and eight rollouts are live; merchant-level readiness is designed, reviewed, and proven for one subject area, and the framework-wide rollout is sequenced behind the net-settlement ramp."                                                                                                                                                                                                             |
| "The Ruby / legacy migration?"               | "The Amex settlement logic used to live in our Rails payout service; my pipeline is the Snowflake-native replacement on the receiving side — the payout service now consumes my output."                                                                                                                                                                                                                              |
| "Sentry?"                                    | 主讲 Datadog + 自建 Streamlit 监控 + 健康检查存储过程带 on-call 属性；Sentry 是应用层错误跟踪。                                                                                                                                                                                                                                                                                                                                                  |
| "Kafka?"                                     | 讲生产的：Gateway 交易事件 → Kafka → Snowpipe Streaming 落地表 → Stream/Task；Funding→Snowflake 的 Kafka CDC 管道；实习期 Kafka→Snowflake connector + protobuf converter + poison-message 隔离。消费者语义（at-least-once + 幂等写）说得清；broker 运维是边界。                                                                                                                                                                                                  |
| "Did you mentor anyone?"                     | "Yes — a newer engineer whose work — the Snowglobe exclusion service in the pricing app and the journaling-schedule sync from the payout service — plugs into the domain I own. I set the contracts on my side, reviewed his designs against how the downstream consumes the same events, and I'm the fee-calculation authority he pulls in during incidents. Plus an intern's ML project I inherited and re-scoped." |
| "Why leave PayPal?"                          | "I've owned one platform end to end for two years; the next step in depth is building the primitives I've been consuming." 不抱怨。                                                                                                                                                                                                                                                                                       |
| "Level / comp?"                              | "I'm focused on fit at this stage; happy to discuss with the recruiter once we know the team and level."                                                                                                                                                                                                                                                                                                              |
| 它问的场景我没做过                                    | "I haven't built X, but the closest thing I've done is Y — and here's how I'd approach X."                                                                                                                                                                                                                                                                                                                            |
| "Are you a senior engineer?"                 | "I operate like one on my platform: I write the design docs and ADRs, own the on-call and the incidents, set the frameworks other engineers onboard onto, and mentor. The title will follow the scope."                                                                                                                                                                                                               |
|                                              |                                                                                                                                                                                                                                                                                                                                                                                                                       |

## 8. 收尾（20 秒）

> To sum up: I bring end-to-end ownership of a Snowflake-native settlement platform, a track record of getting correctness right at scale — idempotent pipelines, quality gates, honest postmortems — and I want to move from consuming these primitives to building them. Thank you — I'm looking forward to the next conversation with the team.

## 9. 前一晚 / 当天

- 前一晚：`../../../07-mock.md` 跑两遍（一遍看稿，一遍不看稿只看 `CARD.md`）；每个故事录音 90 秒回听——检查是否有 headline / 原语名 / "I decided" / learning。
- 当天：`../../../../../core/playbooks/ai-voice-screen.md` §4 清单逐项打勾；用 **Chrome**；关键词卡贴摄像头旁；开 real-time transcript。
- 面完：实际被问的题写进 `../../../02-process.md` 末尾「亲历」节，新题追加到 `bank.json`。
