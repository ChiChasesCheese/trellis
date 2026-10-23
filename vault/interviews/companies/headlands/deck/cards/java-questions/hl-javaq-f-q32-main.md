---
id: hl-javaq-f-q32-main
node: java-questions.f-concurrency
type: qa
step: 24
---
## Q
怎么确定线程池大小？`Executors` 有哪些陷阱？
How do you size a thread pool? What are the pitfalls of `Executors`?

## A
一句话：CPU 密集 ≈ 核数（+1）；I/O 密集 ≈ 核数 × (1 + 等待时间 / 计算时间)，或直接用虚拟线程；**队列必须有界、拒绝策略显式**；别用 `newFixedThreadPool` 的无界队列和 `newCachedThreadPool` 的无界线程。

- **Little 定律**：并发度 L = 吞吐 λ × 延迟 W。要 1000 请求/秒、每个 50 ms → 平均需要 50 个在途请求。
- 算术：200 线程、每任务阻塞 1 s ⇒ 吞吐上限 200/s ⇒ 2000 个任务需要 10 s（实测约 11.3 s），与 CPU 核数无关——I/O 密集型池的大小由"阻塞时间"决定。
- 过载时：fixed 池无界 `LinkedBlockingQueue` → 内存爆；cached 池无上限线程 → 线程爆。
