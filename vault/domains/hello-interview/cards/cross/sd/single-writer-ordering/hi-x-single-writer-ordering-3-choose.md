---
id: hi-x-single-writer-ordering-3-choose
node: sd.cross.single-writer-ordering
type: qa
step: 3
---
## Q
**单写者、序号与版本排序**｜跨题模式 · 怎么选

给定一个新的「同一实体有并发事件」的设计题，怎样选择单写者、版本号、世代号或合并？列出判断信号，每个分支配一个例子。

## A
| 信号 | 选择 | 例子 |
|---|---|---|
| 实体小而强一致，事件少，状态可放内存 | 按实体 ID 哈希固定所有者，单线程串行，日志放外部，宕机后重放 | [[online-chess-platform\|在线国际象棋平台]] |
| 涉及金额的承诺，宁慢不可错 | 单一拥有者加数据库条件写入，世代号拒绝旧写者；不把易失缓存当唯一账本 | [[tt-realtime-auction-bidding\|实时竞价拍卖]] |
| 只要一个范围内有序 | 在该范围的分区内分配序号，客户端发现空洞再拉取 | [[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |
| 外部更新会乱序、重复 | 版本号加条件更新，消费端只接受更高版本，删除也带版本（墓碑） | [[merchant-product-listings\|商家商品上架与更新系统]] |
| 接收方是外部服务器，重试会打乱顺序 | 给版本号，让接收方排序；确需顺序时只在同一资源内串行 | [[tt-merchant-webhook-delivery\|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]] |
| 下游异步报告会乱序 | 按账户分区排下单与撤单，报告按 execId 去重，状态机只允许合法迁移 | [[stock-trading-platform\|设计简化版股票交易平台（券商端，限价单）]] |
| 多设备离线后追赶 | 提交带 baseVersion，游标追变更日志，冲突保留两份 | [[file-sync-system\|设计云盘与文件同步系统（Dropbox / Google Drive）]] |
| 多个用户同时改同一对象且要保留各自意图 | 服务端排序加属性粒度合并，预览不进历史 | [[figma-draw-api\|矢量图形编辑器的绘图 API（类 Figma）]] |
| 单进程内的流水线 | 专职线程加有界队列 | [[multithreaded-logging-framework\|多线程日志框架]] |

先问「顺序的范围多大」，范围越小，越容易用分区加序号解决。
