---
id: uth-os-net-epoll-1-rbtree-ready
node: os-net.epoll
type: qa
step: 1
---
## Q
**epoll 为什么不用扫描所有 fd**｜Linux · epoll · 内核 7.3

一个 epoll 监听 10 万个连接，`epoll_wait` 为什么仍然很快？

## A
**背景。** 服务器要同时盯着 10 万个连接（每个连接在内核里是一个整数编号 fd），谁有数据就处理谁。最笨的办法是循环问每个连接“有数据吗”：每一轮 10 万次询问，绝大多数是白问。epoll 反过来：先登记“我关心这些连接”，之后有数据到达时由内核把它记进一张就绪名单，程序只读这张名单。

**结构。** 每个 epoll 实例（`struct eventpoll`）里有两样东西：红黑树 `rbr`（一种保持平衡的有序树，增删查都是 O(log n)）存全部登记过的 fd；就绪链表 `rdllist` 只存已有数据的 fd。例：登记了 fd 5 和 fd 10，10 号来了数据，它被挂进 `rdllist`，`epoll_wait` 只返回它。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<line x1="170" y1="43" x2="110" y2="53" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="170" y1="43" x2="230" y2="53" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="110" y1="79" x2="80" y2="91" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="110" y1="79" x2="140" y2="91" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="230" y1="79" x2="200" y2="91" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="230" y1="79" x2="260" y2="91" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="170" cy="30" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">8</text>
<circle cx="110" cy="66" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<circle cx="230" cy="66" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">12</text>
<circle cx="80" cy="104" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<circle cx="140" cy="104" r="13" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<circle cx="200" cy="104" r="13" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="200" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">10</text>
<circle cx="260" cy="104" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">15</text>
<text x="14" y="22" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">红黑树 rbr</text>
<text x="14" y="36" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">全部 fd</text>
<line x1="140" y1="117" x2="130" y2="148" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200" y1="117" x2="200" y2="148" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">回调</text>
<rect x="105" y="148" width="50" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">fd 5</text>
<rect x="175" y="148" width="50" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="200" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">fd 10</text>
<line x1="155" y1="160" x2="170" y2="160" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M175.0,160.0 L168.2,163.3 L168.2,156.7 Z" fill="currentColor" stroke="none"/>
<text x="14" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">rdllist</text>
<text x="14" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">只存就绪</text>
<line x1="225" y1="160" x2="253" y2="160" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M258.0,160.0 L251.2,163.3 L251.2,156.7 Z" fill="currentColor" stroke="none"/>
<text x="262" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">epoll_wait</text>
</svg>
```

**细节。**

- `epoll_ctl(ADD)` 把 fd 插进红黑树，并在该 fd 的等待队列（内核记录“谁在等它有数据”的名单）上挂回调 `ep_poll_callback`
- 数据到达时内核调用这个回调，回调把节点 `list_add_tail` 进 `rdllist`
- `epoll_wait` 只遍历 `rdllist`，开销是 O(就绪数)，与监听总数无关

**为什么。** 把“登记”和“等待”拆开：登记一次，之后由事件推动，而不是每次调用都把所有 fd 重新问一遍。

**对应 LeetCode：** 无直接对应的题
