---
id: hi-sdx-zk-prevote
node: sd.deep-dives.zookeeper.more
type: qa
step: 3
---
## Q
**Raft 节点被隔离再回来，为何会搅乱 leader**｜补充 · ZooKeeper · 追问

面试官：「一个 Raft 节点被不稳定的链路隔离，期间反复超时、不断增大任期号；链路恢复后，它的高任期号迫使健康的 leader 下台，明明什么都没出问题。标准的两个防御是什么？」

## A
**结论。** 预投票（pre-vote）和 leader 侧的法定人数检查（check-quorum）。原始 Raft 把任何更高的任期号都当作权威，一个抖动的节点就能反复废黜正常工作的 leader，每次都带来一次无谓的选举和短暂的写停顿。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<rect x="10" y="8" width="152" height="36" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="86.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有 pre-vote</text>
<rect x="178" y="8" width="152" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有 pre-vote</text>
<rect x="10" y="60" width="152" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">孤立节点反复超时</text>
<text x="86.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">任期号 5 加到 9</text>
<rect x="178" y="60" width="152" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先试探：有 leader</text>
<text x="254.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存活，试探失败</text>
<polyline points="86,108 86.0,119.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="86,126 82.8,119.0 89.2,119.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="254,108 254.0,119.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="254,126 250.8,119.0 257.2,119.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="126" width="152" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">链路恢复</text>
<text x="86.0" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">leader 看到任期 9</text>
<rect x="178" y="126" width="152" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任期号仍是 5</text>
<text x="254.0" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有被抬高</text>
<polyline points="86,174 86.0,185.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="86,192 82.8,185.0 89.2,185.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="254,174 254.0,185.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="254,192 250.8,185.0 257.2,185.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="192" width="152" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="212.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">健康 leader 下台</text>
<text x="86.0" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">白白重新选举</text>
<rect x="178" y="192" width="152" height="48" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="212.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">安静回归</text>
<text x="254.0" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作为 follower</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再配 check-quorum：联系不上多数的 leader 自己下台。</text>
</svg>

**要点。**
- **预投票：** 候选人在增加任期号之前先做一轮试探，问「如果我参选，你们会投给我吗」。对方只有在超时内没收到存活 leader 的消息时才回答是。被隔离的节点总是试探失败，任期号不会被抬高，恢复后安静地当 follower。
- **法定人数检查：** leader 在超时内联系不上多数节点，就自己下台。被困在少数派一侧的旧 leader 因此停止服务，这对基于租约的读尤其重要。
- **一句话：** 任期号保证安全，预投票和法定人数检查保证不稳定链路下的活性。

**面试里这样说。** 「生产里的 Raft 我会开预投票和 check-quorum：前者防止被隔离的节点抬高任期号搅乱 leader，后者让被孤立的 leader 主动下台，避免它继续服务旧数据。」

**易错。**
- **以为任期号越大越好：** 没有预投票时，一个孤立节点的大任期号会毁掉整个集群的稳定。
- **只开预投票不开 check-quorum：** 被隔离的旧 leader 可能继续响应租约读。
