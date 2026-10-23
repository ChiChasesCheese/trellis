---
nodes: [cpp.atomics, machine.memory-ordering, java.memory-model]
url: https://preshing.com/20120913/acquire-and-release-semantics/
---
# Acquire and Release Semantics

用图解释 acquire / release 语义：它们禁止哪些方向的重排、怎样配对实现消息传递。

**读的时候提取：**
- release 写 + acquire 读如何保证数据可见。
- 和完全顺序一致（seq_cst）的成本差别。

%% trellis:begin %%
## Source
[Open the original ↗](https://preshing.com/20120913/acquire-and-release-semantics/)

## Archived copy
![[preshing-acquire-release-clip]]
%% trellis:end %%
