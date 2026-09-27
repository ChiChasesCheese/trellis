# q01 · 包裹追踪系统（Parcel Tracking System）逐级带写

题面：`../problems/q01_parcel_tracking/problem.md`。通用心法：`essentials_codesignal_icf.md`（建议先读）。
代码：`../problems/q01_parcel_tracking/solution.py`。你自己写的版本放在 `starter.py`，用 `IMPL=starter` 跑测试。

```bash
cd vault/interviews/companies/airbnb/problems/q01_parcel_tracking
IMPL=starter python3 -m unittest tests.test_level_1      # 只跑 Level 1
IMPL=starter bash run_single_test.sh case_06              # 只跑一个测试
python3 -m unittest discover -s tests -p "test_*.py"      # 参考解：32/32 应该全绿
```

## 第 0 步：读题。先看 4 行概要，再看 Level 1

Requirements 里那 4 行就是整道题的地图：

1. tag 的 set / get / remove
2. 列出 tag
3. **带时间戳（timestamp）和可选 TTL**
4. **checkpoint 保存和恢复**

看到第 3、4 行，Level 1 的数据模型就定了：值必须能附带过期时间，状态必须能整体拍快照。
所以我们**不存裸字符串**，而是存一个 `_Tag` 对象。

还有一点：照片里题目页的标题写着 "Filesystem with Unit Tests"，那是 CodeSignal 的项目模板名，**不是题目**。别被它带偏。

## Level 1：数据模型决定一切

```python
@dataclass
class _Tag:
    value: str
    expires_at: int | None = None   # None = 永不过期；存活区间 [设置时刻, expires_at)

    def alive(self, timestamp: int | None) -> bool:
        return timestamp is None or self.expires_at is None or timestamp < self.expires_at
```

状态只有一个字段：`self._parcels: dict[str, dict[str, _Tag]]`，即 parcel_id → tag → _Tag。

**为什么是两层 dict，而不是 `dict[(parcel_id, tag), value]`？** Level 2 要"列出某个包裹的所有 tag"。
用两层 dict，取一个包裹就是 O(1)；用元组做 key，每次都得扫全表。**数据结构要跟着访问模式走（shape follows access pattern）。**

三个私有原语都带一个 `timestamp`，传 `None` 表示不看过期：

```python
def _get(self, parcel_id, tag, timestamp):
    entry = self._parcels.get(parcel_id, {}).get(tag)
    return entry.value if entry is not None and entry.alive(timestamp) else None
```

- `self._parcels.get(parcel_id, {})`：包裹不存在和 tag 不存在走的是**同一条路径**，不需要写两个 if。
- `entry is not None`，**不要写成 `if entry.value`**。空字符串 `""` 是合法值，`test_level_1_case_06` 专门测这个。

`_remove` 有一个细节：删到包裹一个 tag 都不剩时，把包裹也删掉。这样 Level 4 数"非空包裹"时就不会数错。
另外它返回的是 `alive`，而不是 `True`：已经过期的 tag 等于不存在，删除它应该返回 `False`，这是 Level 3 的要求。
这里还是会把过期条目删掉，因为它迟早是垃圾。

公有方法就是薄壳：

```python
def set_tag(self, parcel_id, tag, value):  self._set(parcel_id, tag, value, None)
def get_tag(self, parcel_id, tag):         return self._get(parcel_id, tag, None)
def remove_tag(self, parcel_id, tag):      return self._remove(parcel_id, tag, None)
```

## Level 2：一个通用的列表函数

```python
def _list(self, parcel_id, prefix, timestamp):
    alive = self._alive_tags(parcel_id, timestamp)
    return [f"{t}({alive[t]})" for t in sorted(alive) if t.startswith(prefix)]
```

`list_tags` 就是 `prefix=""` 的特例，因为任何字符串都以空串开头。一个函数覆盖 4 个公有方法（L2 两个、L3 两个）。

这一级的坑：

- **排序是按码点（code point）排的**：`"B" < "a"`，大写在前。题目说 "lexicographically"，就用 Python 默认的 `sorted`，
  **不要自作主张加 `key=str.lower`**。
- **前缀不是子串**：要用 `startswith`，不能用 `in`。`"to"` 出现在 `"city_to"` 里，但不是它的前缀。
- 格式逐字照抄：`tag(value)`，中间没有空格。

复杂度：每次调用是 O(k log k)，k 是这个包裹的 tag 数。题目明说不要求最优，所以**不需要**为前缀查询上 trie 或者维护有序结构，那样只会增加 Level 3/4 的改动面。

## Level 3：时间来了，但我们几乎不用改

因为 Level 1 已经把 `expires_at` 和 `alive(ts)` 准备好了，Level 3 的 6 个方法每个一行：

```python
def set_tag_at_with_ttl(self, parcel_id, tag, value, timestamp, ttl):
    self._set(parcel_id, tag, value, timestamp + ttl)
def get_tag_at(self, parcel_id, tag, timestamp):
    return self._get(parcel_id, tag, timestamp)
```

**这就是心法 2 的回报。** 如果 Level 1 存的是裸字符串，你现在要改所有的读写路径，还可能把 Level 1/2 的测试改挂。

语义要点（每条都有测试）：

