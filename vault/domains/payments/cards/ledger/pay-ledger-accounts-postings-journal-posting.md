---
id: pay-ledger-accounts-postings-journal-posting
node: ledger.accounts-postings
type: qa
step: 3
---
## Q
journal（交易）和 posting（分录）各存什么？一笔含手续费的支付落到表里是什么样？

## A
**journal**（一次业务事件）
- `journal_id`
- `kind`：payment_captured、refund、payout、fee_adjustment 等
- `reference`：业务单据，如 `payment:p_1`
- `idempotency_key`：唯一，防止同一事件重复记账
- `created_at`（记账时间）、`effective_at`（生效时间）
- 可选：`reverses_journal_id`（冲正指向）

**posting**（一行变动）
- `journal_id`、`line_no`
- `account_id`
- `amount`：有符号整数，借为正、贷为负
- `currency`
- 约束：同一 journal 内按币种分别求和为零

**示例**：支付 p_1，100.00 美元，手续费 2.90，请款成功。

journal `J1`（kind=payment_captured，reference=payment:p_1）：
| line | account | amount |
|---|---|---|
| 1 | channel:psp_a:receivable:USD | +10000 |
| 2 | merchant:88:payable:USD | −9710 |
| 3 | platform:fee_revenue:USD | −290 |

**要点**
- 余额 = 账户所有 posting 的和；它们只追加不修改。
- 幂等键让相同事件的重复写入撞唯一约束，被识别为已记账。
- 冲正 journal 的每一行与原 journal 对应行方向相反，并指回原 journal。
