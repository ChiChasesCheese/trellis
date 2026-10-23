%% trellis:begin %%
# SIMD 向量指令
*硬件：CPU 与内存*

一条指令同时处理多个数据（SSE / AVX2 / AVX-512），适合批量比较、解析和数值计算；自动向量化的条件。

**Requires:** [[domains/hft/map/machine.pipeline-ooo|流水线、超标量与乱序执行]]

## Readings
- [[wiki-simd|SIMD]]

## Cards (4)
1. [[hft-machine-simd-what-it-is]]
2. [[hft-machine-simd-hft-use-cases]]
3. [[hft-machine-simd-autovectorization]]
4. [[hft-machine-simd-wide-vector-side-effects]]
%% trellis:end %%

## Notes
