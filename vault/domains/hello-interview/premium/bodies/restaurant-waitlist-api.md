---
slug: restaurant-waitlist-api
kind: low-level-design
---
## Q
**实现餐厅候位（Waitlist）API**｜低层设计

餐厅有几张大小不同的桌子，客人成桌到来。实现候位的接口和数据结构：一桌客人可以加入候位名单（名单有合理的上限）；已加入的客人随时可以离开；桌子空出来时，安排名单里第一个坐得下的人（4 人团可以坐 6 人桌，8 人团坐不下 6 人桌，就跳过他，看后面的）。进阶版本会问：前台怎么告诉客人"大概还要等多久"，队首的大团会不会一直被后来的小团插队饿死，以及名单很长时怎么做得快。面试官看重的是：数据结构的选择理由、"谁坐哪张桌"的规则只写一处，以及复杂度。

给出完整解答：需求、核心实体与接口、整体设计、核心实现、逐步扩展、深入问题、取舍、不同级别的期望。

## A
**一句话。** 把"现在谁能坐哪张桌"写成一个不读实例状态的纯函数 `_drain`，加入、离开、结束用餐都以同一个"能坐的都安排上"收尾；等位估计和防饿死都只是复用或扩展这一个函数，预测和现实就不会各说各话。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求：桌型、团的大小范围、重复 id、名单上限、"第一个坐得下"的含义；定接口 |
| 8–15 分 | 选数据结构（有序列表），说清为什么不是优先队列；写下 `_drain` 的规则 |
| 15–40 分 | 写核心实现：`_best_fit`、`_drain`、`join` / `leave` / `finish` |
| 40–45 分 | 跑例子：直接入座、排队、跳过坐不下的、错误输入 |
| 45–60 分 | 追问：名单很长时的分桶结构、防饿死、等位估计、改人数 |

**需求。**
- 功能：
  - `join(party_id, size)`：有桌就立刻入座并返回桌号，否则排到队尾并返回 `None`；
  - `leave(party_id)`：排队的客人随时可以走；
  - `finish(party_id)`：用餐结束，桌子空出；从队首往后，第一个坐得下的人入座，前面坐不下的留在队里、保持相对顺序；
  - 入座时在坐得下的空桌里选容量最小的（大桌留给大团），容量相同取编号小的；
  - 非法输入：人数小于 1、比最大的桌子还大、id 重复（排队或用餐中）、操作一个不存在的 id，都抛明确的异常，且不改变状态。
- 非功能：
  - 规则只写一处，不同入口不会各写一份；
  - 失败的调用不留半成品；
  - 名单上限：口头约定（例如满了就拒绝加入），实现上是 `join` 开头多一行长度检查；
  - 时间由注入的时钟提供，测试里不 `sleep`（估计功能才用到）。

**核心实体与接口。**
- `_Waiting`：排队的一桌，`id` 和 `size`；内部可变，外部只能看见 id 和桌号。
- **_best_fit 最小够用：** `_best_fit(size, free, sizes)`：在空闲桌里选"坐得下的最小一张"；元组键 `(容量, 桌号)` 一次比较同时解决"最小够用"和"编号小优先"。
- **_drain 就地修改并返回安排：** `_drain(queue, free, sizes)`：就地修改传进来的队伍和空闲桌，返回 `(人, 桌号)` 列表，不读实例状态。
- `Restaurant(table_sizes)`：`join`、`leave`、`finish`、`queue()`、`table_of()`。
- 异常：`InvalidPartyError`、`PartyTooLargeError`（前者的子类）、`DuplicatePartyError`、`UnknownPartyError`，共同基类 `RestaurantError`。

**整体设计。** 三个会改变状态的入口，都走同一条路：
1. 先校验（人数、重复 id、id 是否存在），失败就抛出，状态没动过；
2. 改自己的那一小部分：`join` 往队尾加一个 `_Waiting`，`leave` 从队里删掉，`finish` 把桌号放回 `_free`；
3. **坐下所有能坐的人：** 调 `_seat_everyone_possible()`：它调用 `_drain`，把能坐的人都安排上，并把结果写进 `_seated`。`finish` 的返回值就是这一步的结果。

