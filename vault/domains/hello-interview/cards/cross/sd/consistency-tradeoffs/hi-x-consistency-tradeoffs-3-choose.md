---
id: hi-x-consistency-tradeoffs-3-choose
node: sd.cross.consistency-tradeoffs
type: qa
step: 3
---
## Q
**强一致与最终一致的取舍**｜跨题模式 · 怎么选

拿到一份数据，怎么决定它走强一致还是最终一致、窗口多大、怎么兜底？请按判断信号分情况说明，并各举一例。

## A
| 判断信号 | 一致性选择 | 例子 |
|---|---|---|
| 是钱或余额，不能为负 | 强一致：条件更新加账本，展示余额可异步 | [[tt-wallet-ledger-service\|钱包与复式账本服务（余额、冻结、转账、多币种）]] |
| 要求唯一或只发生一次 | 强一致：主键或唯一约束，不靠程序逻辑 | [[food-item-reviews\|设计带打赏的菜品评价系统（点评 + 投票 + 达标付款）]]、[[url-shortener-design\|短链接服务（URL Shortener / TinyURL）]] |
| 是别人看到的聚合数字 | 最终一致，窗口几秒；可近似；用事实表每天对账 | [[like-unlike-system\|点赞与取消点赞（收藏）系统]] |
| 读极多写极少，下单才要精确 | 读视图可偏旧，写路径最后一步强一致，下单前再核验 | [[hotel-booking-system\|酒店预订系统（Expedia 型聚合与自营）]] |
| 多设备或多副本之间的视图 | 提交点强一致，其余靠游标追赶收敛 | [[file-sync-system\|设计云盘与文件同步系统（Dropbox / Google Drive）]] |
| 展示数字与结算数字不同 | 展示标预估，结算由事件重算并比对 | [[tt-live-gift-coin-settlement\|直播虚拟礼物：金币记账与主播结算]] |
| 缓存加数据库两份副本，被追问要强一致 | 缓存做不到，强一致的读绕过缓存读主库，或用版本号保护回填 | [[tt-cache-consistency-hot-keys\|缓存一致性与热点 Key]] |
