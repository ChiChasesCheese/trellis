---
id: leetcode-c-streaming-stock-span-application
node: topics.uncategorised
type: qa
anki: 1787361363922
tags: [algorithm::amortized-analysis, algorithm::monotonic-stack, algorithm::run-length-compression, application, case, case::streaming-stock-span, category::distributed-streaming, chapter::03, leetcode, system::streaming-analytics-service]
---
## Q
在线 stock span 为什么把被弹出节点的 span 累加后仍然正确？

## A
这些节点代表连续且价格都不高于当前值的区间；当前价格把它们全部支配。合并 span 后，新节点仍精确表示从当前点向左直到第一个更高价格前的连续长度。

**Evidence**

Flink 官方 stateful stream processing 文档说明 keyed state 的生产持久化边界；单调栈提供在线跨度状态的均摊 O(1) 压缩。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2F%E5%9C%A8%E7%BA%BF%E8%82%A1%E7%A5%A8%E8%B7%A8%E5%BA%A6%EF%BC%9A%E5%8D%95%E8%B0%83%E6%A0%88%E5%8E%8B%E7%BC%A9%E8%BF%9E%E7%BB%AD%E5%8E%86%E5%8F%B2)
