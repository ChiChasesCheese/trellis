# 04 · 类设计 + 并发：契约先行 · 四个数据结构 · 锁的五步答法

> 覆盖 `od01`–`od09`（od07 未建题，跳过）。依据 `../../catalog/skills_matrix.md` S09（契约先行）/ S10（并发正确性）/ S11（持久化）/ S12（缓存淘汰）/ S13（队列语义）。先读 `01-solving-framework.md` §2 的 45 min OOD 框架，这里是里面每一步具体怎么落地。

---

## 1. 契约先行清单（45 min 的前 5 分钟必须做完）

`../../catalog/raw/ood.md` 的 cross-cutting 记录：**"task scheduler 挂经就是契约没定清"**——不是算法不会，是没在写代码前把下面 6 件事说出口：

1. **每个 public 方法的完整签名**：参数类型、返回类型、空/异常情况返回什么（`None`？抛异常？空列表？）。
2. **重复调用的语义**：同一个 id 二次 `add` 是覆盖、忽略、还是报错？（`od01`：未执行过的 id 重新 `add` 会**递增版本号**使旧堆条目失效，已执行过的 id 再 `add` 是**静默 no-op**——这是两条不同的规则，必须都说出口。）
3. **不变量**：这个类在任意时刻必须保持什么为真？（`od03`："每个线程自己的事务栈只包含它自己写过的 key"。）
4. **谁持有状态、状态的生命周期**：进程内存？会不会跨请求/跨线程共享？
5. **失败模式先声明**："如果队列空了 `execute()` 返回什么"这类问题，要在写代码前问面试官或自己拍板并说出来。
6. **是否需要并发/持久化**——即使题面没直接问，`od01`–`od09` 里 5/9 道有明确并发追问、2/9 道有持久化追问，默认假设会被问。

**说出口的句子**：
> "Before I write any code, let me lock down the contract: `add(task_id, priority, ts)` is idempotent once executed — re-adding an already-executed id is a no-op — but re-adding a pending id bumps it to the new priority/timestamp. `execute()` returns an empty string if nothing is pending. Does that match your expectation?"

---

## 2. 懒删除堆（Lazy-Deleted Heap）

**用在哪**：优先队列里的某个元素"过期"或"被更新"了，但从堆里物理删除是 O(n)——**不删，等它自然弹出时再判断是否还有效**。

```python
import heapq
class LazyHeap:
    def __init__(self):
        self._heap = []                 # (sort_key, id, version)
        self._versions = {}             # id -> 当前有效版本号
        self._done = set()              # 永久失效的 id

    def push(self, item_id, sort_key):
        if item_id in self._done:
            return
        v = self._versions.get(item_id, 0) + 1
        self._versions[item_id] = v
        heapq.heappush(self._heap, (sort_key, item_id, v))

    def pop_valid(self):
        while self._heap:
            key, item_id, v = heapq.heappop(self._heap)
            if item_id in self._done or self._versions.get(item_id) != v:
                continue                # 过期条目：物理还在堆里，逻辑上已作废
            self._done.add(item_id)
            return item_id
        return None
```

**本 kit**：`od01`（Task Scheduler）——`_heap` 里 `(-priority, timestamp, task_id, version)`，重复 `add` 同一个未执行 id 会递增 `version`，`execute()` 弹出时检查 `version` 是否仍是最新的，不是就跳过继续弹。**这比每次 `add` 都扫描堆找旧条目删除快得多**（O(log n) vs O(n)）。

**面试里怎么说**：
> "Instead of searching the heap for a stale entry, I bump a per-id version counter on re-add and just skip stale versions when popping — amortized O(log n) per operation."

---

## 3. 撤销日志栈（Undo Log Stack）

**用在哪**：需要"撤销一批操作"（事务 rollback），或者"重放操作序列得到等价状态"（持久化/replay）。**两种用途底层是同一个结构：一份只记录"这次改了什么"的增量日志，而不是全量快照。**

