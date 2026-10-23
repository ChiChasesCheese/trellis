%% trellis:begin %%
# 分支预测与无分支（branchless）代码
*硬件：CPU 与内存*

CPU 猜分支方向提前执行，猜错要清空流水线（约 15–20 个周期）；可预测的分支几乎免费，随机分支很贵。

**Requires:** [[domains/hft/map/machine.pipeline-ooo|流水线、超标量与乱序执行]]

**Unlocks:** [[domains/hft/map/cpp.static-dispatch|静态分派：模板、CRTP 与虚函数的代价]], [[domains/hft/map/cpp.compiler|让编译器帮你：内联、likely 提示、PGO 与看汇编]], [[domains/hft/map/measurement.profiling|剖析工具：perf、火焰图、硬件计数器、JFR 与 async-profiler]]

## Readings
- [[wiki-branch-predictor|分支预测器（branch predictor）]]

## Cards (4)
1. [[hft-machine-branch-prediction-mechanism]]
2. [[hft-machine-branch-prediction-sorted-array]]
3. [[hft-machine-branch-prediction-branchless-contrast]]
4. [[hft-machine-branch-prediction-rare-trade-path]]
%% trellis:end %%

## Notes
