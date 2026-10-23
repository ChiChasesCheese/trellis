---
id: hl-os-spsc-benchmark
node: foundations.os-processes-threads-ipc
type: qa
step: 30
---
## Q
映射文件上的 SPSC 环形缓冲和 `ArrayBlockingQueue<Long>` 传 2000 万个 long，吞吐各是多少？数字有多稳定？

## A
5 次运行：环形缓冲约 **74–85 M msgs/s**（0.24–0.27 s），`ArrayBlockingQueue` 约 **6.6–9.2 M msgs/s**（2.17–3.04 s），环形缓冲约 **10 倍**吞吐（每条约 12 ns 对约 130 ns）。

别的时间运行同一程序，环形缓冲吞吐曾落在 27–50 M msgs/s（核心类型和系统负载不同，浮动 2–3 倍），`ArrayBlockingQueue` 稳定在 5–9 M msgs/s；偶有孤立 313 M msgs/s 的异常值，忽略。**倍数方向稳定，绝对数字不稳定。**
