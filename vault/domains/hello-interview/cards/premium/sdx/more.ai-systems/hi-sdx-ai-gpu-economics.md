---
id: hi-sdx-ai-gpu-economics
node: more.ai-systems
type: qa
step: 3
---
## Q
**GPU 利用率 100% 却贵 5 倍**｜补充 · AI 系统 · 追问

面试官：「nvidia-smi 显示 GPU 利用率 100%，可每百万 token 的成本是竞品的 5 倍。这个指标为什么会骗人？应该看什么？降本的杠杆按什么顺序用？」

## A
**结论。** nvidia-smi 的利用率只表示「有内核在跑」，等显存读数据的 GPU 也算忙。小批量解码常显示 100%，实际算力利用不到 10%。要看每卡每秒 token 数换算成每百万 token 成本、MFU 和满足延迟目标下的有效吞吐（goodput）。杠杆顺序：先填满批，再量化，最后优化内核。

**要点。**
- **为什么骗人：** 解码受显存带宽限制，每步都要读全部权重；批量小时算力大部分空闲。
- **算一笔账：** 假设 700 亿参数、FP16，8 张 H100（每卡显存带宽约 3.35 TB/s、稠密 FP16 峰值约 989 TFLOPS、租价每卡每小时 2 美元），忽略 KV 缓存读取：每步读 140 GB 权重约 5.2 毫秒，批量为 1 时 MFU 只有 0.3%，批量 64 时约 22%，同样一步读权重换来 64 倍 token，每百万 token 成本约低 64 倍。
- **该看的指标：** 每卡 token/秒与每百万 token 成本；MFU（有效算力除以峰值）；goodput，即满足延迟目标时的吞吐。
- **批量的限制：** 批越大，单个 token 间隔越长，并受 KV 缓存显存限制，所以容量规划看 goodput。
- **2026 亮点：** 大规模推理会把 prefill 和 decode 拆成两个池（Disaggregated Serving）：prefill 吃算力、decode 吃显存带宽，混跑会互相拖尾延迟；拆开后按 TTFT 和 TPOT 目标分别配副本，用 goodput（满足延迟目标的请求率除以 GPU 数）衡量。代价是要跨节点传 KV cache（需要 RDMA 级网络）、多一层调度，而且不提升总吞吐；短 prompt 或低流量不值得，先用 chunked prefill 调 max_num_batched_tokens 平衡 TTFT 和 token 间延迟。
- **降本顺序：** 先填满批（流量问题先于内核问题），再量化权重与 KV 缓存，再小模型路由、前缀缓存、推测解码；流式只改善感知延迟，不降成本。

**为什么。** 成本由「每次读权重服务了多少个 token」决定。利用率指标看不到这一点，所以要用吞吐和成本直接衡量。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8×H100 · 70B · FP16（理想化估算）</text>
<text x="8" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每步读一遍权重，MFU 随批量上升</text>
<text x="4" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">批量 1</text>
<rect x="70" y="56" width="3" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="79" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">0.3%</text>
<text x="70" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每百万 token 约 $23.2</text>
<text x="4" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">批量 16</text>
<rect x="70" y="108" width="43.2" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="119.2" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5.4%</text>
<text x="70" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每百万 token 约 $1.45</text>
<text x="4" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">批量 64</text>
<rect x="70" y="160" width="173.6" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="249.6" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">21.7%</text>
<text x="70" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每百万 token 约 $0.36</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">nvidia-smi 三行都显示 100%</text>
</svg>

**面试里这样说。** 「nvidia-smi 的利用率不能当效率，我看每卡 token 每秒和每百万 token 成本，再看 MFU 和满足延迟目标的有效吞吐。先把批填满，再量化，最后才去优化内核。」

**易错。**
- **用 nvidia-smi 做容量规划：** 显示 100% 实际远没跑满。
- **只追求吞吐：** 批太大让每 token 延迟违反目标，应看 goodput。
- **一上来优化内核：** 批填不满的流量问题，内核优化救不了。
