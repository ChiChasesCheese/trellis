# GenAI 题库：原题 + 主题 + 变体

- 故事：G1 错数字被抓 · G2 验证机制（senior）· G3 何时不用 / 更慢 · G4 信任判定规则；全文见 [[stories]]，开场 20 秒也在那里。
- 要点用英文写（你要说出口的话），中文只做提示。
- 【待补】= 只有你能提供的真实细节；没有就用已有证据，不编。
- 被问到没有的经历：用「坦白 + 最近的相邻经历」，见文末。

## A. 原题

### A1. "How do you use GenAI?"
- 框架：**开场 20 秒 + G2**
  - Two layers: day to day I run Claude Code / Codex / Cursor in parallel — plan with the agent, TDD each phase, CI and monitoring gates decide; in money code I read every diff.
  - On top, I lead agents like a team: one directory each, at most three at a time, an acceptance gate that's a command, and I never accept "done" without re-running it.
  - Concrete: 49 system-design and 45 low-level-design problems built this way, every number re-derived by script. 【待补：一个最近的工作例子，一句话 + 结果】
- 追问：
  - What's a recent concrete task? → 【待补】
  - How do you keep agents from colliding? → 一个 agent 一个目录，最多三个并行，不得再派 agent。
  - Does your team use it? → schema pool 与 on-call copilot 是个人仓库，相邻团队采用，不是团队官方工具链。

### A2. "How do you use AI?"
- 框架：**开场 20 秒**（15 分钟窗口，答短）
  - One sentence on where: design, scaffolding, refactor, test generation, code review — not "everything".
  - One sentence on control: plan → TDD → gates; I own the diff.
  - Offer a deep-dive: "I can walk through how I verify it, or a time it was wrong — which is more useful?"（把话题递给面试官，是 senior 的控场）
- 追问：
  - Which tools? → Claude Code、Codex、Cursor，各有 usage 上限。
  - What don't you use it for? → 数字、外部系统事实、没有 oracle 的东西。
  - Show me a time it failed? → G1。

### A3. "How do you use LLMs during development?"
- 框架：**开场 20 秒 + G4**
  - Stage by stage: planning (ask it to challenge my design), implementation under TDD, review (a second pass for bugs), test generation, refactoring. Résumé line: Claude Code for code review, test generation and refactoring, behavioral parity through comprehensive tests (R2).
  - Where I don't: numbers, claims about external systems, anything without an oracle.
  - Always mention the loop: generate cheaply, verify mechanically, own the diff.
- 追问：
  - How does parity testing work in the migration? → 【待补】
  - What does the review pass catch? → 【待补：一个具体例子】
  - How do you decide how much to trust it? → G4：oracle × 代价。

### A4. "How do you use GenAI in your workflow ... how do you validate GenAI's output for correctness?"
- 框架：**G2**
  - Validation is a mechanism: an acceptance gate that's a command — reference solution passes, empty starter fails — plus re-deriving every number with a script.
  - The tests get tested too: mutation — a buggy variant that passed all 10 tests exposed a missing assertion; the suite now kills 11/11 mutants.
  - For plain engineering work: compiler and type checks first, then tests, then differential testing against an independent path. 【待补：parity 测试在迁移里具体怎么做】
- 追问：
  - Why must the empty starter fail? → 否则测试可能什么都没测；红灯证明测试有区分能力。
  - What does mutation add? → 全绿不证明代码对；故意写错的版本被抓到才证明测试对。
  - Who reviews the reviewer? → 另一条独立路径得到同一答案：国际象棋 perft、双向 BFS 对拍普通 BFS。

### A5. "Can you tell me a time where AI hallucinated and how did you handle it?"
- 框架：**G1**
  - Agent wrote a hash-collision probability of 38%; recomputing by script gave certainty (exponent off by six orders of magnitude) — and it had already been copied into a flashcard.
  - Fixed the article, then the card; then made it a rule in the shared instructions: every number computed, an unverifiable number never goes into a card.
  - Name the definition honestly: confident, plausible, unsupported output. Lesson: confidence carries no information, arithmetic is cheap to check.
- 追问：
  - How did you notice? → `python3 -c` 复算；【待补：是你本人复算，还是 review 步骤发现的？照实说】
  - Is that really a hallucination? → 更准确是 confident wrong claim（数量级错）；主动说出区分是加分项。
  - Why not a better model? → 更强的模型降低频率，不提供 oracle；一行脚本的成本远低于模型升级，对未来的模型同样有效。
  - Did a wrong number reach a learner? → 在卡片发布前被抓到；【待补：是否有已进入 Anki 复习的卡片后来被纠错】

