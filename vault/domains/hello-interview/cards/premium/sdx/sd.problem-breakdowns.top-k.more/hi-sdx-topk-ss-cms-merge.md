---
id: hi-sdx-topk-ss-cms-merge
node: sd.problem-breakdowns.top-k.more
type: qa
step: 1
---
## Q
**分片后怎么合并近似 Top K**｜补充 · YouTube 热门 Top K · 追问

面试官：「某个国家的流量太大，一个节点放不下，只好再分给 8 个子分片，子分片里的视频有大量重叠。每个子分片各出一个局部 Top K，直接取并集或截断，为什么会错？为什么常常同时用 Space-Saving 和 Count-Min Sketch？」

## A
**结论。** 一个视频可能在 8 个子分片上都只算中等热门，进不了任何一个局部 Top K，但合计很大，并集或截断会悄悄丢掉它。正确的合并分两步：取各子分片 Space-Saving 候选集的并集，再把各子分片的 Count-Min Sketch 逐格相加，用合并后的草图给每个候选打分排名。Space-Saving 负责「谁值得问」，CMS 负责「合并后各是多少」。

**要点。**
- **局部 Top K 会漏：** 每个子分片只看到一部分流量，真正的总冠军可能在每片都排不进前几。
- **候选集取并集：** 全局出现次数超过 εN 的视频，至少在某个子分片上超过 ε 乘以该分片的流量（否则各片之和也不会超过 εN），所以必在那个子分片的候选集里，并集是安全的超集。
- **CMS 逐格相加：** 更新规则是线性的，几张宽度、深度、哈希种子都相同的草图逐格相加，结果和直接对合并后的流建一张草图一样，估计值仍然只偏大不偏小。
- **互补：** CMS 只能回答「某个已知的 ID 有多少」，列不出哪些 ID 高频；Space-Saving 能枚举高频候选，但直接把计数相加并不保持它的保证，专门的合并做法也比 CMS 的逐格相加复杂。
- **流程：** 候选并集 → 对每个候选查合并后的 CMS → 按估计值排序取前 K。

**为什么。** 合并的正确性靠两个性质：候选集合并后仍然是安全的超集，计数合并后仍然是带界的估计。两个结构各管一个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="20" y="10" width="300" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8 个子分片</text>
<text x="170" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各有一个 Space-Saving 和一张 CMS</text>
<rect x="20" y="92" width="140" height="48" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="90" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">候选 ID 并集</text>
<text x="90" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">安全的超集</text>
<rect x="180" y="92" width="140" height="48" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CMS 逐格相加</text>
<text x="250" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可合并的计数</text>
<rect x="20" y="184" width="300" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="200.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查每个候选的合并计数</text>
<text x="170" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">排序取前 K</text>
<polyline points="90,50 90,92" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="90,92 86.8,85.0 93.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="250,50 250,92" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="250,92 246.8,85.0 253.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="90,140 90,184" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,184 86.8,177.0 93.2,177.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="250,140 250,184" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,184 246.8,177.0 253.2,177.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>

**面试里这样说。** 「子分片有重叠，不能合并局部 Top K。我取各子分片 Space-Saving 候选 ID 的并集，保证不漏；再把各子分片的 CMS 逐格相加，得到合并后的计数，对每个候选查一遍再排序。CMS 负责可合并的计数，Space-Saving 负责找出候选。」

**易错。**
- **并集或截断局部 Top K：** 在各子分片都排不进前几的视频被漏掉。
- **草图参数不一致：** 宽度、深度或哈希种子不同的 CMS 不能逐格相加。
