---
id: problems-typeahead-precomputed-topk-vs-onthefly-dfs
node: problems.search.typeahead
type: qa
step: 2
tags: [grown]
---
## Q
A plain trie supports fast prefix lookup (O(prefix length) to reach the node), but why is it not sufficient on its own for a typeahead system, and what has to be added to each node?

## A
A plain trie's node only tells you which characters can follow — it doesn't tell you which of the many words under that node are the most popular ones to suggest. Answering 'what are the top-K completions of this prefix' from a plain trie requires a depth-first traversal of the entire subtree under that node at request time, collecting and sorting all matching words — for a short, popular prefix that subtree can cover tens or hundreds of thousands of words, making per-request traversal infeasible at typeahead's request volume and latency budget. The fix is to precompute and cache the top-K completions directly at each trie node during the offline aggregation pass, so an online request only needs O(prefix length) to reach the node and O(K) to copy its cached list — no traversal or sorting happens on the request path.

## Q zh
普通 trie 支持快速的前缀查找（O(前缀长度) 就能定位到节点），但为什么它本身不足以支撑一个 typeahead 系统？需要在每个节点上额外加什么？

## A zh
普通 trie 的节点只告诉你'接下来可以是哪些字符'，并不知道该节点下众多单词里哪些是最该被建议的热门词。要从普通 trie 里回答'这个前缀的 top-K 补全是什么'，需要在请求时对该节点下的整棵子树做一次深度优先遍历，收集并排序所有匹配的词——对一个很短、很热门的前缀，这棵子树可能覆盖数万到数十万个词，在 typeahead 的请求量和延迟预算下，逐请求遍历完全不可行。修复方法是在离线聚合阶段就把每个 trie 节点的 top-K 补全预先算好并缓存在该节点上，在线请求只需要 O(前缀长度) 走到节点、O(K) 复制它缓存的列表——请求路径上不发生任何遍历或排序。
