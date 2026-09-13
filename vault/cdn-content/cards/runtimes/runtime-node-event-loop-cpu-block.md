---
id: runtime-node-event-loop-cpu-block
node: runtimes.node-event-loop
type: qa
---
## Q
A Node.js edge handler synchronously parses a 20 MB JSON manifest. CPU is below fleet capacity, yet unrelated requests stall. Explain the runtime behavior and fix.

## A
JavaScript callbacks run on one event-loop thread per process. The synchronous parse monopolizes that thread, so socket callbacks, timers, and promise continuations for every request wait behind it. Bound input size, pre-parse/cache manifests, stream when possible, or move CPU-heavy parsing to a worker thread or separate service. Scaling replicas only dilutes the problem; one hostile or large input can still block each event loop.

## Q zh
Node.js edge handler 同步解析 20 MB JSON manifest。fleet CPU 尚未满，但无关请求也停住了。解释 runtime behavior 并给出修复。

## A zh
每个进程的 JavaScript callback 运行在单个 event-loop thread 上。同步 parse 会独占该线程，使所有请求的 socket callback、timer 和 promise continuation 都在后面等待。应限制 input size、预解析或缓存 manifest、尽量 stream，或者把 CPU-heavy parsing 移到 worker thread / 独立服务。增加 replica 只能稀释问题；一个恶意或超大输入仍能阻塞每个 event loop。
