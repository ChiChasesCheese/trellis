# q01 · 包裹追踪系统（Parcel Tracking System）逐级带写

题面：`../problems/q01_parcel_tracking/problem.md`。通用心法：`essentials_codesignal_icf.md`（建议先读）。
代码：`../problems/q01_parcel_tracking/solution.py`（4 级做完后的最终形态；变量名是 `self._parcels`）。你自己写的版本放在 `starter.py`，用 `IMPL=starter` 跑测试。

```bash
cd vault/interviews/companies/airbnb/problems/q01_parcel_tracking
IMPL=starter python3 -m unittest tests.test_level_1      # 只跑 Level 1
IMPL=starter bash run_single_test.sh case_06              # 只跑一个测试
python3 -m unittest discover -s tests -p "test_*.py"      # 参考解：34/34 应该全绿
```

## 第 0 步：读题。先看 4 行概要，再看 Level 1

Requirements 里那 4 行就是整道题的地图：

1. tag 的 set / get / remove
2. 列出 tag
3. **带时间戳（timestamp）和可选 TTL**
4. **checkpoint 保存和恢复**

读这 4 行只是为了**选对容器**：第 2 行要"列出一个包裹的所有 tag"，所以用两层 dict，先按包裹、再按 tag。
**不是**为了提前写 TTL 或快照的代码。每一级只写让这一级测试通过的最少代码。

还有一点：照片里题目页的标题写着 "Filesystem with Unit Tests"，那是 CodeSignal 的项目模板名，**不是题目**。别被它带偏。

## Level 1：两层 dict，三个方法，别的都不写

签名照抄锁定的接口文件 `parcel_tracking_system.py`：

```python
from parcel_tracking_system import ParcelTrackingSystem


class ParcelTrackingSystemImpl(ParcelTrackingSystem):
    def __init__(self):
        self.parcels = {}  # parcel_id -> {tag: value}

    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        self.parcels.setdefault(parcel_id, {})[tag] = value

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        return self.parcels.get(parcel_id, {}).get(tag)

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        tags = self.parcels.get(parcel_id)
        if tags is None or tag not in tags:
            return False
        del tags[tag]
        return True
```

逐行说明：

- **`setdefault(parcel_id, {})`**：包裹不存在就建一个空 dict 再返回，存在就直接返回。一行代替"`if parcel_id not in self.parcels: ...`"。
- **`.get(parcel_id, {}).get(tag)`**："包裹不存在"和"tag 不存在"走同一条路径，都返回 `None`，正好就是题目要的。
  这里**不需要写 `if`**：dict 的 `.get` 在找不到时本来就返回 `None`。
- **`remove_tag` 先判断再删**：`del` 一个不存在的 key 会抛 `KeyError`。也可以写成
  `return tags.pop(tag, None) is not None`，但那样会把"值是 `None`"和"不存在"混为一谈。本题值都是字符串，这么写不会出错，
  只是不如显式判断直白。
- **返回真正的 `bool`**：`True/False`。测试用的是 `assertTrue/assertFalse`，返回 `1/0` 也能过，但签名写的是 `-> bool`，照签名来。

真实测试里有一个值得注意的用例（`case_04`，截图里看得到）：

```python
self.tracker.set_tag('sender_name', 'parcel6', 'error')   # 参数故意反过来
```

它检查的是：包裹 id 和 tag 名是两个独立的命名空间。`'sender_name'` 在这里是一个**新包裹**，不能影响 `parcel6` 的 `sender_name` tag。
用两层 dict 就天然满足。如果你图省事用 `f"{parcel_id}:{tag}"` 拼成一个 key，还可能撞 key（比如 `"a:b"` + `"c"` 和 `"a"` + `"b:c"` 拼出来都是 `"a:b:c"`）。

**要不要删掉空包裹？** Level 1 不需要，所有测试都不关心。等到 Level 4 要"数非空包裹"时再处理（参考解是在 `remove` 里删掉空 dict）。

跑测试：`IMPL=starter python3 -m unittest tests.test_level_1`，10 个全绿就进 Level 2。

标准答案单独存在 `../problems/q01_parcel_tracking/solution_level1.py`，可以直接贴进 CodeSignal。

### 常见错法对照（每一种都用测试实际跑过）

| 错法 | 挂在哪些测试 | 错在哪里 |
|---|---|---|
| A. 单层 dict，`f"{parcel_id}{tag}"` 拼 key | case_07 | `"ab"+"c"` 和 `"a"+"bc"` 撞 key；而且 Level 2 列一个包裹的 tag 时得扫全表 |
| B. `get` 写成 `self.parcels[pid][tag]` | case_02–07 | 包裹或 tag 不存在就抛 `KeyError`，题目要求返回 `None` |
| C. `remove` 不判断直接 `del` | case_05, 06 | 删不存在的 tag 会抛 `KeyError`，应该返回 `False` |
| D. `set` 写成 `self.parcels[pid] = {tag: value}` | case_04, 08 | 每次 set 都把这个包裹的其他 tag 冲掉了 |
| E. `remove` 永远返回 `True` | case_05, 06 | 返回值要区分"删掉了"和"本来就没有" |

