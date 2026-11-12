---
slug: simple-bank-system
---
## Q
**LC 2043 简易银行系统**｜Medium

`n` 个账户编号 `1..n`，实现 `transfer`、`deposit`、`withdraw`：账户须存在且转出或取款的余额足够才算有效，成功返回 `true`。

## A
**一句话。** 每个方法先校验全部条件，通过后再改余额，编号从 1 开始所以访问时减 1。

```python
class Bank:
    def __init__(self, balance):
        self.b = balance
        self.n = len(balance)

    def ok(self, acc):                 # 账户是否存在
        return 1 <= acc <= self.n

    def transfer(self, a1, a2, money):
        if not (self.ok(a1) and self.ok(a2)):
            return False
        if self.b[a1 - 1] < money:     # 先校验再改
            return False
        self.b[a1 - 1] -= money
        self.b[a2 - 1] += money
        return True

    def deposit(self, acc, money):
        if not self.ok(acc):
            return False
        self.b[acc - 1] += money
        return True

    def withdraw(self, acc, money):
        if not self.ok(acc) or self.b[acc - 1] < money:
            return False
        self.b[acc - 1] -= money
        return True
```

**复杂度。** 时间 每个操作 `O(1)`，空间 `O(n)`。

**易错点。**
- 忘了下标减 1：5 个账户时 `transfer(5, 1, 20)` 访问 `b[5]` 越界。
- 上界写成 `< n`：账户 `n` 被误判为不存在。
- 转账只查转出方存在：`transfer(5, 10, 1)` 应返回 `False` 且不能先扣账户 5。

**追问。**
- 要支持并发？：每个账户一把锁，转账按账户编号从小到大加锁以免死锁。
- 要记录交易流水？：每次成功操作追加一条记录，余额可由流水回放校验。

**同模式。** LC 146 LRU 缓存、LC 1396 设计地铁系统、LC 2241 设计一个 ATM 机、LC 635 设计日志存储系统
