---
id: runtime-node-event-loop-worker-pool
node: runtimes.node-event-loop
type: qa
---
## Q
Why can raising `UV_THREADPOOL_SIZE` make a Node image service worse even when requests use asynchronous APIs?

## A
Some async APIs delegate CPU- or blocking-heavy work such as compression, crypto, DNS, and filesystem operations to libuv's worker pool. More workers can reduce queueing until they oversubscribe CPU or memory; then context switching and concurrent image buffers raise tail latency and OOM risk. Measure worker-pool queue delay, bound transformation concurrency, and scale processes/hosts based on the saturated resource instead of treating the setting as free parallelism.

## Q zh
即使请求使用 asynchronous API，为什么提高 `UV_THREADPOOL_SIZE` 仍可能让 Node image service 更差？

## A zh
某些 async API 会把 compression、crypto、DNS、filesystem 等 CPU-heavy 或 blocking-heavy 工作交给 libuv worker pool。增加 worker 起初会减少 queueing，但超过 CPU 或内存能力后，context switching 和并发 image buffer 会提高 tail latency 与 OOM 风险。应测量 worker-pool queue delay、限制 transformation concurrency，并按真正饱和的资源扩展 process/host，而不是把该设置当成免费 parallelism。
