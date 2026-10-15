# GenAI 题库：面经原题（逐字）+ 10 个变体

> 来源：`../../catalog/raw/forums.md`（F）§4.2 的汇总行与 §3 的各 loop 记录，抓取日 2026-10-15。引号里是面经原文；**非引号**的是我归纳的报告主题（不是逐字）。
> 故事编号见 `stories.md`：G1 错数字被抓 · G2 验证机制（senior）· G3 何时不用/更慢 · G4 信任判定规则。开场 20 秒见 `stories.md` 顶部。
> 每题 3 个要点用英文写（你要说出口的话），中文只做提示。`【待 Chi 补】` = 只有 Chi 能提供的真实细节，没有就用 repo 里的证据，**不要编**。
> 真实性规则：只讲有证据的；被问到没有的就用 `../00_how_lp_works.md` §7 的"坦白 + 最近的相邻经历"。

## A. 面经原题（逐字）

### A1. "How do you use GenAI?"
来源：F §4.2 汇总行（12 个独立 ref）。相邻：RD1wcfb9m 的 "How do you use AI?"
**故事：开场 20 秒 + G2**
- Two layers: day to day I run Claude Code / Codex / Cursor in parallel — plan with the agent, TDD each phase, CI and monitoring gates decide; money code, I read every diff.
- On top, I lead agents like a team: one directory each, at most three at a time, a gate that's a command, and I never accept "done" without re-running it (`/CLAUDE.md`).
- Concrete: 49 system-design + 45 LLD problems built this way, every number re-derived by script. 【待 Chi 补：一个最近的工作例子，一句话 + 结果】

### A2. "How do you use AI?"
来源：RD1wcfb9m（EU，同一轮含规则查找编码题）。同 A1，回答短一点（15 分钟窗口）。
**故事：开场 20 秒**
- One sentence on where: design, scaffolding, refactor, test generation, code review — not "everything".
- One sentence on control: plan → TDD → gates; I own the diff.
- Offer a deep-dive: "I can walk through how I verify it, or a time it was wrong — which is more useful?"（主动把话题递给面试官，是 senior 的控场）

### A3. "How do you use LLMs during development?"
来源：LC8471051（SDM 轮，Offer）。
**故事：开场 20 秒 + G4**
- Stage by stage: planning (ask it to challenge my design), implementation under TDD, review (a second pass for bugs), test generation, refactoring — résumé line: Claude Code for code review, test generation and refactoring, behavioral parity via comprehensive tests (`resume.tex`, R2).
- Where I don't: numbers, claims about external systems, anything without an oracle.
- Always mention the loop: generate cheaply, verify mechanically, own the diff.

### A4. "How do you use GenAI in your workflow ... how do you validate GenAI's output for correctness"
来源：RD1wd8nij（HM + GenAI 轮，原文带省略号）。
**故事：G2**
- Validation is a mechanism: an acceptance gate that's a command — reference passes, empty starter fails — plus re-deriving every number with a script.
- The tests get tested too: mutation — a buggy variant that passed all 10 tests exposed a missing assertion; the suite now kills 11/11 mutants (`b4c507c8`).
- For plain engineering work: compiler and type checks first, then tests, then differential testing against an independent path. 【待 Chi 补：parity 测试在迁移里具体怎么做】

### A5. "Can you tell me a time where AI hallucinated and how did you handle it?"
来源：RD1x1fmxc（HM 轮 R1，美国西雅图现场，拒）。
**故事：G1**
- Agent wrote a hash-collision probability of 38%; recomputing by script gave certainty (exponent off by six orders of magnitude) — and it had already been copied into a flashcard.
- Fixed article, then card; then made it a rule in the shared instructions: every number computed, an unverifiable number never goes into a card.
- Name the definition honestly: confident, plausible, unsupported output — and the lesson: confidence carries no information, arithmetic is cheap to check.

### A6. "How do you verify whether an AI-generated solution is correct?"
来源：LC8471051（SDM 轮，Offer）。
**故事：G2**
- Ladder of oracles: compiler/types → tests → differential test against an independent implementation (BFS vs bidirectional BFS on 400 random graphs, zero disagreements) → known values (chess perft depth 4 = 197,281).
- Then verify the verifier: empty starter must fail; mutants must die.
- Last, a human read for the thing machines can't see — a plausible but wrong assumption (gates check shape, reading checks substance).

