---
id: cbr-hm-ai-gap-framing
node: hm.ai-gap
type: qa
step: 1
---
## Q
面试被问到 AI / ML 经验，你没有，怎么诚实地答？按顺序有哪几步？

## A
1. **Say it first**: "I'm **new to ML**, and I won't pretend otherwise."
2. **What I understand**: inference runs fixed weights one token at a time; **decode is memory-bandwidth-bound**; weights in **on-chip SRAM** is why the wafer is fast; the cost is **capacity**, so models **pipeline across wafers**.
3. **What I've touched**: PyTorch training on my **8-GPU** server; apps on the **OpenAI API**; **AI coding agents** daily, with tests as the guardrail.
4. **How I learn**: "I taught myself backtest statistics by **building** the platform and **testing each piece**. For ML I'm going **in order** — basics, inference, serving, numerics — and I'd **pair with feature engineers** in the first month."
5. **What transfers**: parity testing → **reference comparison**; quality gates → **readiness gates**; on-call RCA → **cross-stack triage**.

> 中文提示：不要编 ML 项目；不要用解释不了下一层的术语。说完第 2 条可以停，看他想不想往下问。
