# q01 · 包裹追踪系统（Parcel Tracking System）逐级带写

题面：`../problems/q01_parcel_tracking/problem.md`。通用心法：`essentials_codesignal_icf.md`（建议先读）。
代码：`../problems/q01_parcel_tracking/solution.py`（4 级做完后的最终形态；变量名是 `self._parcels`）。你自己写的版本放在 `starter.py`，用 `IMPL=starter` 跑测试。

```bash
cd vault/interviews/companies/airbnb/problems/q01_parcel_tracking
IMPL=starter python3 -m unittest tests.test_level_1      # 只跑 Level 1
IMPL=starter bash run_single_test.sh case_06              # 只跑一个测试
python3 -m unittest discover -s tests -p "test_*.py"      # 参考解：38/38 应该全绿
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
> **已核实**：Chi 在 mock 里贴出的真实接口 docstring 确认，Level 2 就叫 `list_tags` / `list_tags_by_prefix`，
> 格式 `"tag(value)"`，按 tag 名字典序排列，包裹不存在时返回空列表。真实 Level 2 有 10 个测试。

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

## Level 3：时间来了，做第一次重构

> 题面已有真实截图（`../catalog/raw/codesignal_parcel_tracking_photos.md` 第三批），下面是按真实签名写的。
> 我最初按同构原题补全的版本错了两处：带 TTL 的方法叫 **`set_tag_with_hold`**，不叫 `set_tag_at_with_ttl`；
> **`ttl == 0` 表示永不过期**，不是立即过期。其余（方法名、`"tag(value)"` 格式、按 tag 字典序、右端点开区间）都对上了。

到这一级，Level 2 的写法才第一次不够用：value 需要带上过期时间。完整文件是 `solution_level3.py`。
相对 Level 2 **只有两处改动**，大约 5 分钟：

**改动 1：存储从 `{tag: value}` 变成 `{tag: (value, expires_at)}`**，`expires_at=None` 表示永不过期。另外加一个判断存活的函数：

```python
def set_tag_with_hold(self, parcel_id, tag, value, timestamp, ttl):
    expires_at = None if ttl == 0 else timestamp + ttl   # 题面：ttl 为 0 时不过期
    self.parcels.setdefault(parcel_id, {})[tag] = (value, expires_at)
```

`ttl == 0` 这一条是题面里最容易读漏的一句。直接写 `timestamp + ttl` 的话，tag 在设置的那一刻就过期了，因为 `timestamp < timestamp` 为假。

```python
def _alive(entry, timestamp):
    expires_at = entry[1]
    return timestamp is None or expires_at is None or timestamp < expires_at
```

**改动 2：逻辑搬进 `_at` 版本，旧方法改成调用它，传 `timestamp=None`**（表示不看过期）：

```python
def get_tag(self, parcel_id, tag):
    return self.get_tag_at(parcel_id, tag, None)

def get_tag_at(self, parcel_id, tag, timestamp):
    entry = self.parcels.get(parcel_id, {}).get(tag)
    if entry is None or not _alive(entry, timestamp):
        return None
    return entry[0]

def remove_tag_at(self, parcel_id, tag, timestamp):
    tags = self.parcels.get(parcel_id)
    if tags is None or tag not in tags or not _alive(tags[tag], timestamp):
        return False
    del tags[tag]
    return True

def list_tags_by_prefix_at(self, parcel_id, prefix, timestamp):
    tags = self.parcels.get(parcel_id, {})
    return [f"{tag}({tags[tag][0]})" for tag in sorted(tags)
            if tag.startswith(prefix) and _alive(tags[tag], timestamp)]
