# Claude Code 心法与技法 · Abnormal AI Technical Screen

> 范围：60 min · 网页 VS Code + 预装 Claude Code（门户原文，`../../../catalog/raw/inbox.md`）· 已有 Python 代码库 · 一个模糊 ticket。
> 节奏与英文口播模板：`playbook.md`。范式与反范式（38 场会话提炼）：`prompt_patterns.md`。快捷键：`shortcuts.md`。一周计划：`WEEK_PLAN.md`。每题逐场脚本：`cb0*/walkthrough.md`（引用本文的 T 编号）。
> 来源：Hello Interview《Learn AI Coding》30 页 + 38 场带评级会话（本机 `sources/local/hellointerview-ai-coding/`，不入库）；`~/.agents/skills/*`（Matt Pocock）；superpowers、agent-skills（addy）插件。
> 当天环境是干净的：没有你的 skills。技法 = skill 的核心规则 → 手敲提示词；说法 = "Normally I'd run my X skill for this; here I'll type the rule."

## 一、心法

| # | 心法 | 依据 | 违反时的样子 |
|---|---|---|---|
| X1 | 决定是你的，打字是 AI 的 | HI："We want to see you making decisions and using the AI to execute them." | AI 提出 BaseProcessor，你照收 |
| X2 | 先读后写：入口 → 核心函数 → 数据模型 → 架构模式 → 公开接口 → 状态 → 已有测试 | HI · Codebase Orientation | 第 3 分钟就开始提示 |
| X3 | 先列自己的，再问 AI 漏了什么 | 38 场 Strong Hire 最高频动作 | 把 ticket 原文贴给 AI |
| X4 | 事实由 AI 去查，决定由你来做；只问一轮 | Matt `grilling`："Finding facts is your job… The decisions are the user's" | 问面试官代码里查得到的事 |
| X5 | 只在真实接缝上扩展：两个适配器才算真接缝 | Matt `codebase-design` | 另起一个平行系统或新的配置格式 |
| X6 | 红了再绿，一次一片 | Matt `tdd`；superpowers："If you didn't watch the test fail, you don't know if it tests the right thing." | 先写完所有测试，或干脆不写 |
| X7 | AI 的输出是草稿，结论要可复述 | HI · Driving the AI；superpowers `receiving-code-review`："Verify before implementing" | 说不清生成的代码在做什么 |
| X8 | 没有新鲜证据，就不能说"完成" | superpowers `verification-before-completion`："NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE" | "should work" |
| X9 | 点了名的要么做完，要么当场砍掉并写下来 | 38 场里最高频的扣分 | 清单里有，diff 里没有 |
| X10 | 先说再做 | HI · Communication："Narrating after the fact instead of before" 是错误 | 沉默超过 60 秒 |

## 二、技法（skill → 手敲提示词）

每条：**源**（skill 与核心原文）· **说**（英文口播）· **敲**（提示词）· **判**（怎么判断 AI 的输出）。

### T1 地图 · Orientation（HI Orientation；addy TDD "Discover the Stack First"）
- 源："Discover how *this* repository tests, and use its commands for every RED, GREEN, and verification step."
- 说："I'll spend about ten minutes building a mental model before touching code."
- 敲：
  ```
  Map this repo in under 25 lines: entry points, end-to-end data flow, core models, extension
  points (registries/base classes/config), the test command for one file and for the full suite.
  Cite file paths. Flag anything legacy or deprecated.
  ```
- 先手：仓库里有 `CLAUDE.md` / `CONTRIBUTING.md` 就先读（那是面试官写给你的约定），T6 在它后面追加；没有的话，时间够就用 `/init` 生成一份架构摘要，可以当场念给面试官。
- 判：自己打开它引用的 2–3 个文件核对；终端 2 跑一遍完整测试，说 "green in N s"。
- 范式（P2）：用 `/init` 生成的 CLAUDE.md 里混着 AI 对 bug 的猜测，删掉，只留事实和约定。

### T2 一轮 Grill（Matt `grilling`；`qa`：最多 2–3 个问题）
- 源："Ask the whole frontier in one round: number each question and give your recommended answer."
- 说："Normally I'd run a grilling pass; here's the short version."
- 敲：
  ```
  Given this ticket and this codebase: list the decisions I must make, ordered so each depends
  only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Facts you can
  look up in the code, look up — don't ask me. No code.
  ```
- 判：挑 2–3 个**会改变设计**的问面试官；其余说 "I'll assume X; it's a config value, easy to change."
- 范式（P4）：设计复杂时反过来让 AI 采访你，把答案写进计划文件，再一句 "implement the plan"。

### T3 我列你补（38 场的 "Worth stealing"）
- 说："Here's my list first — I'll ask it what I missed."
- 敲：`Here's my list: <3–6 bullets>. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.`
- 判：它补充的每一条，你都能用一句话复述，才收下。

