---
id: hl-javaq-e-q24-steps
node: java-questions.e-jit-gc
type: qa
step: 24
---
## Q
一次 safepoint 的过程分几步？为什么一个没有检查点的长计数循环会拖慢它？常见 safepoint 原因有哪些？

## A
1. VM 线程请求 safepoint，等待所有线程到达（time-to-safepoint）。
2. 线程 A 运行一阵后到达 safepoint 检查点，停下。
3. 线程 B 的一个很长的计数循环**没有检查点**，迟迟不停，所有线程都得等它。
4. 全部到达后，VM 线程执行操作，再释放所有线程。

- 旧版本里 `int` 计数的长循环没有 safepoint 检查；现在 loop strip mining 缓解（记大意即可）。
- 常见原因：GC、`Deoptimize`、`ThreadDump`（`jstack` / `jcmd Thread.print` 本身会造成一次）、类重定义、`RevokeBias`（偏向锁，已移除）。
