---
id: ai-generation-loop
node: ai.foundations
type: qa
---
## Q
In backend terms: what does an LLM server actually do with a request, and why does the response stream out token-by-token instead of arriving at once?

## A
Two phases:

- **Prefill**: the whole prompt is read in one parallel pass — this sets **time-to-first-token**.
- **Decode**: a loop — predict the next token, append it to the input, repeat until a stop condition. Each token depends on everything before it, so generation is **inherently sequential**; there is no "compute the whole answer in parallel".

Consequences: latency scales with **output length**, streaming APIs exist because tokens genuinely become available one at a time, and the API is **stateless** — the server keeps no conversation memory; the client resends history every call.

## Q zh
用后端术语来说：LLM 服务器实际上如何处理请求，为什么响应是逐 token 流出而不是一次到达？

## A zh
两个阶段：

- **预填充（Prefill）**：整个 prompt 在一次并行通过中读取 — 这设置了 **time-to-first-token**。
- **解码（Decode）**：一个循环 — 预测下一个 token，将其追加到输入，重复直到停止条件。每个 token 依赖它前面的所有东西，所以生成是 **本质上顺序的**；没有"并行计算整个答案"。

后果：延迟按 **输出长度** 缩放，流 API 存在是因为 token 确实一次一个地变得可用，API 是 **无状态的** — 服务器不保留对话历史；客户端每次调用都重新发送历史。