### A6. "How do you verify whether an AI-generated solution is correct?"
- 框架：**G2**
  - Ladder of oracles: compiler/types → tests → differential test against an independent implementation (BFS vs bidirectional BFS on 400 random graphs, zero disagreements) → known values (chess perft depth 4 = 197,281).
  - Then verify the verifier: empty starter must fail; mutants must die.
  - Last, a human read for what machines can't see — a plausible but wrong assumption (gates check shape, reading checks substance).
- 追问：
  - Why a gate and not careful reading? → gate 查形状，读才查实质；两者都要。
  - Where does differential testing fail? → 两个实现共享同一个误解；改用独立来源或已知值。
  - What did you give up? → 并行度（上限 3）、速度（每个返回都复核）、对 agent 自治的信任；换来可审计。

### A7. "When do you trust an LLM and when do you not?"
- 框架：**G4**
  - Two inputs: is there an oracle that can say it's wrong, and what does a wrong answer cost?
  - Oracle + low cost → trust and verify by machine (refactors under green tests, scaffolding). Oracle + high cost (money code) → I still read the diff.
  - No oracle → don't trust: numbers, secondhand sources, security-sensitive logic; build an oracle first or do it myself.
- 追问：
  - Give me an example of not trusting it. → 一个 agent 把某数字标成官方披露，实际来自单个备考网站。
  - What's the failure of your rule? → oracle 本身错（测试和代码同源）→ 变异测试、独立路径对拍；以及合理假设上的错误结论。
  - Would you let an agent run unsupervised? → 不：agent 提议，测试裁决，人读 diff；权限由我控制，agent 不能改自己的权限。

### A8. "Where have you used GenAI and later felt it was unnecessary?"
- 框架：**G3**
  - Counting and coverage: deterministic, so a script is the oracle — hand counts were wrong twice, and became a rule.
  - Small fixes: an agent round trip is ~5–6 min and +40–60k tokens, so a one-line fix I make in place.
  - Delegation shape: one agent per problem wasted context; I moved to two per agent, three agents max. Principle: use a model where output is open-ended and checkable.
- 追问：
  - Did it ever cost you? → 手工计数错进了正文两次，读者会拿到错的 cut line；【待补：具体是哪两次】
  - How do you decide delegate vs do it? → 答案确定性吗（→ 脚本）？改动多大（一行 → 就地改）？有可执行验收吗（没有 → 先写验收再委派）？
  - Isn't that anti-AI? → 不是：把 AI 放在开放式且可验证的优势区。
  - At work? → 【待补：PayPal 里「脚本 / SQL 比 agent 好」的真实例子】

## B. 常见主题

### B1. 项目里的 GenAI：hallucination、验证、输入安全、prompt engineering
- 框架：**G1 + G2 + [[primer]]**
  - Hallucination → G1; verification → G2.
  - Input security: untrusted text in the context window can carry instructions (prompt injection), so least privilege, no secrets in prompts, human approval for side effects.
  - A real guard I added: tests refuse the real Anki client, after a fixture deck once reached the live collection.
- 追问：
  - What would you add for production? → evals、注入测试、监控。
  - Prompt engineering vs context engineering? → 措辞 vs 窗口里放什么；agent 场景下后者更重要。
  - Where does your data go? → 【待补：工作中的做法，只说你确知的】

### B2. "Why did you choose certain technologies / designs? Trade-offs?"
- 框架：**G1 + G4**
  - Tie each tool choice to a constraint (cost, latency, data sensitivity).
  - Name what I gave up (parallelism cap 3, speed of review).
  - One rejected alternative per decision (self-report + spot check; agents reviewing agents).
- 追问：
  - Why not agents reviewing agents? → 一个 agent 派了 reviewer，破了并行上限，于是「不得再派 agent」成了规则。
  - Why cap at three? → 瓶颈是我的验收，不是生成。
  - What did it cost? → 一个问题 8–10 分钟 / 130–145k tokens。

### B3. 在线测评：用 AI 修有失败测试的仓库
- 框架：**G2 / G4**
  - Read the failing tests first — they're the oracle.
  - Make the smallest change, rerun.
  - Don't accept a "fix" that edits the test to pass.
- 追问：
  - What if the test is wrong? → 从一手需求写断言，人读。
  - What if the AI's fix passes but you don't understand it? → 不合并：能解释每一行才能提交。

### B4. 一场 GenAI 讨论占整轮前 30 分钟或 15 分钟
- 框架：**全部**
  - 把 G1–G4 各留 90 秒，余下时间给追问。
  - 先问面试官想听「用法」还是「验证」（控场）。
