# od09 · Queue → Service — deque API, at-least-once ack/visibility timeout, crash redelivery

**类型：** onsite（VO，coding + SD 混合，60 min，3 part）· **最近：** 2026-08
**置信度：** HIGH for 主题/追问方向；具体 ack/visibility-timeout API 与崩溃模拟接口是**重建**

## 背景
一手挂经（1point3acres，t.me/s/usinterview/29299）原话（转述）："Queue class（类 Python
deque）→ 扩展为云端 queue service"，讨论 **enqueue/dequeue 在故障下的行为**；候选人此轮未通过。
面试官后续追问汇总："故障时 enqueue 是否需要确认落盘再返回；at-least-once vs exactly-once 消费；
多消费者的公平调度/优先级队列；队列积压时的背压策略"。这条挂经明确了**主题**（从一个玩具级 deque
类出发，逐步逼近真实云队列服务的故障语义）和**追问方向**，但没有给出具体的方法签名——本题按
"SQS 风格的可见性超时（visibility timeout）+ ack"这个业界标准模式把它具体化成一道可测试的
3-part 题，具体 API 形状标注为**重建**。

## API 契约（英文签名）
```python
class SimpleQueue:
    def enqueue(self, item) -> None: ...
    def dequeue(self) -> object: ...   # raises IndexError if empty (matches collections.deque)
    def peek(self) -> object: ...      # raises IndexError if empty
    def __len__(self) -> int: ...

class MessageQueue:  # (reconstructed: SQS-style ack / visibility timeout)
    def enqueue(self, payload: object) -> str: ...   # returns a new message_id
    def dequeue(self, now: int, visibility_timeout: int) -> tuple[str, object] | None: ...
    def ack(self, message_id: str) -> bool: ...       # False if unknown/already-acked/not in-flight
    def requeue_all_in_flight(self) -> int: ...        # (reconstructed) forces immediate
                                                        # redelivery of every un-acked in-flight
                                                        # message; returns how many were requeued
```

## 规则

### Part 1 — deque 风格的基础队列
`SimpleQueue` 就是一个 FIFO：`enqueue` 追加到队尾；`dequeue` 弹出并返回队首（空队列抛
`IndexError`，与 `collections.deque.popleft()` 在空 deque 上的行为一致，而不是返回哨兵值）；
`peek` 只读队首、不弹出（空队列同样抛 `IndexError`）。这是 Part2/3 的"云端 service"要在故障语义
上加固的那个原始玩具类。

### Part 2 — at-least-once：ack 与可见性超时
`MessageQueue` 把 Part1 的玩具队列升级成一个简化的云队列服务：
- `enqueue(payload)` 生成一个新的 `message_id`（字符串，构造时序单调递增，便于测试断言顺序），
  把消息放进"待投递"队列，返回这个 id。
- `dequeue(now, visibility_timeout)` 从"待投递"队列头部取出一条消息**投递给消费者**，但**不
  从队列里永久移除**——它进入"in-flight"状态，可见性截止时间是 `now + visibility_timeout`
  （半开区间语义，与 od04/od08 一致：`now + visibility_timeout` 这一刻本身视为已经超时）。返回
  `(message_id, payload)`；如果此刻没有任何消息可投递（待投递队列为空，且没有 in-flight 消息
  因超时而回到待投递队列——见下一条），返回 `None`。
- **可见性超时**：每次调用 `dequeue(now, ...)`，**先**把所有 in-flight 里"可见性截止时间
  `<= now`"的消息（还没被 `ack`）**重新放回待投递队列尾部**（按它们各自超时的先后顺序追加，
  超时越早的排越前面），再从待投递队列头部弹出这次要投递的那一条——也就是说，一条消息如果一直
  没被 `ack`，会在超时之后自动被**重新投递**（at-least-once：同一条消息可能被投递不止一次）。
- `ack(message_id)` 把一条 in-flight 的消息标记为"已完成"，从系统里永久移除（之后再也不会被
  投递）。如果 `message_id` 不存在、已经被 ack 过、或者当前不处于 in-flight 状态（比如已经超时
  被重新放回待投递队列、正等着被再次 `dequeue`），返回 `False`；成功返回 `True`。

