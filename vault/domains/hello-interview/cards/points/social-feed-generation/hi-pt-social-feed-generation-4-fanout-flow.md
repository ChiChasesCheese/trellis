---
id: hi-pt-social-feed-generation-4-fanout-flow
node: qb.sd.social-feed-generation.points
type: qa
step: 3
---
## Q
**社交信息流生成系统 · 发帖到读取的整体流程**｜必会 · 出自：社交信息流生成系统 › 整体设计

从发帖到用户读到信息流，整条链路怎么走？

## A
**发帖。** 写帖子库（按 `post_id` 分片），发 Kafka `PostCreated`；扇出服务查粉丝列表，把 `post_id` 追加到粉丝收件箱（Redis 有序列表，裁到 800 条）。
**读取。** 候选一：收件箱；候选二：实时拉关注名人的近期帖子；候选三：推荐内容。合并去重后粗排到几百条，精排取前 50，多样性规则（同作者不连续），插入广告位，批量取详情返回一页。

```mermaid
flowchart TB
    subgraph W["发帖"]
        P["帖子库"] --> K["Kafka PostCreated"]
        K --> F["扇出服务：查粉丝列表"]
        F --> I["粉丝收件箱：Redis，裁到 800 条"]
    end
    subgraph R["读取"]
        C["三路候选：收件箱、名人近期帖、推荐"] --> M["合并去重"]
        M --> R1["粗排到几百条"]
        R1 --> R2["精排取前 50"]
        R2 --> D["多样性规则，插入广告位"]
        D --> O["批量取详情，返回一页"]
    end
```
