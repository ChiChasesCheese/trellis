# AI Technical Screen Playbook · 60 min · 浏览器 VS Code + Claude Code · 已有 Python 代码库

> 依据：`../../../catalog/raw/inbox.md`（门户官方原文，[高]）· `../../../catalog/raw/ai_screen_format.md`（视频 / VP of AI 博客 / 同类面试，[中]）· `../../../catalog/raw/process_and_rounds.md`（面经）。
> 练：`python3 loop/ai_screen.py start cb02 t1` → 在打印出的目录里开 VS Code + `claude`，严格 60 分钟 → `check` → `reveal`。
> 一句话：**这一轮不考你会不会写代码，考你像不像一个第一天就能接 ticket 的工程师——AI 是你带的实习生，你是 owner。**
>
> **报道过的真题（LeetCode Discuss #8335187，2026-06-15，编排者已逐字核对）**：代码库 = security-events 管线（collection/ingestion → enrichment（geo-ip、history、+1，**硬编码**）→ 规则 threat level → ranking → alerts → API → DB）；feature ① "allow users to suppress some rules (it can be complex rules like based on geo-ip)" ② "clients want more configurability without touching platform code. Implement a plugin based mechanism"。该候选人 20 分钟只在口头讲 decorator pattern，最后让 Claude 全写，自评 No。**cb01 就是照这个形态造的，先练它。原题原文、中文讲解与参考答案：`cb01_sentinel/REAL_QUESTION.md`；口述版原题练习：`python3 loop/ai_screen.py start cb01 real`。**
> 另一份 SWE II 报道（#8496901，2026-09-02）：先"explain how it worked"，再实现 feature，最后"discuss possible extensions and modifications … mostly discussion-based"——**第 45 分钟后的扩展讨论也是评分段**，每个练习的 `interviewer.md` 追问就是为它准备的。

## 0. 评分 → 可被看见的行为（每一条都要"被看见"，没说出口 = 没发生）

| 官方维度（原文） | 面试官能观察到的行为 | 反面（AI 照抄型候选人） |
|---|---|---|
| **Judgment** — evaluate approaches, scope into milestones, decide what fits | 说出 2 个方案并选一个、给理由（"fits the registry pattern" / "keeps policy in one place"）；把需求切成 M1/M2/M3；指出 AI 产出里不契合的地方并改掉 | 让 AI 直接写；接受第一版；做一个"看起来解决了"的平行系统 |
| **Agency** — decide, state assumptions, test your own work, keep momentum | 问 2–3 个澄清问题后**不等答案也能推进**："I'll assume X; easy to change because it's a config value"；自己跑测试、自己演示；时间到点主动收敛 | 等面试官拍板；遇到不确定就停；从不跑代码 |
| **Fits the system** — notice existing abstractions and patterns | 在写代码**之前**就点名要复用的抽象（"there's a `@register_detector` registry and per-tenant settings; my detector goes there"）；新测试放在约定位置；用已有工具函数 | 新建一个 dict 当配置；自己写 email 归一化；改 deprecated 模块 |
| **Think about the user** | 问"谁用、看到什么、误报代价"；输出里有 reason/解释；默认值保守 | 只关心测试绿 |
| **AI relationship** — supervise, explain, own | 给 AI 的提示词带上下文（文件、约束、"follow the pattern in X"）；能解释 AI 写的每个关键决定；在 right altitude 审 diff | 复制粘贴；说不清生成的代码；被问"为什么这样"答"AI 写的" |
| **Communication** — synthesize, don't narrate | 每 3–5 分钟一句结论："So the flow is ingest → enrich → detect → policy → act; the extension point I need is detectors." | 念文件名；长时间沉默 |

## 1. 逐分钟（写在纸上，贴屏幕边）

