---
id: foundations-latency-requirement-precision
node: foundations.method
type: qa
---
## Q
"It should be fast" — turn that into an engineering requirement. What elements make a response-time requirement precise enough to design against?

## A
- **Metric**: response time **measured at the client** (includes queueing + network), not server service time.
- **Percentiles**: a median *and* a tail target (e.g. p99) — never the mean, which no actual user experiences.
- **Threshold + window**: "p99 < 1 s over rolling 10-min windows".
- **Load assumption**: the requirement holds *at* a stated load (e.g. 1,000 RPS peak) — latency without load is meaningless.

Sample: "median < 200 ms, p99 < 1 s, client-measured, at peak 1k RPS."


## Q zh
"它应该要快" — 把这句话变成一个工程需求。哪些要素能让一个响应时间需求精确到足以据此设计？

## A zh
- **指标**：**在客户端测量**的响应时间（包含排队 + 网络），不是服务器端的服务时间。
- **百分位**：既要中位数**也**要尾部目标（例如 p99）— 永远不要用均值，没有真实用户经历的是均值。
- **阈值 + 窗口**：例如"滚动 10 分钟窗口内 p99 < 1 秒"。
- **负载假设**：需求只在**指定负载**下成立（例如峰值 1,000 RPS）— 不带负载谈延迟毫无意义。

示例："中位数 < 200 ms，p99 < 1 秒，客户端测量，峰值 1k RPS 下。"
