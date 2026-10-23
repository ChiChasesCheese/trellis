---
id: hl-j19-hiccup-results
node: java21.j19-runtime-zgc-jit
type: qa
step: 29
---
## Q
hiccup 实验里 G1、分代 ZGC、基线的 p50、p99、p99.9、max 各是多少？怎么解读？

## A
| | p50 | p99 | p99.9 | max |
|---|---|---|---|---|
| G1 | 7.24 ms | 13.27 ms | **116.53 ms** | **132.02 ms** |
| 分代 ZGC | 6.94 | 8.14 | 9.00 | 11.83 |
| 基线 G1（无压力） | 6.67 | 8.02 | 8.47 | 13.50 |

解读：
- p50 ≈ 7 ms 不是 GC，是 `Thread.sleep(1)` 在 macOS 上的误差；
- G1 的 p99.9 / max 远高于基线：是 G1 Full GC（`G1 Old Generation` 15 次），分配快过并发回收，退化成整堆 STW；
- ZGC 的 max 11.8 ms 与基线同量级：**GC 没有产生可测的尾部延迟**（JFR 实测最长暂停 0.011 ms）。

局限：2 GB 堆、4 个分配线程的合成负载；ZGC 的吞吐、CPU、内存头部空间代价没有测量。
