---
id: craft-exception-family-3-value-or-exception
node: craft.idioms.exception-family
type: qa
step: 3
---
## Q
**异常家族 · 余额不足是返回值，键被复用才抛异常**｜写法

幂等转账里，余额不足被拒绝返回 `TransferResult("rejected")`，而同键不同内容却抛 `KeyReuse`。两种失败都是「没转成」，为什么一个走返回值、一个走异常？判据是什么？

## A
**要点。** 看调用方能不能把它当作一种正常结果。业务上预期会发生、调用方必须逐一处理的结果（余额不足、被限流、库存为零）是**值**：放进返回类型，调用方的类型检查器和 `match` 能提醒它别漏分支。调用方写错了、不可能被「处理掉」的情况（键被复用、参数非法）是**异常**：该让它沿调用栈冒到有能力修的地方。

```python
class TransferError(Exception): ...
class KeyReuse(TransferError):
    """调用方的 bug：同一个键配了不同内容。"""

@dataclass(frozen=True, slots=True)
class TransferResult:
    status: Literal["succeeded", "rejected"]
    reason: str | None = None

class Bank:
    def __init__(self, balance: int) -> None:
        self.balance, self.seen = balance, {}

    def transfer(self, key: str, amount: int) -> TransferResult:
        if key in self.seen and self.seen[key][0] != amount:
            raise KeyReuse(key)              # 调用方写错了：这是异常，不可能「正常」处理
        if key in self.seen:
            return self.seen[key][1]
        # 余额不足是业务的正常结果之一：返回值，并且要存进幂等表
        res = (TransferResult("succeeded") if self.balance >= amount
               else TransferResult("rejected", "insufficient_funds"))
        self.seen[key] = (amount, res)
        return res

b = Bank(10)
print(b.transfer("k1", 50))
print(b.transfer("k1", 50))                  # 同键重试：同一个答案，不用 try
try:
    b.transfer("k1", 60)
except KeyReuse as e:
    print("KeyReuse:", e)
```

实际输出：

```
TransferResult(status='rejected', reason='insufficient_funds')
TransferResult(status='rejected', reason='insufficient_funds')
KeyReuse: k1
```

**为什么。** 被拒绝的结果要存进幂等表并原样重放：它是值，才能存。异常不可能被存起来再返回给下一次重试。

**易错。** 反过来的错误也常见：把「找不到用户」这类每个调用方都得处理的情况抛成异常，调用处就到处是 `try`；把真正的编程错误写成返回码，调用方忘了检查就静默继续。
