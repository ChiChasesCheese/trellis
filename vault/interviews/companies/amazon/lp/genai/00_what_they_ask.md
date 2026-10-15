# 00 · GenAI fluency 轮：他们问什么、为什么问、怎么打分（教科书版）

> 目标岗位 SDE I，AWS Data Services（job 10414316）；Chi 的 bar 永远是 senior（`../../AGENT_RULES.md`）。Onsite 约 2026-10-20/21（推断，见 AGENT_RULES）。
> 本目录：`00_what_they_ask.md`（这篇）· `stories.md`（4 个英文 STAR）· `question_bank.md`（题库 + 变体）· `primer.md`（说得精确所需的原理）。
> 标注：`[面经]` = 论坛原始记录，见 `../../catalog/raw/forums.md`（简称 F）；`[官]` = amazon.jobs 一手页面，见 `../../catalog/raw/official.md`（简称 O）；`推断` = 我的判断，没有官方来源；`【待 Chi 补】` = 只有 Chi 知道的事实，不替他编。

---

## 1. 这一轮到底是什么（事实）

**没有任何官方页面描述它。** 我在 O（amazon.jobs 的 interview-loop、SDE II / SDE III 备考页、LP 页）里没有找到 GenAI 面试的说明；唯一的一手线索是岗位 JD 的一句话 "using GenAI tools to boost productivity"（引自 `../../AGENT_RULES.md` 与 `../../LOOP_GUIDE.md` §2；我用 r.jina.ai 重抓 job 10414316 页面，该页是 SPA，没有取回正文，所以这句话是 orchestrator 转述，**未独立复核**，2026-10-15）。因此下面全部来自面经。

### 1.1 出现频率（F §4.1、§4.1b；口径见 F 原文）

| 口径 | GenAI-fluency 轮 | 备注 |
|---|---|---|
| F §4.1 SDE I（n=63，一份报告里出现即计 1） | **16 / 63** | 通常是 HM 轮；refs 前 8：JC-qbgerq, LC7584467, LC8293563, LC8471051, LC8500377, LC8520348, LC8535500, LC8542502 +8 |
| F §4.1 SDE II+（n=47） | 3 / 47 | LC8420230, LC8468910, RD1wjhv3k |
| F §4.1b 未筛选全量，SDE I / US | 2 / 5（40%） | 样本很小 |
| F §4.1b SDE I / 地区未判 | 15 / 60（25%） | |
| F §4.1b SDE I / IN | 1 / 28（3%） | 印度新毕业生报告里几乎没有 |
| F §4.1b SDE II+ / US | 0 / 9 | |
| F §4.2 LP/GenAI 题目表 | GenAI 题 **12 个独立 refs** | JC-qbgerq, LC8293563, LC8471051, LC8520348, LC8535500, LC8542502, RD1wcfb9m, RD1wd8nij, RD1wjhv3k, RD1wvqv67, RD1wzfres, RD1x1fmxc |

读法（推断）：US + SDE I + 2026 年 loop 里它是**近乎标配的一个 15–30 分钟模块**；SDE II+ 的报告里少，但 F 自己说 SDE II+ 样本偏设计向，且 F §4.1b 的 SDE II+ 帖子很少提到它，所以**不能据此认为 senior 档不考**——Chi 的 bar 是 senior，按会被问来准备。数据有幸存者偏差（愿意发帖的人，F §4.1 口径说明）。

### 1.2 它出现的形式（逐条来自 F §3 的 loop 记录）

