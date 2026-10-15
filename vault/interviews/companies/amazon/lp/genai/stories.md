# GenAI 故事库：4 个英文 STAR（每个 60–90 秒）

> 全部取自 trellis 仓库里**可验证**的证据。引用格式：`commit 短哈希` / 文件路径（仓库根 = `/Users/chiserver/sessions/trellis`）。面试官问你"能给我看吗"，你说得出是哪个提交、哪个文件。
> 关于"我"：证据能证明的是规则、门禁、台账和被纠正的错误；**不能证明**某次审查是 Chi 亲手发现还是 orchestrator 会话在 Chi 的规则下发现。所以口播句子主语用 "I set up / I wrote the rule / my review step caught"，被追问时用 `【待 Chi 补】` 里 Chi 自己的真实回忆回答。**不要编出你没有的回忆。**
> 日常工作（PayPal）的 AI 使用只引用 `core/` 里已有的话（`../../../../core/stories/S7 Schema pool.md`、简历一句、`../stories/R2_ai-native-migration.md`）；其余 `【待 Chi 补】`。
> 时长按每分钟约 150 词估算；字数由脚本统计（文末）。

| # | 故事 | 回答的题 | 主 LP | 副 LP |
|---|---|---|---|---|
| G1 | 一个自信的错数字：碰撞概率 38% vs 必然 | "a time AI hallucinated" | Dive Deep | Insist on the Highest Standards, Earn Trust |
| G2 | 让正确性不依赖 agent 的自述：门禁 + 复算 + 变异测试（**senior 机制故事**） | "how do you verify" | Insist on the Highest Standards | Invent and Simplify, Ownership |
| G3 | 什么时候 AI 不必要或更慢：计数用脚本、委派有成本 | "where GenAI was unnecessary" | Frugality | Dive Deep, Bias for Action |
| G4 | 信任的判定规则：oracle × 爆炸半径 | "when do you trust an LLM" | Are Right, A Lot | Ownership, Learn and Be Curious |

**最先背的 20 秒开场（回答 "How do you use GenAI?"）**——全部来自 S7 与简历：

**Hook：「I use it in two layers.」**

**Layer 1 · Day to day**
- I run **Claude Code, Codex and Cursor** in parallel.
- I **plan** the change with the agent, do **TDD** for each phase, and let **CI and monitoring gates** decide.
- In **money code** I **read every diff** myself.

**Layer 2 · On top**
- I treat it as a **team of agents I lead**: I set the **rules** and an **acceptance gate that's a command**.
- I **never accept** an agent's own "done".
- My **study-system repo** is where those rules are written down and measured.
- 【待 Chi 补：一句具体的日常例子——最近一次用它做的具体任务和结果。】

<details><summary>逐字稿（参考，不背）</summary>

> I use it in two layers. Day to day I run Claude Code, Codex and Cursor in parallel — I plan the change with the agent, do TDD for each phase, and let CI and monitoring gates decide; in money code I read every diff myself. On top of that I treat it as a team of agents I lead: I set the rules, an acceptance gate that's a command, and I never accept an agent's own "done". My study-system repo is where those rules are written down and measured. 【待 Chi 补：一句具体的日常例子——最近一次用它做的具体任务和结果。】

</details>

边界：S7 的 schema pool 与 on-call copilot 是**个人仓库**，相邻团队采用，不是团队官方工具链。

---

## G1 · 一个自信的错数字（hallucination 被验收门抓到）

**主 LP：Dive Deep。** 备用 LP：Insist on the Highest Standards（"defects do not get sent down the line"）、Earn Trust（对读者负责）。

### 口述提纲（60–90 秒）

**Hook：「I re-derived the number with a script instead of trusting how confident it sounded.」**

**S · Situation**
- I'm building a **system-design study bank**: about **50 problems**, drafted by **Claude Code subagents**.
- A learner **memorizes** those numbers, so a wrong one is a **shipped defect**.

**T · Task**
- I **own correctness**: the agent drafts, and **I** make sure nothing wrong gets through.