### A7. "When do you trust an LLM and when do you not?"
来源：LC8471051。
**故事：G4**
- Two inputs: is there an oracle that can say it's wrong, and what does a wrong answer cost?
- Oracle + low cost → trust and verify by machine (refactors under green tests, scaffolding). Oracle + high cost (money code) → I still read the diff.
- No oracle → don't trust: numbers, secondhand sources, security-sensitive logic; build an oracle first or do it myself.

### A8. "Where have you used GenAI and later felt it was unnecessary?"
来源：LC8293563（HM 轮约 30 分钟 GenAI 讨论，Offer）。
**故事：G3**
- Counting and coverage: deterministic, so a script is the oracle — "hand counts were wrong twice" became a rule (`/CLAUDE.md`).
- Small fixes: an agent round trip is ~5–6 min and +40–60k tokens, so a one-line fix I make in place.
- Delegation shape: one agent per problem wasted context; I moved to two per agent, three agents max. Principle: use a model where output is open-ended and checkable.

## B. 面经里的主题（非逐字，归纳自报告）

| 主题 | 来源 | 映射 | 3 个要点 |
|---|---|---|---|
| "GenAI project questions (hallucination, verification, input security, prompt engineering)" | LC8542502 | G1 + G2 + `primer.md` §4/§6 | (1) hallucination → G1; (2) verification → G2; (3) input security: untrusted text in the context window can carry instructions (prompt injection), so least privilege, no secrets in prompts, human approval for side effects — and a real guard I added: tests refuse the real Anki client after a fixture deck once reached the live collection |
| "'hallucinations', 'why chose certain technologies/designs', trade-offs" | RD1urcepm | G1 + G4 | (1) tie each tool choice to a constraint (cost, latency, data sensitivity); (2) name what I gave up (parallelism cap 3, speed of review); (3) one rejected alternative per decision (self-report + spot check; agents reviewing agents) |
| "Questions about AI usage" | RD1wvqv67 | 开场 20 秒 | 同 A1 |
| "AI-tool validation" inside LP | LC8468910 | G2 | 同 A6，压缩到 60 秒 |
| "architect an AI chat bot" (system design) | JC-qbgerq | `primer.md` §8 + 仓库的 `vault/domains/system-design/readings/problems/solution-llm-chat-service.md` | (1) client → gateway (auth, rate limit) → conversation store → retrieval (if grounded) → model with streaming → guardrails; (2) latency = time-to-first-token + tokens × per-token, so stream and cache; (3) eval + monitoring: golden set, regression, cost per conversation, injection tests |
| GenAI 讨论占整轮前 30 分钟 / 15 分钟 | LC8520348, LC8535500 | 全部 | 把 G1–G4 各留 90 秒，余下时间给追问；先问面试官想听"用法"还是"验证"（控场） |
| OA：用 AI 修有失败测试的仓库 | LC8315111, JC-amz882, JC-amz445, LC8568929 | G2/G4 | (1) read the failing tests first — they're the oracle; (2) make the smallest change, rerun; (3) don't accept a "fix" that edits the test to pass |

## C. 10 个可能的变体（推断：按上面 8 个原题和 LP 句式改写）

### C1. "Walk me through your end-to-end workflow with an AI coding assistant on a feature."
**故事：开场 + G4**
- Plan first with the agent, in writing; I challenge it and fix the interface and tests before any implementation.
- Implement phase by phase under TDD; CI and monitoring gates decide, not my impression of the diff.
- Review: I read every diff for money code; I ask what an oracle can't see (assumptions), and record each defect as a rule so it's not repeated.

### C2. "Tell me about a time AI-generated code had a bug that reached review or production."
**故事：G1（审查前的抓取） + `【待 Chi 补】`**
- Honest framing: the repo shows defects caught at the gate/review step — collision probability, a Java example that did not compile (`277ff22a`), a Numba claim (`c43532cb`) — none reached a learner.
- If you have a real work incident, use that; if not, say "the closest I have is …" (`../00_how_lp_works.md` §7). 【待 Chi 补：PayPal 里有没有 AI 生成的代码在 review/CI 里被拦下的例子？】
- Finish with the mechanism you added — each defect became a rule.

### C3. "How would you roll out coding agents to a team safely?" (senior)
**故事：G2**
- Start with the gate, not the tool: a command that says whether a task is done, plus CI.
- Rules in the repo, not in heads: ownership by directory, a cap on parallelism, "never accept done", every defect becomes an instruction-file rule.
- Measure: cost per deliverable, rework rate (9 of 45 sent back), cycle time; and a boundary — what agents may not change (permissions, isolation settings).