```

对照 Level 2 看改了什么：`get` 多一个 `_alive` 判断；`remove` 的 `if` 多一个条件；`list` 的推导式多一个 `and _alive(...)`，
value 变成 `tags[tag][0]`。结构完全没变，**这就是 Level 1/2 不超前设计的回报**：没有多余的东西需要拆。

**为什么让旧方法调用 `_at` 版本，而不是复制一份？** 如果 `get_tag` 和 `get_tag_at` 各写一份，Level 4 或者以后改存储格式时就要改两处，漏改一处测试就会挂。
这次重构是 Level 3 真的需要了才做的，不是提前准备的。
（小瑕疵：签名写的是 `timestamp: int`，这里传的是 `None`。Python 不强制类型标注，测试也不检查；介意的话可以另写一个私有的 `_get(…, timestamp)`，效果一样。）

**重构完先重跑 Level 1、2 的测试，再跑 Level 3。** 下面错法 G 就是例子：`set_tag` 忘了改，还在存裸字符串，Level 1、2 挂了 14 个测试。

几个细节：

- **`set_tag_at` 直接调用 `set_tag`，不存设置时刻。** 判断 tag 在 `ts` 是否有效需要 `设置时刻 <= ts < 过期时刻`。
  题面保证时间戳不倒退，所以之后任何查询都满足 `ts >= 设置时刻`，前半个条件自动成立，只需要存过期时刻。
  验证方法：写一个存完整历史、按"as it was at timestamp"字面意思回答的 oracle，和本解法跑随机操作做对照。
  时间非递减时，20 个种子 × 3000 次操作结果完全一致；时间乱序时第 8 步就不一致（先在较晚时刻 set，再查询更早时刻）。
  **所以这个简化的正确性完全依赖"时间不倒退"这条保证。** 想上保险就存 `(value, start, expires_at)`，改两行，
  但这样会引出 L1 的 `set_tag` 没有时间、L4 restore 时 `start` 怎么算之类题面没定义的问题，属于超前设计，不建议加。
- **时间戳是"非递减"（non-decreasing），不是严格递增**：同一时刻可以有多个操作（测试 case_09）。
  另外，题面自己的第二个例子在 `remove_tag_at(..., 50)` 之后又调用了 `set_tag_with_hold(..., 20, ...)`，时间倒回去了，和它自己的保证矛盾。
  好在 Level 3 的写法根本不依赖时间单调，所以不受影响。**一般原则：别让正确性依赖题面上看起来可有可无的保证。**
- **`remove_tag_at` 遇到过期的 tag 返回 `False`，但不删除它。** 过期条目留在 dict 里没有害处，因为 get 和 list 都会过滤掉它。
  删不删是性能问题，不是正确性问题，OA 里不管它。
- **`entry is None`**，不要写成 `if not entry[0]`：空字符串 `""` 是合法值。

语义要点（每条都有测试）：

| 情形 | 行为 | 为什么 |
|---|---|---|
| 在 `expires_at` 那一刻查询 | `None` | 左闭右开 `[t, t+ttl)` |
| TTL 值被 `set_tag_at` 覆盖 | 变成永不过期 | set 就是整个替换 tuple，旧的 `expires_at` 自然没了 |
| TTL 值被新的 TTL 覆盖 | 按新的 TTL 算 | 同上 |
| 删除已过期的 tag | `False` | 过期即不存在 |

### 常见错法对照（每一种都用测试实际跑过）

| 错法 | 挂在哪些测试 | 错在哪里 |
|---|---|---|
| A. `timestamp <= expires_at` | L3 case_01, 02, 04, 06–08 | 区间是左闭右开，到 `expires_at` 那一刻就已经过期 |
| B. `expires_at = timestamp + ttl - 1` | L3 case_04, 06, 08 | 用 `<` 判断时，再减 1 就提前一刻过期了 |
| C. `set_tag_at` 保留旧的 TTL | L3 case_05, 07 | 重新 set 就是整条替换，旧的过期时间应该清掉 |
| D. 删除过期 tag 返回 `True` | L3 case_02, 07 | 过期等于不存在 |
| E. list 不过滤过期 | L3 case_08 | 所有读操作都要判断存活 |
| F. get 不看过期 | L3 case_01, 04, 06 | 同上 |
| G. 重构时 `set_tag` 忘了改，还存裸字符串 | L1 挂 9 个、L2 挂 5 个、L3 挂 4 个 | **重构后必须回归测试** |
| H. `ttl == 0` 当成立即过期 | L3 case_03 | 题面明写 "If `ttl` is `0`, the tag does not expire" |
| I. 方法名写错（比如写成 `set_tag_at_with_ttl`） | L3 case_01–04, 06, 08 | 报的是 **FAIL 不是 AttributeError**：锁定的接口类有默认实现（`pass`），写错名字的调用被它悄悄吞掉了 |

**真实案例（Chi 的 mock，2026-09-27）**：重构后 `list_tags_by_prefix` 还保留着 Level 2 的方法体，把整个 tuple 格式化了出来：
`"address(('1', None))"` 对比期望的 `"address(1)"`，Level 2 挂了 6 个测试。`list_tags` 没挂，因为它已经改成直接调用 `_at` 版本。
这正是错法 G 那一类问题。**检查办法：重构后在编辑器里搜 `self.parcels`，只有 5 个方法应该直接碰它**
（`set_tag`、`set_tag_with_hold`、`get_tag_at`、`remove_tag_at`、`list_tags_by_prefix_at`），其余都应该是一行转调。多出来的那个就是漏改的。

错法 I 值得单独记住：CodeSignal 的接口类给每个方法都写了默认实现。**方法名拼错时不会报"方法不存在"，只会出现"值不对"**，很容易误以为是逻辑错了。
遇到"整级都在 FAIL"时，先对一遍方法名和参数顺序。

**为什么采用"惰性过期"（lazy expiry），而不是后台清理？** 题目保证时间戳不会倒退，但并不会每个时刻都调用你。
惰性过期就是读的时候再判断 `_alive(...)`，实现最简单，也不会出错。
主动清理（用堆 heap 按 `expires_at` 排）是生产系统的做法，比如 Redis 就是惰性 + 定期抽样两种结合；放在 OA 里是过度设计。

## Level 4：checkpoint / restore_checkpoint，只加不改

> 题面已有真实截图（`../catalog/raw/codesignal_parcel_tracking_photos.md` 第五批）。和我最初补全的版本相比，只有方法名不同：
> 真实的是 **`restore_checkpoint`**，不是 `restore`。过期时间公式 `original_expiration + (timestamp - checkpoint_timestamp)`
> 和我补全的 `timestamp + (original_expiration - checkpoint_timestamp)` 代数上等价。

完整文件是 `solution_level4.py`。和 Level 3 的 diff 只有三块，**已有代码一行都没改**：

**第 1 块：`__init__` 加一个字段**

```python
        self.checkpoints = []  # [(checkpoint_timestamp, copy of self.parcels)], oldest first
