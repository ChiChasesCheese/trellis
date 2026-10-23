# 一手材料：候选人门户（ModernLoop）· 2026-10-06

> 来源：Abnormal AI 候选人门户页（ModernLoop，候选人专属链接，导出为 PDF 由 Chi 提供）。可信度 **[高]**（官方、本人流程）。
> 仓库是公开的：门户链接、姓名、招聘人员信息不入库，只保留流程事实与官方原文。

## 流程状态

- 职位：**Software Engineer II - Insider Risk**（Abnormal AI）。
- 已完成：HR（recruiter）+ HM（Chi 口述，2026-10-06）。
- 门户 "What's next?"：*"Your recruiting team is scheduling your next interview — Based on availability requested on Oct 6"*。
- 门户标签页：Home · Tips & Tricks · InterviewBox · Messages。门户写明 *"It'll update as you move through each stage, so check back before every interview."* → **每轮前回门户看一次**，后续轮次的官方说明会出现在这里。

## AI Technical Screen —— 官方原文（逐字）

视频：*"AI Technical Screen Overview — David Hagar, Sr Director of Engineering"*；*"Interviewing at Abnormal: How To Use Claude — Shrivu Shankar, VP of AI, gives a quick walkthrough of Claude Code tips & tricks"*。

### What This Is

> The format: Live coding in an existing Python codebase, 60 minutes total. AI tools are expected, not optional.
>
> Think of it as your first day picking up a ticket in an unfamiliar codebase. The session has two parts: exploration (~10 min), where you orient yourself and build a mental model of the system, and feature extension (~35 min), where you'll be given an intentionally underspecified feature to build. How you handle the ambiguity is part of what we're evaluating. The remaining time is yours — walkthrough and questions for us.

### What We're Evaluating

> - **Judgment** is how you evaluate approaches, scope work into milestones, and decide what fits the existing system. It's the difference between output that solves the problem and output that looks like it does.
> - **Agency** is how you move forward when things aren't fully specified — how you make decisions, state assumptions, test your own work, and keep momentum without waiting to be told what's next.
> - Strong candidates ship a working v1 that fits the system. They make decisions, name their assumptions, and iterate. They notice existing abstractions and patterns and let those inform their approach. They think about the user, not just the code.

### How We Think About AI

> AI tools are not a bonus. They're part of how we work at Abnormal, and we expect you to use them throughout the session.
>
> What matters is your relationship with the tools. You are the engineer; AI is a resource you supervise. Use it to move faster while maintaining judgment over the output. If AI generates something, you should be able to explain it, evaluate it, and decide whether it belongs.
>
> - AI will produce working code. That's not enough. The bar is whether the code fits the existing system — its patterns, its conventions, its infrastructure. AI doesn't know what's already in the codebase unless you tell it to look.
> - You won't be able to read every line of AI output. Don't try. Review at the right altitude: does the overall approach make sense? Does it integrate correctly? Does it handle the cases that matter?
> - Use AI for exploration, not just implementation. AI is good at summarizing unfamiliar code, mapping architecture, and finding existing patterns. Candidates who only use AI to write code leave signal on the table.
> - A working v1 with known gaps beats a perfect plan with no code. Ship something. Name what's missing. Iterate if there's time.
> - We're not scoring you on which tools you use or how often. We're watching whether you maintain ownership of the work.

### Your Environment

> At the start of the interview, you'll receive a URL that opens a web-based VS Code environment with Claude Code and the codebase pre-installed. Nothing to install locally, just open the link and you're ready to go.

Tips（原文要点）：新终端 Ctrl+` / Cmd+`，`+` 开并排终端；左侧 Source Control 看 diff；Ctrl/Cmd+Shift+F 全局搜索；Claude Code **Plan mode（Shift+Tab）** "explores the codebase and proposes an approach before writing code"；**`claude --resume` / `/resume`** 在新终端里接上之前的会话上下文。

### How to Prepare

> - Practice navigating unfamiliar Python codebases. Build a mental model fast, find the important files, skip what doesn't matter yet. Practice extending existing systems rather than building from scratch — the skill is integrating with what's already there. Pay attention to existing patterns and abstractions. The best extensions reuse them.
> - Practice working out loud. You'll be asked questions about your decisions and tradeoffs as you go. Synthesize your observations rather than narrating them — tell us what you conclude, not what you're reading.
> - Have your AI workflow ready. Fluency is what matters. If you're going to use AI, it should accelerate you.
> - This is a 60-minute session. Treat it like real work.

## 由原文直接推出的结论（不是猜测）

1. 题型 = **扩展已有系统**，不是从零写算法；评的是"契合系统"，所以**复用已有抽象**是第一得分点。
2. 时间盒写死：探索 ~10 / 实现 ~35 / walkthrough + 反问 ~15。**v1 必须在 35 分钟内能演示。**
3. 模糊性是故意的、被评分的：**问澄清问题 + 写下假设 + 继续推进**三件事都要被看见。
4. "Synthesize your observations rather than narrating them" → 口播说**结论**（"The extension point is X; I'll hook in there because Y"），不是读代码。
5. 工具 = 浏览器 VS Code + Claude Code（官方点名 plan mode、`--resume`）→ 练习时就在 Claude Code 里练，不用 Cursor。