**A · Action** (in the order it happened)
1. On the **first pilot problem**, the article stated a hash-collision probability of **38 percent**.
2. I **re-derived** it with a one-line script: the real answer was **certainty**, the exponent off by **six orders of magnitude**.
3. The wrong figure was **already in a flashcard**, so I fixed the **article first, then the card**.
4. I stopped treating it as one bug and wrote a **rule** into the shared agent instructions: every number is **computed, never recalled**.
5. Second rule: a number you **couldn't verify** never goes into a card.
6. **Later**, a second article had correct arithmetic on **two contradicting assumptions** (a **1,560x** peak ratio), so I added: assumptions must **agree with each other**.

**R · Result**
- All **49** problems passed the gate; **two** were redone for design substance.
- **Four lessons** now live in the instruction file.

**L · Learning / Mechanism**
- The model's **confidence tells you nothing**; arithmetic is cheap, so **check it by machine**.

<details><summary>逐字稿（参考，不背）</summary>

> **Situation.** I'm building a system-design study bank — about fifty problems, each a worked solution plus flashcards — and Claude Code subagents write the drafts. A learner will memorize those numbers, so a wrong one is a shipped defect.
>
> **Task.** I own correctness. The agent's job is to draft; mine is to make sure nothing wrong gets through.
>
> **Action.** On the first pilot problem, the article stated a hash-collision probability of 38 percent. I re-derived it with a one-line script, and the real answer was certainty — the exponent was off by six orders of magnitude. Worse, the wrong figure had already been copied into a flashcard, so I fixed the article first, then the card. Then I stopped treating it as one bug. I wrote a rule into the shared agent instructions: every number is computed by a script, never recalled; and a number you couldn't verify never goes into a card. Later a second article was arithmetically correct but built on two assumptions that contradicted each other — a 1,560-times peak ratio — so I added a rule that assumptions must agree with each other.
>
> **Result.** All 49 problems passed the gate, two were redone for design substance, and four lessons now live in the instruction file.
>
> **Learning.** The model's confidence tells you nothing. Arithmetic is cheap to check, so check it by machine.

</details>

### 证据（Chi 可以引用）

| 事实 | 证据 |
|---|---|
| 碰撞概率 38% vs 必然、指数差 6 个量级、已抄进卡片 | `proposals/design-problems/AGENT.md`（"Every number is computed, never recalled" 一段）；该规则随 URL shortener 试点一起提交：`8785a2cd`（2026-09-19） |
| 1,560 倍峰均比来自两个矛盾假设（2% 开场一分钟下单 vs 0.5% 全天） | 同文件 "Assumptions must agree with each other"；规则提交 `5bc67c2b` |
| 未核实数字不进卡片 | 同文件；规则提交 `79de2b64` |
| 49/49 通过、391 张题目卡、两篇因设计实质返工（live-comments、leaderboard）、一处逻辑矛盾改正、四条教训写入 AGENT.md | `vault/domains/system-design/BUILD.md` 台账 2026-09-20 两行；总结提交 `9743d8b3` |
| 同类失败表（算术、矛盾假设、二手当官方、节点 10 倍低估） | `.claude/skills/building-problem-banks/SKILL.md` "What agents get wrong" |

**可选的第二个例子（编译器当 verifier）**：Java 21 课本里的矩阵例子 `case Order(var id, Side.BUY, var px, var q)` 不能编译（record 模式里不能写常量，要用 `when` 守卫）。「36 个示例全部 javac 通过」这个门禁发现了它，在 `277ff22a`（分支 `headlands-kit`，未合并 main）里改成 `when side == Side.BUY`。LEDGER 行："J01–J09 课本 | 36 示例 javac 通过；J04 矩阵例子改正"（`headlands/LEDGER.md`，同分支）。
**第三个：** Numba 卡片曾写"退回 object 模式"，0.59 起 `@jit` 不再回退，只有 `forceobj=True`；已纠正，`c43532cb`（2026-09-21），`vault/domains/python/BUILD.md` 台账。

### 追问与答题要点

**How did you notice?**
- 用 **`python3 -c` 复算**（orchestrator 的 review 规则：**每个数字复算**，`/CLAUDE.md`），不是"感觉不对"。
- `【待 Chi 补：这一次是你本人复算的，还是 review 步骤里发现的？照实说。】`

