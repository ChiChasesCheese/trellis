---
nodes: [problems.search.typeahead]
url: https://blog.mikemccandless.com/2010/12/using-finite-state-transducers-in.html
---
# Using Finite State Transducers in Lucene

值得读：Lucene 提交者 Mike McCandless 撰写的工程博客，给出了 FST（有限状态转换机）相比
trie 额外共享公共后缀带来的压缩效果的真实例子——980 万词项压缩进一个 69MB 的 FST，用
不到 256MB 堆内存、约 8 秒构建完成——并明确指出 FST 的紧凑表示不支持增量更新，任何一次
修改都要从排好序的静态输入整体重建。本题解「深入探讨」第 1 节直接引用了这个具体数字和
这条限制，作为"基础在线服务层不选 FST、把它留给只读快照场景"这一决策的依据。

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.mikemccandless.com/2010/12/using-finite-state-transducers-in.html)

## Archived copy
![[src-mccandless-typeahead-clip]]
%% trellis:end %%
