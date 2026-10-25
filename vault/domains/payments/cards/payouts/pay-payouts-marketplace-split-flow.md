---
id: pay-payouts-marketplace-split-flow
node: payouts.marketplace-split
type: qa
step: 5
---
## Q
一笔 USD 100.01 的平台订单从支付、分账、到买家全额退款，账本里每一步的分录是什么？如果卖家已经提走了钱，退款会怎样？

## A
科目：`psp_receivable`（渠道应收，资产）、`seller_payable`（应付卖家，负债）、`platform_fee_revenue`（平台佣金收入）、`bank_cash`（银行存款，资产）。佣金 12.5%，拆分结果：卖家 87.51，平台 12.50。为简化，忽略渠道手续费。

1. **支付成功**：借 psp_receivable 100.01；贷 seller_payable 87.51；贷 platform_fee_revenue 12.50。借贷相等，同一事务内写入。
2. **渠道结算到账**：借 bank_cash 100.01，贷 psp_receivable 100.01。
3. **卖家待结算期满，打款 87.51**：借 seller_payable 87.51，贷 bank_cash 87.51（经打款单流程）。

**情形 A：买家在卖家提现之前全额退款**
- 借 seller_payable 87.51；借 platform_fee_revenue 12.50；贷 psp_receivable（或 bank_cash）100.01。
- 卖家待结算余额减少 87.51，平台收入冲回。账平。

**情形 B：卖家已提现后，买家才全额退款**
- 同样的分录，但 seller_payable 此时已被打款清零，再借记 87.51 后变成**借方余额 87.51**，即卖家欠平台 87.51。
- 平台有三种办法：从卖家后续销售款里扣回；动用已扣留的保证金；联系卖家归还。都不行时，平台自己承担损失。

**要点**
- 退款的分录是原分账的镜像，按原比例冲回；若是部分退款，同样用最大余数法按比例拆。
- 卖家的 `seller_payable` 允许出现借方余额（负债变应收），要有单独监控。
- 所有分录引用原订单和退款单号，便于对账和审计。
