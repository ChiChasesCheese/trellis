---
id: ai-context-window-budget
node: ai.foundations
type: qa
---
## Q
Why should you treat an LLM's context window as a fixed resource budget rather than "room for everything", and who competes for it?

## A
The context window is a hard cap on **input + output tokens per request**, and four things compete for it: the system prompt, conversation history, injected documents (RAG), and the space reserved for the answer.

Treat it like a memory budget because:
- Overflow means **truncation** — something silently drops, usually oldest history.
- Cost and prefill latency scale with tokens sent, so "stuff everything in" is paying per request for data the model may ignore.
- Effective use degrades before the hard limit — models attend best to the **start and end** of long contexts ("lost in the middle"), so placement of critical facts matters.

## Q zh
为什么应该把 LLM 的上下文窗口看作固定的资源预算而不是"能装所有东西的空间"，谁在竞争它？

## A zh
上下文窗口对 **每次请求的输入 + 输出 token 数** 有硬限制，四样东西竞争它：系统提示、对话历史、注入的文档（RAG）和为答案预留的空间。

把它看作内存预算的原因是：
- 溢出意味着 **截断** — 某些东西会被默默丢弃，通常是最老的历史记录。
- 成本和 prefill 延迟随着发送的 token 数缩放，所以"把所有东西都塞进去"是在为模型可能忽视的数据按请求付费。
- 有效利用在到达硬限制之前就会降级 — 模型在长上下文的 **开始和结尾** 注意力最好（"lost in the middle"），所以关键事实的位置很重要。
