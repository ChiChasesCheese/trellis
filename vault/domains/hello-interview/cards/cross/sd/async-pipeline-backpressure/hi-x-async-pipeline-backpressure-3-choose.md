---
id: hi-x-async-pipeline-backpressure-3-choose
node: sd.cross.async-pipeline-backpressure
type: qa
step: 3
---
## Q
**异步流水线、背压与批量 (Async Pipeline / Backpressure / Batching)**｜跨题模式 · 怎么选

面对一道需要异步处理的新题，怎么决定队列的形状和满了以后的行为？请按判断信号分支，各举一题。

## A
1. **丢一条的代价是什么？** 承诺不丢（日志、提交、审核任务）：满了阻塞或拒绝，不丢弃。例：[[multithreaded-logging-framework|多线程日志框架]]、[[coding-contest-platform|在线判题与编程竞赛平台]]。允许少量丢（指标点）：满了丢最老的并记录丢弃计数，同时保证不长时间静默丢数据。例：[[metrics-monitoring-alerts|指标监控与告警平台]]。
2. **单个任务占用资源很久吗？** 是：按并发路数设上限，排队，等待超阈值就拒绝，取消时回收资源。例：[[chatbot-design|对话式 AI 聊天服务]]。
3. **有没有不同重要性的流量混在一起？** 是：物理隔离（独立队列、独立消费者池），每个环节检查过期。例：[[notification-system-scale|通知系统]]；批量让路给单条的例子见 [[merchant-product-listings|商家商品上架与更新系统]]。
4. **瓶颈在外部对象的承受力吗？** 是：按被保护的对象分队列（主机、渠道、商家），而不是按处理能力。例：[[web-crawler-design|网络爬虫]]。
5. **各阶段成本差别大、逻辑常改吗？** 是：事件流加持久中间产物，阶段独立伸缩，改了只重跑那一段。例：[[video-moderation-system|视频内容审核系统]]。
6. **事件来自用户界面，频率远高于需要吗？** 是：每帧最多处理一次，区分预览和提交，只提交的才进入撤销与同步。例：[[figma-draw-api|矢量图形编辑器的绘图 API]]。