**事务嵌套版**（`od03`，每线程一份 overlay 栈）：
```python
_DELETED = object()
class TxnKV:
    def __init__(self):
        self._global = {}
        self._stack = []            # 每个 frame: dict[key -> value 或 _DELETED]

    def get(self, key):
        for frame in reversed(self._stack):
            if key in frame:
                v = frame[key]
                return None if v is _DELETED else v
        return self._global.get(key)

    def put(self, key, value):
        (self._stack[-1] if self._stack else self._global)[key] = value

    def begin(self):  self._stack.append({})
    def commit(self):
        frame = self._stack.pop()
        (self._stack[-1] if self._stack else self._global).update(frame)
    def rollback(self): self._stack.pop()      # 直接丢弃这一帧，不需要额外的"反操作"记录
```

**关键洞察**：`rollback()` 不需要记录"反操作"（比如"把 x 改回旧值"），因为每个 frame **只保存这次事务自己写过的 key**，丢弃整个 frame 就等价于撤销这次事务的所有写入——这比记录 undo 操作列表更简单，前提是 frame 之间是严格嵌套的栈结构。

**操作日志 replay 版**（`od01` 的持久化）：`snapshot()` 返回操作日志（`["ADD t1 3 10", "EXEC", ...]`），`replay(log)` 从空状态重新执行一遍日志重建调度器——**这是"撤销日志栈"思路在持久化场景的变体：日志本身就是"可重放的操作序列"，不需要序列化内部数据结构（堆、版本号）**。

**本 kit**：`od03`（S10，事务嵌套 + 并发：每线程 `threading.local()` 一份栈，读写全局态才加锁）、`od01`（S11，日志 + replay 做持久化）。

**最易错**：
- frame 只存"这次事务自己碰过的 key"，**不要**在 `begin()` 时把当前全局状态整个复制一份（那是全量快照，不是增量日志，嵌套事务下会退化成 O(depth × size)）。
- `commit()` 把当前 frame 合并进上一层（`update`，后写赢），**不是**直接写穿到全局——只有最外层 `commit()` 才真正落地到全局态。

---

## 4. 哈希 + 双链表（LRU 的标准结构；kit 里用 `OrderedDict` 实现同等效果）

**用在哪**：需要 O(1) 的"按最近使用顺序淘汰"。标准答案是**手写**哈希表 + 双向链表（面试官可能明确要求"不许用语言内置的有序字典"）；`od08` 的参考实现为了简洁用了 `collections.OrderedDict`（`move_to_end` + `popitem(last=False)` 就是双链表的"移到尾部"和"弹出头部"）。**两种写法说的是同一件事，面试时先说 O(1) 的原理，再问面试官要不要手写双链表。**

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity):
        self._cap = capacity
        self._data = OrderedDict()      # 插入序 = 访问序：get/set 都 move_to_end

    def get(self, key):
        if key not in self._data: return -1
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self._cap:
            self._data.popitem(last=False)   # 弹出最久未使用（链表头）
```

**如果被要求手写双链表**：每个节点 `{key, value, prev, next}`，哈希表存 `key -> node`；`get`/`put` 都要做"从当前位置摘除 + 插到链表尾"两步，`evict` 就是"摘除头节点（哨兵之后那个）"。**核心是所有操作都是 O(1) 的指针改动，不涉及遍历。**

**本 kit**：`od08`（LRU/TTL/两级缓存，S12——对应 Snowflake 的仓库 SSD 缓存 + 远端对象存储两层框架，见 `05-sd-framework-snowflake-primitives.md`）。TTL 版本的追问："优先淘汰已过期的条目，其次才做真正的 LRU 淘汰"——`od08` 的 `TTLCache` 就是先查有没有已过期的，没有才退化成普通 LRU 弹出。

**最易错**：
- 双链表版忘记**哨兵头尾节点**（dummy head/tail），导致空链表/单节点链表的边界代码要写两套。
- `get` 命中后也要移动位置（"访问即最近使用"），这一步经常被漏掉，只在 `put` 时更新顺序。

---

## 5. Deque 滑窗：限流器与事件流

**用在哪**：「过去 W 秒内最多 N 次」——`deque` 存时间戳，左边过期就弹出，右边追加。

```python
from collections import deque
class SlidingWindowLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self._accepted = deque()

    def allow(self, t):
        while self._accepted and self._accepted[0] <= t - self.window:
            self._accepted.popleft()          # 过期的历史记录，左边弹出
        if len(self._accepted) < self.limit:
            self._accepted.append(t)
            return True
        return False