为什么用有序列表，不用优先队列：规则是"从队首往后第一个坐得下的人"，不是"最大"或"最小"；中间离开、坐不下的人要留在原位保持相对顺序，列表最直接。

**核心实现。** 约 25 分钟，下面是全部要写的代码：

```python
from collections.abc import Sequence
from dataclasses import dataclass


class RestaurantError(Exception): ...
class InvalidPartyError(RestaurantError, ValueError): ...
class PartyTooLargeError(InvalidPartyError): ...         # 比最大的桌子还大，永远排不上
class DuplicatePartyError(RestaurantError): ...
class UnknownPartyError(RestaurantError): ...


@dataclass(slots=True)
class _Waiting:                                          # 内部可变，外部只看见 id 和桌号
    id: str
    size: int


def _best_fit(size: int, free: set[int], sizes: Sequence[int]) -> int | None:
    """能坐下的空桌里选最小的（大桌留给大团），容量相同取编号小的：元组键一次比较搞定。"""
    fit = min(((sizes[t], t) for t in free if sizes[t] >= size), default=None)
    return None if fit is None else fit[1]


def _drain(queue: list[_Waiting], free: set[int], sizes: Sequence[int]) -> list[tuple[_Waiting, int]]:
    """"谁坐哪张桌"的规则只写在这一处，不读实例状态：就地修改传入的 queue 和 free。
    从队首往后找第一个有桌可坐的人，让他入座，再从头找，直到没人能坐。"""
    seated = []
    while True:
        for i, w in enumerate(queue):
            table = _best_fit(w.size, free, sizes)
            if table is not None:
                del queue[i]
                free.remove(table)
                seated.append((w, table))
                break
        else:                                            # 整个队伍找遍也没人能坐
            return seated


class Restaurant:
    def __init__(self, table_sizes: Sequence[int]) -> None:
        if not table_sizes or any(n < 1 for n in table_sizes):
            raise ValueError("need at least one table, every table seats 1 or more")
        self._sizes = list(table_sizes)
        self._free = set(range(len(self._sizes)))
        self._queue: list[_Waiting] = []
        self._seated: dict[str, int] = {}                # party -> 桌号

    def join(self, party_id: str, size: int) -> int | None:
        self._check_size(size)                           # 所有校验在改状态之前
        if party_id in self._seated or any(w.id == party_id for w in self._queue):
            raise DuplicatePartyError(party_id)
        self._queue.append(_Waiting(party_id, size))
        self._seat_everyone_possible()
        return self._seated.get(party_id)                # 入座了是桌号，还在排队是 None

    def leave(self, party_id: str) -> None:
        for i, w in enumerate(self._queue):
            if w.id == party_id:
                del self._queue[i]
                self._seat_everyone_possible()
                return
        raise UnknownPartyError(party_id)

    def finish(self, party_id: str) -> list[tuple[str, int]]:
        if party_id not in self._seated:
            raise UnknownPartyError(party_id)
        self._free.add(self._seated.pop(party_id))
        return self._seat_everyone_possible()

    def queue(self) -> list[str]:
        return [w.id for w in self._queue]

    def table_of(self, party_id: str) -> int | None:
        return self._seated.get(party_id)

    def _check_size(self, size: int) -> None:
        if size < 1:
            raise InvalidPartyError(f"party size must be at least 1, got {size}")
        if size > max(self._sizes):
            raise PartyTooLargeError(f"no table seats {size}")

    def _seat_everyone_possible(self) -> list[tuple[str, int]]:   # 每个改状态的入口都以它收尾
        placed = _drain(self._queue, self._free, self._sizes)
        for w, table in placed:
            self._seated[w.id] = table
        return [(w.id, table) for w, table in placed]
```