| 形式 | 例子 | 来源 |
|---|---|---|
| HM 轮开头一段**纯 GenAI 讨论**，然后写代码 | "first 30 min entirely GenAI discussion; then First Non-Repeating Character (10 min) + a Merge Intervals modification"（美国西雅图现场，Offer） | LC8520348 |
| 15 分钟 GenAI/AI tools + 45 分钟编码 | "R2 15 min GenAI/AI tools + 45 min sliding-window substring"（AWS S3 Glacier，西雅图，拒） | LC8535500 |
| HM 轮：GenAI + 一道 LC | "R1 HM: GenAI + LC 'Longest Substring without repeating characters' (+ 'Can you tell me a time where AI hallucinated and how did you handle it?')" | RD1x1fmxc |
| 单独的「GenAI 面试」，含规则查找题 + "How do you use AI?" | "R2 GenAI interview: rule/decision lookup with DEFAULT wildcard + 'How do you use AI?'" | RD1wcfb9m |
| SDM（工程经理）轮：简历 + AI fluency | "AI fluency discussion ('How do you use LLMs during development?', 'How do you verify whether an AI-generated solution is correct?', 'When do you trust an LLM and when do you not?')"（Offer） | LC8471051 |
| 技术深挖：项目里的 GenAI | "GenAI project questions (hallucination, verification, input security, prompt engineering)" | LC8542502 |
| 技术深挖：架构取舍 | "technical deep dive: GenAI/project/architecture ('hallucinations', 'why chose certain technologies/designs', trade-offs)" | RD1urcepm |
| GenAI 工作流 + 难 DSA | "R3 = 'GenAI round' with a hard DSA + GenAI workflow talk"（Offer） | LC8546875 |
| 编码轮顺带问 AI 用法 | "'GenAI Essential + Coding' round: ... 'Just another dsa round ... with how you use GenAi'" | LC7584467 |
| 设计题：架构一个 AI 聊天机器人 | "GenAI: 'architect an AI chat bot' system design question from one interviewer" | JC-qbgerq |
| Senior EM 轮 LP 里夹带 AI 工具验证 | "R4 Senior Eng Manager: LP incl. AI-tool validation" | LC8468910 |
| **OA 里直接让你用 AI** | "AI-assisted repo (controller/service/repository layers, 6 failing tests)"；"Django debugging (AI assistant provided, limited)"；"OA with AI coding (fix repo from README)"；"1 AI-chatbot coding" | LC8315111, JC-amz882, JC-amz445, LC8568929 |

**三点结构性结论（均为从上表归纳，推断）**
1. 99% 是**口述 + 追问**，不写 prompt、不现场调 API；时间 15–30 分钟，往往和一道编码题同轮（HM 轮）。
2. 面试官是 HM / SDM / 工程师，不是专门的 AI 专家，所以追问的是**工程判断**（验证、信任边界、取舍），不是 transformer 细节。
3. OA 已经在**测你会不会用 AI 工具修 repo**（带失败测试的仓库）——说明「用 AI」是被当作一项可观察的技能，不只是态度。

### 1.3 原题（逐字，12 个 ref 的汇总行，F §4.2）

> "How do you use GenAI?" / "Can you tell me a time where AI hallucinated and how did you handle it?" / "How do you verify whether an AI-generated solution is correct?" / "When do you trust an LLM and when do you not?" / "Where have you used GenAI and later felt it was unnecessary?"

另有 3 条逐字：`"How do you use LLMs during development?"`（LC8471051）、`"How do you use AI?"`（RD1wcfb9m）、"How do you use GenAI in your workflow ... how do you validate GenAI's output for correctness"（RD1wd8nij，原文带省略号）。全部在 `question_bank.md` 里，每题映射到 `stories.md` 的故事。

---

## 2. 为什么 Amazon 加这一轮（全部 推断，官方没有说明）

官方没有解释。能从证据推出的、按可信度排序：

1. **岗位本身写了它。** JD 的职责里有 "using GenAI tools to boost productivity"（O/AGENT_RULES 转述）。面试考的是 JD 里的职责——这是最直接的理由。
2. **OA 已经让你用 AI。** F 里至少 4 份报告的 OA 带 AI 助手或「修一个有失败测试的仓库」（LC8315111, JC-amz882, JC-amz445, LC8568929）。公司在把 AI 辅助编码当作日常工作方式，那么面试要知道「候选人拿到一份 AI 写的东西会怎么处理」。
3. **信号迁移（我的判断）**：当写出代码变便宜，区分工程师的是**验证、判断、承担责任**。这三样恰好是 Amazon 一直在打分的 LP：Dive Deep（"skeptical when metrics and anecdote differ"）、Insist on the Highest Standards（"ensure that defects do not get sent down the line"）、Ownership、Earn Trust（公开认错）、Learn and Be Curious、Bias for Action（可逆决定先动）——原文见 `../00_how_lp_works.md` §1。GenAI 轮不是新的评分维度，是**同一批 LP 在 AI 场景下的取证**。
4. **风险筛查（我的判断）**：问「when do you trust」「input security」「hallucination」是在筛两类人：全盘接受 AI 输出的人，和把机密数据贴进公共工具的人。LC8542502 的题目主题（hallucination / verification / input security / prompt engineering）正好是这四个风险点。

