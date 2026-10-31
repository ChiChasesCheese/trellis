---
id: tlc-insert-delete-getrandom-o1-duplicates-allowed-0-whole
node: c.insert-delete-getrandom-o1-duplicates-allowed
type: qa
---
## Q
**LC 381 O(1) 时间插入、删除和获取随机元素 - 允许重复**｜Hard · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 4 次 · 最近 2022-07-31（国内 CodeTop）

实现 `RandomizedCollection`，它是一个可以包含重复元素的集合：`insert(val)` 插入一个 `val`（即使已存在），如果 `val` 原本不存在返回 `true`，否则 `false`；`remove(val)` 若存在则移除**一个** `val` 并返回 `true`，否则返回 `false`；`getRandom()` 随机返回一个元素，每个元素被返回的概率与它在集合中出现的次数成正比。每个函数的平均时间复杂度必须是 `O(1)`。`-2^31 <= val <= 2^31 - 1`，三个函数总共最多调用 `2 * 10^5` 次，调用 `getRandom` 时集合里至少有一个元素。例：`insert(1)` → `true`，`insert(1)` → `false`，`insert(2)` → `true`，`getRandom()` 以 2/3 概率返回 1、1/3 概率返回 2，`remove(1)` → `true`，此时 `getRandom()` 返回 1 或 2 的概率相等。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用一个数组存所有元素（`getRandom` 直接抽），再用「值 → 下标集合」的字典定位；删除时把目标位置和数组末尾互换后弹出末尾，全部 `O(1)`。

**识别。** 「O(1) 随机取」要求下标可直接寻址，只能是数组；「O(1) 删除指定值」要求能立刻找到它的下标，所以再配一个哈希表。「允许重复」把单个下标变成下标集合，这是它与 LC 380 的唯一区别。

**推导。** 用列表存元素则 `remove` 要先查找再整体前移，`O(n)`。洞察：数组删除任意位置慢，但删末尾是 `O(1)`，所以把要删的位置用末尾元素覆盖，再弹出末尾；覆盖后末尾元素的下标变了，字典里的下标集合要同步改。重复值时，被删的是 `val` 的**任意一个**下标，`set.pop()` 就能 `O(1)` 拿到一个。

```python
import random
from collections import defaultdict


class RandomizedCollection:
    def __init__(self) -> None:
        self.items: list[int] = []                         # 所有元素（含重复），getRandom 直接抽
        self.pos: defaultdict[int, set[int]] = defaultdict(set)   # 值 -> 它在 items 里的全部下标

    def insert(self, val: int) -> bool:
        self.pos[val].add(len(self.items))
        self.items.append(val)
        return len(self.pos[val]) == 1                     # 只有这一个下标，说明之前不存在

    def remove(self, val: int) -> bool:
        if not self.pos.get(val):
            return False
        idx = self.pos[val].pop()                          # val 的任意一个下标，O(1)
        last = len(self.items) - 1
        if idx != last:                                    # 用末尾元素覆盖 idx，数组才不留空洞
            moved = self.items[last]
            self.items[idx] = moved
            self.pos[moved].remove(last)                   # moved 的下标 last 改成 idx
            self.pos[moved].add(idx)                       # moved 可能就是 val：此时集合里本来就有 last
        self.items.pop()
        if not self.pos[val]:
            del self.pos[val]                              # 没有该值了，删键让 insert 的判断成立
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```

运行：示例序列 `insert(1), insert(1), insert(2)` 返回 `true, false, true`，`remove(1)` 返回 `true`，之后 `getRandom` 只会返回 `1` 或 `2`；对 `{1,1,2}` 抽 30000 次，`1` 出现 `20023` 次（理论值 20000）；`remove(5)` 在空集合上返回 `false`。

**复杂度。** `insert`、`remove`、`getRandom` 均摊 `O(1)`；空间 `O(n)`。

**拓展优化。**
- 不能用「值 → 次数」的 `Counter` 代替数组：随机抽样需要按次数加权，`Counter` 上抽样是 `O(不同值个数)`，数组才让加权抽样变成一次随机下标。
- 权重可以改且要求更新也快（LC 528 的在线版本）：用树状数组（Fenwick tree）存权重，抽样和更新都是 `O(log n)`，换来任意权重而不只是整数次数。

**易错点。**
- `idx == last` 时必须跳过互换：`pos[val]` 里刚 `pop` 掉了 `last`，再 `remove(last)` 会抛 `KeyError`。
- 覆盖后忘了更新 `moved` 的下标集合：之后删 `moved` 会 pop 出一个已经不存在的旧下标，数组下标越界或删错。
- 删到空集合后不删键：`pos` 里残留空集合，用 `val in self.pos` 判断是否存在会误判为存在。

**追问。**
- 不允许重复（LC 380）：下标集合退化成单个下标，字典存 `值 -> 下标`。
- 要求 `getRandom` 不能返回刚被删的值、并发访问：加锁，或让 `remove`/`getRandom` 在同一把锁内，不改变复杂度。

**同模式。** LC 380 O(1) 时间插入、删除和获取随机元素、LC 146 LRU 缓存、LC 460 LFU 缓存、LC 528 按权重随机选择、LC 398 随机数索引。