**运行。**
- 桌 `[2, 4]`：`a(2)` 坐桌 0，`b(4)` 坐桌 1，`c(4)`、`d(2)` 排队，`queue()` 是 `['c', 'd']`；
- **finish 示例：** `finish("a")` 返回 `[('d', 0)]`：桌 0 只有 2 个座位，`c` 坐不下被跳过，`d` 是第一个坐得下的，队里剩 `['c']`；
- `leave("c")` 之后队伍为空；`join("a", 0)` 抛 `InvalidPartyError`，`join("x", 9)` 抛 `PartyTooLargeError`，`join("b", 1)`（`b` 正在用餐）抛 `DuplicatePartyError`，`leave("b")`（不在排队）抛 `UnknownPartyError`；
- 桌 `[6, 2, 4]`：3 人坐 4 人桌（桌 2），2 人坐 2 人桌（桌 1），5 人坐 6 人桌（桌 0）。

**逐步扩展。**
1. 【追问再讲】名单很长时的分桶结构：触发"名单有一千个团，每次 `finish` 都扫一遍太慢"。按人数分桶，每桶是 `OrderedDict`（哈希表加双向链表，按到达顺序），值是全局到达序号。桌子空出来时，只看人数不超过桌子容量的那几个桶的队首，取到达序号最小的。关键是不变量：队伍里没有人坐得下任何一张空桌，所以一张桌子空出来，也只需要为它这一张找人，`finish` 最多让一个人入座。

```python
from collections import OrderedDict
from itertools import count


class BucketQueue:
    """按人数分桶。每桶是 OrderedDict（哈希表加双向链表，按到达顺序），值是全局到达序号。"""
    def __init__(self, max_size: int) -> None:
        self._buckets = [OrderedDict() for _ in range(max_size + 1)]
        self._seq = count()
        self._size_of: dict[str, int] = {}                # id -> 人数：判重和删除都是 O(1)

    def __contains__(self, party_id: str) -> bool:
        return party_id in self._size_of

    def push(self, party_id: str, size: int) -> None:
        self._buckets[size][party_id] = next(self._seq)
        self._size_of[party_id] = size

    def remove(self, party_id: str) -> None:
        del self._buckets[self._size_of.pop(party_id)][party_id]

    def pop_first_fitting(self, capacity: int) -> str | None:
        """人数不超过 capacity 的队伍里，最早到的那个：每个桶只看队首，跨桶比到达序号。"""
        heads = [(seq, pid) for b in self._buckets[1:capacity + 1] if b for pid, seq in [next(iter(b.items()))]]
        if not heads:
            return None
        _, party_id = min(heads)
        self.remove(party_id)
        return party_id

    def ordered(self) -> list[str]:
        return [pid for _, pid in sorted((seq, pid) for b in self._buckets for pid, seq in b.items())]


class BucketRestaurant(Restaurant):
    """不变量：队伍里没有人坐得下任何一张空桌。所以新来的人要么直接入座，要么排队；
    一张桌子空出来，也只需要在队伍里找"坐得下这张桌的第一个人"。"""
    def __init__(self, table_sizes: Sequence[int]) -> None:
        super().__init__(table_sizes)
        self._bq = BucketQueue(max(table_sizes))

    def join(self, party_id: str, size: int) -> int | None:
        self._check_size(size)
        if party_id in self._seated or party_id in self._bq:
            raise DuplicatePartyError(party_id)
        table = _best_fit(size, self._free, self._sizes)
        if table is None:
            self._bq.push(party_id, size)
            return None
        self._free.remove(table)
        self._seated[party_id] = table
        return table

    def leave(self, party_id: str) -> None:
        if party_id not in self._bq:
            raise UnknownPartyError(party_id)
        self._bq.remove(party_id)

    def finish(self, party_id: str) -> list[tuple[str, int]]:
        if party_id not in self._seated:
            raise UnknownPartyError(party_id)
        table = self._seated.pop(party_id)
        nxt = self._bq.pop_first_fitting(self._sizes[table])
        if nxt is None:
            self._free.add(table)
            return []
        self._seated[nxt] = table
        return [(nxt, table)]

    def queue(self) -> list[str]:
        return self._bq.ordered()
```

