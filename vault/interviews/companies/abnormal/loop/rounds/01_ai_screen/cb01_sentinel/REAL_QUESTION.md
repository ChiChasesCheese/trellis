# 真题复刻 · Abnormal AI Screening Round（security-events 代码库）—— 原帖与错因

> 来源：LeetCode Discuss #8335187 "Abnormal Ai screening round was a sh*t"（2026-06-15，候选人自述；编排者 2026-10-06 经 `POST leetcode.com/graphql` 重取，逐字核对）。另有 1p3a thread 1181621（2026-06-29，Telegram 镜像摘要）与 PracHub 标题 "Extensible Security-Event Pipeline: Rule Suppression and Plugin-Based Enrichment" 印证同一代码库形态。

## 1. 原帖原文（英文原话 + 中文翻译）

> "They ask you to read a codebase which I skimmed through in like 10 mins and claude (allowed). Then they … again mentioned you still have 3 mins to go through code. I was like - let me understand the question first then I'll deep-dive into specific component … Then he gave me a question after I started acting on it. He said sorry I gave the wrong question and it was still a vague question."

中文：先给你一个代码库读，可以用 Claude，他大概 10 分钟扫完；面试官又说"你还有 3 分钟看代码"；他想先看题再深入；面试官给了题，他开始做之后，面试官说"抱歉给错题了"，换的题依然很模糊。

> "The repo did was - processed all security events like collection/ingestion, ranking, threat levelling based on some rules, created alerts, created apis on top of it and put it to database."

中文：代码库做的是——处理所有安全事件：采集/摄入、排序、基于规则定威胁等级、生成告警、在上面提供 API、存进数据库。

> **题①（面试官说给错了）**："We've to allow users to suppress some rules (it can be complex rules like based on geo-ip (existing in code) and other rules)."

中文：要让用户能**抑制（静音）某些规则**；条件可能很复杂，比如基于 geo-ip（代码里已有）以及其它规则。

> **题②（真正的题）**："The enrichment layer currently hardcodes based on some threats (geo-ip, history, 1 more) clients want more configurability without touching platform code. Implement a plugin based mechanism to ensure no code touching by clients. (On these lines, very vague)"

中文：富化层目前**写死**了几种威胁信息（geo-ip、history，还有一种）；客户想要更多可配置性，而且**不碰平台代码**。实现一个**插件机制**，保证客户不用改我们的代码。（大意如此，非常模糊）

> "After 20 mins of struggling and explaning them how can we add decorator pattern and clients can choose which threats they want to use/avoid etc I resorted to claude to code it completely for me. I'll mostly get a No."

中文：他花了 20 分钟挣扎、口头解释"可以加 decorator 模式、让客户选择用哪些威胁信息"，最后让 Claude 全部代写。自评大概率挂。

### 他哪里做错了（对照官方评分）

| 官方要的 | 他做的 | 应该做的 |
|---|---|---|
| Agency：做决定、说假设、保持推进 | 20 分钟停在口头讨论 | 2–3 个澄清问题后**当场定下假设**，5 分钟内开始写 M1 |
| Judgment：契合现有系统 | 提 decorator 模式（通用答案，没先看代码里有什么） | 先发现代码里**已有一个没被用起来的 `Enricher` 基类**，让它成为插件契约 |
| "AI is a resource you supervise" | 最后让 Claude 全写 | 让 Claude 先找已有模式，再按你定的方案写，你审 diff |
| "ship a working v1" | 没有能跑的东西 | 第 30 分钟前通过 CLI 演示：插件文件丢进目录 → 配置启用 → 事件上出现新字段 |
| 模糊性被评分 | 抱怨题目模糊 | 模糊是考点：把模糊拆成决策点，逐个说"我选 X，因为 Y，可配置/可改" |

---

讲解、参考答案、澄清问题、方案对比、里程碑、实现要点与追问：见 `walkthrough.md` §t2（口述版练习：`python3 loop/ai_screen.py start cb01 real`）。