```

**多规则叠加版**（`od04` part2/3）：多个限流规则同时生效，"最早能通过所有规则的时刻"要对每条规则各自维护一个 deque，反复把候选时间 `t` 往后推，直到**同时**满足所有规则（`_advance` 函数：`while advanced: for each rule: 若还不满足就把 t 推到该规则允许的最早时刻`）。

**本 kit**：`od04`（S06/S10 都覆盖：单规则版是纯滑窗，多规则版加了"线程安全的原子占用"追问）。

**最易错**：
- 判断"过期"用 `<=` 还是 `<` 取决于窗口是左闭右开还是双闭区间，题面通常用"过去 W 秒"这种模糊说法，要主动跟面试官确认边界。
- 多规则版每条规则的 deque 长度天然不会超过它自己的 `limit`（因为只有确认有空位才会 append），所以按下标访问是安全的，不需要额外检查长度。

---

## 6. 锁的五步答法：临界区 → 最小锁 → 分段 → 存储层 CAS/lease → 怎么测

面试问"how would you make this thread-safe"时，按这五步说，每一步都要有 kit 里的具体例子撑住，不要停在"加个锁"就结束。

### ① 先指出临界区（critical section）是什么

> "The critical section is 'scan the heap for a valid candidate, then mark it executed' — if two threads interleave here, both could return the same task id."（`od01`）

### ② 最小化锁的范围

> "I wrap only the scan-and-mark sequence, not the whole `add()`/`execute()` call — building the heap entry itself doesn't need the lock."

`od02` 的文件系统是范例：**结构锁**（`_tree_lock`）只在遍历目录树/改变树形状时持有，且只持有 O(depth) 的时间；一旦定位到具体文件，写内容用的是**那个文件自己的锁**，不再占用结构锁。

### ③ 分段（按 key 拆锁，减少争用）

> "Different files have independent locks, so two threads writing to different files never contend — only concurrent writes to the *same* file serialize."

```python
class _File:
    def __init__(self):
        self.chunks = []
        self.lock = threading.Lock()      # 每个文件自己的锁，不是全局一把锁
```

`od02` 正是"结构锁 + 每文件锁"两层分段的例子：树形状变更互斥（全局但短暂），文件内容写入按文件分段（细粒度、可并行）。

### ④ 存储层用 CAS / lease，不是长期持锁

> "For the multi-instance case, I wouldn't hold a distributed lock — I'd have each instance attempt an atomic claim (a lease keyed by (job_id, minute)); losing the race is a normal outcome, not an error."

```python
class LeaseStore:
    def __init__(self):
        self._claimed = set()
        self._lock = threading.Lock()

    def try_claim(self, job_id, minute):
        with self._lock:
            key = (job_id, minute)
            if key in self._claimed:
                return False              # 别的实例已经抢到了，正常失败，不是异常
            self._claimed.add(key)
            return True
