---
id: lct-learn-data-structures-5-6
node: data-structures.5.6
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 懒删除堆**｜学习卡

套路是什么？

## A
**一句话。** `heapq` 只能弹堆顶，要删任意元素就先不删：记账说明「这个值要删」，等它浮到堆顶时才真正弹掉，删除变成 `O(1)` 记账加均摊 `O(log n)` 清理。

下图：删除只记账；真正的弹出推迟到被标记的值浮到堆顶时。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="40.7" y="17.5" width="78.6" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="34.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">remove(x)</text>
<rect x="36.6" y="65.0" width="86.8" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">rm[x] += 1</text>
<text x="80" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只记账 O(1)</text>
<rect x="196.8" y="17.5" width="106.5" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="34.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">top() / pop()</text>
<polygon points="186.1,85.0 195.1,72.5 304.9,72.5 313.9,85.0 304.9,97.5 195.1,97.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="89.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆顶在 rm 里欠着？</text>
<rect x="198.7" y="125.0" width="102.6" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="250" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">rm[堆顶] -= 1</text>
<text x="250" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">真正弹掉</text>
<rect x="218.0" y="182.5" width="64" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="199.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回堆顶</text>
<path d="M 80.0 42.5 L 80.0 65.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,65.0 77.0,58.7 83.0,58.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 250.0 42.5 L 250.0 72.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,72.5 247.0,66.2 253.0,66.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 250.0 97.5 L 250.0 125.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,125.0 247.0,118.7 253.0,118.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="258.0" y="115.2" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 198.7 145.0 L 170.0 145.0 L 170.0 85.0 L 186.1 85.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="186.1,85.0 179.8,88.0 179.8,82.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 313.9 85.0 L 332.0 85.0 L 332.0 195.0 L 282.0 195.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,195.0 288.3,192.0 288.3,198.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="322" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 123.4 85.0 L 186.1 85.0" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="186.1,85.0 179.8,88.0 179.8,82.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
</svg>

```python
class LazyHeap:
    def __init__(self):
        self.h = []
        self.rm = defaultdict(int)   # 每个值还欠几次删除
    def push(self, x):
        heappush(self.h, x)
    def remove(self, x):             # 懒删除：只记账
        self.rm[x] += 1
    def _clean(self):                # 堆顶若已被标记就真弹掉
        while self.h and self.rm[self.h[0]] > 0:
            self.rm[self.h[0]] -= 1
            heappop(self.h)
    def top(self):
        self._clean()
        return self.h[0]
    def pop(self):
        self._clean()
        return heappop(self.h)
```

**要点。**
- 为什么对？：被删的元素只要不在堆顶就不影响最小值；一到堆顶，`_clean` 马上清掉，所以每次 `top / pop` 看到的都是真正的最小有效元素；每个元素最多入堆、出堆一次。
- LC 3408 怎么改？：同一任务会改优先级，按值计数不够用：堆里放 `(-优先级, -taskId)`，另用字典记每个任务的当前状态，弹出时若任务已删除或优先级对不上就丢弃。
- 要最大堆怎么改？：存相反数，或把键取负。
- 元素个数怎么办？：另外维护 `size`，`push` 加一、`remove` 减一，不能用 `len(h)`。

**易错点。**
- `remove` 一个不在堆里的值：计数会残留，之后同值入堆会被误删，调用前必须保证它在堆里。
- 只校验任务还在、不比较优先级：`edit` 后旧条目仍被当作有效，会错误地先执行旧优先级。
- 用 `len(h)` 判空：堆里还有待清理的过期条目，应先 `_clean` 再看。

**对应题目。** LC 3408 设计任务管理器
