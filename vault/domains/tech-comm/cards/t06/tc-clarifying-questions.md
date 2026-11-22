---
id: tc-clarifying-questions
node: t06.clarifying-questions
type: qa
step: 1
tags: [惯用说法]
---
## Q
**Clarifying questions · 提澄清问题**｜惯用说法 · 必会

面试官说："Design a rate limiter." 你不确定它是限制单个用户，还是限制整个服务，要在动手前问清楚。英文怎么问？

## A
**可以这么说：**
- "Could you clarify whether we're limiting per user or globally?"
- "Just to confirm, we're talking about an API rate limiter, not a network-level one, right?"
- "Is it okay if I assume about a million users?"
- "What matters more here: low latency or strict accuracy?"
- "Let me make sure I have this right. You want X, and Y is out of scope. Is that correct?"

**别这么说：**
- "What do you mean?" （听起来像质疑对方说得不清楚，要加上你的理解）
- "Is it A or B?" 连问五个：像在审问。

**语气：** 用 "Could you…" 或 "Just to confirm…" 让问题软一点；先给出自己的假设，再请对方确认，对方回答更快。

**一个习惯：** 问完把答案复述一遍："Got it, so per user, about 100 requests a minute."

**出处：** 惯用说法，非引用；做法见 Restate & clarify
