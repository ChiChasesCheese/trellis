---
id: hi-x-observer-pubsub-3-choose
node: sd.cross.observer-pubsub
type: qa
step: 3
---
## Q
**观察者与发布订阅**｜跨题模式 · 怎么选

新题里出现“某件事发生后要通知别人”，怎么决定发布订阅的形态？请按订阅者的特征分情况说明，并各举一例。

## A
| 订阅者的特征 | 形态 | 例子 |
|---|---|---|
| 进程内，几个固定渠道 | 观察者或事件总线，订阅者各自注册；主流程不关心失败 | [[job-board-platform\|招聘信息平台（Job Board）]]、[[beverage-vending-system\|多地点饮品自助售卖系统]] |
| 触发条件是阈值或水位 | 边沿触发加去重：状态转换才发布，已有未关闭任务不重复生成 | [[beverage-vending-system\|多地点饮品自助售卖系统]]、[[stock-price-alerts\|股票价格提醒系统]] |
| 订阅者数量极大 | 订阅者名单分块存储，触发拆成多个“发送这一块”的任务并行，受通知服务限流 | [[stock-price-alerts\|股票价格提醒系统]] |
| 公司内多个业务方，多种渠道 | 平台级发布订阅：关键与促销物理隔离，去重，过期检查，回执 | [[notification-system-scale\|通知系统（支持单发与群发，百万级每秒）]] |
| 订阅者是外部服务器 | 投递表加重试调度，签名、事件编号、按端点隔离，商户自己去重 | [[tt-merchant-webhook-delivery\|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]] |
| 发布订阅只负责路由加速 | 允许丢，由持久收件箱、游标补收兜底 | [[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |
