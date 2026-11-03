---
id: craft-source-of-truth-and-derived-caches-1-truth-and-projection
node: craft.architecture.source-of-truth-and-derived-caches
type: qa
step: 1
---
## Q
**真相与派生缓存 · 余额到底存在哪**｜架构

电子钱包要快速回答「A 现在有多少钱」，又要保留每一笔转账的明细。如果余额字段和明细表各自独立地更新，哪天一个 bug 只更新了其中一个，两边就对不上，而且没人知道该信哪个。怎样设计才能让这种漂移（drift）可发现、可修复？

## A
**要点。** 每条信息只准有一个真相（source of truth），其余都是可以丢弃重建的派生物（derived，投影）。这里：明细账本是真相，只追加；余额是缓存，写路径在同一次操作里同步更新；对账（reconcile）的方向永远是「账本覆盖缓存」，因为缓存可以从账本重算，反过来不行。

```python
@dataclass(frozen=True)
class Entry:
    account: str
    delta: int

class Wallet:
    def __init__(self) -> None:
        self.ledger: list[Entry] = []                 # 真相：只追加
        self.cache: dict[str, int] = {}               # 投影：读路径用

    def transfer(self, src: str, dst: str, amount: int, *, forget_cache: bool = False) -> None:
        self.ledger += [Entry(src, -amount), Entry(dst, +amount)]   # 先落账（真相）
        self.cache[src] = self.cache.get(src, 0) - amount
        if not forget_cache:                       # 模拟漏更新的 bug
            self.cache[dst] = self.cache.get(dst, 0) + amount

    def derived(self, account: str) -> int:
        return sum(e.delta for e in self.ledger if e.account == account)

    def reconcile(self, account: str) -> bool:
        d = self.derived(account)
        if self.cache.get(account, 0) == d:
            return False
        self.cache[account] = d                    # 方向固定：账本覆盖缓存
        return True

w = Wallet()
w.transfer("A", "B", 30, forget_cache=True)
print("缓存 B =", w.cache.get("B", 0), " 账本推导 B =", w.derived("B"))
print("reconcile 纠正了吗:", w.reconcile("B"), "-> 缓存 B =", w.cache["B"])
print("账本总和（恒为 0）:", sum(e.delta for e in w.ledger))
```

做一笔 A→B 30 的转账并漏掉 B 的缓存，实际输出：

```
缓存 B = 0  账本推导 B = 30
reconcile 纠正了吗: True -> 缓存 B = 30
账本总和（恒为 0）: 0
```

**为什么。** 账本里每笔转账成对记两条，总和恒为 0，这条不变量也是检查账本本身的办法。

**代价。** 读余额快了，写路径多了一份要同步的工作；对账需要扫账本，可能很慢，所以通常抽查或定期做，不在热路径上做。
