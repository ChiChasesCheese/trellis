%% trellis:begin %%
# 频率、节能状态与超线程对抖动的影响
*硬件：CPU 与内存*

睿频（turbo）、C-state 深度睡眠唤醒、P-state 降频、超线程（SMT）共享核心资源，都会让延迟不稳定；交易服务器通常关掉它们。

**Requires:** [[domains/hft/map/machine.pipeline-ooo|流水线、超标量与乱序执行]]

## Readings
- [[rigtorp-low-latency-guide|Low latency tuning guide]]

## Cards (4)
1. [[hft-machine-power-smt-c-states]]
2. [[hft-machine-power-smt-turbo-and-p-states]]
3. [[hft-machine-power-smt-hyperthreading]]
4. [[hft-machine-power-smt-bios-tradeoff]]
%% trellis:end %%

## Notes
