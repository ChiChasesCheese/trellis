---
id: pay-landscape-parties-psp-gateway-payfac
node: landscape.parties
type: qa
step: 4
---
## Q
支付网关、处理器、PSP、支付便利商（PayFac）这几个词分别指什么？区别在哪里？

## A
- **支付网关**（payment gateway）：商户系统调用的接入层。接收下单请求，加密卡数据，转发给处理器，把结果返回商户。可以理解为"收银台的接口"。
- **处理器**（processor）：真正和卡组织、发卡行网络通信的一方，负责授权报文、清算文件、结算对账。
- **收单行**（acquirer）：持有卡组织成员资质并承担商户风险的银行。处理器可以是收单行自己，也可以是它外包的技术方。
- **PSP**（payment service provider，如 Stripe、Adyen）：把网关、处理器连接、风控、对账、打款打包成一个产品，商户只集成一次。
- **PayFac**（payment facilitator）：自己向收单行申请一个大的"主商户"账户（master merchant），让成千上万个子商户（sub-merchant）无需逐个审核就能入网。资金先进 PayFac，由它分发给子商户，同时它承担子商户的风险和合规责任。

区别的核心是**谁承担风险、钱先到谁手里**。传统 PSP 模式下商户各有商户账户；PayFac 模式下 PayFac 是法律上的收款方，必须有分账、风控、保证金能力。TikTok Shop 这类市场平台在资金角色上接近 PayFac：买家的钱先到平台，平台再结算给卖家。
