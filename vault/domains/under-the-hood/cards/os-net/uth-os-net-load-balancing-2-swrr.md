---
id: uth-os-net-load-balancing-2-swrr
node: os-net.load-balancing
type: qa
step: 2
---
## Q
**平滑加权轮询**｜Nginx · upstream round_robin · 1.31

权重 5:1:1 的三台机器，怎样避免连续 5 次打到同一台？

## A
**结构。** 每台机器有一个 `current_weight`。每次选择：所有机器先加上自己的 `effective_weight`，选 `current_weight` 最大的，再给它减去总权重。

**细节。**

- 权重 a=5、b=1、c=1，总权重 7：七次选择依次是 a a b a c a a
- 七轮之后所有 `current_weight` 回到 0，进入下一个循环
- 每次扫一遍后端，O(n)；`down`、失败超限、`max_conns` 已满的后端会被跳过

**为什么。** 朴素加权轮询会 aaaaabc 地突发，平滑版把 a 均匀打散，而且不依赖随机数。

**对应 LeetCode：** LC 767 重构字符串 · LC 1054 距离相等的条形码
