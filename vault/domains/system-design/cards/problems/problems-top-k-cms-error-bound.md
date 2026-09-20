---
id: problems-top-k-cms-error-bound
node: problems.search.top-k
type: qa
step: 1
tags: [grown]
---
## Q
In a Top-K trending design counting views with a Count-Min Sketch (CMS) over a daily window of N=60 billion events, using parameters ε=1e-6 and δ=1e-3, what are the sketch's width, depth, memory footprint (4-byte counters), and guaranteed absolute error — and why can't the same ε be reused unchanged for a 1-minute window's sketch?

## A
Width `w = ⌈e/ε⌉ = 2,718,282`, depth `d = ⌈ln(1/δ)⌉ = 7`, memory `w*d*4 bytes ≈ 76.1MB`. The Count-Min Sketch guarantee (Cormode & Muthukrishnan) is: the estimate never undercounts, and with probability ≥ 1-δ it overcounts by at most `ε*N`, giving an absolute error of `1e-6 * 6e10 = 60,000` here. Because the error is `ε*N` (not just `ε`), the same ε produces a wildly different absolute error at a different window's event volume `N` — a 1-minute window has roughly 1,440x fewer events than a full day, so reusing the day's ε there is fine (error shrinks proportionally), but reusing a 1-minute window's looser ε for the full day would blow up the absolute error by that same factor.

## Q zh
在一个用 Count-Min Sketch（CMS）统计观看次数的热门榜设计中，某天窗口的事件总量 N=600 亿，取参数 ε=1e-6、δ=1e-3，这个 sketch 的宽度、深度、内存占用（4 字节计数器）和保证的绝对误差各是多少？为什么不能把同一个 ε 原封不动地用到 1 分钟窗口的 sketch 上？

## A zh
宽度 `w = ⌈e/ε⌉ = 2,718,282`，深度 `d = ⌈ln(1/δ)⌉ = 7`，内存 `w*d*4 字节 ≈ 76.1MB`。Count-Min Sketch 的保证（Cormode & Muthukrishnan）是：估计值永不低估，且以至少 1-δ 的概率，过计数不超过 `ε*N`，这里绝对误差是 `1e-6 * 6e10 = 60,000`。因为误差是 `ε*N`（不只是 ε），同一个 ε 在不同窗口的事件总量 N 下绝对误差天差地别——1 分钟窗口的事件量大约是全天的 1/1440，把全天的 ε 直接用在 1 分钟窗口上没问题（误差按比例缩小），但反过来把 1 分钟窗口那种更宽松的 ε 用到全天窗口上，绝对误差会按同样的倍数放大。
