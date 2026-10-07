# AI Technical Screen Playbook · 60 min · 浏览器 VS Code + Claude Code · 已有 Python 代码库

> 依据：`../../../catalog/raw/inbox.md`（门户官方原文，[高]）· `../../../catalog/raw/ai_screen_format.md`（视频 / VP of AI 博客 / 同类面试，[中]）· `../../../catalog/raw/process_and_rounds.md`（面经）。
> 练：`python3 loop/ai_screen.py start cb02 t1` → 在打印出的目录里开 VS Code + `claude`，严格 60 分钟 → `check` → `reveal`。
> 怎么驾驶 Claude（哲学、当场提示词卡、亮点、练习配置、38 场真实会话的规律）：`claude_playbook.md`。
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

## 1. 逐分钟与 Claude Code 驾驶

见 `claude_playbook.md` §三（阶段流程）与 §二（技法 T1–T12）。

## 2. 必会快捷键（考前在干净配置里各按一次）

见 `shortcuts.md`（含网页版 VS Code 里会被浏览器抢走的键）。

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

## 6. 练习顺序

见 `claude_playbook.md` §五。

## 7. 复盘表（每次模拟后填一行）

| 日期 | 题 | core/stretch | 新增测试 | 心智模型 ≤10' | M1 ≤30' | 最大失误 | 下次改什么 |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
