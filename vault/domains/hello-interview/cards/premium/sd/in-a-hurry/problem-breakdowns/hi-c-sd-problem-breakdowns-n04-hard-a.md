---
id: hi-c-sd-problem-breakdowns-n04-hard-a
node: sd.in-a-hurry.problem-breakdowns.notes
type: qa
step: 4
---
## Q
**常见题目拆解 · 困难题上半（7 道）**｜摘要 · 必会

困难级的 YouTube Top K、Uber、Robinhood、Google Docs、Web Crawler、Ad Click Aggregator、FB Post Search 各自的考点是什么？

## A
- **YouTube Top K：** 海量事件流上的近似计数（count-min sketch 一类的数据结构）、时间窗口、预聚合与精确 / 近似的取舍。
- **Uber：** 位置高频上报、地理空间匹配、同一个司机被多人叫的竞争、行程状态的实时推送。
- **Robinhood：** 行情实时推给大量用户、订单提交的可靠与一致、自选股和资产计算。
- **Google Docs：** 协同编辑：OT（操作变换）或 CRDT 合并并发修改，同一文档的用户落到同一台有状态服务器。
- **Web Crawler：** 待爬取队列、礼貌（限制对同一站点的频率）、URL 去重、失败重试与规模扩展。
- **Ad Click Aggregator：** 流处理做点击聚合、精确一次与去重、热点广告、离线对账。
- **FB Post Search：** 搜索索引的构建与分片、索引新鲜度、排序和相关性。
