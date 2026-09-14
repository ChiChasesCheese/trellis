---
id: leetcode-c-kafka-weighted-partition-selection-application
node: topics.uncategorised
type: qa
anki: 1787359912893
tags: [algorithm::binary-search, algorithm::prefix-sum, algorithm::weighted-random-sampling, application, case, case::kafka-weighted-partition-selection, category::distributed-streaming, leetcode, system::apache-kafka]
---
## Q
Kafka BuiltInPartitioner 如何用 prefix sum + binary search 完成 weighted random partition selection？边界为何是第一个 cumulative > random？

## A
每个 partition 的 weight 被转成累积区间；在总权重内取随机整数，然后二分第一个 strictly greater 的 cumulative value。这个 index 就是随机点落入的权重区间。exact hit 要移动到下一段，因此不能直接把 Arrays.binarySearch 的非负结果当答案。

**Evidence**

Kafka 官方 BuiltInPartitioner 源码明确构建 sorted cumulativeFrequencyTable，并用 Arrays.binarySearch 后的 insertion-point 变换选择 partition。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FKafka%20%E5%8A%A0%E6%9D%83%E5%88%86%E5%8C%BA%E9%80%89%E6%8B%A9%EF%BC%9A%E5%89%8D%E7%BC%80%E5%92%8C%E5%8A%A0%E4%BA%8C%E5%88%86)
