---
id: hl-javaq-rubric-e-jit-gc
node: java-questions.rubric
type: qa
step: 8
---
## Q
回答 JIT 与 GC 内部机制的问题时，强、一般、弱的答案各有什么特征？

## A
- **强**：分层编译（解释器 → C1 → C2）、OSR、阈值概念；内联的条件（方法大小）和多态内联缓存（单 / 双 / 多态）；逃逸分析的收益与失败条件；去优化的触发例子与对延迟的影响；GC 的根、分代、Parallel / G1 / ZGC 权衡，选型与诊断顺序（**先量再调，降分配率优先**）；safepoint 的两段时间；能说出怎么观测（`-XX:+PrintCompilation`、`-Xlog:gc,safepoint`、`jstat`、JFR）。
- **一般**：知道 JIT / GC 的存在与名称，会说"G1 默认、ZGC 低延迟"，但说不出观测方法或权衡。
- **弱**：把 JIT 说成"第一次运行时编译一次"；"调大堆就能解决 GC 问题"；不知道 `System.gc()` 的危害；不区分 young / full GC。
