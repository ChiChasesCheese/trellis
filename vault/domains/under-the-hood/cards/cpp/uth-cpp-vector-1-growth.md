---
id: uth-cpp-vector-1-growth
node: cpp.vector
type: qa
step: 1
---
## Q
**push_back 为什么是均摊 O(1)**｜C++ · libstdc++ / libc++ / MSVC

`std::vector` 连续 `push_back` 时，容量是怎样增长的？

## A
**背景。** 数组要连续才能按下标快速访问，所以满了不能原地接长，只能新开一块更大的，把旧元素搬过去。每次只多开 1 格，插入 n 个元素要搬约 n²/2 次；每次翻倍就划算得多。例：容量 1、2、4、8，放满 8 个元素一共只搬 1+2+4 = 7 次。

**结构。** 三根指针（begin、end、end_of_storage）指向一整块连续堆内存。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实心 = 旧元素, 蓝框 = 新元素, 虚线 = 余量</text>
<text x="8" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cap 1</text>
<rect x="52" y="24" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="8" y="72" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cap 2</text>
<rect x="52" y="56" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="78" y="56" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="110" y="72" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">搬 1 个</text>
<text x="8" y="104" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cap 4</text>
<rect x="52" y="88" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="78" y="88" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="104" y="88" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<rect x="130" y="88" width="24" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="162" y="104" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">搬 2 个</text>
<text x="8" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cap 8</text>
<rect x="52" y="120" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="78" y="120" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="104" y="120" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="120" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="156" y="120" width="24" height="22" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<rect x="182" y="120" width="24" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="208" y="120" width="24" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="234" y="120" width="24" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="266" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">搬 4 个</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">搬运总数 1+2+…+n/2 &lt; n, 均摊每次 O(1)</text>
<text x="170" y="178" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">若每次只加固定的 k, 总搬运 ≈ n²/2k</text>
</svg>
```

**细节。**

- 满了就申请更大的新块，把旧元素搬过去，再释放旧块
- libstdc++ 与 libc++ 是 2 倍，MSVC 是 1.5 倍
- libc++ 实测连续 push_back 100 次，容量依次为 1 2 4 8 16 32 64 128

**为什么。** 容量按倍数增长，每个元素平均只被搬常数次，总搬运量小于 2n；若每次只加固定的 k，总搬运量就是 O(n²)。

**坑。** 提前知道个数就先 `reserve(n)`，省掉所有中间的重新分配。

**例题：** LC 232 用栈实现队列（同类：LC 155 最小栈）

只用两个栈实现先进先出的队列：`push`、`pop`、`peek`、`empty`。要求每个操作均摊 O(1)。出栈那只栈空了才把进栈那只整个倒过去，每个元素最多被搬一次，和 `vector` 翻倍扩容是同一种均摊账。

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