```

**第 2 块：`checkpoint`**

```python
    def checkpoint(self, timestamp: int) -> int:
        self.checkpoints.append((timestamp, {pid: dict(tags) for pid, tags in self.parcels.items()}))
        return sum(1 for tags in self.parcels.values() if any(_alive(e, timestamp) for e in tags.values()))
```

- **拷贝要拷两层**：外层 dict（包裹）和内层 dict（tag）各新建一份。tuple 本身不可变，不用再往下拷。
  只拷外层（`dict(self.parcels)`）的话，内层 tag dict 还是共享的，之后 `set_tag` 往里写，快照就跟着变了（错法 A）。
- **原样存，不过滤、不换算**。过期的 tag 也一起存进去，这样是安全的：它的过期时刻 ≤ checkpoint 时刻，
  平移 `delta` 之后 ≤ restore 时刻，而之后的查询都 ≥ restore 时刻（时间不倒退），所以它永远查不出来。
  我拿"先过滤过期、再存剩余寿命"的旧版 `solution.py` 和这份答案做了对照：200 个随机种子，每个 1500 次操作，结果完全一致。
- **返回值数的是包裹，不是 tag**："number of parcels that are currently alive (have at least one valid tag)"。
  `any(...)` 表示至少有一个有效 tag，`sum(1 for ...)` 数有多少个这样的包裹。

**第 3 块：`restore_checkpoint`**

```python
    def restore_checkpoint(self, timestamp: int, timestamp_to_restore: int) -> None:
        for checkpoint_timestamp, saved in reversed(self.checkpoints):
            if checkpoint_timestamp <= timestamp_to_restore:
                delta = timestamp - checkpoint_timestamp
                self.parcels = {
                    pid: {tag: (value, None if exp is None else exp + delta) for tag, (value, exp) in tags.items()}
                    for pid, tags in saved.items()
                }
                return