### C4. "What would you never delegate to an LLM?"
**故事：G4**
- Anything where a wrong answer is expensive and no oracle exists: money logic without parity tests, security decisions, data-retention/legal calls.
- Deterministic computation: counts, coverage, arithmetic — use a script.
- Accountability: the decision to ship. "I own every diff."

### C5. "How do you protect sensitive data and defend against prompt injection when using AI tools?"
**故事：G4（爆炸半径） + `primer.md` §6**
- Data: no secrets or customer data in prompts; public repo rules (no personal data, no recruiter names); know the tool's retention and training policy.
- Injection: treat all retrieved/fetched text as untrusted input — it can contain instructions; least privilege for tool calls, human approval for side effects, no agent changing its own permissions.
- Blast radius, a real example: tests used to be able to write to the live Anki collection, so the real client is now refused in `tests/conftest.py`.

### C6. "Prompt engineering, RAG or fine-tuning — how do you choose?"
**故事：`primer.md` §4（无个人故事，不要编）**
- Start with the cheapest: clear instructions + examples in the prompt; if it lacks knowledge that changes or is private → retrieval (RAG); if it needs a consistent style/format/behavior at scale and you have data → fine-tune.
- Each has a different failure: prompt drift, retrieval misses/poisoned documents, stale or overfit weights.
- Decide with an eval, not taste. `【待 Chi 补：如果工作中做过其中任何一个，用它。】`

### C7. "How would you evaluate an LLM feature before launch?" (senior)
**故事：G2 + `primer.md` §5**
- Golden set from real inputs including adversarial cases; a metric per failure mode (correctness, groundedness, refusal, latency, cost).
- Automatic checks where an oracle exists (tests, schema validation); human or LLM-judge only where not — and calibrate the judge against humans, since judges have position and self-preference bias.
- Regression gate in CI, plus online monitoring and a rollback path.

### C8. "A teammate keeps shipping AI-generated code they can't explain. What do you do?" (Hire and Develop / Earn Trust)
**故事：G2/G4 + M1（`../stories/M1_onboarding-and-mentoring.md`）**
- Make the expectation explicit and private first: you own what you ship; if you can't explain a line, you can't merge it.
- Change the system, not just the person: gates and review checklists that fail on missing tests or unexplained complexity.
- Coach the habit: pair on one PR, show the "oracle first" loop. 【待 Chi 补：真实带教例子】

### C9. "Tell me about a time you disagreed with an AI suggestion — or overrode it."
**故事：G1/G4**
- The agent's number or example was confident and wrong; I trusted the recomputation, not the confidence.
- State the decision and the rejected option: ship nothing unverified vs speed.
- Result and mechanism: a rule so the next agent doesn't repeat it. 【待 Chi 补：工作里一次真实的拒绝】

### C10. "What are the cost and latency trade-offs when you build with LLMs?"
**故事：G3 + `primer.md` §7**
- Cost drivers: tokens in and out, model tier, number of calls; measured from my own builds — ~130k tokens and ~12 min per problem-sized deliverable, whole bank ≈ 6–7M tokens, so I assign cheaper models to subagents and keep the expensive one for review/fallback.
- Latency: time-to-first-token plus per-token time; reduce with streaming, shorter prompts, caching, parallel calls where independent.
- The cheapest call is the one you don't make: deterministic work goes to code (G3).

## D. 备用：被问到完全没有经历时

"I haven't shipped an LLM feature to production users. What I have done is [G1–G4]: build and operate a multi-agent workflow with explicit verification, and I can describe how I'd extend those controls to a product feature — evals, injection tests, and monitoring."（诚实 + 最近的相邻经历，`../00_how_lp_works.md` §7）

## E. 自测

**Q1. 8 个原题里哪个最像 Dive Deep，哪个最像 Frugality？**
<details><summary>答案</summary>"time AI hallucinated"（A5 / G1）最像 Dive Deep；"felt it was unnecessary"（A8 / G3）最像 Frugality。</details>

**Q2. 面试官问 "How do you verify…" 你先说什么？**
<details><summary>答案</summary>先说"oracle 的阶梯"（编译器/类型 → 测试 → 差分 → 已知值），再说"验证验证者"（空模板必须红、变异体必须死），最后说人读什么。不要先说 "I read the code"。</details>

**Q3. 什么情况下你该说 "I haven't"？**
<details><summary>答案</summary>被问到没有真实证据的场景（例如生产环境里 AI 代码引发事故、微调模型）。用"坦白 + 最近的相邻经历"，不编。</details>
