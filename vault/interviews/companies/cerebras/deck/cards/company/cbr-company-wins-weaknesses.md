---
id: cbr-company-wins-weaknesses
node: company.competitors
type: qa
step: 2
---
## Q
和 GPU 方案相比，Cerebras 赢在哪、弱在哪？

## A
| 赢在 | 弱在 |
|---|---|
| **单用户速度**：第三方在 gpt-oss-120B 上测的首个回答 token 时间，Cerebras 1.79 s，Groq 4.63 s，SambaNova 5.85 s，Bedrock 19.58 s | **容量**：每块晶圆 44 GB，大模型要几十块晶圆 |
| **供应链**：不依赖 HBM、先进封装和 3 nm 产能 | **长上下文**：KV 缓存和参数挤同一块内存 |
| **订单**：OpenAI 750 MW、在手订单 $26.1B | **毛利**：GAAP 14–20% |
| **对 AI 代理的价值**：速度直接缩短代理任务的等待 | **生态**：没有 CUDA；共享推理只有 2 个模型 |
| | **集中度**：少数客户占大头 |

- **首个 token 时间（TTFT, time to first token）**：从发出请求到收到第一个输出 token 的时间。
- **一句话**："Cerebras sells the lowest single-user latency; it pays in capacity, so big models span many wafers."
