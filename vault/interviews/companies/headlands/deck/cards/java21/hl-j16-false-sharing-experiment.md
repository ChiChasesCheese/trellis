---
id: hl-j16-false-sharing-experiment
node: java21.j16-concurrency-primitives
type: qa
step: 25
---
## Q
伪共享实验：两个线程各改 `AtomicLongArray` 的一个元素，下标 (0,1) 与 (0,32)，每线程 5000 万次，结果如何？

## A
下标 (0,1) 相邻（同一缓存行）vs (0,32) 相距 256 字节：

- 第 1 轮：相邻 270 ms vs 分开 161 ms
- 第 2 轮：相邻 294 ms vs 分开 142 ms
- 第 3 轮：相邻 149 ms vs 分开 115 ms

相邻的更慢，三轮方向一致，幅度波动（机器有别的负载）。逻辑上两线程毫无关系，纯因共享缓存行变慢。
