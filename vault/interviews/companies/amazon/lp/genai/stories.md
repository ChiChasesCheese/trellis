# GenAI 故事库：4 个英文 STAR（每个 60–90 秒）

- 口述时主语用 "I set up / I wrote the rule / my review step caught"；被追问时用你自己的真实回忆回答，不编没有的回忆。
- 日常工作（PayPal）的 AI 使用只讲已有的话：简历一句、S7（[[S7_schema-pool]]）、[[R2_ai-native-migration]]；其余 【待补】。

| # | 故事 | 回答的题 | 主 LP | 副 LP |
|---|---|---|---|---|
| G1 | 一个自信的错数字：碰撞概率 38% vs 必然 | a time AI hallucinated | Dive Deep | Highest Standards, Earn Trust |
| G2 | 让正确性不依赖 agent 自述：验收命令 + 复算 + 变异测试（senior 机制故事） | how do you verify | Insist on the Highest Standards | Invent and Simplify, Ownership |
| G3 | 什么时候 AI 不必要或更慢：计数用脚本、委派有成本 | where GenAI was unnecessary | Frugality | Dive Deep, Bias for Action |
| G4 | 信任的判定规则：oracle × 爆炸半径 | when do you trust an LLM | Are Right, A Lot | Ownership, Learn and Be Curious |

## 开场 20 秒（回答 "How do you use GenAI?"）

**Hook：「I use it in two layers.」**

- **Layer 1 · Day to day**
  - I run **Claude Code, Codex and Cursor** in parallel.
  - I **plan** the change with the agent, do **TDD** for each phase, and let **CI and monitoring gates** decide.
  - In **money code** I **read every diff** myself.
- **Layer 2 · On top**
  - I treat it as a **team of agents I lead**: I set the **rules** and an **acceptance gate that's a command**.
  - I **never accept** an agent's own "done".
  - My **study-system repo** is where those rules are written down and measured.
  - 【待补：一句具体的日常例子——最近一次用它做的任务和结果】
- 边界：schema pool 与 on-call copilot 是个人仓库，相邻团队采用，不是团队官方工具链。

## G1 · 一个自信的错数字

- 主 LP：Dive Deep；备用：Insist on the Highest Standards、Earn Trust（对读者负责）。

**Hook：「I re-derived the number with a script instead of trusting how confident it sounded.」**

- **S · Situation**
  - I'm building a **system-design study bank**: about **50 problems**, drafted by **Claude Code subagents**.
  - A learner **memorizes** those numbers, so a wrong one is a **shipped defect**.
- **T · Task**
  - I **own correctness**: the agent drafts, and **I** make sure nothing wrong gets through.
- **A · Action**
  - On the **first pilot problem**, the article stated a hash-collision probability of **38 percent**.
  - I **re-derived** it with a one-line script: the real answer was **certainty**, the exponent off by **six orders of magnitude**.
  - The wrong figure was **already in a flashcard**, so I fixed the **article first, then the card**.
  - I stopped treating it as one bug and wrote a **rule** into the shared agent instructions: every number is **computed, never recalled**.
  - Second rule: a number you **couldn't verify** never goes into a card.
  - **Later**, a second article had correct arithmetic on **two contradicting assumptions** (a **1,560x** peak ratio), so I added: assumptions must **agree with each other**.
- **R · Result**
  - All **49** problems passed the gate; **two** were redone for design substance.
  - **Four lessons** now live in the instruction file.
- **L · Learning / Mechanism**
  - The model's **confidence tells you nothing**; arithmetic is cheap, so **check it by machine**.
- 可选第二个例子（编译器当 verifier）：Java 21 教材示例 `case Order(var id, Side.BUY, var px, var q)` 不能编译（record 模式里不能写常量，要用 `when` 守卫）；「36 个示例全部 javac 通过」这个 gate 抓到了它。
- 可选第三个例子：Numba 卡片曾写「退回 object 模式」，0.59 起 `@jit` 不再回退，只有 `forceobj=True`；已更正。
- 追问：
  - **How did you notice?**
    - 用 `python3 -c` 复算（review 规则：每个数字复算），不是「感觉不对」。
    - 【待补：这一次是你本人复算的，还是 review 步骤里发现的？照实说】
  - **Is that really a hallucination?**
    - 定义：流畅、自信但没有依据的内容。
    - 这是算术 / 数量级错误，更准确叫 **confident wrong claim**；主动说出区分是加分项。
  - **What did you change so it doesn't recur?**
    - 规则进共享指令文件（每个被发现的缺陷变成一条规则）。
    - 一个 review 辅助脚本 + 一个验收脚本。
  - **Why not just use a better model?**
    - 更强的模型降低频率，不提供 oracle。
    - 检查成本（一行脚本）远低于模型升级，且对未来的模型同样有效。
  - **Did a wrong number reach a learner?**
    - 在卡片发布前被抓到（推送到 Anki 是最后一步）。
    - 【待补：是否有已进入 Anki 复习的卡片后来被纠错？没有就说没有】
  - **What would you do differently?**
    - 在 pilot 之前就把「数字必须脚本复算」写进指令。