### Part 3 — 崩溃模拟：未 ack 的重新投递，已 ack 的永不再来（**重建**）
`requeue_all_in_flight()` 模拟"队列服务本身重启/消费者集体失联"：**立即**（不等可见性超时到期）
把当前所有 in-flight（已投递但尚未 `ack`）的消息全部放回待投递队列头部（按它们**原本被投递的
先后顺序**排列，最早投递的排最前面——这与 Part2 的"超时后放回队尾"不同：崩溃恢复要让最老的
未完成工作优先被重新处理，而不是排到新消息后面），返回被放回的消息数量。已经 `ack` 过的消息
永远不会因为这个方法而复活——它们在 `ack` 那一刻就已经从系统里永久移除，`requeue_all_in_flight`
根本看不到它们。

## Worked examples

**例 1（Part1，deque 基础语义）**
```
q = SimpleQueue()
q.enqueue("a")
q.enqueue("b")
q.peek()       -- "a"，不弹出
q.dequeue()    -- "a"
len(q)         -- 1
q.dequeue()    -- "b"
q.dequeue()    -- 抛 IndexError
```

**例 2（Part2，超时自动重新投递）**
```
mq = MessageQueue()
id_a = mq.enqueue("A")
id_b = mq.enqueue("B")
r1 = mq.dequeue(now=0, visibility_timeout=10)   -- (id_a, "A")，A 的可见性截止=10
r2 = mq.dequeue(now=1, visibility_timeout=10)   -- (id_b, "B")，B 的可见性截止=11
mq.ack(id_b)                                     -- True，B 永久完成
r3 = mq.dequeue(now=5, visibility_timeout=10)    -- None（待投递队列空，A 还没超时：10>5）
r4 = mq.dequeue(now=10, visibility_timeout=10)   -- (id_a, "A")，A 超时(10<=10)被重新投递
mq.ack(id_a)                                      -- True
r5 = mq.dequeue(now=100, visibility_timeout=10)  -- None（A 已 ack 永久移除，B 已 ack，都不会
                                                      再出现）
```
→ `r1..r5 = [(id_a,"A"), (id_b,"B"), None, (id_a,"A"), None]`（`ack` 调用的返回值另外验证，见
`test_od09.py`）

**例 3（Part3，崩溃模拟）**
```
mq = MessageQueue()
id_a = mq.enqueue("A")
id_b = mq.enqueue("B")
id_c = mq.enqueue("C")
mq.dequeue(now=0, visibility_timeout=1000)   -- 拿到 A，in-flight
mq.dequeue(now=0, visibility_timeout=1000)   -- 拿到 B，in-flight
mq.ack(id_b)                                  -- 模拟 B 正常处理完成
                                               -- C 还没被投递过，仍在待投递队列里
n = mq.requeue_all_in_flight()                -- 只有 A 是 in-flight（B 已 ack，不算）-> n=1
mq.dequeue(now=1, visibility_timeout=1000)   -- A（崩溃恢复：最早投递的未完成工作优先）
mq.dequeue(now=1, visibility_timeout=1000)   -- C（从未投递过的原始顺序）
mq.dequeue(now=1, visibility_timeout=1000)   -- None
```
→ `n = 1`；三次 `dequeue` 依次是 `(id_a,"A")`、`(id_c,"C")`、`None`（B 永不重现）。

## `main()` 命令流
**Part1**：`ENQ <item>` / `DEQ` / `PEEK`，一行一操作；`DEQ`/`PEEK` 在空队列时输出字面量
`ERROR:IndexError`，否则输出 item 原文。

**Part2**：`ENQ <payload>` / `DEQ <now> <visibility_timeout>` / `ACK <message_id>`；`ENQ` 输出
生成的 `message_id`；`DEQ` 输出 `"<message_id> <payload>"` 或字面量 `None`；`ACK` 输出
`True`/`False`。

**Part3**：Part2 全部命令，外加 `CRASH`（无参数，调用 `requeue_all_in_flight()`，输出被放回的
消息数量）。

## 边界清单
- 空队列 `dequeue`/`peek`（Part1）抛 `IndexError`，不是返回 `None`/`-1` 之类的哨兵——这与 Part2
  `dequeue` 在"没有可投递消息"时返回 `None`（不抛异常）是刻意的不同设计：Part1 是"调用方的错误"
  （不该在空队列上 dequeue），Part2 的"暂时没消息"是消费者轮询的正常状态，不是错误
- 可见性截止是半开区间：`now == 截止时间` 算已超时（会被重新投递），`now == 截止时间 - 1` 仍
  视为"投递中"，不会被重复投递
