---
id: hi-c-sd-caching-n14-write-behind
node: sd.core-concepts.caching.notes
type: qa
step: 14
---
## Q
**缓存 · 缓存模式 · Write-Behind**｜摘要 · 追问
Write-behind（写回）为什么写得快？风险是什么，适合什么场景？

## A
- **做法：** 应用只写缓存，缓存把数据批量、异步地刷进数据库。
- **优点：** 写入极快，还能把许多小写合并成批量写。
- **风险：** 缓存在刷盘前崩溃会丢数据，适合能容忍偶尔丢数据的场景。
- **适用：** 需要高写吞吐、可以最终一致的场景，如分析和指标管道。
