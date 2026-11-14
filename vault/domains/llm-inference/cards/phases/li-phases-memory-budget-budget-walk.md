---
id: li-phases-memory-budget-budget-walk
node: phases.memory-budget
type: qa
step: 1
---
## Q
一张加速卡的显存在推理时被哪几部分分走？以 Llama 3.1 8B 在 80 GB 显卡上为例，按顺序列出预算，并说明每一项受哪些参数控制。

## A
**显存（加速卡自带的高带宽内存）在推理时被五部分瓜分：**

| 项目 | 大约多少（8B，BF16） | 受什么控制 |
|---|---|---|
| 预留不用 | 8 GB | `--gpu-memory-utilization`（默认 0.9，留 10% 给其他进程和波动） |
| 权重 | 16 GB | 参数个数 × 每参数字节数（BF16 是 2 字节） |
| 中间结果峰值（激活值） | 1–3 GB | 一步最多处理多少 token（`--max-num-batched-tokens`） |
| CUDA Graph 和运行时开销 | 约 1 GB | 预先录制的批大小数量；CUDA 上下文本身约几百 MB |
| KV 缓存 | 剩下的约 52 GB | 每 token 字节数 × 能装的 token 数 |

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 122" font-family="sans-serif" font-size="11">
<text x="10" y="18" fill="currentColor">80 GB 显存（Llama 3.1 8B，BF16）</text>
<rect x="10" y="28" width="32" height="30" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<text x="26" y="47" text-anchor="middle" font-size="10" fill="currentColor">预留8</text>
<rect x="42" y="28" width="64" height="30" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<text x="74" y="47" text-anchor="middle" fill="currentColor">权重 16</text>
<rect x="106" y="28" width="8" height="30" stroke="currentColor" fill="currentColor" fill-opacity="0.2"/>
<rect x="114" y="28" width="4" height="30" stroke="currentColor" fill="currentColor" fill-opacity="0.2"/>
<rect x="118" y="28" width="208" height="30" fill="currentColor" fill-opacity="0.1" stroke="currentColor"/>
<text x="222" y="47" text-anchor="middle" fill="currentColor">KV 缓存 约 52 GB</text>
<line x1="112" y1="58" x2="112" y2="74" stroke="currentColor"/>
<text x="100" y="88" fill="currentColor">激活 1–3 GB + 运行时开销约 1 GB</text>
<text x="10" y="112" fill="currentColor">权重是固定成本；KV 缓存决定能服务多少人</text>
</svg>
```

**名词：**
- **激活值（activation）：** 前向计算过程中每层产生的临时结果。推理时用完即丢，所以只需按"一步里同时处理的 token 数"留出峰值空间，不像训练那样要全部保存。
- **KV 缓存：** 每个请求历史 token 在每层的键、值向量，常驻显存直到请求结束。
- **CUDA Graph：** 把一整步的大量 GPU 操作预先录成一张图，之后一次性提交，省掉逐个提交的开销，但每种批大小都要录一份，占一些显存。

**规律：** 权重是固定成本，KV 缓存是"能服务多少人"的可变容量。模型越大、卡越小，留给缓存的越少：70B 模型 BF16 权重 140 GB，放在两张 80 GB 卡上几乎不剩缓存空间，所以实际要用 4–8 张卡。

**调参的权衡：**
- 调高 `--gpu-memory-utilization` 到 0.95：缓存多约 4 GB，但同卡其他进程或显存波动可能导致内存不足（OOM）。
- 调大 `--max-num-batched-tokens`：长输入预填充更快，但激活峰值变大，缓存变少。
- 调小 `--max-model-len`（最大上下文长度）：不改变缓存总量，但启动检查更容易通过。