| 分钟 | 段 | 目标 | 动作 |
|---|---|---|---|
| 0–1 | 开场 | 环境可用 | 开终端，`claude`；第二个终端留给跑测试/CLI。说："I'll spend about ten minutes building a mental model before touching code." |
| 1–8 | **探索** | 心智模型 | §2 的探索提示词 E1→E4（并行：AI 在读时你自己看 README、目录树、跑一遍测试与 CLI） |
| 8–10 | **说出心智模型** | 被看见 | §5.1 的 60 秒模板：入口 · 数据流 · 扩展点 · 约定 · 一个你注意到的风险 |
| 10–13 | 读 ticket | 澄清 | 复述 ticket 一句（用户视角）；问 2–3 个**会改变设计**的问题（§3）；没有答案就说出默认假设 |
| 13–16 | 方案 + 里程碑 | Judgment | 2 个方案一句话对比 → 选一个；M1（≤ 15 min 可演示）/ M2 / M3；把假设与里程碑写进 `NOTES.md` 或对 Claude 的 plan 里 |
| 16–30 | **M1** | 可用 v1 | Plan mode 让 Claude 出方案（点名要复用的文件）→ 你审 → 实现 → 跑测试 → **通过真实入口演示**（CLI / API） |
| 30–42 | M2 | 迭代 | 模糊点里最重要的一个（安全产品：误报 / 漏报 / 租户隔离 / 幂等）；补测试 |
| 42–45 | 收尾 | 交付 | 全量测试；`git diff --stat`；停止加功能 |
| 45–52 | Walkthrough | 讲清楚 | §5.3 模板：做了什么 · 为什么这样契合 · 假设 · 测了什么 · known gaps · v2 |
| 52–60 | 反问 | | `../../../06-questions-to-ask.md` |

**节奏红线**：第 10 分钟还没说出心智模型 → 立刻说当前版本；第 30 分钟 M1 还不能演示 → 砍范围（去掉 M1 里非核心的部分），先演示；第 45 分钟后不写新功能。

## 2. Claude Code 工作流

### 2.1 开场 30 秒

- 终端 1：`claude`。终端 2：跑 `pytest -q`、CLI。（新终端里接上会话：`claude --resume` 或 `/resume` —— 官方 tip。）
- 先看有没有 `CLAUDE.md` / `README.md` / `CONTRIBUTING.md`：有就让 Claude 先读（Abnormal 自己的 monorepo 有 13 KB 的根 CLAUDE.md，面试库很可能也放了一份——那就是面试官写给你的约定）；没有可以用 `/init` 让它生成（≈1–2 分钟，产物本身就是一份架构摘要，可以当场念给面试官）。时间紧就用 E1 代替 `/init`。

### 2.2 探索提示词（复制即用；边等边自己看目录树）

- **E1 架构地图**："Map this repo for me: entry points (CLI/HTTP), the main data flow end to end, the core domain models, and the extension points (registries, base classes, plugin hooks). Cite file paths. Keep it under 25 lines."
- **E2 约定**："What conventions does this codebase follow — configuration, persistence, error handling, logging, testing layout, naming? Point to one canonical example of each. Flag anything deprecated or legacy I should avoid."
- **E3 跑一遍**（你自己在终端 2）：`pytest -q`；README 里的 CLI 命令跑一次，看真实输出长什么样。说一句"tests are green in N seconds, the CLI produces X"。
- **E4 拿到 ticket 后定位**："Given this ticket: <paste>. Which existing modules and abstractions would a change like this touch? Is there an existing pattern for a similar feature I should copy? Don't write code yet."
- **E4b 让 AI 反问歧义**（Shrivu 本人的工作流，F-9："Flesh out CONCEPT.md, what's ambiguous, ask me questions, what are dimensions I'm not considering"）："Before planning: what is ambiguous in this ticket given this codebase? List the decisions I need to make, with the option you'd pick and why. No code." —— 你从它的清单里挑 2–3 个问面试官，其余自己定。
- **E5（可选）追一条路径**："Trace what happens to one <message/event/request> from <entry> to <output>, function by function."

