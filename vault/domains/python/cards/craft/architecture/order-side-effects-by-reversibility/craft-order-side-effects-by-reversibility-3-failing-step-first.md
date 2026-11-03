---
id: craft-order-side-effects-by-reversibility-3-failing-step-first
node: craft.architecture.order-side-effects-by-reversibility
type: qa
step: 3
---
## Q
**副作用按可逆性排序 · 缓存的 put 为什么先写存储、后更新淘汰策略**｜架构

可配置缓存由两部分组成：存储后端（可能写失败，比如磁盘满）和淘汰策略（只记哪些键在，决定谁被淘汰）。`put` 要同时更新两者。存储写失败时，这两部分各应该处在什么状态？顺序怎么排？

## A
**要点。** 会失败的一步放最前：失败时什么都没变，不需要回滚。策略只是内存里的记账，几乎不会失败，放在存储成功之后。反过来先登记策略再写存储，存储一失败，策略里就留下了一个存储里不存在的「幽灵键」，策略以为缓存里有它，容量计数和淘汰选择都被它带偏，缓存一直处于不一致。

```python
class StoreError(Exception): ...

class Store:
    def __init__(self, fail_on: str | None = None) -> None:
        self.data: dict[str, int] = {}
        self.fail_on = fail_on
    def put(self, k: str, v: int) -> None:
        if k == self.fail_on:
            raise StoreError(f"写 {k} 失败")
        self.data[k] = v

class Cache:
    def __init__(self, store: Store, policy_first: bool) -> None:
        self.store, self.policy_first = store, policy_first
        self.policy: list[str] = []              # 淘汰策略记着「有哪些键」
    def put(self, k: str, v: int) -> None:
        if self.policy_first:
            self.policy.append(k)                    # 先登记，再写存储
            self.store.put(k, v)
        else:
            self.store.put(k, v)                 # 会失败的一步放最前：失败则什么都没变
            self.policy.append(k)

for policy_first in (True, False):
    c = Cache(Store(fail_on="b"), policy_first)
    c.put("a", 1)
    try:
        c.put("b", 2)
    except StoreError:
        pass
    ghosts = [k for k in c.policy if k not in c.store.data]
    print("先动策略" if policy_first else "先写存储", "-> 策略里有、存储里没有的键:", ghosts)
```

存储对键 `b` 的写入总是失败，先写 `a` 成功，再写 `b`，实际输出：

```
先动策略 -> 策略里有、存储里没有的键: ['b']
先写存储 -> 策略里有、存储里没有的键: []
```

**为什么。** 缓存里还有一处同样的思路：满了要淘汰时，新值已经写进存储，如果淘汰旧值失败，就把新值也撤回，缓存回到操作前的状态。写在前面的步骤要为后面的失败负责，所以要么顺序能避免撤销，要么撤销被明确写出来。

**代价。** 并非总能把所有会失败的步骤排到前面：当两步都会失败时，必须选一步做撤销（上面淘汰失败时撤回新值）。
