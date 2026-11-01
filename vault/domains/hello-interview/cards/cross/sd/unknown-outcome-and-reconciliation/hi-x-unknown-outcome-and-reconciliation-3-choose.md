---
id: hi-x-unknown-outcome-and-reconciliation-3-choose
node: sd.cross.unknown-outcome-and-reconciliation
type: qa
step: 3
---
## Q
**结果未知与对账修复**｜跨题模式 · 怎么选

遇到「两边可能对不上」的新设计题，怎样决定用回查、对账还是重算？按什么信号分支，各举一例。

## A
先问三件事：对方是不是外部系统、调用有没有副作用、差异的代价多大。

| 信号 | 做法 | 例子 |
|---|---|---|
| 外部调用超时，副作用不明 | 先写意图，进 UNKNOWN，按引用号查询；查不到就冲正 | [[payment-batch-processing\|设计支付处理系统（授权冻结 + 每日批量结算）]] |
| 对方能查询 | 同步确认加轮询，查到什么就补成什么 | [[donations-website-charities\|设计限时捐款网站]] |
| 对方是撮合方，状态会变 | 引用号加执行报告，收盘后再对账，取消与成交以最终回执为准 | [[stock-trading-platform\|设计简化版股票交易平台（券商端，限价单）]] |
| 要证明钱真的到了 | 多方独立来源对账，现金层靠批次号桥接 | [[tt-payment-reconciliation\|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]] |
| 自己的实时路径与批路径并存 | 批处理重算当真相，实时数字标「预估」，差异超阈值报警 | [[tt-live-gift-coin-settlement\|直播虚拟礼物：金币记账与主播结算]] |
| 迁移或双写 | 每天比对新旧结果，差异清零再切读 | [[tt-wallet-ledger-service\|钱包与复式账本服务（余额、冻结、转账、多币种）]] |
| 接收方要追上发送方 | 游标补拉加手动重发 | [[tt-merchant-webhook-delivery\|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]] |
| 派生计数，错一点无所谓 | 定期从事实表重算 | [[like-unlike-system\|点赞与取消点赞（收藏）系统]] |

规律：金额越大、对方越不可控，越要「先写意图、保留 UNKNOWN、独立对账」；差异代价越低，越可以降级为定期重算。
