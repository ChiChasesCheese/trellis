# 一周练习计划 · AI Technical Screen

> 全部练习按可信度排序：`../../PRACTICE_INDEX.md`（A 一手原题 → B 报告过的轮次 → C 推断 → D 长期能力）。

> 目标：周一面试能过；之后任何 AI coding 轮都不怵；平时工作用同一套方法。
> 每天约 3 小时：**学 30 · 模拟 60 · 复盘 30 · 专项 30 · 迁移 15**。面试在 10/12（周一）就按 D1=10/7 排，D6 压到周日，D7 只做最后检查。
> 环境：`CLAUDE_CONFIG_DIR=~/.claude-interview claude`（`claude_playbook.md` §五）。模拟一律录屏、出声、严格计时。
> 命令都在 kit 根目录跑：`python3 loop/ai_screen.py start|check|reveal <cb> <t>`。

## 每天的固定动作

- **模拟后复盘**（30 min）：`check` → `reveal` → 对照 `cb0*/walkthrough.md` 的逐阶段表，在 `playbook.md` §7 记一行：评级自估 · 沉默超过 60 秒的段 · 漏掉的 T · 点了名却没交付的条目。
- **迁移**（15 min）：把当天练的那个 T 用在你自己的项目里一次（trellis、quant 都行），写一句效果。连续一周，它就成了习惯，不再是面试动作。

## D1 · 读代码与心智模型（X2 · T1）

| 段 | 内容 |
|---|---|
| 学 | `claude_playbook.md` 全文；HI Codebase Orientation |
| 专项 | cb01 / cb02 / cb03 / cb04 / cb05 的 starter 各开一次，**只做前 10 分钟**：T1 + 自己翻文件 → 对着录音讲 60 秒心智模型（英文）→ 对照 walkthrough §0 打分（入口 · 数据流 · 扩展点 · 约定 · 一个风险，每项 1 分） |
| 模拟 | `start cb01 real`（报道过的原题） |
| 迁移 | 给一个你不熟的仓库跑 T1，看 AI 的地图有几处是错的 |

> 2026-10-09 新证据：真实代码库叫 "Sentinal"，题目是 "implement a rule engine"（Glassdoor 2026-07-15）。**规则题优先**：cb01 t1（规则抑制）与 cb05 t1（规则表达式语言）各至少做两遍。

## D2 · 模糊性与设计（X4 X5 · T2 T3 T4 T5）

| 段 | 内容 |
|---|---|
| 学 | HI Planning Your Approach；`interviewer.md` 的澄清问答表（随便挑 3 题读） |
| 专项 | **15 张 ticket，每张 5 分钟，不写代码**：T2 生成问题 → 挑 2–3 个 → 说出假设 → T5 点名接缝 + 两个方案。对照该题 `interviewer.md` ②③，命中率记下来 |
| 模拟 | `start cb01 t1`；加练 HI LRU Cache（30 min） |
| 迁移 | 下一个工作任务开工前跑一次 T2，把答案写进任务描述 |

## D3 · 红 → 绿与验证（X6 X8 · T7 T9 T11）

| 段 | 内容 |
|---|---|
| 学 | HI Verification & Testing；Matt `tdd` 的三个反模式（horizontal slicing、tautological、implementation-coupled） |
| 专项 | `cb05` t1 的解析器：**5 轮红 → 绿**，每轮一个行为（比较、and/or、括号、`any()`、语法错误位置），每轮都看到红再绿；每轮结束检查期望值是不是字面量 |
| 模拟 | `start cb02 t1`（Insider Risk，最贴岗位） |
| 迁移 | 工作里下一个 bug：先写失败测试，再修 |

## D4 · 修 bug + 推到生产可用（X3 X9 · T8 T12）

| 段 | 内容 |
|---|---|
| 学 | `hi_practice.md` 的 A 类公共清单；Matt `diagnosing-bugs` Phase 1（先建反馈回路） |
| 专项 | `cb04` t1：每个埋好的 bug 先写一个能变红的命令，再修；最后按影响排序讲 2 分钟 |
| 模拟 | HI **Schedulr**（60 min，提交拿评级）；时间够再做 `cb06_filevault` t1（Abnormal 真实 take-home 同形：去重 + 并发上传）的 M1 |
| 迁移 | 拿你最近写的一个服务过一遍 A 类清单，记下命中了几条 |

## D5 · 算法型题与认出模式（X1 · T5 T7）

| 段 | 内容 |
|---|---|
| 学 | HI Patterns 总览；Topological Sort、Graph Search 两篇只读"How to recognize / What to tell the AI"两节 |
| 专项 | `cb05` t2（拓扑排序 + 环检测）和 t3（按时间约束的 BFS）各做一次 **M1**（≤ 20 min）：先说出 "this is Kahn's / time-constrained BFS"，再提示；验证用的边界情况由你点名 |
| 模拟 | HI **Gridbot**（45 min）或 **LinkLock**（60 min） |
| 迁移 | 一个工作需求先说出它是什么模式，再交给 AI |

## D6 · 全真彩排（全部 X · T）

| 段 | 内容 |
|---|---|
| 学 | `playbook.md` §5 口播模板，大声读两遍 |
| 模拟 | 干净配置 + 屏幕共享 + 有人（或录音）扮演面试官：`start cb03 t1` 60 分钟；最后 15 分钟用 `interviewer.md` ④ 的追问做扩展讨论 |
| 专项 | **只练嘴**：拿 D1–D5 任意一场的 diff，3–5 分钟 walkthrough（做了什么 · 为什么契合 · 假设 · 测了什么 · known gaps · v2），录两遍，比较第二遍的沉默和废话；再按 `cb06_filevault/walkthrough.md` 末节录一段 5 分钟的"我怎么用 AI"（Abnormal take-home 原要求：只讲 GenAI 用法，不演示功能） |
| 迁移 | 写你自己的工作版 CLAUDE.md（T6 规则 + 你的项目约定），以后每个仓库都用 |

## D7 · 补弱 + 面试当天

- 上午：复盘表里出现最多的那个 T，用它最弱的那道题重做 M1（30 min）。
- 不做新题。准备 2 个反问（`../../../06-questions-to-ask.md`）。
- 面试前 15 分钟：网络 · 麦克风 · 屏幕共享 · 门户链接；开两个终端；读一遍 `claude_playbook.md` §三。

## 题库总览（按题型）

| 题型 | kit 内 | HI |
|---|---|---|
| 在已有系统上加 feature | cb01 t1 t3 · cb02 t1 t2 · cb03 t1 t3 | — |
| 可扩展性（插件 / 新数据源） | cb01 t2（原题）· cb02 t3 · cb03 t2 | — |
| 修 bug + 推到生产可用 | cb04 t1 t2 | Schedulr · Transcribe · Fileshare · LinkLock |
| 规模 / 突发流量 | cb04 t3 | Transcribe |
| 算法：解析 / 拓扑 / 图 | cb05 t1 t2 t3 | Gridbot |
| 并发正确性 | cb04 t1 · cb06 t1 | Schedulr · Transcribe |
| 真实 take-home 同形（去重 · 搜索 · 配额 · 统计） | cb06 t1 t2 t3 | Fileshare |
| 数据结构设计 | — | LRU Cache |
| 从零搭 | — | Gridbot · LRU · Collaborative Editor · Text Render |

没进计划的题留到面试后，按同样的结构继续做：练的是方法，不是题。