> 没有证据说明这轮「淘汰率」多高。F 的结果列里 GenAI 轮出现在 Offer 报告（LC8520348, LC8471051, LC8546875, LC8293563）也出现在拒信报告（LC8535500, RD1x1fmxc, RD1wcfb9m）——**不能从面经推断它单独决定结果**。

---

## 3. 怎么打分（全部 推断）

官方只说面试官会 "take detailed notes"、各自评估不同方面（O §5，interview-loop 页）。GenAI 轮的 rubric 不公开。下面是按 Amazon 通用的「证据驱动」打分方式（`../00_how_lp_works.md` §3）推出来的**可能的评分轴**——用来设计答案，不要当成官方：

| 轴 | 面试官想从笔记里写下什么 | 强信号 | 红旗 |
|---|---|---|---|
| **A. 真实使用**（Learn & Be Curious / Bias for Action） | 候选人在 SDLC 哪几步用 AI：设计、编码、测试、review、调试、文档 | 具体工具 + 具体任务 + 频率；说得出一次具体的 prompt/上下文是怎么给的 | "I use ChatGPT for everything" / 只会说 "autocomplete" |
| **B. 验证纪律**（Dive Deep / Highest Standards） | 怎么确认 AI 的输出是对的 | 有**机制**：测试、类型/编译、脚本复算、对照一手来源；知道测试本身也要被验证 | "I read it and it looks right" |
| **C. 信任边界**（Are Right, A Lot / 判断力） | 什么时候信、什么时候不信、为什么 | 按**爆炸半径 × 可验证性**划线；举得出"不该用"的例子 | 全信或全不信；讲不出任何一次"不该用" |
| **D. 失败与纠正**（Earn Trust / Ownership） | 一次真实的 AI 出错，怎么发现的，之后改了什么 | 自己发现；数字；**之后流程里多了什么** | 编一个无代价的故事；把锅甩给工具 |
| **E. 风险意识** | 数据泄露、prompt injection、许可、机密 | 说得出具体控制手段（最小权限、脱敏、审批） | "AI is safe"/没想过 |
| **F. 责任归属**（Ownership） | 谁对最终代码负责 | "I own every diff"；review 标准不因 AI 降低 | "The AI wrote it" |
| **G. 取舍**（Frugality / Think Big） | 成本、延迟、什么时候不用 | 用数字讲取舍（token、分钟、轮数） | 只讲好处 |

打分形态（推断）：与其他 LP 一样，面试官把你的回答写成「证据」，在 debrief 里对着被分配的 LP 评级。因此每个 GenAI 故事**必须同时能被转述成一个 LP 的证据**（`stories.md` 每个故事标了 LP）。

---

## 4. Senior 答案 vs Junior 答案

| 维度 | Junior | Senior |
|---|---|---|
| **使用** | "I use Copilot/ChatGPT to write code faster." | 分工明确：哪些步骤交给 AI、哪些不交；并行 agent 的**编排**（谁拥有哪些文件、几个并行、上限多少） |
| **验证** | "I check the output / run it." | **机制**：验收门是一条命令；参考解必须绿、空模板必须红；数字由脚本复算；用变异测试验证测试能抓错；每个缺陷变成指令文件里的一条规则 |
| **信任** | "I trust it for simple stuff." | 一个**判定规则**：有无可执行的 oracle（测试/编译/脚本）× 错了的代价；列出 oracle 覆盖不到的盲区（"一个建立在合理假设上的错误结论"） |
| **失败** | 一次 hallucination，我发现了，我改了 | 发现它的**机制**、量化（量级错了 10⁶ 倍、已抄进卡片）、之后让别人不再踩的规则 |
| **取舍** | 只说效率提升 | 成本与延迟：一轮修订 5–6 分钟/+40–60k tokens vs 就地改；何时不用 AI（计数、确定性判定用脚本） |
| **风险** | 一句 "don't paste secrets" | 爆炸半径：最小权限、沙箱、审批、公开仓库规则、测试夹具曾经写到真实 Anki 集合所以加了拒绝写入的 guard |
| **影响力** | 自己用得好 | 别人也能用：规则文件、指令文件、gate 脚本；团队采用（S7 里相邻团队采用 on-call copilot，**边界：个人仓库，不是团队官方工具链**） |
| **语气** | 热情或恐惧 | 工程师的平静：AI 是不可靠但便宜的生成器，工程在验证环节 |

