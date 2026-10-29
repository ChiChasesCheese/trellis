---
id: uth-os-net-epoll-2-select
node: os-net.epoll
type: qa
step: 2
---
## Q
**select 为什么撑不住大量连接**｜Linux · select 对比 epoll

`select` 每次调用都要做什么？为什么 fd 一多就线性变慢，还有 1024 的上限？

## A
**背景。** epoll 之前的老接口是 `select`：把关心的 fd 打成一张位图（每个 fd 占一位，是 1 就表示关心）交给内核，内核再告诉你哪些已就绪。麻烦在于内核没有记忆，每次调用都要把全部 fd 重新交一遍。

**结构。** 这张位图叫 `fd_set`，长度固定，`FD_SETSIZE` 是 1024 位，所以 fd 编号不能超过 1023。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="26" y="20" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">fd_set 定长位图 1024 位</text>
<rect x="26" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="44" y="30" width="18" height="22" rx="1" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="53" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="62" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="80" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="89" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="98" y="30" width="18" height="22" rx="1" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="107" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="116" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="134" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="143" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="152" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="170" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="188" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="197" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="206" y="30" width="18" height="22" rx="1" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="215" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="224" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="233" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="242" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="260" y="30" width="18" height="22" rx="1" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="269" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="278" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="287" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<rect x="296" y="30" width="18" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<line x1="26" y1="68" x2="307" y2="68" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M312.0,68.0 L305.2,71.3 L305.2,64.7 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">内核对每个 fd 调一次 poll 共 n 次</text>
<line x1="26" y1="102" x2="314" y2="102" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="26" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">epoll_wait</text>
<rect x="120" y="108" width="48" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="144" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">fd 1</text>
<rect x="176" y="108" width="48" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="200" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">fd 5</text>
<text x="232" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">只取就绪的</text>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">select 返回后用户态还要再扫一遍位图</text>
</svg>
```

**细节。**

- 每次调用，内核先把位图拷进来，再在 `do_select` 里对每个关心的 fd 调一次 `poll`（询问它是否就绪），共 n 次，O(n)
- 返回时结果位图拷回用户态，用户还得再扫一遍找出就绪的 fd
- epoll 登记一次后，`epoll_wait` 只拿就绪事件

**为什么。** 位图本身很简单，但“每次都把全部关心的 fd 交给内核”的接口，决定了 O(n)，与实现多快无关。

**对应 LeetCode：** 无直接对应的题