## G2 · 让正确性不依赖 agent 的自述（senior 机制故事）

- 主 LP：Insist on the Highest Standards；备用：Invent and Simplify（机制简单到一条命令）、Ownership、Are Right, A Lot。

**Hook：「A green suite isn't proof, so I test the tests.」**

- **S · Situation**
  - I produced about **100 interview-prep artifacts**: **49 system-design** and **45 low-level-design** problems, via **parallel Claude Code subagents**.
  - A model that grades its own work says "**done**" every time.
- **T · Task**
  - Make correctness **independent of the agent's word**.
  - It must **scale** to more agents without me re-reading everything.
- **A · Action**
  - I rejected **self-reports plus a spot check**.
  - **One agent owns one directory**; **three at a time**.
  - I wrote the **acceptance gate as a command** before any content: reference solution must **pass**, empty starter must **fail**.
  - I also rejected **agents reviewing agents**: one spawned a reviewer and broke my cap, so "**never start another agent**" became a rule.
  - I **re-run the gate myself**, **re-derive every number**, and read the agent's **weakest-claims list**; every defect becomes a **rule**.
  - **Later**, to test the tests, I used **mutation**: on one kata, a **concatenated-key** bug passed all **10 tests**.
  - I added the missing assertion; the suite now kills **11 of 11** hand-written mutants.
- **R · Result**
  - **45 of 45** LLD problems and about **900 tests** passed.
  - **Nine** drafts went back for rework.
- **L · Learning / Mechanism**
  - Verification has to be a **mechanism, not a mood**.
- 追问：
  - **Why a gate and not just careful reading?**
    - gate 检查形状（必需小节、测试能红能绿、卡片数量）；读才检查实质。
    - 「建立在合理假设上的错误结论」gate 看不到。
    - 两者都要：the gate is not the review。
  - **Why must the empty starter fail?**
    - 否则测试可能什么都没测。
    - 红灯证明测试有区分能力，是变异测试的最小形态。
  - **What does mutation testing add?**
    - 全绿不证明代码对；故意写错的版本能不能被抓到，才证明测试对。
    - 例：拼接 key 的写法通过了全部 10 个测试，说明测试漏了撞 key（`"ab"+"c"` 与 `"a"+"bc"`）。
  - **Who reviews the reviewer?**
    - 另一条独立路径得到同一个答案：国际象棋 perft 深度 4 = 197,281；双向 BFS 对拍普通 BFS，400 个随机图零不一致。
  - **How did it scale / did others adopt?**
    - 规则在共享指令文件里，新 agent 读同一份；检查点文件让新会话零上下文接手。
    - 【待补：有没有别人（队友 / 同事）采用过这套？没有就别说】
  - **Cost?**
    - 一个问题单独 8–10 分钟 / 130–145k tokens；两题一个 agent 17–29 分钟。
    - 一轮修订 5–6 分钟 / +40–60k tokens；整库约 6–7M tokens。
  - **What did you give up?**
    - 并行度（硬上限 3）、速度（每个返回都复核）、对 agent 自治的信任；换来可审计。
  - **Would this work at Amazon scale?**
    - 原则可迁移：gate = CI；agent 自述 = PR 描述，不是证据；差分 / 变异测试 = 对测试的测试。
    - 【待补：PayPal 的对应物，如迁移里的 parity 测试，见 R2】

## G3 · 什么时候 GenAI 不必要，或者更慢

- 主 LP：Frugality；备用：Dive Deep（用数据而非印象）、Bias for Action。
- 诚实提示：「我最初想让 agent 做」这件事的回忆只有你能确认。

**Hook：「Where the answer is deterministic, I write ten lines of code instead of prompting.」**

- **S · Situation**
  - Same build. My first instinct was to hand **everything** to an agent.
  - That included **counting things** and fixing **small review comments**.
- **T · Task**
  - Find where that actually **cost more than it saved**.
- **A · Action**
  - First, **counts**: cut lines, coverage percentages, "N problems" in prose had been wrong by hand, **twice**.
  - So **every count comes from a script**; a model **never counts**.
  - Second, **small fixes**: an agent revision round measured **5–6 minutes** and **40–60k extra tokens**.
  - So a one-line fix I **edit in place**; the agent round trip is for **substantive** changes.
  - Third, **parallelism**: one agent per problem wasted context; four agents "just this once" broke the cap.
  - I settled on **two problems per agent**, **three agents** at a time.
  - **Later**, my Amazon-prep **coverage matrix** is generated by a script from **one mapping**, so it cannot drift.
