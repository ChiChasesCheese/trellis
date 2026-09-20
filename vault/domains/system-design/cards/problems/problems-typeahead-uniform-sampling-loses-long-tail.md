---
id: problems-typeahead-uniform-sampling-loses-long-tail
node: problems.search.typeahead
type: qa
step: 4
tags: [grown]
---
## Q
At a much larger scale where the offline aggregation pipeline needs to subsample its query logs (say, keep only 1% of events uniformly), why does uniform sampling risk silently dropping legitimate long-tail queries, and what's the fix?

## A
A legitimate query typed only 50 times nationwide in a day has an expected sampled count of just 0.5 under 1% uniform sampling; modeling this as a Poisson process, the probability that this query is sampled zero times — and therefore never appears in the aggregated counts at all — is about e^(-0.5) ≈ 60.7%. Uniform sampling applied everywhere would make a majority of legitimate rare queries invisible to the aggregation, not just noisy. The fix is asymmetric sampling: apply the uniform sampling rate only to already-popular ('head') prefixes to control processing volume, while counting long-tail prefixes (below some occurrence threshold) exactly, without sampling, until they've accumulated enough volume to be safely sampled.

## Q zh
在规模大得多、离线聚合管道需要对查询日志做下采样（比如均匀只保留 1% 的事件）的场景下，为什么均匀采样有可能悄悄丢掉真实存在的长尾查询词？修复方法是什么？

## A zh
一个全国范围内一天只被搜索 50 次的真实查询词，在 1% 均匀采样下期望只被采到 0.5 次；用泊松过程建模，这个查询词被采样到 0 次——因此在聚合计数里完全不出现——的概率约为 e^(-0.5)≈60.7%。如果对所有前缀一视同仁地均匀采样，大多数真实存在的长尾查询词会变得对聚合完全不可见，而不只是带噪声。修复方法是非对称采样：只对已经确认高频的头部前缀应用均匀采样比例来控制处理量，对计数还很低的长尾前缀（在越过某个出现次数阈值之前）保留全量计数，不做采样。