**一句话心法**：generate cheaply, verify mechanically, own the diff.

---

## 5. Chi 的真实材料边界（诚实原则）

- **repo 里能证明的**：trellis 用 Claude Code 多 agent 构建，带显式验证规则（`/CLAUDE.md` 的 "Orchestration rules"）。具体被抓到的错、门禁、变异测试，commit 与路径在 `stories.md`。
- **repo 里不能证明的**：某次审查是 Chi 本人看到的，还是 orchestrator 会话在 Chi 的规则下看到的。Bar Raiser 会问 "What exactly did **you** do?"。安全说法：**"I wrote the rules and the gate; the review step caught it"**，并准备好回答"我自己亲眼看到的是哪几次"（`stories.md` 每个故事有 `【待 Chi 补】`）。
- **日常工作（PayPal）**：仅来自 `core/`：简历一句 "AI-native development workflow (Claude Code for code review, test generation, and refactoring), ensuring behavioral parity through comprehensive testing"；S7 笔记里的 Claude Code / Codex / Cursor 并行、schema pool、on-call copilot（个人仓库，不是团队官方工具链）、"plan with the agent → TDD every phase → CI + monitoring gates"、"in money code I read every diff myself"。迁移规模、parity 通过率、加速倍数、日常里 AI 出过的真实错——全部 `【待 Chi 补】`（见 `../stories/R2_ai-native-migration.md`）。
- **保密**：仓库是公开的；面试里也不要点名内部工具/数据。说 "a payments data platform"，不说内部系统名。

---

## 6. 备考节奏（到 2026-10-20）

| 何时 | 做什么 | 文件 |
|---|---|---|
| 今天 | 读本篇；把 `stories.md` 的 4 个故事各出声讲 2 遍，掐表 60–90 秒；填 `【待 Chi 补】` | `stories.md` |
| 明天 | `primer.md` 读完并做完所有自测（折叠答案先别看）；用 `question_bank.md` 的 3 要点各口述一遍 | `primer.md`, `question_bank.md` |
| onsite 前一晚 | 只过 `question_bank.md` 的"一句话开场"和 4 个故事的第一句；不要再加新内容 | |

## 7. 自测

**Q1. GenAI 轮在面经里通常出现在哪一轮、多长？**
<details><summary>答案</summary>多在 HM（或 SDM）轮，15–30 分钟，常与一道编码题同轮（LC8520348：前 30 分钟；LC8535500：15 分钟 + 45 分钟编码；RD1x1fmxc：GenAI + LC）。F §4.1：SDE I 16/63。</details>

**Q2. 官方对这一轮说了什么？**
<details><summary>答案</summary>我没有找到官方说明；唯一的一手线索是 JD 的 "using GenAI tools to boost productivity"（转述，未独立复核）。"为什么加"和"怎么打分"都是推断。</details>

**Q3. 为什么"I read it and it looks right"是 senior 档的失分答案？**
<details><summary>答案</summary>它不是机制，不能被审计也不能被别人复用；senior 要的是 oracle（测试/编译/脚本复算/一手来源）+ 对 oracle 本身的检验（变异测试）+ 谁负责。</details>

**Q4. 面试官追问 "What exactly did you do?" 时，对 trellis 的故事怎么答最稳？**
<details><summary>答案</summary>"I wrote the rules and the acceptance gate, and the review step I set up caught it"；再补一句自己亲手看到/复算的具体一次。不要说成"我一个人手写了所有东西"，也不要说成"AI 自己发现的"。</details>
