---
id: uth-python-deque-ordereddict-2-index
node: python.deque-ordereddict
type: qa
step: 2
---
## Q
**deque 的中间下标有多慢**｜Python · CPython 3.14

在 100 万元素的 `deque` 上取 `d[500000]`，比 `list` 慢多少？`deque(maxlen=3)` 又有什么用？

## A
**背景。** `list` 取第 i 个是一次地址计算。`deque` 的块在内存里是用指针串起来的，没法直接算出第 i 个在哪一块。

**结构。** 按下标取元素要从离目标近的那一端，沿块链表一块块数过去，每块 64 个。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d[k] 要沿链表数块</text>
<rect x="10" y="30" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="58" y1="44" x2="78" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,44.0 74.0,46.0 74.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="58.0,44.0 62.0,42.0 62.0,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="78" y="30" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="126" y1="44" x2="146" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146.0,44.0 142.0,46.0 142.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="126.0,44.0 130.0,42.0 130.0,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="146" y="30" width="48" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<line x1="194" y1="44" x2="214" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214.0,44.0 210.0,46.0 210.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="194.0,44.0 198.0,42.0 198.0,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="214" y="30" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="262" y1="44" x2="282" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,44.0 278.0,46.0 278.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="262.0,44.0 266.0,42.0 266.0,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="282" y="30" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d[0] 快</text>
<text x="306" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d[-1] 快</text>
<text x="170" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d[500000] 慢</text>
<path d="M 34 28 Q 90 6 146 28" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="146.0,28.0 139.3,28.7 141.4,23.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 306 28 Q 250 6 194 28" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="194.0,28.0 198.6,23.1 200.7,28.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">deque(maxlen=3)</text>
<rect x="105" y="124" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="139" y="124" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="156" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="173" y="124" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="190" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="36" y="124" width="22" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="47" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="58" y="124" width="22" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="69" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="80" y="124" width="22" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="91" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="215" y1="137" x2="262" y2="137" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,137.0 256.0,140.0 256.0,134.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="300" y="141" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">append(5)</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">满了 append 会从另一端丢弃</text>
</svg>
```

**细节。**

- 实测：`d[0]`、`d[-1]` 约 0.02 微秒，`d[500000]` 约 20 微秒；`list` 任何下标都是 0.018 微秒。
- 所以中间下标是 O(n)，不要拿 `deque` 当随机访问数组。
- `maxlen=3` 时，满了再 `append` 会从另一端自动丢弃，实测 `0..5` 依次放入后剩 `[3, 4, 5]`。

**为什么。** 链表块换来了两端的 O(1) 和无搬移，中间随机访问就让位了。

**例题：** LC 994 腐烂的橘子

网格里 `0` 是空格、`1` 是新鲜橘子、`2` 是腐烂橘子。每分钟，腐烂橘子上下左右相邻的新鲜橘子都会腐烂。返回全部腐烂所需的最少分钟数，不可能就返回 `-1`。例：`[[2,1,1],[1,1,0],[0,1,1]]` 返回 `4`。

```python
from collections import deque

def oranges_rotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):  # 只处理当前这一分钟已腐烂的橘子
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return minutes if fresh == 0 else -1
```