2. 【追问再讲】防饿死：触发"队首的 6 人团一直被后来的小团插队"。每个排队的人记 `skipped`（被插队几次），`_drain` 里遇到次数达到 `max_overtakes` 的人，自己坐不了就停止，不许后面的人再越过他。`0` 表示严格先来先坐，`None` 保持原来的行为。

```python
@dataclass(slots=True)
class _Waiting:
    id: str
    size: int
    skipped: int = 0                                     # 新：被排在后面的人插队了几次


def _drain(queue: list[_Waiting], free: set[int], sizes: Sequence[int],
           max_overtakes: int | None) -> list[tuple[_Waiting, int]]:
    seated = []
    while True:
        for i, w in enumerate(queue):
            table = _best_fit(w.size, free, sizes)
            if table is not None:
                for earlier in queue[:i]:                # 排在 w 前面的人，都被 w 插队了一次
                    earlier.skipped += 1
                del queue[i]
                free.remove(table)
                seated.append((w, table))
                break
            if max_overtakes is not None and w.skipped >= max_overtakes:
                return seated                            # 他自己坐不了，又不许后面的人再越过他
        else:
            return seated


class Restaurant:  # 只列出新增或替换的方法
    def __init__(self, table_sizes: Sequence[int], max_overtakes: int | None = None) -> None:
        if not table_sizes or any(n < 1 for n in table_sizes):
            raise ValueError("need at least one table, every table seats 1 or more")
        self._sizes = list(table_sizes)
        self._max_overtakes = max_overtakes              # None：保持原来的行为
        self._free = set(range(len(self._sizes)))
        self._queue: list[_Waiting] = []
        self._seated: dict[str, int] = {}

    def _seat_everyone_possible(self) -> list[tuple[str, int]]:
        placed = _drain(self._queue, self._free, self._sizes, self._max_overtakes)
        for w, table in placed:
            self._seated[w.id] = table
        return [(w.id, table) for w, table in placed]
```

3. 【追问再讲】等位估计：触发"告诉客人还要等多久"。在队伍的副本上往前推演：每张忙桌的空出时刻是入座时间加用餐时长（已超时的算现在），每到一个空出时刻就调用同一个 `_drain`。`quote(size)` 是往副本队尾追加一个探针客人。

```python
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta


class Restaurant:  # 只列出新增或替换的方法
    def __init__(self, table_sizes: Sequence[int], clock: Callable[[], datetime],
                 dining_time: timedelta = timedelta(minutes=60), max_overtakes: int | None = None) -> None:
        if not table_sizes or any(n < 1 for n in table_sizes):
            raise ValueError("need at least one table, every table seats 1 or more")
        self._sizes = list(table_sizes)
        self._clock, self._dining, self._max_overtakes = clock, dining_time, max_overtakes   # 时钟注入，测试不 sleep
        self._free = set(range(len(self._sizes)))
        self._queue: list[_Waiting] = []
        self._seated: dict[str, tuple[int, datetime]] = {}    # party -> (桌号, 入座时间)

    def table_of(self, party_id: str) -> int | None:
        entry = self._seated.get(party_id)
        return entry[0] if entry else None

    def join(self, party_id: str, size: int) -> int | None:
        self._check_size(size)
        if party_id in self._seated or any(w.id == party_id for w in self._queue):
            raise DuplicatePartyError(party_id)
        self._queue.append(_Waiting(party_id, size))
        self._seat_everyone_possible()
        return self.table_of(party_id)

    def finish(self, party_id: str) -> list[tuple[str, int]]:
        if party_id not in self._seated:
            raise UnknownPartyError(party_id)
        table, _ = self._seated.pop(party_id)
        self._free.add(table)
        return self._seat_everyone_possible()

    def _seat_everyone_possible(self) -> list[tuple[str, int]]:
        now = self._clock()
        placed = _drain(self._queue, self._free, self._sizes, self._max_overtakes)
        for w, table in placed:
            self._seated[w.id] = (table, now)            # 记下入座时间，估计用得上
        return [(w.id, table) for w, table in placed]

    def estimate_wait(self, party_id: str) -> timedelta:
        if party_id in self._seated:
            return timedelta(0)
        if not any(w.id == party_id for w in self._queue):
            raise UnknownPartyError(party_id)
        return self._simulate([replace(w) for w in self._queue], party_id)   # 在副本上推演，不污染真实队伍

    def quote(self, size: int) -> timedelta:
        """现在来一桌 size 人，预计要等多久；不改变任何状态。"""
        self._check_size(size)
        probe = "\0quote"
        return self._simulate([replace(w) for w in self._queue] + [_Waiting(probe, size)], probe)

    def _simulate(self, queue: list[_Waiting], target: str) -> timedelta:
        """每张忙桌的空出时刻 = 入座时间 + 用餐时长（超时的算现在）；空出后用和真实完全相同的 _drain。"""
        now = self._clock()
        free = set(self._free)
        busy = {table: max(now, at + self._dining) for table, at in self._seated.values()}
        t = now
        while True:
            for w, table in _drain(queue, free, self._sizes, self._max_overtakes):
                if w.id == target:
                    return t - now
                busy[table] = t + self._dining
            t = min(busy.values())                       # 下一个桌子空出来的时刻
            for table in [tb for tb, ft in busy.items() if ft <= t]:
                del busy[table]
                free.add(table)
```

