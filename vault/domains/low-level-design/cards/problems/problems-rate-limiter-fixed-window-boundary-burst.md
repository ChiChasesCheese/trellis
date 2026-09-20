---
id: problems-rate-limiter-fixed-window-boundary-burst
node: problems.components.rate-limiter
type: qa
step: 1
tags: [grown]
---
## Q
限流器（Rate Limiter）用固定窗口计数（fixed window counter，把时间切成对齐的格子、每格一个计数器）实现时，为什么说它是错的？用限额「每 10 秒 5 次」把账算给面试官看。

## A
因为**边界突发**（boundary burst）：窗口只按格子对齐，不看真实的时间间隔。

限额 5 次／10 秒，客户端在 t=9.9 秒连发 5 次——全落在第 0 格（0–10 秒），计数 5，不超；再在 t=10.1 秒连发 5 次——全落在第 1 格（10–20 秒），计数 5，也不超。两格各自都合法，**可是 0.2 秒之内真实放行了 10 次，是限额的 2 倍**。

最坏情况恒为 2×limit，且与窗口长度无关。换来的是最省的内存（两个整数）。修法是让窗口滑动：滑动窗口日志（sliding window log，精确，内存 O(limit)）或滑动窗口计数（sliding window counter，近似，三个数字）。

在机考里，主动把这笔算术算出来比写完四种算法更能加分——它证明你知道自己第一版错在哪。
