---
id: uth-os-net-rate-limit-2-leaky
node: os-net.rate-limit
type: qa
step: 2
---
## Q
**漏桶只存 excess 一个数**｜Nginx · limit_req · 1.31

配置 `rate=1r/s burst=5`，Nginx 对每个客户端只存什么，就能判断放行、延迟还是拒绝？

## A
**结构。** 漏桶（leaky bucket）当计量器用：每个 key 只存 `excess`（桶里的水，单位是千分之一个请求）和上次到达时间。

**细节。**

- 每个请求到达：`excess = excess - rate × 经过毫秒数 / 1000 + 1000`，下限 0，意思是先漏掉一段时间的水，再倒进一个请求
- `excess` 超过 `burst × 1000` 就拒绝
- 没超过就按 `excess` 折算成延迟排队，加 `nodelay` 则立即放行

**为什么。** 输出速率恒定，对后端最平滑；代价是突发被排队，而令牌桶允许突发直通。

**对应 LeetCode：** LC 933 最近的请求次数 · LC 622 设计循环队列
