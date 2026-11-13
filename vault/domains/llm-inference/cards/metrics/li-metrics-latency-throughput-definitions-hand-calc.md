---
id: li-metrics-latency-throughput-definitions-hand-calc
node: metrics.latency-throughput
type: qa
step: 1
---
## Q
TTFT、TPOT、ITL、端到端延迟和吞吐各怎么精确定义？给一个请求的时间戳，手算这些指标。

## A
**一个流式请求的时间戳（单位毫秒）：** 0 发出请求；300 收到第 1 个 token（token 是文字切成的小片段）；之后又收到 99 个 token，最后一个在 2,280 到达。共 100 个输出 token。

- **TTFT（time to first token，首 token 延迟）：** 发出请求到收到第一个 token。= **300 ms**。包含排队、对输入做预填充（一次性处理整段输入）、第一步生成、网络。
- **端到端延迟（E2E latency）：** 发出到收到最后一个 token。= **2,280 ms**。
- **TPOT（time per output token，每输出 token 时间）：** 第一个 token 之后，平均每个 token 的间隔：
  `TPOT = (E2E − TTFT) / (输出 token 数 − 1)` = (2,280 − 300) / 99 = **20 ms**
  这是**每个请求一个数**，再对所有请求求分布。
- **ITL（inter-token latency，token 间延迟）：** 每两个相邻 token 之间的实际间隔，一个请求有 99 个值。平均值等于 TPOT，但分布能看到卡顿：99 个间隔里 98 个是 15 ms，1 个是 510 ms（比如被别人的长输入预填充挡住），平均仍是 20 ms，ITL 的 P99 却暴露了 510 ms 的停顿。
- **单用户生成速度：** 1,000 / TPOT = **50 token/s**。
- **吞吐（throughput）：** 整个系统单位时间的产出，必须说清口径：
  - 输出 token 吞吐：所有请求的输出 token 总数 ÷ 测试总时长；
  - 总 token 吞吐：输入加输出 token 总数 ÷ 总时长（输入长的负载会显得很高）；
  - 请求吞吐：完成请求数 ÷ 总时长。

**例子：** 测试 60 秒内完成 600 个上述请求，输出吞吐 = 600 × 100 / 60 = **1,000 token/s**，请求吞吐 = 10 个/秒。

**常见混淆：**
- 单用户速度（50 token/s）和系统吞吐（1,000 token/s）是两回事，宣传数字要先问是哪个。
- 平均值掩盖尾部：延迟指标都要报 P50、P90、P99。
- `vllm bench serve` 的输出分别列出 Mean / Median / P99 的 TTFT、TPOT、ITL，以及 "Output token throughput"，读结果时按这几个定义对号入座。