**Is that really a hallucination?**
- 定义：模型生成**流畅、自信但没有依据**的内容。
- 这是**算术/数量级错误**，更准确叫 **confident wrong claim**；hallucination 的机制见 `primer.md` §2。
- **主动说出这个区分**，是加分项。

**What did you change so it doesn't recur?**
- 规则进**共享指令文件**（每个被发现的缺陷变成一条规则）。
- review 辅助脚本 `scripts/review_design_problem.py`；**门禁** `scripts/check_design_problems.py`。

**Why not just use a better model?**
- 更强的模型**降低频率**，不提供 **oracle**。
- 检查的成本（**一行脚本**）远低于任何模型升级，而且对**未来的模型**同样有效。

**Did a wrong number reach a learner?**
- 这个错数字在**卡片发布前**被抓到（卡片在 BUILD 流程里，`anki-push` 是**最后一步**）。
- `【待 Chi 补：是否有任何已进入 Anki 复习的卡片后来被纠错？没有就说没有。】`

**What would you do differently?**
- 在 pilot 之前就把"**数字必须脚本复算**"写进指令（现在 AGENT.md 开头就有）。

---

## G2 · 让正确性不依赖 agent 的自述（senior 机制故事）

**主 LP：Insist on the Highest Standards。** 备用：Invent and Simplify（机制简单到一条命令）、Ownership（持续到不再出问题）、Are Right, A Lot（怎么找反证）。

### 口述提纲（60–90 秒）

**Hook：「A green suite isn't proof, so I test the tests.」**

**S · Situation**
- I produced about **100 interview-prep artifacts**: **49 system-design** and **45 low-level-design** problems, via **parallel Claude Code subagents**.
- A model that grades its own work says "**done**" every time.

**T · Task**
- Make correctness **independent of the agent's word**.
- It must **scale** to more agents without me re-reading everything.

**A · Action** (in the order it happened)
1. I rejected **self-reports plus a spot check**.
2. **One agent owns one directory**; **three at a time**.
3. I wrote the **acceptance gate as a command** before any content: reference solution must **pass**, empty starter must **fail**.
4. I also rejected **agents reviewing agents**: one spawned a reviewer and broke my cap, so "**never start another agent**" became a rule.
5. I **re-run the gate myself**, **re-derive every number**, and read the agent's **weakest-claims list**; every defect becomes a **rule**.
6. **Later**, to test the tests, I used **mutation**: on one kata, a **concatenated-key** bug passed all **10 tests**.
7. I added the missing assertion; the suite now kills **11 of 11** hand-written mutants.

**R · Result**
- **45 of 45** LLD problems and about **900 tests** passed.
- **Nine** drafts went back for rework.

**L · Learning / Mechanism**
- Verification has to be a **mechanism, not a mood**.

<details><summary>逐字稿（参考，不背）</summary>

> **Situation.** I produced about a hundred interview-prep artifacts — 49 system-design problems and 45 low-level-design problems — through parallel Claude Code subagents. A model that grades its own work says "done" every time.
>
> **Task.** Make correctness independent of the agent's word, in a way that scales to more agents without me re-reading everything.
>
> **Action.** I rejected trusting self-reports with a spot check. So, first, each agent owns one directory, and I run three at a time. Second, I wrote an acceptance gate that is a command, before any content, where the reference solution must pass and the empty starter must fail, so I know the tests can fail. Third, I rejected agents reviewing agents: one spawned a reviewer and broke my three-agent cap, so "never start another agent" became a rule. Fourth, I re-run the gate myself, re-derive every number, and read the agent's own list of weakest claims; every defect I find becomes a rule in the instruction file. And fifth, later, for the tests themselves, I used mutation: on one kata, a buggy version that concatenated keys passed all ten tests, so I added the missing assertion, and the suite now kills 11 of 11 hand-written mutants.
>
> **Result.** 45 of 45 LLD problems and about 900 tests passed; nine drafts went back for rework.
>
> **Learning.** Verification has to be a mechanism, not a mood.

</details>

### 证据

