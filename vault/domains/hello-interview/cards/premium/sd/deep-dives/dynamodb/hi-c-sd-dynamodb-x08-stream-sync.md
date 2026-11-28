---
id: hi-c-sd-dynamodb-x08-stream-sync
node: sd.deep-dives.dynamodb.exam
type: qa
step: 9
---
## Q
**DynamoDB · 用 Streams 同步搜索索引**｜考点 · 追问

商品存在 DynamoDB，要做关键词搜索。设计一个用 Streams 同步到 Elasticsearch 的方案，并说出会出什么问题、怎么防。

## A
- **管道：** 商品表变更进入 Stream，触发 Lambda，Lambda 把新增、修改、删除映射为对 Elasticsearch 的写入和删除。
- **搜索查询：** 读搜索走 Elasticsearch 得到商品 ID，再回表取权威数据。
- **问题一：延迟。** 索引总比表晚几秒，刚改的商品搜不到或搜到旧值；这是最终一致，面试时要说明。
- **问题二：失败与重复。** Lambda 处理失败会重试，同一条记录可能多次到达，写入必须幂等：用商品 ID 做文档 ID，带版本号，旧版本不覆盖新版本。
- **问题三：漂移。** 偶发丢失会让两边慢慢不一致，要有定期全量校验或回补。
