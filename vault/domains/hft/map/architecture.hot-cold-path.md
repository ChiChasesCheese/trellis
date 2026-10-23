%% trellis:begin %%
# 快路径与慢路径分离
*tick-to-trade 系统架构*

把日志、监控、持久化、配置变更从热路径（hot path）挪出去，交给别的线程异步处理。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.event-loop|单线程事件循环与忙轮询（busy-spin）]]

**Unlocks:** [[domains/hft/map/cpp.warm-cache|缓存预热：让热路径保持热]], [[domains/hft/map/cpp.errors-logging|异常、错误处理与日志离开热路径]]

## Drills
- [[architecture-risk-inline-explain|练习：向新同事解释，为什么下单前风控放在热路径里]]

## Cards (5)
1. [[hft-architecture-hot-cold-path-definition]]
2. [[hft-architecture-hot-cold-path-async-logging]]
3. [[hft-architecture-hot-cold-path-lossy-vs-lossless]]
4. [[hft-architecture-hot-cold-path-config-change]]
5. [[hft-architecture-hot-cold-path-cold-path-still-hurts]]
%% trellis:end %%

## Notes
