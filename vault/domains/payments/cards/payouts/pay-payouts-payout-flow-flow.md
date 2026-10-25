---
id: pay-payouts-payout-flow-flow
node: payouts.payout-flow
type: qa
step: 4
---
## Q
创作者提现 USD 300.00 的完整流程是怎样的？请写出每一步的状态变化和对应的账本分录。

## A
账户设定：`creator_payable`（平台欠创作者的钱，负债），`payout_in_transit`（已申请提现、尚未到账的款项，负债），`bank_cash`（平台银行存款，资产）。

1. **申请**：校验可提现额度 ≥ 300.00，创建打款单 po_1，状态 `created`，幂等键为（用户 ID、提现请求 ID）。同一事务内写入分录：借 creator_payable 300.00，贷 payout_in_transit 300.00。钱从"可提现"占住，用户余额立刻减少。
2. **风控与合规检查**：收款账户有效、制裁筛查通过、单日限额内。不通过则转入 `rejected`，冲正第 1 步分录。
3. **提交渠道**：打款单 `created` → `submitted`，带上打款单号作为渠道的幂等引用，调用渠道接口。保存渠道返回的引用号。
4. **到账确认**：渠道回调或查询确认成功，`submitted` → `paid`。分录：借 payout_in_transit 300.00，贷 bank_cash 300.00。
5. **失败**：渠道明确失败，`submitted` → `failed`，分录：借 payout_in_transit 300.00，贷 creator_payable 300.00，钱回到用户可提现余额。

**要点**
- 第 1 步的账本动作和打款单创建在同一个数据库事务里，保证"钱被占住"与"有打款单"同生同灭。
- 对外调用在事务之外，通过 outbox 或调度异步触发，超时则查询，不重发。
- 任何时刻 creator_payable + payout_in_transit 的总和，等于平台对该用户的应付总额，钱不会凭空消失或重复。
