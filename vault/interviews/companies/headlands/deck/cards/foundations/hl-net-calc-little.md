---
id: hl-net-calc-little
node: foundations.networking-basics
type: qa
step: 47
---
## Q
计算：一个服务每秒 5000 个请求，平均每个耗时 200 ms。同时有多少个请求在处理？每个请求占一个平台线程需要多少线程？

## A
Little 定律 L = λ × W = 5000 × 0.2 = **1000** 个请求同时在处理。每个请求占一个平台线程就需要约 1000 个线程，已经比较重；用虚拟线程则轻松。