写法 A 一开始通过了全部 10 个测试，说明我最初的测试漏了撞 key。后来在 case_07 里补了一条断言才抓到。
**教训：只看测试全绿不能证明代码是对的，要拿故意写错的版本去验证测试本身能不能抓到 bug。**


## Level 2：在 Level 1 上加两个方法，别的不动

> 方法名和输出格式是 **(reconstructed)**：照片里 Level 2 只有一行概要"support listing tags on parcels"。
> 格式 `"<tag>(<value>)"`、按 tag 字典序排列，来自同构的 In-Memory Database 原题。真实考试的方法名可能不同，**解锁后以题面为准**，思路不变。

在 `solution_level1.py` 的基础上，只在类的末尾追加这两个方法，前面一个字都不改（完整文件：`solution_level2.py`）：

```python
    def list_tags(self, parcel_id: str) -> list[str]:
        return self.list_tags_by_prefix(parcel_id, "")

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        tags = self.parcels.get(parcel_id, {})
        return [f"{tag}({tags[tag]})" for tag in sorted(tags) if tag.startswith(prefix)]
```

逐行说明：

- **`list_tags` 委托给 `list_tags_by_prefix(parcel_id, "")`**：任何字符串都以空串开头，所以空前缀就是"全部"。
  这不是超前设计，是**避免同一段逻辑写两遍**：排序规则或格式只要改一处。
- **`self.parcels.get(parcel_id, {})`**：和 Level 1 的 `get_tag` 一样的写法，包裹不存在就返回 `[]`，不会抛 `KeyError`。
- **`sorted(tags)`**：对 dict 排序得到的就是排好序的 key 列表。先排序再过滤，结果和先过滤再排序一样。
- **列表推导式**：一行做完三件事，过滤（`startswith`）、排序（`sorted`）、格式化（f-string）。

**为什么这里不写 `_list(parcel_id, prefix, timestamp)`？** 因为 Level 2 没有时间戳。现在就加 `timestamp` 参数属于超前设计：
你不知道 Level 3 的时间语义具体长什么样，写了也可能要改。Level 3 解锁后再改，也就是在这个方法里加一个"是否还活着"的过滤条件，大约 1 分钟。

### 常见错法对照（每一种都用测试实际跑过）

| 错法 | 挂在哪些测试 | 错在哪里 |
|---|---|---|
| A. 不排序，直接遍历 dict | case_01, 04, 08 | dict 保持的是**插入顺序**，不是字典序 |
| B. `sorted(tags, key=str.lower)` | case_04 | 题目说 lexicographically，也就是按码点排，`"B" < "a"`，别自作主张忽略大小写 |
| C. `prefix in tag` | case_07 | 这是子串，不是前缀：`"to"` 在 `"city_to"` 里，但不是它的前缀 |
| D. `f"{tag} ({value})"` 多了一个空格 | case_01, 04, 07, 08 | 字符串格式要逐字照抄 |
| E. 按 value 排序 | case_01, 04, 08 | 排序键是 tag |
| F. `self.parcels[parcel_id]` | case_02 | 包裹不存在会抛 `KeyError`，应该返回 `[]` |

**复杂度：** 每次调用 O(k log k)，k 是这个包裹的 tag 数。每个测试的时限是 0.4 秒，这个量级完全够用。
不需要为前缀查询上 trie 或有序容器，那样既超前设计，又会让 Level 3/4 更难改。

## Level 3：时间来了，做一次重构

到了 Level 3，Level 1 的写法才开始不够用：value 需要带上过期时间。这时候做**两处改动**，大约 5 分钟。

**改动 1：value 换成 `(value, expires_at)`**，`expires_at=None` 表示永不过期。

```python
def _alive(expires_at, timestamp):
    return timestamp is None or expires_at is None or timestamp < expires_at
```

**改动 2：旧方法委托给带时间戳的版本。** 与其把 `get_tag` 和 `get_tag_at` 写成两份几乎一样的代码，不如让 `timestamp=None` 表示"不看过期"：

```python
def _get(self, parcel_id, tag, timestamp):
    entry = self.parcels.get(parcel_id, {}).get(tag)
    if entry is None or not _alive(entry[1], timestamp):
        return None
    return entry[0]

def get_tag(self, parcel_id, tag):              return self._get(parcel_id, tag, None)
def get_tag_at(self, parcel_id, tag, timestamp): return self._get(parcel_id, tag, timestamp)
```

set / remove 同理。Level 2 的 `list_tags_by_prefix` 也照此处理：改成带 `timestamp` 的 `_list`，在推导式里加一个 `_alive(...)` 过滤条件。重构完先把 Level 1、2 的测试重跑一遍，确认没有退化（regression），再去跑 Level 3。

注意 `entry is None`：**不要写成 `if not entry[0]`**，空字符串 `""` 是合法值。

`_remove` 也要跟着改：已经过期的 tag 等于不存在，删除它应该返回 `False`，但过期条目还是顺手删掉。

语义要点（每条都有测试）：

