---
id: uth-os-net-epoll-3-level-edge
node: os-net.epoll
type: qa
step: 3
---
## Q
**水平触发和边缘触发差在哪**｜Linux · epoll · 内核 7.3

一个 fd 的数据只读了一半，水平触发（LT）和边缘触发（ET）下一次 `epoll_wait` 分别怎样？

## A
**背景。** 就绪名单把一个 fd 报告给程序之后，要不要继续留着它？有两种约定：水平触发（level-triggered，LT）：只要数据还没读完，每次 `epoll_wait` 都继续报告；边缘触发（edge-triggered，ET）：只在“有新数据到来”的那一刻报告一次。

**结构。** 差别就在 `ep_send_events` 把事件交给用户之后：LT 把节点重新挂回 `rdllist`，ET 不挂。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 168">
<text x="70" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">到达 10 字节</text>
<text x="150" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">read 5 字节</text>
<text x="240" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">再 epoll_wait</text>
<line x1="70" y1="26" x2="70" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<line x1="150" y1="26" x2="150" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<line x1="240" y1="26" x2="240" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="14" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">LT</text>
<line x1="34" y1="64" x2="320" y2="64" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="14" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">ET</text>
<line x1="34" y1="122" x2="320" y2="122" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="70" cy="64" r="7" stroke="currentColor" stroke-width="1.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="122" r="7" stroke="currentColor" stroke-width="1.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<circle cx="240" cy="64" r="7" stroke="currentColor" stroke-width="1.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<circle cx="240" cy="122" r="7" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="240" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">仍报告</text>
<text x="240" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">不报告</text>
<text x="70" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">报告</text>
<text x="70" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">报告</text>
</svg>
```

**细节。**

- LT（默认）：下次 `epoll_wait` 会重新检查该 fd，还有数据就再报告
- ET（`EPOLLET`）：只有新事件到来、回调再次把节点挂进链表时才报告
- `EPOLLONESHOT`：报告一次后不再报告，要用 `EPOLL_CTL_MOD` 重新武装

**坑。** ET 必须配非阻塞 fd（读不到数据时立刻返回，不会卡住），并且一次读到出现 `EAGAIN`（“暂时没数据了”的错误码）为止，否则剩下的数据不会再有通知。

**对应 LeetCode：** 无直接对应的题
