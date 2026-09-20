---
id: problems-search-engine-doc-vs-term-partitioning-zipf-skew
node: problems.search.search-engine
type: qa
step: 2
tags: [grown]
---
## Q
In a sharded inverted index, why does partitioning by term (so a query only needs to visit the few shards holding its query terms) get rejected in favor of partitioning by document, even though document partitioning forces every query to visit every shard?

## A
Term frequencies follow a Zipfian distribution: for a 200,000-term vocabulary, the single most frequent term accounts for about 1/H(200000) ≈ 7.8% of all query-term traffic, while an even split across 200,000 single-term shards would give each shard a 'fair' share of only 0.0005% — meaning the hottest term's shard would receive roughly 15,645x the load of an average shard. Adding more term-shards never fixes this, because the hot term always lands on exactly one shard. Document partitioning avoids this entirely: every shard gets a uniform slice of both storage and query load regardless of which terms are popular, at the cost of a wider, but load-balanced, query fan-out.

## Q zh
在一个分片的倒排索引里，为什么'按词项分片'（一次查询只需要访问持有查询词的少数几个分片）会被放弃，转而选择'按文档分片'（即使这意味着每次查询都要访问全部分片）？

## A zh
词频服从幂律分布（Zipf 分布）：对一个 20 万词的词表，最高频的单个词项约占全部查询词流量的 1/H(200000) ≈ 7.8%，而如果把 20 万个单词项均匀切成 20 万个分片，每个分片'公平'应得的份额只有 0.0005%——意味着最热词项所在的分片实际承受约 15,645 倍于平均分片的负载。增加更多按词项切分的分片永远解决不了这个问题，因为热词永远只落在它自己那一个分片上。按文档分片则完全规避了这个问题：无论哪个词流行，每个分片都获得均匀的一份存储和查询负载，代价是查询扇出更宽，但负载是均衡的。
