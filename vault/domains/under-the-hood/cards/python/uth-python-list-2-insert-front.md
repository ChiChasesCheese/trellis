---
id: uth-python-list-2-insert-front
node: python.list
type: qa
step: 2
---
## Q
**insert(0) 和 pop(0) 为什么慢**｜Python · CPython 3.14

在 100 万元素的 `list` 头部 `insert(0, x)` 再 `pop(0)`，比在尾部 `append` 再 `pop` 慢多少？

## A
**背景。** 连续的格子只在末尾留有空位。往头部插一个，就得让后面所有元素都往后让一格；`pop(0)` 则要让后面所有元素往前补一格。

**结构。** `insert(0)` 把后面所有指针逐个后移一格；`pop(0)` 用一次 `memmove`（整块内存一口气搬）前移一格。都是 O(n)。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="20" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">insert(0, x)</text>
<rect x="40" y="30" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="60" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="60" y1="56" x2="100" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100.0,92.0 94.6,90.5 98.0,86.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="80" y="30" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="100" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="100" y1="56" x2="140" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="140.0,92.0 134.6,90.5 138.0,86.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="120" y="30" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="140" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="140" y1="56" x2="180" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180.0,92.0 174.6,90.5 178.0,86.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="160" y="30" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="180" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<line x1="180" y1="56" x2="220" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="220.0,92.0 214.6,90.5 218.0,86.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="200" y="30" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<line x1="220" y1="56" x2="260" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260.0,92.0 254.6,90.5 258.0,86.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="240" y="30" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="40" y="94" width="40" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="60" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x</text>
<rect x="80" y="94" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="100" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="120" y="94" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="140" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="160" y="94" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="180" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="200" y="94" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="240" y="94" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后面的指针全部后移一格</text>
<text x="20" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">append(x)</text>
<rect x="40" y="180" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="60" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="80" y="180" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="100" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="120" y="180" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="140" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="160" y="180" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="180" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="200" y="180" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="240" y="180" width="40" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x</text>
<text x="170" y="226" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只写末尾一格</text>
</svg>
```

**细节。** 本机实测（100 万元素）：

```
insert(0)+pop(0)  约 226 微秒
append+pop        约 0.023 微秒
```

**为什么。** 连续数组换来 O(1) 的按下标取值和紧凑内存，代价是头部操作线性。两端都要频繁操作就换 `collections.deque`。

**例题：** LC 232 用栈实现队列

只用两个栈实现先进先出队列，支持 `push`、`pop`、`peek`、`empty`；进阶：每个操作均摊 O(1)。例：`push(1)`、`push(2)`、`peek()` 得 `1`、`pop()` 得 `1`、`empty()` 得 `False`。

```python
class MyQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []        # 只负责 push：新元素压在栈顶
        self.outbox: list[int] = []       # 只负责 pop / peek：栈顶就是队首

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _move(self) -> None:
        if not self.outbox:               # 只有 outbox 空了才倒，倒的时候整个 inbox 一次倒完
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._move()
        return self.outbox.pop()

    def peek(self) -> int:
        self._move()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```
