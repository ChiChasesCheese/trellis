%% trellis:begin %%
# 异常、错误处理与日志离开热路径
*低延迟 C++*

零成本异常在抛出时很贵；热路径用返回值或直接不出错；日志只把原始数据写进队列，由另一线程格式化。

**Requires:** [[domains/hft/map/architecture.hot-cold-path|快路径与慢路径分离]]

## Drills
- [[cpp-hot-path-review|练习：评审一段 C++ 热路径，按对 p99.9 的伤害排序]]

## Cards (4)
1. [[hft-cpp-errors-logging-exceptions-cost]]
2. [[hft-cpp-errors-logging-error-codes]]
3. [[hft-cpp-errors-logging-async-logging]]
4. [[hft-cpp-errors-logging-queue-full]]
%% trellis:end %%

## Notes
