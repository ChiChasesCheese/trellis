---
id: uth-os-net-tcp-1-window
node: os-net.tcp
type: qa
step: 1
---
## Q
**滑动窗口：能发多少由谁说了算**｜Linux · TCP · 内核 7.3

一条 TCP 连接任一时刻最多能有多少数据在路上没被确认？

## A
**背景。** 最简单的发送方式：发一个包，等对方确认（ACK），再发下一个。每个包都要等一个往返时间（RTT），链路再快也被往返时间卡死。改进：不等确认，先连发一批，一边收确认一边继续发。“允许同时在路上、还没被确认的数据量”就是窗口。

**结构。** 把要发的字节流想成一排格子：已确认 | 已发未确认 | 可发 | 暂不能发。窗口覆盖中间两段，大小 = min(rwnd, cwnd)：接收窗口 rwnd 是对方说“我的缓冲区还能收多少”，拥塞窗口 cwnd 是自己估计“网络能承受多少”。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="26" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="38" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="50" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="62" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<rect x="74" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="86" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<rect x="98" y="44" width="24" height="26" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="110" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<rect x="122" y="44" width="24" height="26" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="134" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<rect x="146" y="44" width="24" height="26" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="158" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<rect x="170" y="44" width="24" height="26" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="182" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">7</text>
<rect x="194" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="206" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">8</text>
<rect x="218" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="230" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">9</text>
<rect x="242" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">10</text>
<rect x="266" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">11</text>
<rect x="290" y="44" width="24" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">12</text>
<line x1="98" y1="36" x2="266" y2="36" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="98" y1="32" x2="98" y2="40" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="266" y1="32" x2="266" y2="40" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="182" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">窗口 = min(rwnd, cwnd)</text>
<text x="62" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">已确认</text>
<text x="146" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">已发未确认</text>
<text x="230" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">可发</text>
<text x="290" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">不可发</text>
<line x1="100" y1="116" x2="133" y2="116" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M138.0,116.0 L131.2,119.3 L131.2,112.7 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="144" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">收到 ACK 左边界右移</text>
</svg>
```

**细节。**

- 收到 ACK，窗口左边界右移，腾出新的可发空间
- 窗口字段只有 16 位（最大 64 KB）；窗口缩放（window scale）选项把它左移最多 14 位（`TCP_MAX_WSCALE`），上限约 1 GB
- 发包前内核要同时检查两个窗口，都放行才发

**为什么。** rwnd 保护接收方（流量控制），cwnd 保护网络（拥塞控制），取小就是各管各的。

**例题：** LC 3 无重复字符的最长子串（同类：LC 239 滑动窗口最大值）

求字符串中不含重复字符的最长子串（要连续）的长度。例：`"abcabcbb"` → 3（`"abc"`）；`"bbbbb"` → 1；`"pwwkew"` → 3。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}          # 字符 -> 它最近一次出现的下标
    best = left = 0                    # 窗口是 s[left : right + 1]
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:   # ch 在窗口内出现过：左端直接跳过去
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```
