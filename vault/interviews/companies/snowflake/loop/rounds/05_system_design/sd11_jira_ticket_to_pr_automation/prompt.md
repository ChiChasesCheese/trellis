# Automated Jira-Ticket-to-PR System

我们想做一个内部工具，把"有人提了一张 Jira 工单"和"最终产生一个可以被review 的 PR"这两件事自动连起来——工单被打上某个特定标签或者分配给一个自动化账号之后，系统应该自动把工单的标题、描述、相关上下文喂给一个能写代码的自动化系统（可以理解为一个编码 agent），让它尝试理解需求、修改代码、跑测试，如果一切顺利就自动开一个 PR 供人来 review。这里有几个必须考虑清楚的地方：整个过程显然不是同步的、瞬时的——从工单被认领到 PR 真正开出来，中间可能要经过很长的处理时间，且这个处理流程本身有很多步骤（理解需求、生成代码改动、跑测试、可能要重试多次），任何一步都可能失败，失败之后要能重试而不是让整个工单卡死或者产生半成品的、状态不一致的 PR；系统显然需要处理很多个工单的并发排队，不能因为一个工单的自动化流程卡住了就影响其他工单的处理；生成代码的这个"编码 agent"本身可能会有各种奇怪的失败模式——它可能生成的代码编译不过，可能理解错了需求，可能跑测试跑到一半超时，这些都要有对应的处理路径；最重要的是，不管自动化流程多顺利，最终产生的代码变更在合入主干之前，必须经过人工 review 这一道关卡，自动化系统本身没有权限直接合并代码。请设计这个系统。

---

**面试环境说明**：这是 Snowflake onsite System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化。这道题有一手报告明确形容"very unique"（不常见），说明这不是一道能靠"背标准答案"应付的题，需要真正把"异步任务编排 + LLM 步骤的不确定失败模式 + 人工把关"这几个概念组合到一起做原创推理；同时这道题和 Snowflake 自己产品方向高度相关（内部明确使用 Claude Code 做 AI-native 开发），面试官可能会对"人机协作边界"这个话题有额外的兴趣。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.14）：
- **聚合站**："Automated Jira-Ticket-to-PR System"，题面摘要 "distributed systems, asynchronous job processing, queue-based architecture" —— PracHub，Hard，185 人做过、2026-06-15（**低**，AI 题库聚合站）。
- **一手印证（本文件独立发现，与聚合站题目互相印证，较为难得）**：加拿大 mid-level（推测 IC2）候选人 onsite 报告——"设计一个内部工具，需要构建一个自动能 handle jira ticket 的系统"，候选人形容"**very unique**"（不常见）—— 1point3acres.com/bbs/thread-1180916-1-1.html，经 Telegram 镜像搜索命中（**高置信度存在，正文 403 仅摘要，追问细节未知**）。
- 这是该题库里少数**聚合站题库与一手面经互相印证**的条目，建议优先准备。
- 与 Snowflake 自身方向对照：Snowflake 与 Anthropic 合作条款明确内部使用 **Claude Code**（`01-company-brief.md` §2），CEO 提出"a tech lead of agents rather than an IC that writes code one line at a time"的工程文化转向，AI 编码 agent **CoCo**（原 Cortex Code）也是公司当前的核心产品方向之一——本题几乎是这些真实工程实践的简化面试版。
- 整体置信度 **MED-HIGH**。
