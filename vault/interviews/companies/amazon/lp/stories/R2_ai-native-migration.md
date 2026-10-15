# R2 · AI-native 迁移：Ruby/Kotlin → Snowflake/Java（Claude Code 工作流）

> 来源：**仅简历一句**（PayPal, Feb 2025–Present）+ S7 笔记里的 AI 使用原则。没有独立的 `core/stories/` 笔记 → 细节大多 `【待 Chi 补】`。
> 简历原句：*"Migrated legacy Ruby/Kotlin business logic to Snowflake/Java using an AI-native development workflow (Claude Code for code review, test generation, and refactoring), ensuring behavioral parity through comprehensive testing while accelerating delivery."*
> 主 LP：**Bias for Action · Learn and Be Curious**；副：Deliver Results · Insist on the Highest Standards · Invent and Simplify。

## 1. 可用事实

| 事实 | 来源 |
|---|---|
| 迁移对象：legacy Ruby / Kotlin 业务逻辑 → Snowflake / Java | 简历 |
| 方法：AI-native 工作流（Claude Code 做 code review、测试生成、重构） | 简历 |
| 质量手段：全面测试保证 **behavioral parity** | 简历 |
| AI 代码信任原则：plan with the agent → TDD every phase → CI + monitoring gates；"focus on gates and thresholds, not lines of code"；money code 里我读每个 diff | S7 笔记 |
| 日常并行跑 Claude Code / Codex / Cursor，各有 usage 上限；schema pool 让多个 agent 会话并行跑迁移与集成测试 | S7 笔记 |
| **没有**：迁移规模（多少行/多少服务）、周期、parity 测试的通过率、加速倍数 | 【待 Chi 补】 |

## 2. 60–90 秒（口述提纲）

**"The agent proposes, tests decide: I migrated legacy Ruby and Kotlin logic to Snowflake and Java with Claude Code, and held it to behavioral parity."**

**S · Situation**
- PayPal fee platform, **Feb 2025–present**: legacy **Ruby/Kotlin** business logic.
- Scale of the migration: 【待 Chi 补：迁移的具体对象与规模，例如"X 个规则/Y 个服务/Z 行"】

**T · Task**
- Migrate it to **Snowflake/Java** while ensuring **behavioral parity**.
- Deliver **faster**, using an **AI-native workflow**, not AI as autocomplete.

**A · Action**
1. Used **Claude Code** for **code review, test generation, and refactoring**.
2. Ensured parity with **comprehensive testing**. 【待 Chi 补：parity 测试具体怎么做——先写测试固定旧行为？影子对拍？】
3. My general rule with agents: **plan the phase**, **TDD each phase**, let **CI and monitoring gates** catch regressions.
4. It is money code, so **I read every diff myself**.

**R · Result**
- **Behavioral parity** through comprehensive testing; delivery **accelerated** (resume wording).
- 【待 Chi 补：结果——parity 测试的通过情况、发现了几个旧逻辑里的隐藏行为、交付时间比预期短多少（给出基线）】

**L · Learning / Mechanism**
- **Agent proposes, tests decide, human reads the diff.**
- Trust **gates and thresholds**, not lines of code.

<details><summary>逐字稿（参考，不背）</summary>

> I migrated legacy Ruby and Kotlin business logic into Snowflake and Java, and I did it with an AI-native workflow rather than treating AI as autocomplete. The rule I worked by: the agent proposes, tests decide. 【待 Chi 补：迁移的具体对象与规模，例如"X 个规则/Y 个服务/Z 行"】 I used Claude Code for code review, test generation and refactoring, and I ensured behavioral parity through comprehensive testing. 【待 Chi 补：parity 测试具体怎么做——先写测试固定旧行为？影子对拍？】 My general rule with agents is to plan the phase with them, do TDD for each phase, and let CI and monitoring gates catch regressions. Because this is money code, I read every diff myself. 【待 Chi 补：结果——parity 测试的通过情况、发现了几个旧逻辑里的隐藏行为、交付时间比预期短多少（给出基线）】

</details>

## 3. 2 分钟（口述提纲，等 Chi 补完再成文）

**"The agent proposes, tests decide: I migrated legacy Ruby and Kotlin logic to Snowflake and Java with Claude Code, and held it to behavioral parity."**

**S · Situation**
- Legacy **Ruby/Kotlin** logic, PayPal, **Feb 2025–present**.
- Where it lives and why it had to move: 【待 Chi 补】

**T · Task**
- Move it to **Snowflake/Java** with **no behavioral drift**, and faster.

**A · Action**
1. **Decision**: what the AI may do (**review, test generation, refactoring**) and may not. 【待 Chi 补：是否 parity-test-first，被否决的备选是什么】
2. **Mechanism**: a **parity test set**, **CI gates**, and my rule to **read every diff** on money code.
3. Rule I work by: **plan with the agent, TDD every phase, gates and thresholds over lines of code**.

**R · Result**
- **Speed-up plus zero behavioral deviation**: 【待 Chi 补：基线与度量】

**L · Learning / Mechanism**
- Where the **trust boundary** with AI tools sits: **agent proposes, tests decide**.
- What I'd do differently: 【待 Chi 补】

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Bias for Action** (P) | "AI let me move quickly, with tests deciding." | 综合测试保证行为一致；每阶段 TDD（S7 原则） | 说成"AI 做的" |
| **Learn and Be Curious** (P) | "I had to learn where the agent is trustworthy and where it isn't." | gates/thresholds；money code 逐 diff 读 | 夸大工具 |
| **Deliver Results** (S) | 【待 Chi 补：数字后才能写】 | | |
| **Insist on the Highest Standards** (S) | "Behavioral parity was the bar, not 'looks right'." | parity 测试 | — |

## 5. 追问（≥5）

1. **How did you verify parity?**
   - 【待 Chi 补】（对拍/影子运行/表级 diff？）
2. **What did the AI get wrong?**
   - 【待 Chi 补：一个真实例子；没有就说"没有记录"，别编】
3. **How do you trust AI-generated code?**
   - **Plan → TDD → CI + monitoring gates.**
   - Focus on **gates and thresholds**, not lines of code.
   - **Money code: I read every diff.**
4. **How much faster?**
   - 【待 Chi 补：基线（按什么算）+ 度量方式；没有精确数字就给可数事实】
5. **What did you learn about the legacy logic?**
   - 【待 Chi 补】
6. **Would you let an agent do this unsupervised?**
   - **No**: agent proposes, **tests decide**, human reads the diff.
7. **Team adoption?**
   - S7: **schema pool** lets multiple sessions run in parallel.
   - **On-call copilot** adopted by an adjacent team.

## 6. Senior 升级点（bar = senior）

当前档位：**一句话简历，尚无故事**。senior 级需要：(a) 迁移范围/风险（钱的路径）；(b) 一个你拒绝 AI 建议的决定；(c) 机制：别人也能照着用的 parity-test 流程。
- 【待 Chi 补：这套"AI-native + parity-test"流程有没有被队友复用？（Raising the bar）】
- 【待 Chi 补：迁移中和资深同事/其他团队的分歧点（若有）】
