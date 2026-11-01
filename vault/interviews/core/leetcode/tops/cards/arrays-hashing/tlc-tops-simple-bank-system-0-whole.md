---
id: tlc-tops-simple-bank-system-0-whole
node: arrays-hashing.simple-bank-system
type: qa
---
## Q
**LC 2043 简易银行系统（Simple Bank System）**｜Medium · 全公司热度第 228 名

银行共有 `n` 个账户，编号从 `1` 到 `n`，初始余额存储在下标从 0 开始的数组 `balance` 中（第 `i + 1` 个账户的余额是 `balance[i]`）。执行所有**有效**交易：指定的账户编号在 `1` 和 `n` 之间，且取款或转账需要的钱的总数小于或等于账户余额。实现 `Bank` 类：`Bank(long[] balance)` 初始化；`boolean transfer(int account1, int account2, long money)` 从 `account1` 向 `account2` 转账 `money` 美元；`boolean deposit(int account, long money)` 存款；`boolean withdraw(int account, long money)` 取款；交易成功返回 `true`，否则返回 `false`。`n == balance.length`，`1 <= n, account, account1, account2 <= 10^5`，`0 <= balance[i], money <= 10^12`，三个操作各最多调用 `10^4` 次。例：`Bank([10,100,20,50,30])`，`withdraw(3,10)` → `true`；`transfer(5,1,20)` → `true`；`deposit(5,20)` → `true`；`transfer(3,4,15)` → `false`（账户 3 余额只剩 10）；`withdraw(10,50)` → `false`（账户 10 不存在）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 设计题：数组存余额，每个操作先校验（账户存在、余额足够），再修改。

**一句话。** 每个方法都是「先校验全部条件，通过了再改余额」，编号从 1 开始所以访问时减 1。

**识别。** 「按编号查账户并增减」是数组下标访问，`O(1)`；难点只有校验顺序和下标偏移，不是算法。

**推导。** 没有需要优化的地方：账户编号稠密，直接用列表（不用字典）。关键是原子性：转账要先确认两个账户都存在、转出方余额够，之后才两次改动，不能改一半发现失败。

```python
class Bank:
    def __init__(self, balance: list[int]) -> None:
        self.balance = balance
        self.n = len(balance)

    def _exists(self, account: int) -> bool:
        return 1 <= account <= self.n

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if not (self._exists(account1) and self._exists(account2)):   # 两个账户都要存在
            return False
        if self.balance[account1 - 1] < money:                        # 转出方余额要够
            return False
        self.balance[account1 - 1] -= money
        self.balance[account2 - 1] += money
        return True

    def deposit(self, account: int, money: int) -> bool:
        if not self._exists(account):                                 # 存款只看账户是否存在
            return False
        self.balance[account - 1] += money
        return True

    def withdraw(self, account: int, money: int) -> bool:
        if not self._exists(account) or self.balance[account - 1] < money:
            return False
        self.balance[account - 1] -= money
        return True
```

运行：示例五次操作依次得到 `[True, True, True, False, False]`。账户 `1` 转给自己：`transfer(1,1,5)` 在余额 `>= 5` 时为 `True`，余额不变。

**复杂度。** 构造 `O(1)`（直接持有传入的列表），每个操作时间 `O(1)`，空间 `O(n)`。

**拓展优化。**
- 多线程并发：每个账户一把锁；转账要同时拿两把锁，必须**按账户编号从小到大加锁**，否则 `transfer(1,2)` 和 `transfer(2,1)` 同时执行会互相等待造成死锁。

```python
import threading


class ThreadSafeBank:
    def __init__(self, bank: Bank) -> None:
        self.bank = bank
        self.locks = [threading.Lock() for _ in bank.balance]    # 每个账户一把锁，互不相干的账户可以并行

    def deposit(self, account: int, money: int) -> bool:
        if not self.bank._exists(account):
            return False
        with self.locks[account - 1]:
            return self.bank.deposit(account, money)

    def withdraw(self, account: int, money: int) -> bool:
        if not self.bank._exists(account):
            return False
        with self.locks[account - 1]:
            return self.bank.withdraw(account, money)

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if not (self.bank._exists(account1) and self.bank._exists(account2)):
            return False
        first, second = sorted((account1, account2))  # 永远按编号从小到大加锁，避免两笔反向转账互相等待（死锁）
        with self.locks[first - 1]:
            if first == second:                       # 同一账户只能锁一次
                return self.bank.transfer(account1, account2, money)
            with self.locks[second - 1]:
                return self.bank.transfer(account1, account2, money)
```

- 需要审计：另存一份交易流水（时间、类型、金额），余额可由流水回放得到。

**易错点。**
- 忘记下标减 1：`transfer(5, 1, 20)` 会访问 `balance[5]`，抛 `IndexError`（5 个账户的下标只有 `0..4`）；账户编号上界要写成 `<= n`，写成 `< n` 会让账户 `n` 被误判为不存在。
- 转账只检查转出账户存在：`transfer(5, 10, 1)` 目标账户 `10` 不存在，应返回 `False`，且不能已经扣掉账户 5 的钱。

**同模式。** LC 146 LRU 缓存、LC 1396 设计地铁系统、LC 2241 设计一个 ATM 机、LC 635 设计日志存储系统。
