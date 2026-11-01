---
id: hi-x-fan-out-write-vs-read-3-choose
node: sd.cross.fan-out-write-vs-read
type: qa
step: 3
---
## Q
**写扩散与读聚合**｜跨题模式 · 怎么选

面对一道新的「一对多送达」题，怎样决定写扩散、读聚合、混合还是懒扇出？列出判断信号，每个分支给一个例子。

## A
| 信号 | 选择 | 例子 |
|---|---|---|
| 读远多于写，且来源的读者数极不均匀 | 混合：普通来源写扩散，粉丝极多的来源读时拉（阈值如 10 万粉丝），不活跃用户跳过 | [[twitter-clone-feed\|微博客与个性化信息流（Twitter）]]、[[social-feed-generation\|社交信息流生成系统（News Feed）]] |
| 读者共享同一份内容 | 读聚合加缓存，不做每用户写扩散 | [[news-aggregator-feed\|设计新闻聚合系统（Google News）]] |
| 接收者人数有上限，要离线补收 | 写扩散到持久收件箱，用游标补收；超大群改读 | [[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |
| 接收者是外部通道，要受速率约束 | 懒扇出：一条记录加游标，按配置速率分页展开，关键与群发隔离 | [[notification-system-scale\|通知系统（支持单发与群发，百万级每秒）]] |
| 触发是稀疏事件，接收者极多 | 分区内先判断触发，触发后分块并行发送，加防抖 | [[stock-price-alerts\|股票价格提醒系统]] |
| 推的是会被覆盖的状态值 | 不要持久收件箱：按主题广播，合并成最新快照，带版本号，重连拉快照 | [[tt-realtime-auction-bidding\|实时竞价拍卖]] |

排序和广告这类昂贵步骤，放在读取时对少量候选做，而不是写进每个人的收件箱。