4. 【加分】改人数：触发"排队的客人想把 4 人改成 2 人"。先校验再改，位置和被插队次数不变，改完调同一个收尾步骤（改小后可能立刻坐下，也可能带动后面被挡住的人）。

```python
class Restaurant:  # 只列出新增或替换的方法
    def change_size(self, party_id: str, size: int) -> list[tuple[str, int]]:
        """排队中的客人改人数：位置和被插队次数不变；改小后可能立刻坐下。"""
        waiting = next((w for w in self._queue if w.id == party_id), None)
        if waiting is None:
            raise UnknownPartyError(party_id)
        self._check_size(size)                           # 先校验，失败队伍原样
        waiting.size = size
        return self._seat_everyone_possible()
```

**运行（逐步扩展）。**
- 分桶版本和核心版本做随机对照：300 组随机桌型、每组 200 次随机的加入、离开、结束用餐，返回值（含异常类型）和队伍顺序全部一致；
- 估计：桌 `[2, 4]`，18:00 时 `a(2)`、`b(4)` 入座，`c(4)`、`d(2)`、`e(2)` 排队：18:00 时 `c`、`d`、`e` 分别要等 60、60、120 分钟，此刻来一个 4 人团 `quote(4)` 是 120 分钟；到 18:30 分别是 30、30、90；
- 防饿死：桌 `[2, 6]`，`a(6)` 占 6 人桌，`b(6)` 排队，`c(2)` 坐桌 0（`b` 被插队 1 次）。`max_overtakes=1` 时，`c` 结束后新来的 `d(2)` 只能排队（`queue` 是 `['b', 'd']`）；`a` 结束时 `finish("a")` 返回 `[('b', 1), ('d', 0)]`，一次入座两个人；`max_overtakes=None` 时 `d` 直接坐桌 0。

**深入。**
1. 【必讲】规则只写一处，预测与现实共用：
   - `_drain` 不读实例状态，输入队伍、空闲桌，就地修改传入的对象：真实的 `join` / `finish` 传真状态，等位推演传副本，规则只写一遍；写进方法里，估计就得复制一份，两份迟早不一致（函数式核心，命令式外壳）；
   - 每个会改变状态的入口都以 `_seat_everyone_possible` 收尾，所以 `finish` 在防饿死时可以一次入座多个人，而签名不用改；挡路的人 `leave` 之后后面的人也要能坐下，`leave` 因此同样以它收尾；
   - `for ... else` 表达"找遍整个队伍都没人能坐就结束"：入座后 `break` 重新从头找，`else` 分支返回；用标志变量要多一个可变状态。
2. 【必讲】选桌与"第一个坐得下"：
   - 入座选容量最小的够用桌，保住大桌给大团；放弃"编号最小的空桌"，因为它会让 2 个人占掉 6 人桌，后来的大团只能干等。代价：这是贪心，不是全局最优；
   - `_best_fit` 用 `min` 加生成器表达式和 `default=None`，键是 `(容量, 桌号)`，先建列表再判空要多写分支；
   - 队伍保持到达顺序，前面坐不下的人被跳过但留在原位；不用优先队列，因为规则不是取最大或最小。
