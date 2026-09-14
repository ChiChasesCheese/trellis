---
id: s24-payments-domain-vocab
node: stripe.vocab
type: qa
---

## Q
Stripe OA 题面里那些支付领域词汇（charge、dispute、BIN、reserve……）分别是什么意思？看不懂这些词就读不懂题目规格。

## A
看不懂业务词就读不懂规格。最小词表：

| 词 | 含义 |
|---|---|
| charge | 一笔扣款 |
| dispute / chargeback | 持卡人向发卡行发起的争议，会把钱扣回去 |
| refund | 商户主动退款（与 dispute 不同） |
| payout | Stripe 把余额打给商户 |
| MCC | Merchant Category Code，商户品类码（4 位数字） |
| BIN | 卡号前 6–8 位，决定发卡行和卡组织 |
| Luhn | 卡号校验算法 |
| idempotency key | 幂等键，重复请求只生效一次 |
| minor units | 最小货币单位（分） |
| zero-decimal currency | 没有"分"的货币（JPY、KRW） |
| proration | 中途变更时按比例计费 |
| Connect / platform / connected account | 平台模式：平台代收，再分账给子账户 |
| Radar | Stripe 的风控规则引擎 |
| KYC | 商户身份/资质核验 |
| reserve | 平台冻结的一部分余额 |
| statement descriptor | 出现在持卡人账单上的商户名 |