| 情形 | 行为 | 为什么 |
|---|---|---|
| 在 `expires_at` 那一刻查询 | `None` | 左闭右开 `[t, t+ttl)` |
| TTL 值被 `set_tag_at` 覆盖 | 变成永不过期 | set 就是整个替换 `_Tag`，旧的 `expires_at` 自然没了 |
| TTL 值被新的 TTL 覆盖 | 按新的 TTL 算 | 同上 |
| 删除已过期的 tag | `False` | 过期即不存在 |

**为什么采用"惰性过期"（lazy expiry），而不是后台清理？** 题目保证时间戳严格递增，但并不会每个时刻都调用你。
惰性过期就是读的时候再判断 `alive(ts)`，实现最简单，也不会出错。
主动清理（用堆 heap 按 `expires_at` 排）是生产系统的做法，比如 Redis 就是惰性 + 定期抽样两种结合；放在 OA 里是过度设计。

## Level 4：checkpoint / restore，本题真正的难点

### checkpoint：只存活着的，存剩余寿命

```python
def checkpoint(self, timestamp):
    snapshot = {}
    for parcel_id, tags in self._parcels.items():
        kept = {t: (e.value, None if e.expires_at is None else e.expires_at - timestamp)
                for t, e in tags.items() if e.alive(timestamp)}
        if kept:
            snapshot[parcel_id] = kept
    self._checkpoint_times.append(timestamp)
    self._snapshots.append(snapshot)
    return len(snapshot)
```

这几行里有三个决定：

1. **新建字典和 tuple**，而不是引用活状态。这是深拷贝，也就是心法 4：`test_level_4_case_05` 专门测浅拷贝漏写。
2. **只存 `alive(timestamp)` 的**。已经过期的不进快照，否则 restore 会让它复活（`case_07`）。
3. **存 `remaining = expires_at - timestamp`**（心法 5）。返回值 = 至少有一个活 tag 的包裹数，`len(snapshot)` 正好就是。

### restore：找"≤ t 的最近一个"，再重建

```python
def restore(self, timestamp, timestamp_to_restore):
    i = bisect.bisect_right(self._checkpoint_times, timestamp_to_restore) - 1
    self._parcels = {pid: {t: _Tag(v, None if r is None else timestamp + r) for t, (v, r) in tags.items()}
                     for pid, tags in self._snapshots[i].items()}
```

- **`bisect_right(..) - 1`** 就是"最后一个 ≤ x 的位置"的标准写法。`bisect_left` 找的是"第一个 ≥ x"，差一位，而恰好等于 x 的情形会错。
  checkpoint 时间是严格递增追加的，列表天然有序，所以可以直接二分。
  不用 bisect 也行，线性扫一遍完全够用；但 bisect 这个写法值得背下来，它在 Time-Based Key-Value Store（LC 981）等一大类"按时间查历史版本"的题里反复出现。
- **重新构造 `_Tag`**，而不是 `self._parcels = self._snapshots[i]`。后者让活状态和快照共享对象，下一次写入就污染了快照（`case_06`）。
- **TTL 换算**：`timestamp + remaining`。例子：checkpoint(3) 时 p1.a 在 11 过期，剩 8；restore(20, 3) 之后在 28 过期。
- restore **整体替换**状态，所以 checkpoint 之后新建的包裹会消失（`case_08`）。

## 复杂度（实测）

| 操作 | 时间 | 说明 |
|---|---|---|
| set / get / remove（含 `_at`） | O(1) | dict |
| list（含前缀、`_at`） | O(k log k) | k = 这个包裹的 tag 数 |
| checkpoint | O(N) | N = 全部 tag 数，每次全量拷贝 |
| restore | O(N + log C) | C = checkpoint 个数 |

`test_level_3_case_08`：5 万次 set + 5 千次 get + 500 次前缀列表，在本机几十毫秒内跑完，离 3 秒的时限还很远。
全量快照的内存是 O(N × C)；OA 的规模下没问题。生产系统会用写时复制（copy-on-write）或持久化数据结构（persistent data structure）来共享没有变化的部分，面试可以口头提一句，**OA 里别写**。

## 如果是面试官追问

- "checkpoint 很多、数据很大怎么办？"：增量快照（delta）或写时复制，只记录两次 checkpoint 之间的变化。
- "时间戳如果不保证递增呢？"：`_checkpoint_times` 不能再直接 append，要用 `bisect.insort`；而且 `set_tag_at` 要考虑乱序写入覆盖更新值的问题，那就需要按 tag 保存多版本历史。
- "多线程呢？"：每个包裹一把锁，或者整体一把读写锁；checkpoint 需要一致性快照，要么全局停写，要么 MVCC。

## 自测清单（合上代码，能答出来就算掌握）

1. 为什么 Level 1 就要把 value 包成 `_Tag`？
2. `alive` 为什么用 `<` 而不是 `<=`？
3. 为什么 `get` 里不能写 `if entry.value:`？
4. 浅拷贝快照和 restore 引用别名分别会让哪个测试挂掉？
5. 快照里为什么存 remaining，而不是 expires_at？
6. `bisect_right(a, x) - 1` 求的是什么？换成 `bisect_left` 会在什么输入上错？