- 追问：
  - 见各故事。

### B5. "Architect an AI chat bot"（设计题）
- 框架：**[[primer]] 末节 + 题库里的 LLM 聊天服务题解**
  - Client → gateway (auth, rate limit) → conversation store → retrieval (if grounded) → model with streaming → guardrails.
  - Latency = time-to-first-token + tokens × per-token, so stream and cache.
  - Eval + monitoring: golden set, regression, cost per conversation, injection tests.
- 追问：
  - Why stream? → 首 token 之后用户就能读，感知延迟大降。
  - Internal documents? → 加检索：权限过滤 + 引用来源 + 注入防护。
  - GPU scarce? → 准入控制和分档配额。

## C. 变体

### C1. "Walk me through your end-to-end workflow with an AI coding assistant on a feature."
- 框架：**开场 + G4**
  - Plan first with the agent, in writing; I challenge it and fix the interface and tests before any implementation.
  - Implement phase by phase under TDD; CI and monitoring gates decide, not my impression of the diff.
  - Review: I read every diff for money code; I ask what an oracle can't see (assumptions); each defect becomes a rule.
- 追问：
  - What if the plan is wrong? → 实现前就改接口和测试。
  - What do you check in the diff? → 假设，不是语法。
  - How long does a phase take? → 【待补】

### C2. "Tell me about a time AI-generated code had a bug that reached review or production."
- 框架：**G1（在审查前被拦下）+ 【待补】**
  - Honest framing: the defects were caught at the gate or review step — collision probability, a Java example that did not compile, a Numba claim — none reached a learner.
  - 【待补：PayPal 里有没有 AI 生成的代码在 review / CI 里被拦下的例子】
  - Finish with the mechanism: each defect became a rule.
- 追问：
  - Did anything reach production? → 如实：没有；最近的相邻经历是 G1。
  - What did the Java example teach? → record 模式里不能写常量，要用 `when` 守卫；编译所有教材示例的 gate 抓到了它。
  - What about Numba? → 0.59 起 `@jit` 不再回退 object 模式，只有 `forceobj=True`；对照文档更正。

### C3. "How would you roll out coding agents to a team safely?"（senior）
- 框架：**G2**
  - Start with the gate, not the tool: a command that says whether a task is done, plus CI.
  - Rules in the repo, not in heads: ownership by directory, a cap on parallelism, "never accept done", every defect becomes an instruction-file rule.
  - Measure: cost per deliverable, rework rate (9 of 45 sent back), cycle time; and a boundary — what agents may not change (permissions, isolation settings).
- 追问：
  - What would you measure first? → 返工率和每个交付物的成本。
  - Who owns the rules? → 共享指令文件，新 agent 读同一份。
  - Has anyone else adopted it? → 【待补：有人采用过就说，没有就别说】

### C4. "What would you never delegate to an LLM?"
- 框架：**G4**
  - Anything where a wrong answer is expensive and no oracle exists: money logic without parity tests, security decisions, data-retention and legal calls.
  - Deterministic computation: counts, coverage, arithmetic — use a script.
  - Accountability: the decision to ship. "I own every diff."
- 追问：
  - Why not let it count? → 手工计数错过两次，成了规则。
  - And with an oracle? → 可以交给它，但高代价时我仍读 diff。
  - Who is accountable? → 我，无论谁写的。

### C5. "How do you protect sensitive data and defend against prompt injection when using AI tools?"
- 框架：**G4（爆炸半径）+ [[primer]]**
  - Data: no secrets or customer data in prompts; public-repo rules (no personal data, no recruiter names); know the tool's retention and training policy.
  - Injection: treat all retrieved or fetched text as untrusted input — it can contain instructions; least privilege for tool calls, human approval for side effects, no agent changing its own permissions.
  - Blast radius, a real example: tests used to be able to write to the live Anki collection, so the real client is now refused in the test config.
- 追问：
  - Why not just tell the model not to? → 边界必须在 harness（沙箱、白名单、审批），prompt 里的禁止只是建议。
  - What is the three-factor risk? → 私有数据 + 不可信内容 + 对外通信，三者齐备就可能被诱导外发；打断其中一条。
  - At work? → 【待补：公司数据怎么处理】