```

- **找"最后一个 ≤ `timestamp_to_restore`"的 checkpoint**：checkpoint 按时间顺序追加，所以倒着扫，第一个满足条件的就是。
  时间相同时，倒着扫先遇到的是后加的那个，也就是最新的。
  `bisect_right(times, x) - 1` 也能做（旧版 `solution.py` 就是这么写的），但线性扫描更短、不容易写错，0.4 秒的时限完全够用。
- **`delta` 用 `checkpoint_timestamp` 算，不是 `timestamp_to_restore`**。题面专门给了一个例子讲这一点：
  checkpoint 在 31，`restore_checkpoint(110, 35)` 的 delta 是 110 − 31 = 79，不是 110 − 35 = 75。`route_east` 从 100 过期变成 179 过期。
- **`None` 保持 `None`**："Tags that were set without a TTL keep no expiration"。`ttl == 0` 在 Level 3 已经存成 `None`，这里自然也不会被平移。
- **restore 时再新建一份 dict**。如果直接 `self.parcels = saved`，活状态和快照就是同一个对象，下一次写入会污染快照，第二次 restore 就错了（错法 C）。**拷贝要两个方向都做。**
- **找不到就什么都不做**：循环走完没有 `return`，状态不变，正好符合 "the operation has no effect"。

### 常见错法对照（每一种都用测试实际跑过）

| 错法 | 挂在哪些测试 | 错在哪里 |
|---|---|---|
| A. `dict(self.parcels)` 浅拷贝 | L4 case_02, 05, 06 | 内层 tag dict 共享，之后的写入漏进快照 |
| B. 直接存 `self.parcels` 的引用 | L4 case_02, 05, 06, 10 | 快照就是活状态本身 |
| C. restore 时 `self.parcels = saved` | L4 case_02, 07 | 活状态指向快照，下一次写入污染快照 |
| D. `delta = timestamp - timestamp_to_restore` | L4 case_02 | 题面例子专门考这一点 |
| E. 不平移过期时间 | L4 case_02 | 恢复出来的 tag 会提前过期 |
| F. 正着扫，选到最早的 checkpoint | L4 case_05 | 要的是最近的那个 |
| G. `<` 而不是 `<=` | L4 case_05, 06, 07, 10 | "at or before"，恰好相等也算 |
| H. 计数时不看过期 | L4 case_04 | 要"至少有一个有效 tag" |
| I. 数的是 tag 数，不是包裹数 | L4 case_02 | 同一个包裹两个 tag，应该算 1 |
| J. 找不到 checkpoint 时清空状态 | L4 case_03 | 应该什么都不做 |
| K. 给 `None` 也加 delta | L4 case_05–10 | 没有 TTL 的 tag 应该保持永不过期 |

**这一级最值得记住的是：快照的拷贝，存和取两个方向都要做。** 错法 A、B、C 都是同一个问题：共享了可变对象。

## 复杂度（实测）

| 操作 | 时间 | 说明 |
|---|---|---|
| set / get / remove（含 `_at`） | O(1) | dict |
| list（含前缀、`_at`） | O(k log k) | k = 这个包裹的 tag 数 |
| checkpoint | O(N) | N = 全部 tag 数，每次全量拷贝 |
| restore_checkpoint | O(N + C) | C = checkpoint 个数，线性倒扫 |

`test_level_3_case_08`：5 万次 set + 5 千次 get + 500 次前缀列表，在本机几十毫秒内跑完，离真实测试的 `@timeout(0.4)` 还很远。
全量快照的内存是 O(N × C)；OA 的规模下没问题。生产系统会用写时复制（copy-on-write）或持久化数据结构（persistent data structure）来共享没有变化的部分，面试可以口头提一句，**OA 里别写**。

## 如果是面试官追问

- "checkpoint 很多、数据很大怎么办？"：增量快照（delta）或写时复制，只记录两次 checkpoint 之间的变化。
- "时间戳如果不保证递增呢？"：`_checkpoint_times` 不能再直接 append，要用 `bisect.insort`；而且 `set_tag_at` 要考虑乱序写入覆盖更新值的问题，那就需要按 tag 保存多版本历史。
- "多线程呢？"：每个包裹一把锁，或者整体一把读写锁；checkpoint 需要一致性快照，要么全局停写，要么 MVCC。

## 自测清单（合上代码，能答出来就算掌握）

1. Level 1 为什么用两层 dict，而不是 `f"{parcel_id}:{tag}"` 拼成一个 key？（提示：`case_04`）
2. `_alive` 为什么用 `<` 而不是 `<=`？`ttl == 0` 为什么要存成 `None`？
3. 为什么 `get_tag_at` 里不能写 `if not entry[0]`？重构后怎么确认没有漏改的方法？
4. 快照为什么要拷两层？restore 时为什么还要再拷一次？
5. 快照里原样存过期的 tag 为什么是安全的？这依赖题面的哪条保证？
6. `restore_checkpoint(110, 35)` 在 checkpoint 为 31 时，delta 是多少，为什么不是 75？
