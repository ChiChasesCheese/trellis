---
id: craft-dry-run-on-a-copy-3-validate-on-candidate
node: craft.patterns.dry-run-on-a-copy
type: qa
step: 3
---
## Q
**在副本上试运行 · 先造候选状态，验过再替换**｜写法

额度账本里，每笔扣费按时间顺序从额度包里取钱。现在收到一笔迟到的扣费（时间戳排在已接受扣费之前）。先把它写进账本再检查，和先造一个候选状态、检查通过才替换，抛错时有什么差别？

## A
**要点。** 迟到的扣费会改变排在它后面的所有扣费的结果（它先拿走额度，后面的可能被饿死）。所以「这笔能不能接受」只能靠把整段历史重放一遍判断。重放是纯函数，把候选状态喂给它：通过才赋值，抛错时真实状态从头到尾没被碰过，回滚不需要写。

```python
class Short(Exception): ...

def replay(grants, charges):
    """纯函数：按时间重放全部事件，任何一笔凑不够就抛。值是 (时刻, 数量)。"""
    events = sorted([(t, 0, k, n) for k, (t, n) in grants.items()] +
                    [(t, 1, k, n) for k, (t, n) in charges.items()])   # 同刻先发放后扣费
    pool = 0
    for _, is_charge, key, n in events:
        if not is_charge:
            pool += n
        elif n > pool:
            raise Short(key)
        else:
            pool -= n

class Ledger:
    def __init__(self):
        self.grants = {"g1": (0.0, 10)}          # 额度包 10，时刻 0
        self.charges = {}

    def charge_inplace(self, key, at, n):        # 坏写法：先改再验
        self.charges[key] = (at, n)
        replay(self.grants, self.charges)        # 抛了，但 charges 里已经有它

    def charge(self, key, at, n):                # 好写法
        candidate = {**self.charges, key: (at, n)}   # 新字典，旧的不动
        replay(self.grants, candidate)           # 抛了就走不到下一行
        self.charges = candidate

a, b = Ledger(), Ledger()
a.charge("c1", 1.0, 8); b.charge("c1", 1.0, 8)   # 先接受 c1（时刻 1.0，8 点）
try: a.charge_inplace("late", 0.5, 5)            # 迟到的一笔排在 c1 之前，会把 c1 饿死
except Short as e: print("原地改: 抛了", e, "但账本已被污染:", sorted(a.charges))
try: b.charge("late", 0.5, 5)
except Short as e: print("副本版: 抛了", e, "账本仍是:", sorted(b.charges))
```

额度包 10，已接受一笔 8（时刻 1.0），再收到一笔 5（时刻 0.5）：

```
原地改: 抛了 c1 但账本已被污染: ['c1', 'late']
副本版: 抛了 c1 账本仍是: ['c1']
```

**为什么。** 抛出的异常指向 `c1`（被饿死的那笔），而不是新来的那笔。若原地改，调用方看到异常、以为拒绝了，实际上账本里已经有了这笔，之后每次重放都会抛。

**代价。** 每次提交都重放整段历史，是 O(事件数)。事件少时无所谓；多时要缓存重放结果，或者只重放受影响的后缀。
