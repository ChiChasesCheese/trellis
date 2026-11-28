---
id: lct-learn-graph-9
node: graph.9
type: qa
step: 1
---
## Q
**图论算法 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 两两关系里的淘汰赛：每问一次必定淘汰一个人，`n - 1` 次得到唯一候选，再完整验证候选。

下图：LC 277 的淘汰赛，候选人一路往后换。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="40" y="40" width="52" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="66.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="92" y="40" width="52" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="118.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="144" y="40" width="52" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="196" y="40" width="52" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="248" y="40" width="52" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<path d="M 66.0 40 Q 117.0 10 168.0 40" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="168.0,40.0 161.3,38.1 165.2,33.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="117.0" y="22.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 认识 2：cand = 2</text>
<text x="170" y="92" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">knows(cand, i)：cand 不是名人，换成 i</text>
<text x="170" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">否则 i 不是名人；每问一次淘汰一人</text>
<text x="170" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">n - 1 次后剩唯一候选，再完整验证一遍</text>
</svg>

```python
def find_celebrity(n):
    cand = 0
    for i in range(1, n):
        if knows(cand, i):           # cand 认识 i：cand 不是名人
            cand = i
    for i in range(n):               # 验证：人人认识他，他谁也不认识
        if i == cand:
            continue
        if knows(cand, i) or not knows(i, cand):
            return -1
    return cand
```

**要点。**
- 为什么对？：`knows(a, b)` 为真则 `a` 不可能是名人，为假则 `b` 不可能是名人，每次问一个人出局；剩下的候选只是「没被淘汰」，仍要验证。
- LC 997 怎么改？：不用 `knows`，直接数每个人的入度和出度，名人（法官）是入度 `n - 1`、出度 `0` 的人。

**易错点。**
- 只验证一个方向：`[[1,1,1],[1,1,0],[1,1,1]]` 里 `1` 认识 `0`，得 `1`，应为 `-1`。
- 候选人不验证就返回：`[[1,0,1],[1,1,0],[0,1,1]]` 会返回 `2`，应为 `-1`。
- 验证时问 `knows(cand, cand)`：`graph[i][i] = 1` 会误判为认识别人。

**对应题目。** LC 277 搜寻名人
