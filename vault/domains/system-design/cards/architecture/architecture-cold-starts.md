---
id: architecture-cold-starts
node: architecture.serverless
type: qa
---
## Q
What actually happens during a FaaS cold start, roughly how expensive is it, and what are the mitigations?

## A
On a request with no warm instance, the platform must **provision a sandbox (microVM/container), load the runtime, load your code, and run init** before handling the request — typically ~100ms–1s+, worst with heavy runtimes (JVM) and large bundles; VPC networking and big dependency trees make it worse.

Mitigations:
- **Provisioned concurrency / min instances**: pay to keep N instances warm — the real fix for latency-sensitive paths.
- **Shrink init**: smaller bundles, lazy-load dependencies, lighter runtimes; snapshot-based starts (e.g. JVM snapshotting à la SnapStart) cut runtime init.
- Note cold starts hit a small fraction of requests but dominate **tail latency** — and every concurrency spike is a burst of them.

## Q zh
FaaS 冷启动期间实际发生什么，大约昂贵多少，缓解是什么？

## A zh
在没有温暖实例的请求上，平台必须**配置沙箱（microVM/容器）、加载运行时、加载你的代码、运行 init**在处理请求之前——通常 ~100ms–1s+，最坏与重运行时（JVM）和大包；VPC 网络和大依赖树使它更坏。

缓解：
- **已配置并发 / min 实例**：支付保持 N 实例温暖——延迟敏感路径的真正修复。
- **缩小 init**：更小的包、延迟加载依赖、更轻运行时；快照基础启动（例如 JVM 快照方式 SnapStart）切割运行时 init。
- 注意冷启动击中少数请求但主导**尾延迟** ——每个并发峰值是它们的一阵。
