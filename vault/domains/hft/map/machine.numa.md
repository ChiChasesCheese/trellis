%% trellis:begin %%
# NUMA：本地内存与远端内存
*硬件：CPU 与内存*

多路服务器每个 CPU 插槽有自己的内存，访问另一插槽的内存更慢；把线程和它的内存放在同一个 NUMA 节点。

**Requires:** [[domains/hft/map/machine.memory-hierarchy|存储层级与延迟数字]]

## Readings
- [[drepper-memory|What Every Programmer Should Know About Memory]]
- [[wiki-numa|NUMA]]

## Cards (4)
1. [[hft-machine-numa-local-vs-remote]]
2. [[hft-machine-numa-pinning-and-first-touch]]
3. [[hft-machine-numa-single-socket-contrast]]
4. [[hft-machine-numa-wrong-node-scenario]]
%% trellis:end %%

## Notes