### C6. "Prompt engineering, RAG or fine-tuning — how do you choose?"
- 框架：**[[primer]] prompt / RAG / fine-tune 一节（无个人故事，不要编）**
  - Start with the cheapest: clear instructions + examples; if it lacks knowledge that changes or is private → retrieval; if it needs consistent style, format or behavior at scale and you have data → fine-tune.
  - Each has a different failure: prompt drift, retrieval misses or poisoned documents, stale or overfit weights.
  - Decide with an eval, not taste. 【待补：如果工作中做过其中任何一个，用它】
- 追问：
  - Knowledge base updated daily? → RAG，更新索引即可；仍需评测检索质量。
  - Does RAG remove hallucination? → 不：检索未命中、文档被投毒、模型忽略检索内容时仍会错。
  - How do you decide to upgrade? → 用 eval。

### C7. "How would you evaluate an LLM feature before launch?"（senior）
- 框架：**G2 + [[primer]] 评测一节**
  - Golden set from real inputs including adversarial cases; a metric per failure mode (correctness, groundedness, refusal, latency, cost).
  - Automatic checks where an oracle exists; human or LLM-judge only where not — calibrate the judge against humans (position and self-preference bias).
  - Regression gate in CI, plus online monitoring and a rollback path.
- 追问：
  - Is 82% vs 78% on 50 samples a win? → 不能说：标准误约 5.5–6 个点，要更多样本或配对比较。
  - Judge bias? → 位置偏好、自我偏好、偏长；随机换位并用标注样本校准。
  - Offline vs online? → 离线防回归，在线看漂移、成本、延迟。

### C8. "A teammate keeps shipping AI-generated code they can't explain. What do you do?"（Hire and Develop / Earn Trust）
- 框架：**G2 / G4 + M1**
  - Make the expectation explicit and private first: you own what you ship; if you can't explain a line, you can't merge it.
  - Change the system, not just the person: gates and review checklists that fail on missing tests or unexplained complexity.
  - Coach the habit: pair on one PR, show the "oracle first" loop. 【待补：真实带教例子】
- 追问：
  - What if it continues? → 【待补】
  - How do you give the feedback? → 私下、具体、对事不对人。
  - What do you put in the repo? → 门槛：缺测试或无法解释的复杂度，检查失败。

### C9. "Tell me about a time you disagreed with an AI suggestion — or overrode it."
- 框架：**G1 / G4**
  - The agent's number or example was confident and wrong; I trusted the recomputation, not the confidence.
  - State the decision and the rejected option: ship nothing unverified vs speed.
  - Result and mechanism: a rule so the next agent doesn't repeat it. 【待补：工作里一次真实的拒绝】
- 追问：
  - What was the rejected option? → 速度：不验证就上。
  - What was the rule? → 数字必须脚本算；未核实数字不进卡片；假设必须互相一致。
  - At work? → 【待补】

### C10. "What are the cost and latency trade-offs when you build with LLMs?"
- 框架：**G3 + [[primer]] 成本一节**
  - Cost drivers: tokens in and out, model tier, number of calls; from my own builds, ~130k tokens and ~12 min per problem-sized deliverable, whole bank ≈ 6–7M tokens; cheaper models for subagents, the expensive one for review and fallback.
  - Latency: time-to-first-token plus per-token time; reduce with streaming, shorter prompts, caching, parallel calls where independent.
  - The cheapest call is the one you don't make: deterministic work goes to code (G3).
- 追问：
  - Why do agent tasks cost more than steps × per-step? → 每步输入含此前全部历史，输入随步数累积。
  - Caching? → 稳定内容放前面；20k 前缀调 100 次，缓存读取价 0.1 倍时约省 89%（示意）。
  - Parallel vs serial? → 5 个独立 10 秒任务：墙钟 10 s vs 50 s，成本相同；并行增加验收带宽需求。

## D. 完全没有经历时

- "I haven't shipped an LLM feature to production users. What I have done is G1–G4: build and operate a multi-agent workflow with explicit verification, and I can describe how I'd extend those controls to a product feature — evals, injection tests, and monitoring."

## 自测

- 8 个原题里哪个最像 Dive Deep，哪个最像 Frugality？ → "time AI hallucinated"（A5 / G1）像 Dive Deep；"felt it was unnecessary"（A8 / G3）像 Frugality。
- 被问 "How do you verify…" 先说什么？ → 先说 oracle 阶梯（编译器 / 类型 → 测试 → 差分 → 已知值），再说验证验证者（空模板红、变异体死），最后说人读什么；不要先说 "I read the code"。
- 什么时候该说 "I haven't"？ → 被问到没有真实证据的场景（生产里 AI 代码引发事故、微调模型）；用「坦白 + 最近的相邻经历」，不编。

## 延伸阅读

- [[solution-llm-chat-service]]