> 用 AI 做探索本身是加分项（官方："Candidates who only use AI to write code leave signal on the table"）。但**结论要你说出来**，不是把 AI 的输出念一遍。

### 2.3 实现：Plan mode → 审 → 执行

- `Shift+Tab` 切到 **plan mode**（官方点名）："Plan the smallest change that implements M1: <M1 一句话>. Constraints: reuse <X registry / settings / store / util> (look at <file> as the pattern), put tests in <tests/…> following <existing test>, no new dependencies, don't touch <legacy module>. List files to change and the test cases."
- **审 plan（right altitude 的三问）**：① 方法对吗（挂在正确的扩展点上？）② 集成对吗（配置/存储/注册/审计走已有的路？）③ 覆盖了要紧的情况吗（误报样本、租户隔离、空/缺字段）？不对就当场改 plan，并**说出来**："I'm changing this: it added a new JSON config file, but tenants already have settings in `settings.py` — use that."
- 执行后：终端 2 跑测试 + 真实入口演示。**证据优先**（Abnormal 工程博客 "Make Every PR Prove Itself"，F-3："a diff shows you what the agent typed, not whether it works"）：演示时给面试官看真实输出——CLI 结果、API 响应里的新字段、日志行——而不只是"tests pass"。让 Claude 加测试时点名约定："Add tests next to `tests/detectors/test_suspicious_links.py` in the same style: one benign and one malicious fixture."
- **审 diff**：`git diff` 扫一遍形状（改了哪些文件、有没有新建平行结构、有没有改不该改的文件），关键函数读透。可以再让 Claude 自审："Review this diff against the codebase conventions you found earlier. List deviations, not style nits."
- 卡住（AI 来回改不对）超过 3 分钟：`Esc` 打断，自己读那段代码，给更窄的指令；或缩小 M1。

### 2.4 必会快捷键（考前在本地 Claude Code 里各按一次）

`Shift+Tab` 切换模式（含 plan mode）· `/context` 看上下文用量（Shrivu："run /context mid coding session at least once"）· `Esc` 打断当前生成 · `Esc Esc` 回到上一条消息改写 · `@path` 把文件放进上下文 · `!cmd` 直接跑 shell · `/clear` 清上下文（换任务时）· `/compact` 压缩 · `/resume` 接回会话。VS Code：`Ctrl/Cmd+\`` 开终端、`+` 开第二个、`Ctrl/Cmd+Shift+F` 全局搜、左栏 Source Control 看 diff。

## 3. 模糊性：澄清 → 假设 → 推进（被评分的核心）

**问会改变设计的问题，不问能自己决定的问题。** 每张 ticket 问 2–3 个，按这四类挑：

| 类 | 问法（English） | 为什么值钱 |
|---|---|---|
| 用户与代价 | "Who consumes this — the end user, an admin, or an analyst? What's worse here, a false positive or a false negative?" | 安全产品的核心权衡；决定阈值与默认值 |
| 范围 | "Is v1 scoped to <the narrow case> — e.g. only VIPs / only one data source — or everyone?" | 决定 M1 能否 15 分钟做完 |
| 交互 | "Should this override <existing behavior> — e.g. should an allowlist beat a malware verdict?" | 判断力题，常是隐藏期望 |
| 运行面 | "Per-tenant configurable, or a global default for now? Any volume I should design for?" | 契合已有配置/多租户 |

面试官若说"you decide"——这就是考点：**当场决定 + 说理由 + 让它可改**：
> "Then I'll go with X for v1 because <user reason>. I'll put the threshold in the tenant settings so it's a config change, not a code change, and I'll note it as an assumption."

把假设写下来（`NOTES.md` 或 PR 描述式的注释），walkthrough 时逐条念。

### 2.5 一个容易忽略的点：你也可以手写

"You are the engineer; AI is a resource you supervise." 小改动（一个配置键、一行注册、一个测试断言）自己敲比写提示词快，也让面试官看到你真懂。经验法则：**说得清楚的大块交给 AI，改一两行的自己来**；被 AI 来回改错两次，自己接手。