| 事实 | 证据 |
|---|---|
| 规则本体：sonnet 子代理 ≤3、不得再派代理、一个代理一个目录、交付物可由命令验证、"Never accept a subagent's done"、复算数字、每个缺陷变规则 | `/CLAUDE.md` "Orchestration rules for multi-agent work in this repo"；规则成文于 `1634949e`（2026-09-13）、`58061727`（2026-09-20，复算/读自报弱项/缺陷变规则）、`9743d8b3`（2026-09-20） |
| 验收门 = 命令，参考解绿 + 空 starter 红 | `vault/interviews/companies/amazon/tools/verify_suites.py`（同款在各公司 kit 的 `tools/`）；`scripts/check_design_problems.py`、`scripts/check_lld_problems.py`；"先写门禁再写内容"见 `.claude/skills/building-problem-banks/SKILL.md` step 4（技能成文 `58061727`，2026-09-20；设计题门禁本体 `52474eb1`，2026-09-19） |
| "不得再派代理，连复查自己也不行" | `proposals/lld/PROBLEM_AGENT.md`，提交 `9429f863` |
| 45/45、约 900 个测试、发回重做 9 次；3 处独立复核（国际象棋 perft 深度 4 = 197,281；职业社交双向 BFS 对拍普通 BFS，400 个随机图零不一致；键值存储三层嵌套事务 + TTL 回滚） | `vault/domains/low-level-design/BUILD.md` §7 台账（提交 `f5bddda7`，2026-09-20） |
| 代理反复犯的 9 类错 → 9 条防线 | 同文件 "代理写题时反复犯的错" 表；规则提交 `eb16176f`、`a15a15bd`、`27b9deae`、`4b7d6d66`… |
| 变异测试：包裹追踪 kata，拼 key 的写法 A 一开始通过全部 10 个测试 → 补 case_07 断言 | `vault/interviews/companies/airbnb/study/q01_parcel_tracking.md`（"常见错法对照"）；提交 `b4c507c8`（2026-09-27）；`.../airbnb/problems/q01_parcel_tracking/REPORT.md`："Mutation check (11 hand-written bugs…): 11/11 killed"、"Empty starter.py: 32/38 fail"、200 种子 × 1500 操作差分对拍 |
| 单点自查：`"ab"+"c"` 与 `"a"+"bc"` 拼成同一个 key | 同 study 文件 + `b4c507c8` 提交说明 |

计数复核（我对台账数字做了一致性检查，不是自己手数的）：LLD 45 题、SD 49 题均来自 BUILD.md 台账里脚本验收行（`check_lld_problems.py --all`、`check_design_problems.py --all`）。

### 追问与答题要点

**Why a gate and not just careful reading?**
- 门禁检查**形状**（必需小节、测试能红能绿、卡片数量）；读才检查**实质**。
- "一个建立在合理假设上的错误结论"门禁看不到，skill 明确写了。
- 两者都要：**gate is not the review**。

**Why must the empty starter fail?**
- 否则测试可能**什么都没测**。
- 红灯证明测试有**区分能力**；这是**变异测试的最小形态**。

**What does mutation testing add?**
- **全绿不证明代码对**；故意写错的版本能不能被抓到，才证明**测试对**。
- Airbnb 例子：写法 A 通过了全部 10 个测试，说明测试**漏了撞 key**。

**Who reviews the reviewer?**
- **台账 + 独立复核**：国际象棋 **perft** 的已知值、双向 BFS **对拍**普通 BFS（差分测试）。
- 用**另一条独立路径**得到同一个答案。

**How did it scale/others adopt?**
- 规则在**共享指令文件**里，新代理读同一份；`CHECKPOINT.md` 让新会话**零上下文接手**。
- `【待 Chi 补：有没有别人（队友/同事）采用过这套？没有就别说。】`

**Cost?**
- 技能文件里有**实测**：一个问题单独 **8–10 分钟 / 130–145k tokens**；两题一个代理 **17–29 分钟**。
- 一轮 SendMessage 修订 **5–6 分钟 / +40–60k tokens**；整库约 **6–7M tokens**。
- 我对 3 surveys + 3 pilots + 23 pairs 做了**加总一致性检查**（见 G3）。

