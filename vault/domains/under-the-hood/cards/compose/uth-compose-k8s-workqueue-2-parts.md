---
id: uth-compose-k8s-workqueue-2-parts
node: compose.k8s-workqueue
type: qa
step: 2
---
## Q
**三个结构怎么搭**｜Kubernetes · client-go v0.37

workqueue 由哪三个结构搭成？`Add`、`Get`、`Done` 各碰哪几个？

## A
**结构。** 一个 `queue`（先进先出的 key 列表，只管顺序），两个 `set`（集合）：`dirty` 记"还欠一次处理"的 key，`processing` 记"正被 worker 处理"的 key。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="10" y="22" width="320" height="54" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="18" y="38" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">queue: 先进先出的 key 列表, 只管顺序</text>
<rect x="18" y="46" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="33.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="52" y="46" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="67.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="86" y="46" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="101.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<text x="130" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队头 Get 取走, 队尾 Add 放入</text>
<rect x="10" y="110" width="150" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="18" y="126" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">dirty 集合</text>
<text x="18" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还欠一次处理的 key</text>
<rect x="18" y="148" width="26" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="31.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="48" y="148" width="26" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="61.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="78" y="148" width="26" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="91.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="108" y="148" width="26" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"  stroke-width="1"/>
<text x="121.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="180" y="110" width="150" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="188" y="126" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">processing 集合</text>
<text x="188" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">正被 worker 处理的 key</text>
<rect x="188" y="148" width="26" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"  stroke-width="1"/>
<text x="201.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<line x1="60" y1="110" x2="60" y2="76" stroke="currentColor" stroke-width="1"/>
<polygon points="60,76 56,84 64,84" fill="currentColor"/>
<text x="68" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Add</text>
<line x1="215" y1="76" x2="215" y2="110" stroke="currentColor" stroke-width="1"/>
<polygon points="215,110 211,102 219,102" fill="currentColor"/>
<text x="223" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Get</text>
<line x1="300" y1="110" x2="300" y2="76" stroke="currentColor" stroke-width="1"/>
<polygon points="300,76 296,84 304,84" fill="currentColor"/>
<text x="294" y="98" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">Done</text>
<text x="10" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d 在两个集合里: 处理期间又被 Add</text>
<text x="10" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Add: 记入 dirty; 不在 processing 才入队</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Get: 出队, 进 processing, 从 dirty 删除</text>
<text x="10" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Done: 离开 processing; 仍在 dirty 就重新入队</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `Add(k)` | 查 `dirty`、插 `dirty`、查 `processing`，最后推 `queue` | O(1) |
| `Get()` | 弹 `queue`、插 `processing`、删 `dirty` | O(1) |
| `Done(k)` | 删 `processing`、查 `dirty`，必要时推 `queue` | O(1) |

**为什么。** 两个集合相当于两个开关，一个 key 恰好处在四种状态之一，连"处理中又变了"也能表示：

| 在 dirty | 在 processing | 含义 |
|---|---|---|
| 否 | 否 | 空闲 |
| 是 | 否 | 排队等待，在 `queue` 里 |
| 否 | 是 | 正在处理，期间没有新变化 |
| 是 | 是 | 正在处理，期间又被 `Add`：`Done` 时重新入队 |

**对应 LeetCode：** 无直接对应的题
