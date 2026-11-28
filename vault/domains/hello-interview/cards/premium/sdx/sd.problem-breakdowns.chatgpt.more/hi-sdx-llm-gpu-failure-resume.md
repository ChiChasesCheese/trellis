---
id: hi-sdx-llm-gpu-failure-resume
node: sd.problem-breakdowns.chatgpt.more
type: qa
step: 3
---
## Q
**GPU 节点宕机：续写而不是重来**｜补充 · ChatGPT · 追问

面试官：「用户的回答正在流式生成，已经输出了 300 个 token，承载这次生成的 GPU 节点宕机了。客户端断线重连的机制救不了它，因为生成本身没了。你是让用户重发一遍，还是能接着写？KV 缓存要不要复制到别的节点？」

## A
**结论。** 可以接着写，不用复制 KV 缓存。KV 缓存只是 token 序列的函数，丢了可以重算：新节点读取这次生成已经写入流的 300 个 token，把提示加这 300 个 token 一起重新预填充，然后从第 301 个继续。用户看到的文字是连续的。

**要点。**
- **为什么不复制缓存：** 每个在途会话约 0.65 GB，实时复制的带宽和显存代价远大于偶发宕机的损失。
- **续写的依据：** 流里已经发出去的 token 就是事实，新节点只需在它们之后采样，不需要和旧节点的采样一致。
- **抢占要幂等：** 用条件更新把这次运行从「运行中且心跳超时」抢给新节点，防止旧节点复活后和新节点同时写流。
- **成本：** 一次预填充，计算量按提示加已生成的长度算，前缀缓存命中时更便宜。
- **还没输出任何 token 时：** 直接重派，用户感觉不到。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<rect x="10" y="8" width="320" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker A 已向流写入 300 个 token</text>
<text x="170.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">然后崩溃</text>
<polyline points="170,44 170.0,55.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,62 166.8,55.0 173.2,55.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="62" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调度器条件抢占该 Run</text>
<text x="170.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">WHERE status=running 且心跳超时</text>
<polyline points="170,106 170.0,117.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,124 166.8,117.0 173.2,117.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="124" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker B 读取流里的 300 个 token</text>
<text x="170.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提示 + 这 300 个 token 重新预填充</text>
<polyline points="170,168 170.0,179.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,186 166.8,179.0 173.2,179.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="186" width="320" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="204.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从第 301 个 token 继续生成</text>
<text x="170.0" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">客户端看到的文字是连续的</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">KV 缓存只是 token 序列的函数，</text>
<text x="8" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">丢了可以重算，不必跨节点复制。</text>
</svg>

**为什么。** 重连机制处理的是「客户端没了」，生成还在；GPU 节点宕机是「生成没了」。后者能恢复，是因为生成的状态可以由已发出的文本重建，而不是靠保存显存里的状态。

**面试里这样说。** 「节点宕机我不让用户重发：流里已有的 token 是事实，新节点把提示加这些 token 重新预填充，从下一个 token 接着生成。KV 缓存不复制，太贵，也没必要；用条件更新抢占运行，防止旧节点复活后双写。」

**易错。**
- **从头重新生成再续到同一条流：** 采样有随机性，新旧文字拼在一起会乱。
- **复制所有在途会话的缓存：** 为了偶发故障付持续的代价。
- **不防双写：** 旧节点只是网络隔离，恢复后继续往流里写。
