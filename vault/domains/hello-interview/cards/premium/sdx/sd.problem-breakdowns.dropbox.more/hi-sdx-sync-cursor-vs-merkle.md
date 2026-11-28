---
id: hi-sdx-sync-cursor-vs-merkle
node: sd.problem-breakdowns.dropbox.more
type: qa
step: 1
---
## Q
**游标之外还要树对账**｜补充 · 文件存储（Dropbox） · 追问

面试官：「设备重连后只要拿上次的游标去拉变更日志就能追平，已经比逐个文件比对便宜得多。那还需要对比两边的目录树吗？游标日志能不能完全替代它？」

## A
**结论。** 不能替代。游标是日常的便宜追赶手段，再加一个低频的树对账（Merkle 树比较）作为正确性兜底，两者回答的是不同的问题。

**要点。**
- **游标回答：** 「服务端认为这个游标之后变了什么」，只比较日志位置，不比较真实状态。
- **它默认三件事成立：** 日志完整、设备把每一条都正确应用了、没有文件在同步之外被改动或损坏。
- **树对账回答：** 「两边现在是否一致」。目录哈希由子项哈希自底向上算出，根哈希相同就整棵树一致。
- **怎么定位差异：** 根不同就比较子节点，只下钻哈希不同的子树，代价约为差异数乘树的深度。
- **能抓到什么：** 漏掉的日志、没落地的变更、磁盘上被外部改坏的文件，这些游标都发现不了。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="95" y="8" width="150" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根 hash 不同</text>
<polyline points="130,42 90.9,66.3" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,70 89.3,63.6 92.6,69.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="210,42 249.1,66.3" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,70 247.4,69.0 250.7,63.6" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="70" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">/docs</text>
<text x="85.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash 相同，整棵跳过</text>
<rect x="180" y="70" width="150" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">/photos</text>
<text x="255.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash 不同，继续下钻</text>
<polyline points="215,104 176.1,126.5" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,130 174.5,123.7 177.7,129.3" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="295,104 298.7,123.1" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="300,130 295.5,123.7 301.8,122.5" style="fill:var(--accent,#3b6fd4)"/>
<rect x="100" y="130" width="100" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="150.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a.jpg</text>
<text x="150.0" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">相同</text>
<rect x="220" y="130" width="110" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="275.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b.jpg</text>
<text x="275.0" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不同，修复</text>
<text x="10" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">游标日志：只知道服务端日志里有什么</text>
<text x="10" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">树对账：直接比较两边「现在是否一致」</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只下钻不同的子树，代价约 差异数 × 深度</text>
</svg>

**为什么。** 日志位置只能证明「读到哪儿了」，不能证明「读到的都生效了」。要发现漂移，必须拿状态和状态比。

**面试里这样说。** 「日常我让设备带游标拉变更日志，成本最低。同时每天或发现异常时做一次 Merkle 树对账：先比根哈希，不同就只往哈希不同的子树下钻，能修复游标发现不了的漏应用和本地损坏。」

**易错。**
- **把游标当作完整保证：** 日志缺一条或本地写坏一个文件，设备会一直偏离而没人知道。
- **每次都全量比较目录树：** 代价和文件总数成正比，应当低频、且只在哈希不同时下钻。
- **只做树对账不做游标：** 每次同步都要计算整棵树的哈希，延迟和 CPU 都高。