## 4. 地雷（练习代码库里都埋了，真实面试大概率也有）

1. **重造已有抽象**：自己写配置加载、邮箱归一化、时间窗口、分页、存储。→ 先问 Claude "is there an existing helper for X?"，再 `Ctrl+Shift+F`。
2. **改 deprecated / legacy 模块**：README 可能还在提它。→ E2 就把 legacy 标出来。
3. **跨租户 / 权限**：多租户系统里所有查询都带 tenant；新端点要过已有的认证与角色装饰器。
4. **同步副作用放在请求路径上**（发 webhook、发通知）→ 已有队列/outbox 就用它。
5. **只有单元测试没有端到端**：最后一定通过真实入口（CLI/HTTP）演示一次。
6. **AI 顺手大改**：格式化整个文件、改无关代码、加依赖。→ diff 里看到就回滚那部分并说出来。
7. **沉默**：超过 60 秒没说话 = 面试官不知道你在想什么。

## 5. 口播模板（English）

### 5.1 第 10 分钟：心智模型（60 s）

> "Here's my model of the system. The entry point is <CLI/API>, which <loads X>. Data flows <A → B → C → D>. The extension point for new behavior is <registry/base class> in <file> — each <detector/signal/route> is registered with <decorator>, and configuration is per-<tenant> in <settings>. Persistence goes through <repository/store> on SQLite. Tests mirror the package layout under `tests/`. Two things I'd be careful with: <legacy module> is deprecated, and <tenant isolation / time zones> is handled in <place>, so I'll reuse that rather than reimplement it."

### 5.2 方案与里程碑（30 s）

> "Two ways to do this: <A> or <B>. I'll go with <A> because it fits <existing pattern> and keeps <policy/config> in one place. Milestone one, which I want working end to end in about fifteen minutes, is <narrow slice>. Milestone two is <the ambiguous part>. Milestone three, if there's time, is <polish/config/observability>. Assumptions so far: <1>, <2>."

### 5.3 Walkthrough（3–5 min）

> "What I shipped: <one sentence, user-facing>. How it fits: it's a <detector/signal/route> registered like the others, config lives in <settings>, state in <store>, and it reuses <util>. Assumptions: <list>. How I tested: unit tests for <cases> next to the existing ones, plus an end-to-end run through <CLI/API> — here's the output. Known gaps: <2–3 honest items>. If I had another hour: <v2>. One thing I changed from what the AI first proposed: <x>, because <y>."

### 5.4 被问"AI 写的这段为什么这样"

> "It <does X>. I kept it because <fits Y / handles Z>. The part I checked carefully is <edge>, since that's where it could be wrong. I'd change <minor thing> with more time."

## 6. 考前 48 小时

1. 按 `../../../catalog/PARETO.md` 的顺序做：**cb01 t1（规则抑制）→ cb01 t2（插件化 enrichment）→ cb02 t1 → cb03 t1 → cb01 t3 → cb02 t3 → cb03 t2 → cb02 t2 → cb03 t3**。前两张是报道过的原题形态，至少各做两遍（第二遍换一种设计）。每次严格 60 分钟、出声（或录屏）。
2. 每次 `check` 后 `reveal`，把自评表里的 0 写进 `../../../debrief/`（若有）或本文件末尾的复盘表。
3. 本地 Claude Code 熟练度：plan mode、`Esc` 打断、`@file`、`!cmd`、`/resume` 各用一次；VS Code 网页版快捷键试一遍。
4. 准备 2 个反问 + Why Abnormal / Why Insider Risk（`../../../fit.md`）。
5. 面试当天：门户再看一次（"It'll update as you move through each stage"）。

## 7. 复盘表（每次模拟后填一行）

| 日期 | 题 | core/stretch | 新增测试 | 心智模型 ≤10' | M1 ≤30' | 最大失误 | 下次改什么 |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
