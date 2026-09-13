---
id: s17-ledger-balance-tracking
node: stripe.balances-limits
type: qa
---

## Q
为什么台账式余额跟踪是 Stripe OA 的常客？不变量该怎么定义，拒绝路径最容易在哪一步翻车？

## A
**为什么考**：Stripe 的核心业务就是账。

**不变量优先**（写在类的注释里，然后在每个方法末尾维持它）：

```
balance == sum(credits) - sum(debits)
balance >= 0        （除非题面允许透支 / 有平台授信额度）
```

**做法**：

```python
def debit(self, acct, cents):
    if self.bal[acct] < cents:            # 严格还是非严格？看题面
        return f"REJECTED:{acct}"         # 拒绝时**不要**修改余额
    self.bal[acct] -= cents
    return None
```

**两个常见变体**：
- **平台授信**：余额不足时可以向平台借，但借款总额有上限 `MAX_RESERVE`。
- **储备金**：一部分余额被冻结，可用余额 = 余额 − 储备。

**典型翻车**：拒绝的路径上改了余额（先扣再判断再加回来，中间抛异常就漏了）。
**先判断，后修改。**