- **R · Result**
  - Reviewing a finished pair takes **three to six tool calls**, using a **script**, not a model.
- **L · Learning / Mechanism**
  - Use a model where output is **open-ended and checkable**.
  - Where the answer is **deterministic**, write **ten lines of code**.
- 追问：
  - **Give me a case where the AI was just wrong for the job.**
    - 计数 / 覆盖率：确定性问题，模型给出「看起来合理的数」；脚本就是 oracle。
  - **Did that ever cost you?**
    - 有：手工计数错进了正文两次；读者拿到错的 cut line。
    - 说「手数 / 凭记忆数的计数错过两次」，不要说成「agent 数错了」。
    - 【待补：具体是哪两次？没有记忆就别展开】
  - **How do you decide to delegate vs do it?**
    - 答案是确定性的吗？是 → 脚本。
    - 改动多大？一行 → 就地改；实质 → 回到同一个 agent（它还有上下文）。
    - 有可执行的验收吗？没有 → 先写 gate 再委派。
  - **What about at work?**
    - 【待补：PayPal 里一个「脚本 / SQL 比 agent 好」的真实例子；没有就说上面这个】
  - **Isn't that anti-AI?**
    - 不是：把 AI 放在优势区，开放式、可验证；成本 / 延迟取舍见 [[primer]]。

## G4 · 什么时候信任 LLM：一条判定规则

- 主 LP：Are Right, A Lot（判断力 + 找反证）；备用：Ownership、Learn and Be Curious。

**Hook：「Trust depends on whether an oracle can say the output is wrong.」**

- **S · Situation**
  - After months of **running agents in parallel**, I needed a rule better than "it **feels right**".
- **T · Task**
  - Decide **per task** how much to trust the output, and **write it down**.
- **A · Action**
  - The rule has two inputs: is there an **oracle** (compiler, test, re-runnable script), and what does a wrong answer **cost**?
  - Oracle plus **low blast radius**: I **trust and verify by machine** — refactors under green tests, scaffolding, examples that must compile.
  - **No oracle**: I **don't trust** numbers, claims about external systems, anything **secondhand**.
  - Example: an agent labelled a figure **officially disclosed**; it came from a **single prep site**.
  - **High cost**, like money code: I **read every diff** myself regardless.
  - The blind spot is a **wrong conclusion on a plausible assumption**: gates check **shape**, only reading checks **substance**.
  - So I read the agent's own "**least sure**" list first.
- **R · Result**
  - Defects surface at the **gate or in review**, not with the reader.
  - Example: a Java example that **would not compile**, caught when I **compiled every textbook example**.
- **L · Learning / Mechanism**
  - Trust is a property of the **verification around the model**, not of the model.
- 信任矩阵（口述用）：
  - 有 oracle + 错的代价低 → 信任 + 机器验证：脚手架、重构、样例代码。
  - 有 oracle + 错的代价高 → 信任 + 机器验证 + 我读 diff（money code）。
  - 无 oracle + 代价低 → 当草稿用，我改写。
  - 无 oracle + 代价高 → 不信任：数字、外部系统事实、安全、权限、二手来源；先造 oracle，或自己做。
- 追问：
  - **Tell me about a time you overrode the tool / didn't trust it.**
    - G1（38%）、编译失败的 Java 例子、Numba（行为已变）。
    - 【待补：工作中一次你拒绝了 AI 建议的具体决定，见 R2】
  - **How do you stop a teammate from over-trusting?**
    - 规则放进仓库而不是口头：gate、PR 模板、「AI 写的也要你能解释每一行」。
    - 【待补：真实带教或 code review 里的做法，见 M1】
  - **What's the failure of your rule?**
    - oracle 本身错（测试和代码同源盲区）→ 变异测试、独立路径对拍。
    - 以及「合理假设上的错误结论」gate 看不见。
  - **Would you let an agent run unsupervised?**
    - 不：agent 提议、测试裁决、人读 diff。
    - 权限由我控制，agent 不能改自己的权限。
  - **Security?**
    - 公开仓库规则（不放招聘人员姓名、邮件内容）、爆炸半径 guard、最小权限；见 [[primer]] 安全一节。

## LP 口袋表

| LP | 用哪个故事 | 开场一句 |
|---|---|---|
| Dive Deep | G1 | "I re-derived the number with a script instead of trusting how confident it sounded." |
| Insist on the Highest Standards | G2 | "A green suite isn't proof, so I test the tests." |
| Frugality | G3 | "Where the answer is deterministic, I write ten lines of code instead of prompting." |
| Are Right, A Lot | G4 | "Trust depends on whether an oracle can say the output is wrong." |
| Earn Trust | G1（对读者负责） | "I fixed the article first, then the card." |
| Ownership | G2 / G4 | "I own every diff, whoever or whatever wrote it." |
| Invent and Simplify | G2 | "One command decides whether a task is done." |
