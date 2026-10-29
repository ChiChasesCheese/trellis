---
id: uth-compose-indexed-heap-2-structures
node: compose.indexed-heap
type: qa
step: 2
---
## Q
**组合：堆数组 + 下标表**｜Java ScheduledThreadPoolExecutor · JDK 21

要让取消和改期也是 O(log n)，该给堆配什么结构？每个操作碰哪几个结构？

## A
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<line x1="157.3" y1="30.0" x2="112.7" y2="58.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="182.7" y1="30.0" x2="227.3" y2="58.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="89.9" y1="77.1" x2="70.1" y2="98.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="110.1" y1="77.1" x2="129.9" y2="98.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="240.0" y1="81.0" x2="240.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="22" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor"/>
<text x="170" y="26.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a:1</text>
<circle cx="100" cy="66" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="100" y="70.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b:3</text>
<circle cx="240" cy="66" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor"/>
<text x="240" y="70.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c:2</text>
<circle cx="60" cy="110" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor"/>
<text x="60" y="114.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d:7</text>
<circle cx="140" cy="110" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor"/>
<text x="140" y="114.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e:5</text>
<circle cx="240" cy="110" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor"/>
<text x="240" y="114.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f:9</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标</text>
<text x="8" y="167" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">堆数组</text>
<text x="71" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="50" y="150" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="71" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a:1</text>
<text x="113" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="92" y="150" width="42" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="113" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b:3</text>
<text x="155" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="150" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="155" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c:2</text>
<text x="197" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="176" y="150" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="197" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d:7</text>
<text x="239" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="218" y="150" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="239" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e:5</text>
<text x="281" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="260" y="150" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="281" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f:9</text>
<text x="8" y="225" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pos 表</text>
<rect x="50" y="208" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3" fill="none"/>
<text x="71" y="225.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a:0</text>
<rect x="92" y="208" width="42" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="113" y="225.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b:1</text>
<rect x="134" y="208" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3" fill="none"/>
<text x="155" y="225.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c:2</text>
<rect x="176" y="208" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3" fill="none"/>
<text x="197" y="225.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d:3</text>
<rect x="218" y="208" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3" fill="none"/>
<text x="239" y="225.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e:4</text>
<rect x="260" y="208" width="42" height="26" rx="3" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3" fill="none"/>
<text x="281" y="225.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f:5</text>
<line x1="113" y1="208" x2="113.0" y2="184.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="113,178 116.0,184.0 110.0,184.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="121" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 key 查到下标</text>
</svg>
```

**结构。** 两个结构互相指：堆数组存元素，`pos` 表存「key → 它在数组里的下标」。有了下标，取消和改期就从「找人」变成「直接去那一格修」。

**细节。**

- 上浮（sift up）：和父节点交换，直到不比父小；下沉（sift down）：和较小的孩子交换，直到不比孩子大。
- 删除：先和末尾元素交换，删掉末尾，再让换来的元素上浮或下沉；改期：原地改值，再上浮或下沉。换来的元素可能比父小，也可能比孩子大，两个方向都试，只会发生其中一个。

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `push(key, p)` | 数组末尾追加后上浮，`pos` 记下标 | O(log n) |
| `pop()` | 取 `a[0]`，换到末尾删掉，下沉；`pos` 删 key | O(log n) |
| `remove(key)` | 查 `pos` 得下标，换到末尾删掉，上浮或下沉 | O(log n) |
| `update(key, p)` | 查 `pos` 得下标，改值，上浮或下沉 | O(log n) |

**对应 LeetCode：** 无直接对应的题
