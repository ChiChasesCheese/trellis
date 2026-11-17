---
id: fsm-illegal-transitions-idempotency-key
node: fsm.illegal-transitions
type: qa
step: 3
---
## Q
还款已经禁止超额。客户端超时后把同一笔 20 元的还款又发了一次，剩余金额 100 并不超额。状态检查拦得住吗？

## A
**禁止超额不等于幂等，要靠幂等键**

- **状态检查拦不住**：第二次的 20 在状态机里是合法的，它和“用户真的又还了 20”无法区分；
- **幂等键**：客户端给每次意图一个编号，服务记下编号与第一次的结果；
- **重放**：同一个编号再来，直接返回第一次的结果，不再扣款；
- **键和结果一起存**：记录与状态变更在同一个事务里提交，否则崩溃后记录和状态对不上。

```python
class Loan:
    def __init__(self): self.remaining, self.seen = 100, {}

    def repay(self, amount, key=None):
        if key in self.seen: return self.seen[key]          # 重放：第一次的结果
        if not 0 < amount <= self.remaining: raise ValueError("illegal")
        self.remaining -= amount
        if key is not None: self.seen[key] = self.remaining
        return self.remaining

a, b = Loan(), Loan()
print(a.repay(20), a.repay(20))                  # 80 60：重发被当成新的还款
print(b.repay(20, key="p1"), b.repay(20, key="p1"))     # 80 80
```

**知识点：**非法转移与幂等（Illegal Transitions）
