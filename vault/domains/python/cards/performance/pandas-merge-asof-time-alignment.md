---
id: pandas-merge-asof-time-alignment
node: performance.pandas-at-scale
type: qa
tags: [grown]
---
## Q
`pd.merge_asof()` 和常规的 `pd.merge()` 在连接两个时间序列时有什么本质区别？为什么常规 merge 处理不了时间戳不完全对齐的场景？

## A
常规 `merge()` 要求连接键精确相等才能配对，两边时间戳只要没有严格对齐就配不上；`merge_asof()` 要求两边先按时间键排好序，再为左表每一行找右表里最近的前一个（或后一个）时间戳做匹配，不要求精确相等，专门用来对齐两个采样频率或时间戳不同步的序列，比如把逐笔成交价对齐到最近一次的报价。
