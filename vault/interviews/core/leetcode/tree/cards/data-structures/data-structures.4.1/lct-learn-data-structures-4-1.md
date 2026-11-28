---
id: lct-learn-data-structures-4-1
node: data-structures.4.1
type: qa
step: 1
---
## Q
**常用数据结构 › 队列 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 队列先进先出，只在队尾追加、队头弹出；凡是「只关心最近一段时间 / 最早进来的」，就把数据按时间顺序入队，查询前先从队头弹掉过期项。

下图：时间戳按序入队；查询前从队头弹掉窗口外的项。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="40" y="50" width="44" height="30" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="62" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="84" y="50" width="44" height="30" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="106" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="128" y="50" width="44" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">120</text>
<rect x="172" y="50" width="44" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="194" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">250</text>
<rect x="216" y="50" width="44" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="238" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">301</text>
<rect x="260" y="50" width="44" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">305</text>
<line x1="40" y1="65" x2="8" y2="65" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="8.0,65.0 14.3,62.0 14.3,68.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="20" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队头弹出</text>
<text x="20" y="113" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">≤ t-300</text>
<line x1="330" y1="65" x2="306" y2="65" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="306.0,65.0 312.3,62.0 312.3,68.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="310" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">队尾追加</text>
<line x1="128" y1="42" x2="128" y2="36" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="304" y1="42" x2="304" y2="36" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="128" y1="42" x2="304" y2="42" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="216.0" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查询 t = 305：窗口 (5, 305]</text>
<text x="172" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队头先弹过期项，剩下的个数就是答案</text>
</svg>

```python
class HitCounter:
    def __init__(self):
        self.q = deque()             # 时间戳递增

    def hit(self, t):
        self.q.append(t)             # 队尾入

    def get_hits(self, t):
        while self.q and self.q[0] <= t - 300:
            self.q.popleft()         # 队头出：超出 300 秒窗口
        return len(self.q)
```

**要点。**
- 为什么对？：时间戳单调不减，过期的一定在队头；每个元素最多入队、出队各一次，均摊 `O(1)`。
- 同一秒大量敲击怎么改？：队里存 `(时间, 次数)`，再维护一个总次数，空间随秒数而不是敲击数增长。
- 用 Python 注意什么？：不要用 `list.pop(0)`（`O(n)`），用 `collections.deque`。

**易错点。**
- 窗口边界：窗口是 `(t - 300, t]`，`t - 300` 本身已过期；`hit(1)` 后 `get_hits(300)` 应为 `1`，`get_hits(301)` 应为 `0`。
- 只在 `hit` 时弹出过期：之后很久才查询，队里仍有过期项，必须在 `get_hits` 里清理。

**对应题目。** LC 362 敲击计数器
