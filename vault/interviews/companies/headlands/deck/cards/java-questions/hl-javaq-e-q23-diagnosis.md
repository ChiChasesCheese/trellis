---
id: hl-javaq-e-q23-diagnosis
node: java-questions.e-jit-gc
type: qa
step: 20
---
## Q
p99/p999 出现延迟尖刺时，诊断 GC 问题的五步流程是什么？

## A
先测量，不要先调参：
1. **现象**：p99/p999 尖刺。是 GC 吗？用统一日志对齐时间线：`-Xlog:gc*,safepoint:file=gc.log`。
2. **GC 暂停？** 看 `Pause Young / Remark / Cleanup` 时长；ZGC 看 allocation stall。
3. **不是 GC？** 查 safepoint 的其他原因（去优化）、页错误、操作系统调度。
4. **降分配率**：JFR 分配 profile / `getThreadAllocatedBytes`，消除热路径装箱和临时对象。
5. **再选 / 调 GC**。

G1 的一行暂停日志示例：`Pause Young (Normal) (G1 Evacuation Pause) 781M->267M(1024M) 5.288ms`。另一次带 `-Xlog:gc` 的 G1 运行最大间隔是 14.0 ms，说明 G1 抖动较大。
