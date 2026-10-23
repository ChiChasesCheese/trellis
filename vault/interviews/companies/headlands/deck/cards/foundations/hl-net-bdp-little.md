---
id: hl-net-bdp-little
node: foundations.networking-basics
type: qa
step: 18
---
## Q
带宽时延积（BDP）和 Little 定律（Little's law）各是什么？分别举一个计算例子。

## A
- **BDP** = 带宽 × RTT：要填满链路，在途数据量至少等于它。1 Gbps × 10 ms RTT = 10⁹/8 B/s × 0.01 s = **1.25 MB**；窗口小于它，发送方发完窗口就得停下等 ACK，链路填不满。
- **Little 定律** L = λ × W：系统里平均同时存在的请求数 = 到达率 × 每个请求平均停留时间。服务每秒 10,000 个请求、每个平均 100 ms → 同时有 10,000 × 0.1 = **1000 个**请求在处理。

每个请求占一个线程就需要 1000 个线程，这是虚拟线程存在的原因之一。
