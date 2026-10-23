%% trellis:begin %%
# 流水线、超标量与乱序执行
*硬件：CPU 与内存*

CPU 把指令拆成多级流水、每周期发射多条、在依赖允许时乱序执行；指令级并行（ILP）与依赖链。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/hft/map/machine.branch-prediction|分支预测与无分支（branchless）代码]], [[domains/hft/map/machine.memory-ordering|内存序、x86 TSO 与原子操作的成本]], [[domains/hft/map/machine.simd|SIMD 向量指令]], [[domains/hft/map/machine.power-smt|频率、节能状态与超线程对抖动的影响]]

## Readings
- [[wiki-branch-predictor|分支预测器（branch predictor）]]
- [[wiki-ooo|乱序执行（out-of-order execution）]]

## Cards (4)
1. [[hft-machine-pipeline-ooo-how-it-works]]
2. [[hft-machine-pipeline-ooo-dependency-chain]]
3. [[hft-machine-pipeline-ooo-memory-level-parallelism]]
4. [[hft-machine-pipeline-ooo-ipc-in-practice]]
%% trellis:end %%

## Notes
