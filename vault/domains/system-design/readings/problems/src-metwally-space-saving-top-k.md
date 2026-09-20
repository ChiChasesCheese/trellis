---
nodes: [problems.search.top-k]
url: https://www.cse.ust.hk/~raywong/comp5331/References/EfficientComputationOfFrequentAndTop-kElementsInDataStreams.pdf
tags: []
---
# Efficient Computation of Frequent and Top-k Elements in Data Streams

值得读：Space-Saving 算法的原始论文，给出算法本身（`m` 个计数器，替换最小者并记录过计数
`ε_i`）和确定性的命中保证（定理 3：任何真实频次 `f_i > εN` 的元素一定出现在候选集合里，
`m ≥ 1/ε`）。还给出了 Zipf 分布下更紧的界，以及和 Sticky Sampling、Lossy Counting、
GroupTest 的对比表。本题「深入探讨」第 3 节的参数反推和"为什么不能像 CMS 一样逐 cell
相加"直接来自这篇论文；本题没有用到它 Zipf 分布下的更紧界。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.cse.ust.hk/~raywong/comp5331/References/EfficientComputationOfFrequentAndTop-kElementsInDataStreams.pdf)

## Archived copy
![[src-metwally-space-saving-top-k-clip]]
%% trellis:end %%
