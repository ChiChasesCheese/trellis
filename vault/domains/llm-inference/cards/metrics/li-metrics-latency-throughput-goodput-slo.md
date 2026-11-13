---
id: li-metrics-latency-throughput-goodput-slo
node: metrics.latency-throughput
type: qa
step: 2
---
## Q
什么是有效吞吐（goodput）？为什么只看吞吐会误导？怎样用 `vllm bench serve` 测 goodput？

## A
**吞吐（throughput）的陷阱：** 往推理服务里塞更多并发请求，每一步凑的批更大，总吞吐（每秒输出的 token 数）几乎总能继续上升。但每个用户的首 token 延迟（TTFT，从发出请求到看到第一个字）和每 token 间隔（TPOT）也在变差。把并发堆到 512 时，吞吐可能是最高的，可每个人要等 10 秒才出第一个字，这个吞吐对产品没有意义。

**有效吞吐：只统计满足服务等级目标（SLO，service level objective）的请求。** 例如 SLO 定为 TTFT ≤ 500 ms 且 TPOT ≤ 50 ms：
- goodput = 每秒完成的、**两个条件都满足**的请求数（也可以按这些请求的 token 数算）。

**例子：**

| 并发 | 吞吐（请求/秒） | 满足 SLO 的比例 | goodput（请求/秒） |
|---|---|---|---|
| 16 | 8 | 100% | 8 |
| 64 | 20 | 95% | 19 |
| 256 | 30 | 40% | 12 |

吞吐最高的是 256 并发，但 goodput 最高的是 64 并发。容量规划应按 goodput，或者按"满足 SLO 比例 ≥ 99% 的最大负载"来定每台机器能接多少流量。

**用 `vllm bench serve` 测：**

```bash
vllm bench serve --model meta-llama/Llama-3.1-8B-Instruct \
  --dataset-name random --random-input-len 1024 --random-output-len 256 \
  --request-rate 10 --num-prompts 1000 \
  --goodput ttft:500 tpot:50 \
  --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,99
```

`--goodput` 的值以毫秒为单位，可选 `ttft`、`tpot`、`e2el`（端到端延迟）。输出结果会多出 "Request goodput" 一行。

**SLO 怎么定：** 按产品场景。对话产品常见要求是 TTFT 几百毫秒到 1–2 秒、TPOT 在 20–50 ms（每秒 20–50 个 token，快于阅读速度）；代码补全要更快；离线批处理只看吞吐。MLPerf Inference 的 Llama 2 70B 服务器场景用 TTFT ≤ 2 s、TPOT ≤ 200 ms，更严格的交互场景用 450 ms 和 40 ms。
