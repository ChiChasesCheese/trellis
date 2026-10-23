---
id: hl-j19-jfr-experiment
node: java21.j19-runtime-zgc-jit
type: qa
step: 5
---
## Q
约 400 万个长寿对象 + 持续分配、2 GB 堆、跑 8 秒，G1 与分代 ZGC 的 GC 暂停统计相差多少？

## A
用 JFR 的 `jdk.GCPhasePause` 事件：

| | 事件数 | 总暂停 | 平均 | p99 | 最长 |
|---|---|---|---|---|---|
| G1 | 277 | 1480.7 ms | 5.345 ms | 75.045 ms | 77.890 ms |
| 分代 ZGC | 2189 | 4.8 ms | 0.002 ms | 0.006 ms | 0.011 ms |

G1 平均 5 ms 但 p99 达 75 ms；ZGC 最长 0.011 ms（11 µs）。8 秒里 G1 共停了约 1.5 秒，ZGC 共停 4.8 ms。
