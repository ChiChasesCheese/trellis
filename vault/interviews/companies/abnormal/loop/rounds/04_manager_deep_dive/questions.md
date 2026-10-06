# Manager / Behavioral + Technical Deep Dive · 题库（16 题）

> 来源：#8496901 R5（"Past projects · Technical decisions I had made · Challenges I had faced · Impact of my work · General behavioral/situational questions"）与 R6（"technical deep dive into my experience and decision-making"，挂在 "lacked sufficient judgment"）· Glassdoor（"Why do you want to work at Abnormal?"、"most challenging project"、"the hiring manager put emphasis on the ownership mentality"）· F-14 / Q19（"how I used AI in everyday work"）· 1p3a 1146766（"What does your current team structure look like?"）· 官方 O-15（"specific examples grounded in real decisions: what you owned, what the result was, where something didn't go as planned"）。
> 练：`python3 loop/mock.py bq hm -n 5 -m 3`。故事在 [[Core]]（[[S1]]–[[S11]]）；通用答案 [[Answers]]。**本轮唯一详细的挂法是"判断力"**，所以每个故事都按下面的"判断力五步"准备，而不是按 STAR 平铺。

## 判断力五步（deep dive 会一层层追到这里）

1. **当时的约束**：时间、数据、谁依赖你、错了的代价。
2. **备选方案**：至少两个，各自的代价（不是稻草人）。
3. **我选了什么、为什么**：用约束解释，不用"best practice"。
4. **结果 + 证据**：数字（量级）或可观察的事实。
5. **回头看**：哪里判断错了 / 现在会怎么改（Intellectual honesty，O-10）。

## 题表

| # | 题 | 考点 | 主故事 | 来源 |
|---|---|---|---|---|
| 1 | Walk me through the project you're most proud of — the decisions, not the tasks. | deep dive · 判断 | [[S1]] Amex 结算管线（六条 Stream、复合键 MERGE、校验 UDTF） | #8496901 R5/R6 · Glassdoor |
| 2 | Tell me about a technical decision you made that you'd make differently today. | intellectual honesty | [[S10]] 推翻自己 10× 的 blast radius · [[S1]] "我会改"清单 | #8496901 R6 · O-10 |
| 3 | Tell me about a time you decided NOT to build or ship something. | 判断 · 说不 | [[S6]] 实习生 ML 检测器 go/no-go（QA 6 商户 vs 生产 1.8 万） | R6 挂点 · O-10 |
| 4 | How do you use AI in your day-to-day work? How do you trust what it produces? | AI-native（HM 必问） | [[S7]] schema pool + on-call copilot："tech lead of a team of agents, I still own every diff" | F-14 · Q19 · O-12 |
| 5 | Tell me about the hardest bug or incident you handled. | 调试 · 压力 | [[S3]] ACH `'BT_' \|\| NULL` 静默事故 · [[S8]] 7 分钟 RCA | #8496901 R5 · JD "debugging with logs, metrics" |
| 6 | Tell me about a time you owned something end to end with nobody telling you what to do. | Ownership（"No one here says 'that's not my job'"） | [[S7]] schema pool · [[S1]] 从 stub 起 | O-10 · Glassdoor SF 2026-02 |
| 7 | Tell me about a time requirements were unclear. What did you do? | Agency · 模糊性 | [[S6]]（先把模糊状态写成文档）· [[S5]] 数据源切换 | O-11 · O-13 "When the path isn't clear, you're expected to make one" |
| 8 | Tell me about a time you disagreed with your manager or a senior engineer. | 价值观 · 判断 | [[S9]] region conditional > revert · [[S6]] | 通用 |
| 9 | What's the biggest impact you've had, and how do you know? | Impact · 证据 | [[S1]] / [[S5]]（量级口径表） | #8496901 R1/R5 |
| 10 | Describe a time you had to move fast and still not break things. | Velocity × Excellence | [[S5]] deploy ≠ release · 影子核对 | O-10 |
| 11 | Tell me about a time you worked across teams to get something unblocked. | 协作 | [[S4]] 一条查询结束 50 条回复 · [[S8]] | O-14 Team Interviews |
| 12 | What does your current team look like and what's your role in it? | 背景 | Braintree 结算/费用平台；我拥有 Amex 管线 + on-call | 1p3a 1146766 |
| 13 | Why Abnormal, and why Identity Security / insider risk? | 动机 | `../../../fit.md` §1–§2 | Glassdoor（多条） |
| 14 | Why are you leaving PayPal? | 动机 | `../../../fit.md` §3 | F-14（"why I was changing roles"） |
| 15 | How would you detect a fake candidate in a hiring pipeline? Walk me through a v1. | 领域 · 0→1 判断 | `../01_ai_screen/cb03_vetting/` 的 walkthrough + [[S6]]（规则先行、ML 后置、阈值与告警量） | JD O-1（"Drive 0→1 iteration … test fraud detection assumptions"） |
| 16 | An analyst says your detector is too noisy. What do you do in the first week? | 判断 · 用户 | [[S6]]（99.5% 阈值 × 每天数亿行 = 每天数百万条告警）· cb02 t2 / cb03 t3 | O-10 Customer obsession · JD |

## 3 个必背的英文首答（60–90 s）

### Q4 · How do you use AI? (这家公司一定会问)

> Two layers. Day to day I run Claude Code — and Codex or Cursor when one hits its limit — on real tickets: I have it map the code first, write a short plan with the assumptions spelled out, then implement in small steps with tests, and I read the diff at the level of "does this fit the system" before anything merges. Because several agent sessions were colliding on our shared Snowflake schema, I built a pool of zero-copy clones so each session gets its own isolated schema in about two seconds. On top of that I built an on-call copilot that pulls context from Slack, PagerDuty and Datadog into an agent session and drafts a reply I review before sending; a neighbouring team adopted it. The rule I keep: AI writes most of the code, I own every decision and every diff — in money-moving code I read every line.

### Q3 · Something you decided not to ship

> When an intern left, they handed over an ML anomaly detector for our fees that had only ever run in QA. The momentum was to just finish it. I wrote a go/no-go assessment first: QA had six synthetic merchants, production has about eighteen thousand and up to roughly 760 million rows on a peak day, and the inference ran row by row in numpy — it would never finish in time, and at a 99.5th-percentile threshold it would page us millions of times a day. So I split it: phase one, the deterministic consistency rules as SQL pushdown, which we could ship in weeks; phase two, retraining and re-architecting inference, behind an explicit go/no-go gate. And I exported the analysts' labels first, because that was the only thing that couldn't be rebuilt once the intern was gone. The judgment call was ranking by risk-adjusted value, not by sunk cost.

### Q2 · A decision I'd make differently

> 用 [[S10]] §5 的英文首答：先给出原来的结论、再给出推翻它的那个数字、最后说现在的流程改动（"I now size blast radius from the production distribution, not from the ticket"）。
