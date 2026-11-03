---
id: craft-dependency-direction-consumer-owns-interface-2-missing-method
node: craft.architecture.dependency-direction-consumer-owns-interface
type: qa
step: 2
---
## Q
**依赖方向 · 接口里「没有」的方法也是设计**｜架构

ATM 的余额由银行说了算，ATM 自己不该有任何办法改账户。银行网络接口 `BankNetwork` 里故意没有 `get_account()`。测试用的假银行为了方便，往往有后门可以直接取账户对象。这个「没有」到底怎么防止 ATM 写错？运行时能防住吗？

## A
**要点。** 接口是使用方能做的事的全集：类型检查器只允许通过接口声明的方法访问对象，接口里没有，就写不出来。「余额归银行」从一句口号变成了结构：ATM 拿到的是 `BankNetwork`，够不到账户对象。注意这是静态保证，运行时的 Python 不拦。

```python
from typing import Protocol

class BankNetwork(Protocol):                     # ATM 能问银行的全部问题
    def withdraw(self, account_id: str, amount: int, ref: str) -> int: ...
    def balance(self, account_id: str) -> int: ...

class Account:
    def __init__(self) -> None:
        self.balance = 100

class FakeBank:
    def __init__(self) -> None:
        self.accounts = {"acc-1": Account()}
    def withdraw(self, account_id: str, amount: int, ref: str) -> int:
        self.accounts[account_id].balance -= amount
        return self.accounts[account_id].balance
    def balance(self, account_id: str) -> int:
        return self.accounts[account_id].balance
    def get_account(self, account_id: str) -> Account:   # 测试后门
        return self.accounts[account_id]

class ATM:
    def __init__(self, network: BankNetwork) -> None:
        self._network = network
    def cheat(self) -> None:
        self._network.get_account("acc-1").balance = 10**9   # 想直接改余额

ATM(FakeBank()).cheat()                          # 运行时能过：后门还在
```

把上面的脚本存成 `demo.py`，`mypy --strict` 的实际输出（直接运行脚本不报错，后门还在）：

```
demo.py:26: error: "BankNetwork" has no attribute "get_account"  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
```

**为什么。** 券商的订单簿同理：它只认股数、价格、先后，不认钱，所以资金规则换了（融资融券、手续费）撮合代码一行不动，撮合也能脱离账户单独测。

**易错。** 接口里每多一个方法，所有适配器都要多实现一个，使用方也多一条可以违规的路。新增方法前先问：消费者现在真的用得到吗。