**What did you give up?**
- **并行度**（硬上限 3）、**速度**（每个返回都要复核）、对**代理自治的信任**。
- 换来**可审计**。

**Would this work at Amazon scale?**
- 原则可迁移：**门禁 = CI**；agent 自述 = **PR 描述，不是证据**；差分/变异测试 = **对测试的测试**。
- `【待 Chi 补：PayPal 的对应物，如迁移里的 parity 测试，见 R2。】`

---

## G3 · 什么时候 GenAI 不必要，或者更慢

**主 LP：Frugality。** 备用：Dive Deep（用数据而非印象）、Bias for Action。**诚实提示**：repo 证明的是规则和实测成本；"我最初想让 agent 做"这件事的回忆，只有 Chi 能确认。

### 口述提纲（60–90 秒）

**Hook：「Where the answer is deterministic, I write ten lines of code instead of prompting.」**

**S · Situation**
- Same build. My first instinct was to hand **everything** to an agent.
- That included **counting things** and fixing **small review comments**.

**T · Task**
- Find where that actually **cost more than it saved**.

**A · Action** (in the order it happened)
1. First, **counts**: cut lines, coverage percentages, "N problems" in prose had been wrong by hand, **twice**.
2. So **every count comes from a script**; a model **never counts**.
3. Second, **small fixes**: an agent revision round measured **5–6 minutes** and **40–60k extra tokens**.
4. So a one-line fix I **edit in place**; the agent round trip is for **substantive** changes.
5. Third, **parallelism**: one agent per problem wasted context; four agents "just this once" broke the cap.
6. I settled on **two problems per agent**, **three agents** at a time.
7. **Later**, my Amazon-prep **coverage matrix** is generated by a script from **one mapping**, so it cannot drift.

**R · Result**
- Reviewing a finished pair takes **three to six tool calls**, using a **script**, not a model.

**L · Learning / Mechanism**
- Use a model where output is **open-ended and checkable**.
- Where the answer is **deterministic**, write **ten lines of code**.

<details><summary>逐字稿（参考，不背）</summary>

> **Situation.** In the same build, my first instinct was to hand everything to an agent — including counting things and fixing small review comments.
>
> **Task.** Find out where that actually cost more than it saved.
>
> **Action.** Three places. One: counts. Cut lines, coverage percentages, "N problems" in prose — those had been wrong when done by hand, twice, so I made it a rule that every count comes from a script, and a model never counts. Two: small fixes. A revision round through an agent measured about five to six minutes and forty to sixty thousand extra tokens; so for a one-line fix I edit in place and reserve the agent round trip for substantive changes. Three: parallelism. One agent per problem wasted context, four agents "just this once" broke the cap, so I settled on two problems per agent and three agents at a time. Later, the same rule reached my Amazon prep: the story-versus-principle coverage matrix is generated by a small script from one mapping, so it cannot drift.
>
> **Result.** Review of a finished pair takes three to six tool calls, using a script rather than a model.
>
> **Learning.** Use a model where the output is open-ended and checkable. Where the answer is deterministic, write ten lines of code.

</details>

### 证据

| 事实 | 证据 |
|---|---|
| "Counts in prose … come from a script, never from memory — hand counts were wrong twice." | `/CLAUDE.md` Gotchas，提交 `1634949e`（2026-09-13）。注：文件没写 "hand" 是人还是代理——说"手数/凭记忆数的计数错过两次"，不要说成"agent 数错了" |
| Amazon 覆盖矩阵由脚本从 `MATRIX` 字典生成 | `vault/interviews/companies/amazon/lp/coverage.py`；`lp/story_matrix.md` 开头说明；提交 `4a2ecdbd` |
| 一轮 SendMessage 修订 5–6 分钟、+40–60k tokens；小修就地改 | `.claude/skills/building-problem-banks/SKILL.md`（"Measured cost" 表 + step 7 "small fixes: edit in place"） |
| 一题一个代理浪费上下文、三题一个代理耗尽；"四个代理，就这一次" 是常见错误 | 同文件 step 6 与 "Common mistakes" |
| review 一对题 = 3–6 个工具调用，由脚本打印门禁/容量估算/孤儿数据 | 同文件表 "orchestrator review of one pair"；`scripts/review_design_problem.py` |
| 预算 130k tokens/12 分钟每题 | 同文件；我对"3 surveys + 3 pilots + 23 pairs ≈ 6–7M tokens"做了乘法复核：3×115k + 3×138k + 23×260k ≈ 6.8M（取表内区间中值，脚本算，量级一致） |

