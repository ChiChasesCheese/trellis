# 06 · 反问清单

## A. 对 Chakra（AI）— 它只能答流程类；目的是在 transcript 留下「具体兴趣」

挑 2 个流程题 + 1 句表态：

1. "What are the next steps after this screen, and roughly when would I hear back?"
2. "Which areas does this screen weight most heavily — so I can prepare well for the technical rounds?"
3. 表态（不是问题，是让 transcript 有这句话）：
   > "One thing I'd like to ask the team in the next round: how the tasks and dynamic-tables scheduling side is organized, and whether the metering and billing pipeline is a place an early-career engineer can own something end to end."

不要问：薪资、level、具体组、manager、RTO（留到 HR / HM）。

## B. 对 recruiter / HR（GenSWE 流程）

- "Is the Chakra screen the same as the Ashby 'Talent Intake', or are those two separate steps?"（矛盾 #1，必问）
- "For GenSWE, when does team matching happen — before or after the onsite — and how much say do candidates have?"
- "Which orgs are hiring through GenSWE in Menlo Park vs Bellevue right now?"
- "Is there an OA before the technical phone screens for this track?"
- Level 只在 recruiter 主动提时接："I'd like leveling to reflect the end-to-end ownership I've had; happy to discuss once we know the team."

## C. 对工程师（电面 / onsite 的最后 10 分钟）— 每轮挑 2 个，要能听懂答案

**分布式 / 内部**
- "The Execution Anchor post said ~99% of queries never move between GS instances. How do you test the 1% — the retry and crash-transfer paths? Chaos testing, or replay?"
- "After the September 9 metadata infrastructure incident, is blast-radius isolation at the FoundationDB layer something the org is investing in?"

**调度 / Dynamic Tables**
- "For task graphs and dynamic tables, what's the current thinking on partial-failure semantics — does a failed downstream node retry independently or re-run the DAG?"
- "Adaptive Refresh decides between incremental and reinitialize — what signal drives that?"

**计量 / 计费**
- "AI workloads carry a lower gross margin — 74% guided. On the backend, what does that translate into: metering precision, routing cost, both?"
- "With dynamic model routing, how do you attribute cost back to a customer when the model choice changed mid-pipeline?"

**产品线**
- "Is Datastream a separate ingestion kernel from Snowpipe Streaming, or the same engine with a Kafka wire protocol in front?"
- "How do the Snowflake Postgres team and the Unistore/FDB team divide the transactional layer?"

**团队 / 日常（team matching 时）**
- "What does on-call look like on this team — pager frequency, rotation size?"
- "How is the 3-day RTO applied on this team in practice?"
- "How are Claude Code / CoCo used in the team's own development workflow?"（对上简历 bullet 4）

## D. 对 hiring manager

- "What would a strong first six months look like for an IC1 on this team?"
- "What's the one system on this team you wish someone would own end to end?"
- "How does the team decide between shipping a feature and paying down a correctness debt?"
