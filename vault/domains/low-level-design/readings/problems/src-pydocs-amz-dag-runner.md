---
nodes: [amazon.amz-dag-runner]
url: https://docs.python.org/3/library/graphlib.html
---
# graphlib — Functionality to operate with graph-like structures（Python 标准库文档）

值得读：英文官方文档。`TopologicalSorter` 的 `prepare()`、`get_ready()`、`done()` 是「一边执行一边划掉已完成节点」的并行调度接口，有环时抛 `graphlib.CycleError`。面试里要手写 Kahn 算法来展示算法，工作中应当优先用它。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/graphlib.html)
%% trellis:end %%
