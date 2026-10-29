---
id: uth-java-arraylist-arraydeque-1-arraylist
node: java.arraylist-arraydeque
type: qa
step: 1
---
## Q
**ArrayList 怎么扩容**｜Java · OpenJDK 25

`new ArrayList<>()` 一路 `add`，底层数组的长度依次是多少？

## A
**背景。** 想按下标秒取，又要随时往后添加：数据得放在一整块连续内存里，可这一块放满后没法原地变大，只能搬到更大的新块，复制全部旧数据。如果每加一个就搬一次，太贵；所以搬家时多要一些空位。

**结构。** 一个 `Object[] elementData` 加一个 `size`；满了就 `Arrays.copyOf` 到更大的新数组。例：容量 10 的数组放满，再 `add` 一个，搬进容量 15 的新数组（复制 10 个），之后 5 次 `add` 都不用搬。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="20" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧数组 容量 10 已满</text>
<rect x="20" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="30" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="40" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="60" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="70" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="80" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="90" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="100" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="110" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="120" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="140" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="150" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="160" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="180" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="190" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="200" y="28" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="210" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<line x1="120" y1="56" x2="120" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,96.0 117.0,90.0 123.0,90.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">add 第 11 个 复制 10 个</text>
<text x="20" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新数组 容量 15 = 10 + 10&gt;&gt;1</text>
<rect x="20" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="30" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="40" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="60" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="70" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="80" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="90" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="100" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="110" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="120" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="140" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="150" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="160" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="180" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="190" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="200" y="120" width="20" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="210" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="220" y="120" width="20" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="230" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="240" y="120" width="20" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="260" y="120" width="20" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="280" y="120" width="20" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="300" y="120" width="20" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接下来 4 次 add 都不用搬</text>
</svg>
```

**细节。**

- 无参构造先共用一个空数组，第一次 `add` 才分配 10。
- 新容量 = 旧容量 + 旧容量 >> 1，即约 1.5 倍；实测依次是 `10 15 22 33 49 73 109 163 244`。
- `new ArrayList<>(n)` 或 `ensureCapacity(n)` 可预先分配，批量添加时省掉中间的多次复制。

**为什么。** 按比例增长，偶尔一次搬家摊到许多次 `add` 上，平均每次是常数时间（均摊 O(1)）；1.5 倍比 2 倍少浪费内存。CPython 的 `list` 更省，只多留约 12.5%。

**例题：** LC 1472 设计浏览器历史记录

实现 `BrowserHistory`：`visit(url)` 访问新页面并清空所有能前进到的记录；`back(steps)`、`forward(steps)` 最多后退或前进 `steps` 步，返回当前页面。

```python
class BrowserHistory:
    def __init__(self, homepage: str) -> None:
        self.history: list[str] = [homepage]
        self.cursor = 0

    def visit(self, url: str) -> None:
        del self.history[self.cursor + 1:]
        self.history.append(url)
        self.cursor += 1

    def back(self, steps: int) -> str:
        self.cursor = max(0, self.cursor - steps)
        return self.history[self.cursor]

    def forward(self, steps: int) -> str:
        self.cursor = min(len(self.history) - 1, self.cursor + steps)
        return self.history[self.cursor]
```