- 同一条消息可能因为反复超时被投递多次（at-least-once 的字面意思）；本题用 `message_id` 本身
  兼任"消息标识"和"当前这次投递的凭证"（不像真实 SQS 那样每次投递发一个独立的 receipt handle）
  ——`ack(message_id)` 只要这个 id **当前**处于 in-flight 状态就成功，不区分这是第几次投递；
  但如果消息已经超时**回到待投递队列、且尚未被重新取走**（不处于任何 in-flight 状态），此时的
  `ack` 必须返回 `False`（一次迟到的 ack 不能凭空让一个"当前根本没有在被处理"的消息被错误标记
  为完成）
- `ack` 一个从未存在过的 `message_id`、或已经 `ack` 过的 `message_id`，都返回 `False`，不抛异常
- `requeue_all_in_flight()` 在没有任何 in-flight 消息时返回 `0`，不报错
- 已 `ack` 的消息永远不会通过 `requeue_all_in_flight` 或超时机制复活——`ack` 是终态
- 10^5 次 `enqueue`/`dequeue`/`ack` 混合操作在 2s 预算内完成

## 并发追问
1. "`enqueue` 在故障（比如刚写完内存还没来得及持久化就挂了）下会不会丢消息？" —— 这是来源
   原话的追问之一。期望候选人指出玩具级内存实现天然会丢，生产实现需要"先写 WAL/持久化日志，
   确认落盘后再返回"，与 od01/od02/od05 反复出现的"持久化"主题呼应，讨论层面即可，不要求实现。
2. "at-least-once 能不能收紧成 exactly-once？" —— 期望候选人指出纯队列语义做不到真正的
   exactly-once（除非消费者自己做幂等处理，比如按 `message_id` 去重），队列服务能提供的是
   "至少一次投递 + 消费者侧幂等"的组合，讨论去重窗口的取舍。
3. "多个消费者并发 `dequeue`，会不会两个消费者拿到同一条消息？" —— 期望候选人指出"从待投递队列
   弹出 + 标记 in-flight"必须是一个原子操作（一把锁包住整个 `dequeue` 方法体），否则两个线程
   可能都读到同一条消息还没被标记 in-flight 之前的队列状态。
4. "队列积压（enqueue 远快于 dequeue）时怎么做背压？" —— 期望候选人讨论给 `enqueue` 设置队列
   长度上限、超限时阻塞/拒绝/丢最老的消息（多种策略各有取舍），是一个开放式延伸讨论。

## 变体
- 来源提到"多消费者的公平调度/优先级队列"作为追问方向——本题的 `MessageQueue` 是纯 FIFO，不
  实现优先级，作为口头追问方向而非测试覆盖点。
- 这道题与 `catalog/CATALOG.md` sd05（Distributed Queue Service）是编码/系统设计两个轮次对
  同一主题的不同深度考法：sd05 讨论落盘确认、公平调度、背压的架构层面；本题聚焦可以现场写代码
  验证的 ack/可见性超时核心机制。

## 来源与置信度
- 1point3acres 一手挂经 t.me/s/usinterview/29299 → 1point3acres bbs thread-1185881（"Queue
  class（类 deque）→ 云端 queue service"，讨论 enqueue/dequeue 故障行为，onsite SD，候选人未
  通过）；`catalog/raw/system_design.md` §（Queue class 段落）
- staffengprep 的题库分类将其归入编码题清单（主题级印证，LOW，不单独计分）
- `catalog/raw/ood.md` "Cross-cutting concurrency notes" 未把这道题列入 5/10 显式并发追问清单，
  但 sd05 一侧的追问（"落盘确认、at-least-once vs exactly-once、优先级/公平、背压"）与本题的
  并发追问逐条对应
- `catalog/CATALOG.md` Table B od09 行；置信度 **HIGH** 针对主题与追问方向；具体的 ack/
  visibility-timeout 方法签名与 `requeue_all_in_flight` 崩溃模拟接口标注为**重建**（业界标准
  SQS 模式的简化实现，不是面试官原话给出的确切 API）。

## 考什么
S13 队列语义（at-least-once、落盘确认、背压）· S09 类设计先定 API 契约（Part1 抛异常 vs Part2
返回 `None` 的刻意区分）· S10（并发追问：dequeue 的原子 claim）· S11（持久化追问：enqueue 落盘）