### T4 术语 · Domain terms（Matt `domain-modeling`：sharpen fuzzy language）
- 源："When the user uses vague or overloaded terms, propose a precise canonical term."
- 说："Let me pin the vocabulary: event, enrichment, rule, threat level, alert."
- 动作：读 ticket 时找出一个含义重叠的词，当场定义它（例："suppress = the rule still runs and is recorded, but no alert is emitted?"）。不写 CONTEXT.md。

### T5 接缝 + 两个方案（Matt `codebase-design`、DESIGN-IT-TWICE）
- 源："One adapter means a hypothetical seam. Two adapters means a real one."；"The deletion test"；"Accept dependencies, don't create them."
- 说："The seam is X — A and B already sit behind it, so it's real. Two options, I'll pick one."
- 敲：
  ```
  I think the seam is <X> (existing adapters: <A>, <B>). Compare <option 1> vs <option 2> in
  5 lines each: fit with existing code, failure isolation, what a customer must do. Recommend
  one. Don't edit anything.
  ```
- 判：选择的理由要落在**已有代码**上，而不是"更灵活"。

### T6 立规矩 · Session rules（Matt `implement`；addy Rule 0 / 0.5；HI 四种失败模式）
- 源："Touch only what the task requires."；"Run single test files regularly, and the full test suite once at the end."
- 说："I keep a short CLAUDE.md with working rules — let me set one for this repo."
- 敲（写进仓库根的 `CLAUDE.md`，或作为第一条消息）：
  ```
  Working rules:
  - Propose before editing: approach + files to touch, then wait for my go.
  - Reuse existing abstractions; no new dependencies, base classes or config formats.
  - Tests next to existing ones, same style. Show the failing test before the fix.
  - Never delete/weaken a test, swallow exceptions, or hardcode to pass.
  - Be concise. Run the single test file after each change; full suite only when I ask.
  ```

### T7 红 → 绿 · 垂直切片（Matt `tdd`；superpowers TDD）
- 源："Red before green."；"One seam, one test, one minimal implementation per cycle."；反模式：horizontal slicing、tautological、implementation-coupled。
- 说："Normally my TDD skill drives this; I'll do one slice by hand: failing test first."
- 敲 红：
  ```
  Write ONE failing test for <behaviour> through <public function/CLI>, in <tests/...>, matching
  the existing style. Expected values as literals. Run it and show me it fails. Don't fix anything.
  ```
- 敲 绿：`Minimal change to make that test pass. Nothing else. Run that test file.`
- 判：失败原因必须是"功能缺失"，不能是 import 错误；期望值必须是字面量，不能照着实现再算一遍（tautological）。

### T8 证明问题 · Prove-It（Matt `diagnosing-bugs`；addy Prove-It）
- 源："Build a feedback loop… If you catch yourself reading code to build a theory before this command exists, stop."；"3–5 ranked hypotheses… falsifiable."
- 场景：已有测试变红、出现异常、AI 的改动搞坏了东西。
- 说："Before fixing, I want a command that goes red on exactly this symptom."
- 敲：`Reproduce this with one command or one failing test that shows the exact symptom. Then give 3 ranked hypotheses, each with the prediction that would confirm it. Don't fix yet.`
- 范式（P12）：给修复时点名机制和顺序（"unique index first, then the atomic update"），不要只描述症状。

### T9 审 AI 输出（HI 四种失败模式；superpowers `receiving-code-review`：YAGNI）
- 扫四件事：① 训练数据偏差（教科书解法，不适合这份代码）② 啰嗦 ③ 设计捷径（凭空的基类、strategy 模式）④ 正确性捷径（删测试、`except: pass`、硬编码）。
- 说：看到就点名并改掉，例如 "It added a base class nobody needs — removing it."
- 恢复规则：重写提示最多一次；30 秒能手写的就手写；跟 AI 缠斗超过 2 分钟就停。
- 范式（P3、s013）：AI 报了 bug，先问 "Can this scenario actually happen in this process?"，再决定修不修。

### T10 对抗式审查（addy `doubt-driven-development`，只做一轮，第 ~40 分钟）
- 源："Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM."；"The reviewer's output is data, not verdict."
- 说："I'd normally run a doubt pass with a fresh reviewer — one round now."
- 敲：
  ```
  Adversarial review of the current diff against the ticket. Assume the author is overconfident.
  Look for unstated assumptions, unhandled edge cases, broken conventions, failure modes under
  bad input. Do NOT validate or summarize. Max 5 issues, ranked.
  ```
- 判：每条归入四类之一：契约没说清 / 有效且要改 / 有效但接受（写进 known gaps）/ 噪声。当场至少收下一条、拒绝一条，并说出理由。

