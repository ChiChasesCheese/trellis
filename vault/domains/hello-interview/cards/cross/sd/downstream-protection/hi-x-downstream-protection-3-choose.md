---
id: hi-x-downstream-protection-3-choose
node: sd.cross.downstream-protection
type: qa
step: 3
---
## Q
**下游保护：熔断、隔离与扇出预算**｜跨题模式 · 怎么选

遇到一个依赖外部资源的设计题，怎么判断该用哪种下游保护？请按下游的特征分情况说明，并各举一例。

## A
| 下游的特征 | 手段 | 例子 |
|---|---|---|
| 会变慢或变坏，调用方有备选 | 熔断加降级；有备用通道就切换 | [[api-circuit-breaker\|熔断器（Circuit Breaker）]]、[[notification-system-scale\|通知系统（支持单发与群发，百万级每秒）]] |
| 很多租户或端点共用一条投递管道 | 按端点的并发额度、限速和熔断，恢复时慢启动加抖动，积压放存储 | [[tt-merchant-webhook-delivery\|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]] |
| 每次调用都花钱 | 缓存、请求合并、按期望收益选下游、搜索级预算，昂贵的确认动作后移 | [[flight-search-system\|设计机票搜索系统（多供应商聚合，按调用计费）]] |
| 对方有“礼貌”上限，不能被并发碰 | 按下游分队列，每个下游串行并按下次允许时间排序 | [[web-crawler-design\|网络爬虫（Web Crawler）]] |
| 容量固定且昂贵 | 并发上限加准入队列，等待过长就快速失败，支持取消回收 | [[chatbot-design\|对话式 AI 聊天服务（简化版 ChatGPT）]] |
| 调用不可逆，必须只成交一次 | 稳定的订单引用号保证幂等，超时进入“结果不明”后先查询再重试 | [[book-seller-platform\|图书比价代购平台（Book Seller Platform）]] |