```

`od05`（Cron Scheduler）用 `LeaseStore.try_claim` 实现"多副本不重复触发"——这正是 `05-sd-framework-snowflake-primitives.md` 里"唯一约束 + CAS"构件的类设计版本，也是 Snowflake **Execution Anchor**（每个查询绑定恰好一个 GS 实例）的迷你复刻。

### ⑤ 怎么测并发正确性

**面试里说的测试策略**（写不完代码时，口述这一步也能拿分）：
1. **不变量断言**，而不是掐时间：跑 N 个线程各自调用 `execute()` M 次，断言"所有返回结果里没有重复的 task_id"（`od01`），而不是断言"运行时间应该是多少"。
2. **用 `concurrent.futures.ThreadPoolExecutor` 压力跑，重复多次**（因为 GIL 下真正的数据竞争不总是每次都触发，多跑几轮提高发现概率）。
3. **人为制造交错**：在关键操作前插入 `time.sleep(0)`（主动让出 GIL）或用 `threading.Barrier` 让多个线程在临界区前对齐，放大竞态窗口。
4. **对 lease/CAS 逻辑**：跑多个"实例"并发调用同一个 `try_claim(job_id, minute)`，断言**恰好一个**返回 `True`。

---

## 7. Python `threading` 在面试里怎么写

- **`threading.Lock()`**：最常用；`with lock:` 包住临界区，忘记 `with` 直接 `acquire()`/`release()` 容易在异常路径上死锁——**面试里永远用 `with`**。
- **`threading.local()`**：每线程私有状态，不需要加锁（`od03` 的事务栈）——**注意它不是"线程安全的共享状态"，而是"从根本上不共享"**，两者语义不同，别混说。
- **`threading.Condition` / `Event`**：需要"等待某个条件成立才继续"时用（kit 里目前的题都没直接考，但队列的阻塞式 `dequeue` 追问可能会问到）。
- **GIL 对面试答案的影响**：Python 的 GIL 保证单条字节码指令级别的原子性，但**不保证复合操作**（`x += 1`、`dict.setdefault` 后再赋值）的原子性——**面试里不要用"反正有 GIL 应该没事"当答案**，这是减分项；正确说法是"GIL 让某些语言给的原子性保证在 CPython 里成立，但业务层的复合操作仍然需要显式锁"。详细见 `../00-prereq/02-concurrency-basics.md` §4。

---

## 8. 队列语义：at-least-once 与故障重投

**一眼信号**：「队列服务」「消息被消费后又要能重新出现」「故障不能丢消息」。

```python
class MessageQueue:
    def __init__(self):
        self._ready = deque()                 # 待投递
        self._in_flight = {}                  # id -> (visible_at, delivery_seq)

    def dequeue(self, now):
        self._requeue_expired(now)            # 超时未确认的，重新排到队尾
        if not self._ready: return None
        mid = self._ready.popleft()
        self._in_flight[mid] = (now + VISIBILITY_TIMEOUT, self._next_seq())
        return mid

    def ack(self, mid):
        self._in_flight.pop(mid, None)        # 确认消费，彻底移除
```

**本 kit**：`od09`（Queue → Service，S13）。两种"消息重新出现"的语义要分清：`dequeue` 里的**被动超时重投**（可见性超时到了，重新排到队**尾**，按超时时间升序）vs. 崩溃恢复的 `requeue_all_in_flight`（服务重启后**不再信任任何在制品**，把所有 in-flight 消息按**原始投递顺序**排到队**头**）——一个是"队尾、按到期时间"，一个是"队头、按投递顺序"，面试里被追问"故障恢复语义"时这个区别是得分点。

**面试里怎么说**：
> "This gives at-least-once delivery — a message can be redelivered after a visibility timeout or a crash, so consumers must be idempotent. I wouldn't try to promise exactly-once at this layer."

---

## 9. 审计日志：不可变 + 时间窗查询

**一眼信号**：「记录访问历史」「查某个时间范围内被访问过什么」「多久没被访问过」——`od06`（S 未单列但属于 D06 审计/治理主题）。

```python
import bisect
class AuditLog:
    def __init__(self):
        self._records = {}          # name -> 按 ts 排序的 (ts, id) 列表
        self._last_access = {}      # name -> 最近一次 ts，O(1) 更新

    def record_access(self, record_id, ts, names):
        for name in names:
            bisect.insort(self._records.setdefault(name, []), (ts, record_id))
            self._last_access[name] = max(self._last_access.get(name, float("-inf")), ts)

    def accessed_in_range(self, name, t_start, t_end):
        lst = self._records.get(name, [])
        lo = bisect.bisect_left(lst, (t_start, ""))
        hi = bisect.bisect_left(lst, (t_end + 1, ""))
        return [rid for _, rid in lst[lo:hi]]
```

**关键点**：访问事件可能**乱序到达**（`bisect.insort` 而不是假设 append 即有序）；"多久没被访问"只需要一个 `name -> last_ts` 的字典，**不需要**为了这一个查询去维护一个额外的按最近访问排序的结构（那个结构在"几乎每次访问都刷新最大值"的场景下会退化）。

**本 kit**：`od06`（S/D06，Query Audit Log，对应 Snowflake `QUERY_HISTORY`/`pg_stat` 类审计场景）。追问方向常是"不可变性"（记录只增不改）和"保留策略"（多久之后归档/删除），详见 `05-sd-framework-snowflake-primitives.md` 的"不可变日志"构件。
