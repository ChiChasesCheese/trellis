---
id: pay-risk-compliance-chargebacks-flow
node: risk-compliance.chargebacks
type: qa
step: 5
---
## Q
一笔 USD 80.00 的虚拟币充值被拒付后，平台的账本和流程是怎么走的？应诉成功和失败各是什么账务结果？

## A
科目：`psp_receivable`（渠道应收）、`chargeback_receivable`（拒付待追回，资产）、`chargeback_loss`（拒付损失，费用）、`dispute_fee_expense`（争议费，费用）、`coin_liability`（用户金币负债）。假设争议费 15.00（仅演算用）。

1. **3 月 5 日 支付成功**：借 psp_receivable 80.00，贷 coin_liability 80.00（用户已获得金币）。
2. **3 月 7 日 渠道结算到账**：借 bank_cash 80.00（扣除手续费另记），贷 psp_receivable 80.00。
3. **4 月 20 日 收到拒付**（原因码：未授权交易）：渠道从结算款里扣回 80.00 和 15.00。借 chargeback_receivable 80.00，借 dispute_fee_expense 15.00，贷 psp_receivable 95.00。同时处理业务侧：冻结账号、回收尚未花掉的金币。
4. **4 月 21 日 起 应诉**：系统自动汇集证据：3DS 记录、登录设备与 IP、金币消费记录。在渠道截止日之前提交。
5. **结果 A：5 月 20 日 应诉成功**：渠道返还 80.00。借 psp_receivable 80.00，贷 chargeback_receivable 80.00。争议费 15.00 通常不返还。
6. **结果 B：应诉失败**：确认损失。借 chargeback_loss 80.00，贷 chargeback_receivable 80.00。总损失 95.00。

**要点**
- 拒付时用"待追回"科目暂挂，应诉结果出来前不确认损失，避免利润来回波动。
- 如果是电商平台，卖家侧要同步回滚分账，向卖家追偿。
- 每一步都引用原交易和拒付案件号，保证可追溯。
- 业务侧动作（回收权益、冻结账号）和账务动作要作为同一案件的两部分，一起触发。