### 追问与答题要点

**Give me a case where the AI was just wrong for the job.**
- **计数/覆盖率**：确定性问题，模型给出的是"看起来合理的数"。
- **脚本就是 oracle 本身**。

**Did that ever cost you?**
- 有：**错误的手数计数**进了 prose（**两次**，CLAUDE.md）。成本是读者拿到**错的 cut line**。
- `【待 Chi 补：具体是哪两次？没有记忆就别展开。】`

**How do you decide to delegate vs. do it?**
- 三个问题：答案是**确定性**的吗（→ **脚本**）？
- 改动多大（一行 → **就地改**；实质 → 回到**同一个代理**，它还有上下文）？
- 有**可执行的验收**吗（没有 → **先写门禁再委派**）？

**What about at work?**
- `【待 Chi 补：PayPal 里一个"用脚本/SQL 比 agent 好"的真实例子。没有就说 repo 里这个。】`

**Isn't that anti-AI?**
- 不是；是把 AI 放在它的**优势区**：**开放式、可验证**。
- `primer.md` §7 **成本/延迟**取舍。

---

## G4 · 什么时候信任 LLM：一条判定规则

**主 LP：Are Right, A Lot**（判断力 + 找反证）。备用：Ownership、Learn and Be Curious。

### 口述提纲（60–90 秒）

**Hook：「Trust depends on whether an oracle can say the output is wrong.」**

**S · Situation**
- After months of **running agents in parallel**, I needed a rule better than "it **feels right**".

**T · Task**
- Decide **per task** how much to trust the output, and **write it down**.

**A · Action**
1. The rule has two inputs: is there an **oracle** (compiler, test, re-runnable script), and what does a wrong answer **cost**?
2. Oracle plus **low blast radius**: I **trust and verify by machine** — refactors under green tests, scaffolding, examples that must compile.
3. **No oracle**: I **don't trust** numbers, claims about external systems, anything **secondhand**.
4. Example: an agent labelled a figure **officially disclosed**; it came from a **single prep site**.
5. **High cost**, like money code: I **read every diff** myself regardless.
6. The blind spot is a **wrong conclusion on a plausible assumption**: gates check **shape**, only reading checks **substance**.
7. So I read the agent's own "**least sure**" list first.

**R · Result**
- Defects surface at the **gate or in review**, not with the reader.
- Example: a Java example that **would not compile**, caught when I **compiled every textbook example**.

**L · Learning / Mechanism**
- Trust is a property of the **verification around the model**, not of the model.

<details><summary>逐字稿（参考，不背）</summary>

> **Situation.** After months of running agents in parallel, I needed a rule better than "it feels right".
>
> **Task.** Decide per task how much to trust the output, and write it down.
>
> **Action.** My rule has two inputs. First: is there an oracle — a compiler, a test, a script I can re-run — that can say the output is wrong? Second: what does a wrong answer cost? With an oracle and low blast radius, I trust and verify by machine: refactors under green tests, scaffolding, generated examples that must compile. Without an oracle, I don't trust: numbers, claims about external systems, anything secondhand — in one of my banks an agent labelled a figure as officially disclosed when it came from a single prep site. And where the cost is high — money code — I read every diff myself regardless. The blind spot is a wrong conclusion built on a plausible assumption: gates check shape, only reading checks substance. So I read the agent's own "least sure" list first.
>
> **Result.** Defects surface at the gate or in review rather than with the reader — for example, a Java example in my conventions table that would not compile was caught when I compiled every textbook example.
>
> **Learning.** Trust is a property of the verification around the model, not of the model.

</details>

### 证据

