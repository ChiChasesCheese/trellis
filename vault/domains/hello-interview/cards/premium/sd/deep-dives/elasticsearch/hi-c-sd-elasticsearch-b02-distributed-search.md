---
id: hi-c-sd-elasticsearch-b02-distributed-search
node: sd.deep-dives.elasticsearch.beyond
type: qa
step: 2
---
## Q
**Elasticsearch · 分布式搜索的深度翻页成本与相关性打分**｜拓展 · 加分

多个分片并行搜索，结果怎么合并？为什么深翻页的代价是分片数倍增？相关性分数在分片间可比吗？

## A
- **分散—汇总（scatter-gather）：** 协调节点把请求发给每个相关分片；每个分片本地取前 `from + size` 条返回 ID 与分数，协调节点合并排序，再到对应分片取回前 `size` 条的文档内容。
- **深翻页的代价：** 每个分片都要返回前 `from + size` 条，所以总传输量约为分片数 × (`from + size`)，页码越深、分片越多越贵，这就是 `from/size` 默认限制在 1 万条的原因。
- **相关性：** 现代版本默认的打分算法是 BM25（词频与文档长度归一的改进），比经典 TF-IDF 更稳；"与 TF-IDF 密切相关"可以作为入门说法。
- **分片间的统计差异：** 默认每个分片用自己本地的词统计打分，分片数据不均时同一个词在各分片的权重不同，分数不完全可比；可用 `dfs_query_then_fetch` 先收集全局统计，代价是多一轮通信。