3. 【必讲】数据结构与复杂度：
   - 核心的列表版：`_drain` 每次从头扫，最坏 O(队伍长度)；`leave`、判重也是 O(队伍长度)；名单几十个团，这完全够用；
   - 分桶版（逐步扩展 1）：团的人数上限是 k（例如 10），取人只看 k 个桶的队首，O(k)；`remove` 和判重靠 `id → 人数` 的字典与 `OrderedDict`，O(1)。设名单 1,000 个团、k = 10（假设），每次 `finish` 的比较次数从最多 1,000 降到最多 10，少两个数量级；
   - 代价：分桶版的不变量（队伍里没人坐得下空桌）只在没有防饿死规则时成立；加了防饿死，一次要入座多个人，要回到 `_drain` 的写法。
4. 【追问再讲】防饿死：
   - 用"被插队次数"的计数器，而不是给等得久的人加优先级：优先级让规则难以预测，计数器的行为可以直接写进测试；
   - 代价是挡路时桌子空着、有人在等，这是公平与利用率的取舍，要在口述里说出来；
   - 计数只数"被后面的人真正越过"的次数，复制队伍估计时要带上计数（`dataclasses.replace(w)` 复制所有字段，加了字段也不用改复制代码）。
5. 【追问再讲】等位估计：
   - 放弃"平均等待时间乘队列位置"：它区分不了大桌和小桌，一个 6 人团前面排着 2 人团时估计会差很远；
   - 推演用同一个 `_drain`，所以防饿死规则自动遵守；超时的桌子算"现在就空"，避免出现负的等待时间；
   - 时钟作为构造参数 `clock: Callable[[], datetime]` 注入，测试里用一个可拨动的假时钟（注入时钟）。
6. 【追问再讲】内部可变，外部只读：`_Waiting` 是 `@dataclass(slots=True)`，可变（要累加被插队次数），但只在模块内部使用，对外只看见 id 和桌号。
7. 【加分】预订、通知与并发：
   - 预订是对某张桌某段时间的占用，`_drain` 之前先扣掉被预订占住的桌，估计里也要把预订当成固定的忙时段；
   - 通知排队的客人"到你了"：`finish` 已经返回新入座的人，调用方据此发通知，不要在 `Restaurant` 里直接发；
   - 多个前台并发：所有入口共用一把锁，因为每个入口都是"读队伍、改队伍、改桌子"的整体。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 名单满了怎么办：`join` 开头检查长度，满了抛异常。
- 用餐时长因人数而异：`dining_time` 换成按人数取值的函数，入座时记录预计结束时刻。
- 怎么证明估计靠谱：属性测试，同一状态下 `quote(n)` 等于随后真的 `join` 再 `estimate_wait`；用假时钟按预计时间推进，检验实际入座时刻吻合。
- 为什么 `finish` 返回列表：核心版最多一个人，防饿死版可以多个，返回类型一开始就留好。

**级别期望。**
- 中级：核心实现通过，选桌规则和"跳过坐不下的人"正确，错误处理完整。
- 高级：规则集中在一个函数里，入口以同一步骤收尾；能说清用列表不用优先队列，并指出名单很长时的分桶结构。
- 资深/专家：估计复用同一规则并在副本上推演；防饿死的计数器与公平性取舍；分桶不变量与防饿死不兼容的说明；预订、拼桌和并发。

**先修概念。**
- [[hi-low-level-design-in-a-hurry-delivery|答题框架]]
- [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]
- [[hi-low-level-design-in-a-hurry-design-principles|设计原则]]
- [[hi-low-level-design-concurrency-intro|并发入门]]

**同类题。**
- [[solution-restaurant|设计题解：餐厅]]
- [[solution-meeting-scheduler|设计题解：会议调度]]
- [[solution-task-scheduler|设计题解：任务调度]]