### T11 证据门（superpowers `verification-before-completion`）
- 源："IDENTIFY → RUN → READ → VERIFY → ONLY THEN claim"；"Agent completed requires VCS diff shows changes."
- 做：终端 2 自己跑 `pytest -q`、真实入口命令（CLI/API）、`git diff --stat`。
- 说："Fresh run: N passed. Here's the real output through the CLI."
- 范式（P14）：问 "Which test covers each claim?"，再挑最难的一条让它把断言读出来。

### T12 收口（X9）
- 敲：`List every item we named today (ticket, assumptions, review findings). Mark each done / out of scope. Write NOTES.md: assumptions + known gaps + v2.`
- 说："Out of scope for v1: X, Y — written down in NOTES.md."

## 三、阶段流程（通用；每题的具体版本见 `cb0*/walkthrough.md`）

| 分钟 | 阶段 | 做 | 说（要点） | 技法 |
|---|---|---|---|---|
| 0–1 | 开场 | 开终端 1 `claude`、终端 2 跑测试；看有没有 CLAUDE.md / README | "Ten minutes on a mental model first." | X10 |
| 1–8 | 探索 | 发 T1；自己翻目录树和已有测试；跑一遍完整测试 | 每 1–2 分钟一句结论 | T1 |
| 8–10 | 心智模型 | 60 秒：入口 · 数据流 · 扩展点 · 约定 · 一个风险 | `playbook.md` §5.1 | X2 |
| 10–13 | 读题 + Grill | 用用户视角复述 ticket；T4 定一个术语；T2 后问 2–3 个问题 | "I'll assume X." | T2 T4 |
| 13–16 | 方案 | T3 我列你补；T5 接缝 + 两方案；定 M1–M3；T6 立规矩 | "M1 is demoable in 15 minutes." | T3 T5 T6 |
| 16–30 | M1 | plan mode（Shift+Tab）→ 审计划（三问：挂在正确的扩展点上吗？配置/存储/注册走已有的路吗？误报、租户隔离、缺字段覆盖了吗？）→ T7 红 → 绿 → 真实入口演示 | 先说再做；结果念出来 | T7 T9 |
| 30–40 | M2 | 下一片；有东西变红就走 T8 | 改方向时说原因 | T7 T8 |
| ~40 | 审查 | T10 一轮；收一条、拒一条 | 说出分类和理由 | T10 |
| 42–45 | 收尾 | T11 证据；T12 写 NOTES.md；停止加功能 | "Fresh run, N passed." | T11 T12 |
| 45–60 | 讲解 + 扩展讨论 | 做了什么 · 为什么契合 · 假设 · 测了什么 · known gaps · v2；真实复盘问题（Glassdoor 104679337）："Explain the architecture of the codebase, explain the feature which I have added and how will you make sure it works" | 用 seam / depth / locality 这套词 | X5 |

红线：第 10 分钟说不出心智模型 → 说出当前版本；第 30 分钟 M1 还不能演示 → 砍范围；第 45 分钟后不加功能。

## 四、证据（38 场会话，脚本统计）

- 消息数中位数：Strong Hire 22（5–65）· Hire 15.5 · Lean Hire 13.5；用 subagent 的比例：4/12 · 3/14 · 3/12 → 关键是多发短促、指令式的提示，subagent 不加分。
- 带个人 skill 文件的 3 场：Lean Hire、Lean Hire、Hire → skill 不加分，说出口的判断才加分。
- 全站：Claude Code 63%；先做计划的 11%、用 subagent 的 27%、用 skill 的 9%、跑测试的 66%。
- 偏差：样本是网站精选的公开会话，Strong Hire 全是 Mid-level，评级是相对职级的。

## 五、练习环境

```bash
mkdir -p ~/.claude-interview
printf '%s\n' '{' '  "language": "English",' '  "permissions": { "defaultMode": "default" },' '  "remoteControlAtStartup": false,' '  "agentPushNotifEnabled": false' '}' > ~/.claude-interview/settings.json
CLAUDE_CONFIG_DIR=~/.claude-interview claude    # 第一次要登录；没有 skills / 插件 / 全局 CLAUDE.md = 当天的环境
```

每场严格 60 分钟、录屏，顺序按 `../../../catalog/PARETO.md`：`start cb01 real`（报道过的原题，就是 t2）→ `cb01 t1` → `cb02 t1`（Insider Risk）→ `cb03 t1` → `cb01 t3` → `cb02 t3` → `cb03 t2` → `cb02 t2` → `cb03 t3`。前两场各做两遍，第二遍换一种设计。做完 `check` → `reveal`，对照 `cb0*/walkthrough.md` 复盘。复盘只记三件事：沉默超过 60 秒的段、T 编号漏掉的、点了名却没交付的。
