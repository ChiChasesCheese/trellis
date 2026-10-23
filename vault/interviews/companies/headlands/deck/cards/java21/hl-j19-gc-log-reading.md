---
id: hl-j19-gc-log-reading
node: java21.j19-runtime-zgc-jit
type: qa
step: 17
---
## Q
G1 日志行末的 `6.720ms` 与 ZGC 日志行末的 `0.043s` 含义有什么根本区别？真正的 ZGC 暂停去哪看？

## A
```
G1:  GC(59) Pause Young (G1 Evacuation Pause) 1942M->957M(2048M) 3.404ms
ZGC: GC(2) Minor Collection (Allocation Rate) 742M(36%)->1198M(58%) 0.043s
```
- G1 那行最后的毫秒数是**应用被暂停（STW）的时间**；
- ZGC 那行最后的时间是**这一整轮并发回收的耗时**，应用期间一直在跑；
- 真正的 ZGC 暂停另有记录：JFR 的 `jdk.GCPhasePause` 或 `-Xlog:gc+phases`。

面试别把两个数字混为一谈。