| 情形 | 行为 | 为什么 |
|---|---|---|
| 在 `expires_at` 那一刻查询 | `None` | 左闭右开 `[t, t+ttl)` |
| TTL 值被 `set_tag_at` 覆盖 | 变成永不过期 | set 就是整个替换 tuple，旧的 `expires_at` 自然没了 |
| TTL 值被新的 TTL 覆盖 | 按新的 TTL 算 | 同上 |
| 删除已过期的 tag | `False` | 过期即不存在 |

**为什么采用"惰性过期"（lazy expiry），而不是后台清理？** 题目保证时间戳严格递增，但并不会每个时刻都调用你。
惰性过期就是读的时候再判断 `_alive(...)`，实现最简单，也不会出错。
主动清理（用堆 heap 按 `expires_at` 排）是生产系统的做法，比如 Redis 就是惰性 + 定期抽样两种结合；放在 OA 里是过度设计。

## Level 4：checkpoint / restore，本题真正的难点

### checkpoint：只存活着的，存剩余寿命

```python
def checkpoint(self, timestamp):
    snapshot = {}
    for parcel_id, tags in self._parcels.items():
        kept = {t: (v, None if exp is None else exp - timestamp)
                for t, (v, exp) in tags.items() if _alive(exp, timestamp)}
        if kept:
            snapshot[parcel_id] = kept
    self._checkpoint_times.append(timestamp)
    self._snapshots.append(snapshot)
    return len(snapshot)
```

这几行里有三个决定：

1. **新建字典和 tuple**，而不是引用活状态。这是深拷贝，也就是心法 4：`test_level_4_case_05` 专门测浅拷贝漏写。
2. **只存还活着的**。已经过期的不进快照，否则 restore 会让它复活（`case_07`）。
3. **存 `remaining = expires_at - timestamp`**（心法 5）。返回值 = 至少有一个活 tag 的包裹数，`len(snapshot)` 正好就是。

### restore：找"≤ t 的最近一个"，再重建

```python
def restore(self, timestamp, timestamp_to_restore):
    i = bisect.bisect_right(self._checkpoint_times, timestamp_to_restore) - 1
    self._parcels = {pid: {t: (v, None if r is None else timestamp + r) for t, (v, r) in tags.items()}
                     for pid, tags in self._snapshots[i].items()}
```

- **`bisect_right(..) - 1`** 就是"最后一个 ≤ x 的位置"的标准写法。`bisect_left` 找的是"第一个 ≥ x"，差一位，而恰好等于 x 的情形会错。
  checkpoint 时间是严格递增追加的，列表天然有序，所以可以直接二分。
  不用 bisect 也行，线性扫一遍完全够用；但 bisect 这个写法值得背下来，它在 Time-Based Key-Value Store（LC 981）等一大类"按时间查历史版本"的题里反复出现。
- **重新构造一份新的 dict**，而不是 `self._parcels = self._snapshots[i]`。后者让活状态和快照共享对象，下一次写入就污染了快照（`case_06`）。
- **TTL 换算**：`timestamp + remaining`。例子：checkpoint(3) 时 p1.a 在 11 过期，剩 8；restore(20, 3) 之后在 28 过期。
- restore **整体替换**状态，所以 checkpoint 之后新建的包裹会消失（`case_08`）。

## 复杂度（实测）

| 操作 | 时间 | 说明 |
|---|---|---|
| set / get / remove（含 `_at`） | O(1) | dict |
| list（含前缀、`_at`） | O(k log k) | k = 这个包裹的 tag 数 |
| checkpoint | O(N) | N = 全部 tag 数，每次全量拷贝 |
| restore | O(N + log C) | C = checkpoint 个数 |

`test_level_3_case_08`：5 万次 set + 5 千次 get + 500 次前缀列表，在本机几十毫秒内跑完，离真实测试的 `@timeout(0.4)` 还很远。
全量快照的内存是 O(N × C)；OA 的规模下没问题。生产系统会用写时复制（copy-on-write）或持久化数据结构（persistent data structure）来共享没有变化的部分，面试可以口头提一句，**OA 里别写**。

## 如果是面试官追问

- "checkpoint 很多、数据很大怎么办？"：增量快照（delta）或写时复制，只记录两次 checkpoint 之间的变化。
- "时间戳如果不保证递增呢？"：`_checkpoint_times` 不能再直接 append，要用 `bisect.insort`；而且 `set_tag_at` 要考虑乱序写入覆盖更新值的问题，那就需要按 tag 保存多版本历史。
- "多线程呢？"：每个包裹一把锁，或者整体一把读写锁；checkpoint 需要一致性快照，要么全局停写，要么 MVCC。

## 自测清单（合上代码，能答出来就算掌握）

1. Level 1 为什么用两层 dict，而不是 `f"{parcel_id}:{tag}"` 拼成一个 key？（提示：`case_04`）
2. `alive` 为什么用 `<` 而不是 `<=`？
3. 为什么 `_get` 里不能写 `if not entry[0]`？
4. 浅拷贝快照和 restore 引用别名分别会让哪个测试挂掉？
5. 快照里为什么存 remaining，而不是 expires_at？
6. `bisect_right(a, x) - 1` 求的是什么？换成 `bisect_left` 会在什么输入上错？
