---
id: pay-payouts-failures-returns-flow
node: payouts.failures-returns
type: qa
step: 4
---
## Q
一笔 USD 300.00 的 ACH 打款在被标记为"已发出"两天后被收款银行退票，时间线和账本分录是怎样的？

## A
账户：`creator_payable`（欠创作者，负债）、`payout_in_transit`（打款在途，负债）、`bank_cash`（平台银行存款，资产）。

**时间线**
1. **周一**：创作者提现 300.00。借 creator_payable 300.00，贷 payout_in_transit 300.00。状态 `created`。
2. **周一下午**：提交 ACH 批次，状态 `submitted`。
3. **周二**：渠道回执"已发出"，打款单变 `paid`，分录：借 payout_in_transit 300.00，贷 bank_cash 300.00。创作者看到"已发出"。
4. **周四**：收款银行发回退票，原因"账户已关闭"。银行流水里平台的账户收到 300.00。
5. **周四处理**：
   - 状态 `paid` → `returned`，记录退票原因码。
   - 分录一：借 bank_cash 300.00，贷 payout_in_transit 300.00（钱回来了，重新成为在途负债）。
   - 分录二：借 payout_in_transit 300.00，贷 creator_payable 300.00（钱还给创作者的可提现余额）。
6. **通知用户**：收款账户无效，请更新。账户标记为"需要重新验证"，更新前不能再次提现，避免重复退票。

**要点**
- 钱始终守恒：任何时刻 creator_payable + payout_in_transit + 已付出的钱，等于应付总额。
- 退票分录引用原打款单，形成可追溯链条。
- 如果创作者已经把余额提空，退回的钱重新入账并不意味着对方多拿了钱，因为原来的 300.00 并没有到他手里。
- 退票到账后可选择自动重新打款，但必须等账户更新并经验证，且生成新的打款单与新的引用号。