| 事实 | 证据 |
|---|---|
| "plan with the agent → TDD every phase → CI + monitoring gates"；"gates and thresholds, not lines of code"；"in money code I read every diff myself" | `vault/interviews/core/stories/S7 Schema pool.md`（AI 工具题完整版）；`lp/stories/S7*.md` |
| 简历：Claude Code 做 code review / 测试生成 / 重构，用全面测试保证 behavioral parity | `vault/interviews/core/resume/resume.tex` 一句；`lp/stories/R2_ai-native-migration.md` |
| "Secondhand as official"（"YouTube officially discloses 500 h/min"）；"Agents' self-reported 'least sure' lists are accurate…What they cannot see is a wrong conclusion built on a plausible assumption" | `.claude/skills/building-problem-banks/SKILL.md` 失败表与其后一段 |
| "The gate checks shape; only reading checks substance." | 同文件 "Common mistakes" |
| 编译失败例子 J04 | `277ff22a`（分支 `headlands-kit`）；见 G1 |
| 爆炸半径的真实例子：测试夹具曾经写进真实 Anki 集合 → `tests/conftest.py` 让真实客户端拒绝；`anki-push` 只重排仍是 new 的卡、从不写已复习卡的 `due` | `/CLAUDE.md` Gotchas；`tests/conftest.py`，引入于 `965dbc89` |
| agent 不得改权限/隔离设置，只能把确切片段交给 Chi | `/CLAUDE.md` Git in a worktree 一条 |

### 信任矩阵（口述用）

| | 错的代价低 | 错的代价高 |
|---|---|---|
| **有 oracle**（测试/编译/脚本/差分） | 信任 + 机器验证：脚手架、重构、样例代码 | 信任 + 机器验证 + **我读 diff**（money code） |
| **无 oracle** | 当草稿用，我改写 | **不信任**：数字、外部系统事实、安全、权限、二手来源；先造 oracle，或自己做 |

### 追问与答题要点

**Tell me about a time you overrode the tool / didn't trust it.**
- **G1（38%）**、**J04（编译失败）**、**Numba（官方行为已变）**。
- `【待 Chi 补：工作中一次你拒绝了 AI 建议的具体决定——R2 senior 升级点 (b)。】`

**How do you stop a teammate from over-trusting?**
- 把规则放进**仓库**而不是口头：**门禁**、**PR 模板**、"AI 写的也要你能解释每一行"。
- `【待 Chi 补：真实带教/code review 里的做法，见 M1。】`

**What's the failure of your rule?**
- **oracle 本身错了**（测试和代码同源盲区）→ **变异测试**、**独立路径对拍**。
- 以及"**合理假设上的错误结论**"门禁看不见。

**Would you let an agent run unsupervised?**
- **不**。agent **提议**、测试**裁决**、人**读 diff**（R2 追问 6）。
- **权限由 Chi 控制**，agent 不能改自己的权限（CLAUDE.md）。

**Security?**
- 公开仓库规则（**不放招聘人员姓名、邮件内容**）、**爆炸半径 guard**、**最小权限**；`primer.md` §6。

---

## 附：把故事映射到 LP 的口袋表

| LP | 用哪个 GenAI 故事 | 开场一句 |
|---|---|---|
| Dive Deep | G1 | "I re-derived the number with a script instead of trusting how confident it sounded." |
| Insist on the Highest Standards | G2 | "A green suite isn't proof, so I test the tests." |
| Frugality | G3 | "Where the answer is deterministic, I write ten lines of code instead of prompting." |
| Are Right, A Lot | G4 | "Trust depends on whether an oracle can say the output is wrong." |
| Earn Trust | G1（对读者负责）| "I fixed the article first, then the card." |
| Ownership | G2/G4 | "I own every diff, whoever or whatever wrote it." |
| Invent and Simplify | G2 | "One command decides whether a task is done." |

## 附：字数脚本

逐字稿（`<details>` 内）英文词数（脚本统计，约 150 词/分钟估算；实际口语 160–170 词/分钟更快）：

| 故事 | 词数 | 150 词/分钟 |
|---|---|---|
| G1 | 216 | ≈ 86 s |
| G2 | 219 | ≈ 88 s |
| G3 | 204 | ≈ 82 s |
| G4 | 210 | ≈ 84 s |

各故事小标题里写的"约 N 词"以此表为准。
