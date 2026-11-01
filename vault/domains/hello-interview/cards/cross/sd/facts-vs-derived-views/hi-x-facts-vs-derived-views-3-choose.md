---
id: hi-x-facts-vs-derived-views-3-choose
node: sd.cross.facts-vs-derived-views
type: qa
step: 3
---
## Q
**事实与派生视图**｜跨题模式 · 怎么选

新题里需要“读优化的数据”时，怎么决定该派生什么、用什么方式更新、容忍多旧？请按派生目的分情况说明，并各举一例。

## A
| 派生的目的 | 更新方式与新鲜度 | 例子 |
|---|---|---|
| 加速高频读（计数、榜单） | 写事实时产生增量事件，窗口内合并后写计数，延迟几秒；用户自己的状态走写穿立即可见 | [[like-unlike-system\|点赞与取消点赞（收藏）系统]] |
| 为浏览和搜索建索引 | CDC 事件驱动缓存和索引，版本号只接受更高版本，保底 TTL 兜底 | [[merchant-product-listings\|商家商品上架与更新系统]] |
| 保护线上库，不拖累请求 | CDC 导出到仓库，延迟几分钟对统计足够 | [[photo-storage-sharing\|照片存储与分享系统（Google Photos）]] |
| 要能出错重跑、可审计 | 批处理从事实重算，新结果写新批次后原子切换，旧结果留档 | [[tt-payment-reconciliation\|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]]、[[tt-live-gift-coin-settlement\|直播虚拟礼物：金币记账与主播结算]] |
| 长时间范围查询太贵 | 写入时或后台周期降采样，按查询范围选分辨率 | [[metrics-monitoring-alerts\|指标监控与告警平台]] |
| 读延迟要求极低，查询是排名 | 写入后预计算，分片内前 K 归并，缓存里保留略旧的结果兜底 | [[top-k-counts\|Top-K 热门榜（视频播放、歌曲、话题标签）]] |
| 读远多于写，下单必须精确 | 视图允许几十秒过期，下单时回到事实核验 | [[hotel-booking-system\|酒店预订系统（Expedia 型聚合与自营）]] |
