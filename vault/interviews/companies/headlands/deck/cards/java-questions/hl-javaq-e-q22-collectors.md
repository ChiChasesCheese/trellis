---
id: hl-javaq-e-q22-collectors
node: java-questions.e-jit-gc
type: qa
step: 16
---
## Q
对比 Parallel、G1、ZGC：暂停特征、适合场景、备注（实测最大间隔）。Shenandoah 和 Epsilon 是什么？

## A
- **Parallel**：全停顿，暂停随存活数据线性增长；适合批处理、吞吐优先；实测最大间隔 22 ms。
- **G1**（9 起默认）：按 `MaxGCPauseMillis` 目标增量回收 Region；适合通用；实测 8 ms；用 mixed 回收清理老年代。
- **ZGC**（15 正式；分代版 21）：并发标记 + 并发整理（读屏障 + 染色指针），暂停亚毫秒；适合低延迟、大堆；实测 0.14 ms；需要留出堆余量，否则出现分配停顿（allocation stall）。
- **Shenandoah**：另一种低暂停收集器；**Epsilon**：只分配、不回收。
