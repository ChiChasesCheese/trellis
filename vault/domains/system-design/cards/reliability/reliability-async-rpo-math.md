---
id: reliability-async-rpo-math
node: reliability.multi-region
type: cloze
---
With async cross-region replication, your effective **RPO equals the replication lag at the moment of disaster**, and writes lost ≈ {{c1::lag × write throughput}} — e.g. 5s of lag at 2,000 writes/s ≈ 10,000 lost writes. Lag is worst exactly when you need it least: {{c2::during traffic spikes and incidents, when the replication channel falls behind}} — so monitor lag as an SLI and alert when it exceeds the RPO objective. True RPO = 0 requires synchronous quorum replication and its cross-region write latency ([[reliability-three-region-quorum]]).

## zh
使用异步跨区域复制，你的有效 **RPO 等于灾难时刻的复制延迟**，丢失的写操作数 ≈ {{c1::lag × write throughput}} ——例如 5 秒延迟在 2,000 writes/s 下约 10,000 条丢失写操作。延迟在最糟的时候最严重：{{c2::traffic spikes 和事故期间，复制通道会落后}} ——所以要监控复制延迟作为 SLI，超过 RPO 目标时告警。真正的 RPO = 0 需要同步 quorum 复制及其跨区域写延迟（[[reliability-three-region-quorum]]）。
