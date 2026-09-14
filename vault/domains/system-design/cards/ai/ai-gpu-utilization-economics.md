---
id: ai-gpu-utilization-economics
node: ai.inference
type: qa
---
## Q
`nvidia-smi` shows 100% GPU utilization but your cost per million tokens is 5x the competition. Why is that metric a lie, and what do you measure instead?

## A
`nvidia-smi` utilization = "a kernel was running" — a GPU stalled on memory reads counts as busy. Decode-heavy serving at small batch can show 100% while using **<10% of peak FLOPs** (it's bandwidth-bound, [[ai-prefill-vs-decode]]).

Measure economics directly:

- **Throughput per GPU**: tokens/sec/GPU → **$ per million tokens** (the number to benchmark against API pricing).
- **MFU** (model FLOPs utilization): useful-FLOPs ÷ peak — reveals headroom.
- **Goodput**: throughput *while meeting the latency SLO* — the real capacity-planning metric, since batch size trades inter-token latency for cheaper tokens ([[ai-continuous-batching]]).

Lever hierarchy: fill batches (utilization is a traffic problem before a kernel problem), then quantize, then optimize kernels.

## Q zh
`nvidia-smi` 显示 100% GPU 利用率但你的每百万 token 成本是竞争对手的 5 倍。为什么这个指标是骗人的，你应该测量什么？

## A zh
`nvidia-smi` 利用率 = "一个内核在运行" — GPU 在内存读上停滞计为忙。小批次的 decode 密集型服务可以显示 100% 同时使用 **<10% 的峰值 FLOP**（它是带宽限制的，[[ai-prefill-vs-decode]]）。

直接测量经济学：

- **每 GPU 吞吐量**：tokens/sec/GPU → **每百万 token 美元**（与 API 定价对标的数字）。
- **MFU**（模型 FLOP 利用率）：有用 FLOP ÷ 峰值 — 揭示余量。
- **Goodput**：在 *满足延迟 SLO 时* 的吞吐量 — 真正的容量规划指标，因为批大小在 token 间延迟和更廉价的 token 之间权衡（[[ai-continuous-batching]]）。

杠杆层级：填充批次（利用率是流量问题而不是内核问题），然后量化，然后优化内核。
