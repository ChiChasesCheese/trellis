---
id: hi-sdx-llm-prefill-decode-split
node: sd.problem-breakdowns.chatgpt.more
type: qa
step: 4
---
## Q
**预填充与解码分开部署**｜补充 · ChatGPT · 加分

面试官：「同一批 GPU 上既做预填充又做解码。有人往对话里贴了一篇长文，其他人的流式输出就明显卡顿。为什么？有什么架构可以避免，代价是什么？」

## A
**结论。** 预填充一次并行处理整个提示，受算力限制；解码一次只出一个 token，受显存带宽限制。长提示的预填充会占住算力，让同批 GPU 上其他会话的解码步延迟。办法是把两个阶段放到不同的 GPU 池，预填充完成后把 KV 缓存传给解码池。

**要点。**
- **两个阶段瓶颈相反：** 混在一起时，一个长提示的预填充让同批所有会话的下一个 token 等待，表现为输出突然停顿。
- **分开部署：** 预填充池按提示吞吐配置，解码池按并发会话和显存配置，各自调到自己的瓶颈。
- **传输代价：** 2000 token 的缓存约 0.65 GB；100 Gb/s 以太网约 52 ms，400 Gb/s 互联约 13 ms，所以要高速互联。
- **效果：** 已发表的评测在首 token 和每 token 延迟都有目标的条件下报告：同样的约束可多服务最多 7.4 倍请求，或延迟目标收紧到 12.6 倍。
- **更轻的办法：** 分块预填充，把长提示切块，与别人的解码步混合调度，不用传缓存。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="10" y="8" width="320" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长提示进入</text>
<text x="170.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">prompt 2000 token</text>
<polyline points="170,44 170.0,55.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,62 166.8,55.0 173.2,55.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="62" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">预填充池 prefill</text>
<text x="170.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一次并行算完整个提示，计算受限</text>
<polyline points="170,106 170.0,127.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,134 166.8,127.0 173.2,127.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">传 KV 缓存 ≈ 0.65 GB</text>
<rect x="10" y="134" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">解码池 decode</text>
<text x="170.0" y="167.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐 token 生成，显存带宽受限</text>
<polyline points="170,178 170.0,189.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,196 166.8,189.0 173.2,189.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="196" width="320" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="214.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">token 流给用户</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长提示的预填充不再挤占别人的解码步。</text>
</svg>

**为什么。** 把互相干扰的两种负载分开，就能分别扩缩和选型。代价是多一次缓存传输、要给两个池定比例，池子不平衡时有一边闲着，系统更复杂。

**面试里这样说。** 「预填充算力受限、解码带宽受限，长提示的预填充会拖慢同批的其他流。先用分块预填充；规模大到要保严格延迟目标时，把预填充和解码拆成两个池，缓存走高速互联传过去。代价是传输、池子比例和复杂度。」

**易错。**
- **一上来就拆池：** 小规模下分块预填充已经够用。
- **忽略缓存传输：** 慢网络下传输吃掉了分离的收益。
- **两个池按同一比例固定：** 提示长度分布变了，一边会饿死。
