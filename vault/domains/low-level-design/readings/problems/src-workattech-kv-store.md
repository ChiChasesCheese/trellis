---
nodes: [problems.components.kv-store]
url: https://workat.tech/machine-coding/practice/design-key-value-store-6gz6cq124k65/index.html
tags: [no-archive]
---
# workat.tech — Design a Key-Value Store

值得读：workat.tech 的机考练习题面，用具体的 API 例子把"每个 key 对应一组 field-value
对"这条设定讲得很直白，适合用来核对第 1、2 关的方法签名该长什么样。题面本身只给到基本
读写、扫描和过期，没有涉及嵌套事务；本题解的撤销日志设计、"commit 折叠进上一层"这套
事务语义，以及方案 A（写时复制覆盖栈）与方案 B（撤销日志）的成本对比，都是独立设计的，
题面里找不到对应内容。

%% trellis:begin %%
## Source
[Open the original ↗](https://workat.tech/machine-coding/practice/design-key-value-store-6gz6cq124k65/index.html)
%% trellis:end %%
