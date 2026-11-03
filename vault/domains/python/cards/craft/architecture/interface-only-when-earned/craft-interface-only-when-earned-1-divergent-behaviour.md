---
id: craft-interface-only-when-earned-1-divergent-behaviour
node: craft.architecture.interface-only-when-earned
type: qa
step: 1
---
## Q
**接口是挣来的 · 什么时候该写 Protocol**｜架构

自动售货机支持投硬币和刷卡。状态机只关心「付款成交」「取消退款」这两件事。如果直接在各处写 `if kind == "card"`，每加一种支付方式要改多少地方？什么情况下，抽出一个接口（Protocol）是值得的，而不是摆设？

## A
**要点。** 判断标准是实现之间的行为真的不同，并且不同点分散在多个方法上。现金成交是把硬币放进币箱，刷卡只扣实际货价；退款时现金原样退回，刷卡撤销授权；找零一个必须用硬币，一个不用。这些差别全部封进实现里，状态机只调用 `settle` 和 `release`，不再出现分支。

```python
class Tender(Protocol):                      # 两种实现的行为真的不同
    def settle(self, price: int, bank: list[int]) -> str: ...
    def release(self) -> str: ...

@dataclass
class CoinTender:
    coins: list[int] = field(default_factory=list)
    def settle(self, price: int, bank: list[int]) -> str:
        bank.extend(self.coins); self.coins.clear()   # 硬币进币箱
        return "硬币入箱"
    def release(self) -> str:
        back, self.coins = self.coins, []
        return f"退回硬币 {back}"

@dataclass
class CardTender:
    authorized: int
    def settle(self, price: int, bank: list[int]) -> str:
        return f"只扣 {price}，释放 {self.authorized - price}"
    def release(self) -> str:
        return "撤销授权，没有硬币可退"

def vend(t: Tender, price: int, bank: list[int], ok: bool) -> str:
    return t.settle(price, bank) if ok else t.release()   # 状态机不关心是哪种

bank: list[int] = []
for t in (CoinTender([100, 100]), CardTender(500)):
    print(type(t).__name__, vend(t, 150, bank, True))
for t in (CoinTender([100, 100]), CardTender(500)):
    print(type(t).__name__, vend(t, 150, bank, False))
```

货价 150：硬币 `[100, 100]` 和授权 500 的卡，各成交一次、各取消一次，实际输出：

```
CoinTender 硬币入箱
CardTender 只扣 150，释放 350
CoinTender 退回硬币 [100, 100]
CardTender 撤销授权，没有硬币可退
```

**为什么。** 没有接口时，分支散在成交、退款、找零三处，加第三种支付（比如手机钱包）要同时改三处，漏一处就是一个只在该支付方式下才出现的 bug。

**代价。** 接口是新概念，读代码的人要多跳一层。只有一种实现、也不需要假实现来测试时，这一层是纯成本。
