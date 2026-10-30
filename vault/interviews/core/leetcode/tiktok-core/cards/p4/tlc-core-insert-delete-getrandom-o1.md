---
id: tlc-core-insert-delete-getrandom-o1
node: p4.insert-delete-getrandom-o1
type: qa
---
## Q
**LC 380 O(1) 时间插入、删除和获取随机元素**｜Medium · LC TikTok 热度 62/100 · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 15 次 · 最近 2026-10-08（面试记录） · 也在：Amazon、Top Interview 150

实现 `RandomizedSet` 类：`RandomizedSet()` 初始化；`bool insert(int val)` 当 `val` 不存在时插入并返回 `true`，否则返回 `false`；`bool remove(int val)` 当 `val` 存在时删除并返回 `true`，否则返回 `false`；`int getRandom()` 随机返回现有集合中的一项，每个元素被返回的概率相同（调用时集合中至少有一个元素）。每个函数的**平均**时间复杂度必须是 `O(1)`。`-2^31 <= val <= 2^31 - 1`，最多调用 `insert`、`remove`、`getRandom` 共 `2 * 10^5` 次，调用 `getRandom` 时至少存在一个元素。例：依次 `insert(1)` → `true`，`remove(2)` → `false`，`insert(2)` → `true`，`getRandom()` → `1` 或 `2`，`remove(1)` → `true`，`insert(2)` → `false`，`getRandom()` → `2`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 一个动态数组 `items` 存元素（`getRandom` 靠下标随机取），一个字典 `pos` 存「值 → 下标」（`insert` / `remove` 靠它 `O(1)` 查找）；删除时把数组**末尾元素**搬到被删位置，再弹出末尾，数组始终紧凑。

**识别。** 「`O(1)` 随机取」要求能按下标访问等概率的元素 → 数组；「`O(1)` 判重 / 删除」要求按值定位 → 哈希表；两者的矛盾是数组删除中间元素 `O(n)`。解法的核心就是把这个矛盾化解成「删除末尾 `O(1)`」：用末尾元素填坑。「设计数据结构 + 全部操作 `O(1)`」是组合两个基本结构、让它们互相维护的信号。

**推导。** 暴力：只用集合 `set`，`insert` / `remove` 是 `O(1)`，但 `getRandom` 要先转成列表，`O(n)`；只用列表，`getRandom` 是 `O(1)`，但 `insert` 要先判重、`remove` 要先找位置，`O(n)`。洞察：列表末尾的增删是 `O(1)`，所以删除时不要整体前移，而是让末尾元素“补位”：`items[i] = items[-1]`，再 `pop()`。补位的元素在字典里的下标也要同步更新。顺序不重要，因为集合本来就无序。

```python
import random


class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```

运行：示例序列依次得到 `True, False, True, True(getRandom 返回 1 或 2), True, False, 2`；依次插入 `10, 20, 30, 40` 再删 `20` 后 `items = [10, 40, 30]`，`pos = {10: 0, 30: 2, 40: 1}`；`getRandom` 在 `{10, 30, 40}` 上抽 `30000` 次，各值的次数都在 `10000` 附近（一次运行是 `10060, 9834, 10106`）。

**复杂度。** `insert`、`remove`、`getRandom` 均摊 `O(1)`（动态数组 `append` 均摊 `O(1)`，哈希表平均 `O(1)`）；空间 `O(n)`。

**易错点。**
- `remove` 时不判断被删元素是否就在末尾：先弹出末尾再无条件 `items[i] = last`，当 `val` 就是末尾元素时 `i` 已经越界，`insert(1)`、`insert(2)`、`remove(2)` 抛 `IndexError: list assignment index out of range`。所以要判断 `i < len(self.items)`。
- 搬了末尾元素却忘了更新它在 `pos` 里的下标：之后删除这个元素会删错位置。
- 用 `set` 存元素再 `random.choice(list(s))`：每次 `getRandom` 是 `O(n)`；`random.choice(set)` 直接抛 `TypeError`（要求序列）。

**追问。**
- 允许重复元素（LC 381）：字典改成 `值 -> 下标集合`，`remove` 随便取一个下标，搬末尾元素时把集合里旧下标换成新下标；`insert` 返回「该值此前是否不存在」。
- 按权重随机（LC 528）：前缀和 + `bisect`，`getRandom` 是 `O(log n)`；加删除后可用树状数组或线段树。
- 线程安全：`insert` / `remove` 涉及两个结构的联动，需要加锁，否则中间状态会让 `items` 与 `pos` 不一致。

**同模式。** LC 381 允许重复、LC 146 LRU 缓存、LC 460 LFU 缓存、LC 432 全 O(1) 的数据结构、LC 528 按权重随机选择。
