---
id: bagu-consensus-1-raft-paxos-zab
node: b.distributed.consensus
type: qa
step: 1
---
## Q
**共识算法 · Raft 选主与日志复制，对比 Paxos、ZAB**｜加分

面试官：「Raft 怎么选主、怎么复制日志？它和 Paxos、ZAB 有什么区别？」

## A
**基本回答。** Raft 的节点分 Leader、Follower、Candidate。Follower 在选举超时内收不到心跳，就把任期号（term）加 1、变成 Candidate，向所有节点发 RequestVote，拿到多数票（N/2+1）当选；超时时间随机，避免同时参选而平票。写请求由 Leader 追加日志，复制到多数节点后提交，再应用到状态机。对比 Multi-Paxos：它允许乱序提交、有日志空洞，活锁（提议者互相打断）要另加退避，实现难；Raft 内置随机超时，更易实现，etcd、Consul、TiKV 都用它。ZAB 同样单主加任期（epoch）加过半确认，侧重按序原子广播。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 292">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">选主：5 个节点，多数 = 3</text>
<rect x="6" y="26" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Follower</text>
<rect x="128" y="26" width="84" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Candidate</text>
<rect x="250" y="26" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Leader</text>
<line x1="90" y1="40" x2="126" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,40.0 119.0,43.2 119.0,36.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="212" y1="40" x2="248" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="248.0,40.0 241.0,43.2 241.0,36.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 收不到心跳，超时 → term+1，发 RequestVote</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 拿到多数票（≥3）→ 成为 Leader</text>
<text x="8" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">日志复制：第 4 条写入</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Leader</text>
<rect x="72" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="162" y="122" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="175.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">F1</text>
<rect x="72" y="150" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="150" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="150" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="162" y="150" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="175.0" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">F2</text>
<rect x="72" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="162" y="178" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="175.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">F3</text>
<rect x="72" y="206" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="206" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="132" y="206" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">F4</text>
<rect x="72" y="234" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="249.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="234" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="249.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="200" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 4 条已在 3 个节点</text>
<text x="200" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">过半 → 提交 ✓</text>
<text x="200" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F3、F4 慢一点，</text>
<text x="200" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之后由 Leader 补齐</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有 Leader 接写；提交 = 复制到多数</text>
</svg>
上半部分是选主：Follower 超时变成 Candidate，拿到多数票成为 Leader。下半部分是复制日志：第 4 条在 Leader 和两个 Follower 上都有，共 3 份，过半，所以提交；F3、F4 慢了，之后补齐。
**容易错。**
- **以为 Leader 把日志发出去就算提交：** 要复制到多数节点才提交。
- **以为旧任期的日志数够了多数就能提交：** 它可能被新 Leader 覆盖，只通过数副本提交当前任期的日志。
- **以为少数派分区还能写：** 凑不齐多数，既选不出主也提交不了。
- **把 Gossip 当共识：** 节点随机互相交换数据，约 O(log N) 轮传遍全网，只保证最终一致，用于成员和故障探测（Redis Cluster 传节点状态），不用于强一致写。
- **把拜占庭容错和崩溃容错混为一谈：** 崩溃容错下 2f+1 个节点容忍 f 个宕机；拜占庭还要防节点撒谎，成本高，多见于区块链。
**举个例子。** 5 个节点，S1 是任期 3 的 Leader 并宕机：S2 超时最短，任期加到 4 变 Candidate，S3、S4 检查它的日志不比自己旧各投一票，加自己 3 票达到多数，当选。写入时 S2 追加日志发给其余节点，S3、S4 确认，共 3 份过半就提交；S5 慢了之后补齐。若 S2、S3 被分到一边只剩 2 个节点，凑不出 3 票，选不出主也提交不了写。
