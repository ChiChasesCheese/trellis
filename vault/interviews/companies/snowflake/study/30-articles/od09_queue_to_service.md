# od09 · Queue → Service：练的是"同一个队列，故障语义一层层加上去"

> [!tldr]
> - **Part 2 的 ack / visibility timeout API 与 Part 3 的崩溃模拟是 (reconstructed)**：一手挂经只给了主题（"类 deque 的 Queue 类 → 扩展为云端 queue service，讨论 enqueue/dequeue 在故障下的行为"），候选人此轮**没过**
> - 这题考的是：玩具 FIFO → at-least-once（投递 ≠ 移除，超时自动重投）→ 崩溃后未确认的工作优先重做
> - 三步套路：Part 1 包一层 `deque` → Part 2 拆出"待投递队列 + in-flight 表"两份状态 → Part 3 只加一个方法，把 in-flight 按投递顺序塞回队首
> - 最值得带走的一个模式：**"交给消费者"和"从系统里删除"是两个动作**，中间隔着一个 ack；所有故障语义都发生在这个缝里

## 类设计先定契约

```python
class SimpleQueue:
    def enqueue(self, item) -> None: ...
    def dequeue(self) -> object: ...        # 空队列抛 IndexError（和 deque.popleft 一致）
    def peek(self) -> object: ...           # 空队列抛 IndexError
    def __len__(self) -> int: ...

class MessageQueue:
    def enqueue(self, payload) -> str: ...                              # 返回 message_id
    def dequeue(self, now: int, visibility_timeout: int) -> tuple[str, object] | None: ...
    def ack(self, message_id: str) -> bool: ...
    def requeue_all_in_flight(self) -> int: ...                         # Part 3
```

**不变量（写代码前先说出来）**：
1. 任意时刻，一条未完成的消息**恰好**在"待投递队列"或"in-flight 表"之一里，不会两处都在，也不会都不在。
2. `ack` 只对**当前 in-flight** 的消息成功；成功后消息从系统永久消失，任何机制都不能让它复活。
3. 可见性截止是半开区间：`now >= visible_at` 就算超时。
4. 超时回来的消息排**队尾**（被动重投，不插队）；崩溃恢复的消息排**队首**（最老的未完成工作优先）。

## 1. 题目在说什么（人话版）

Part 1 是一个普通队列。Part 2 把它变成"云队列"：消费者拿走一条消息后，队列不删它，只是暂时藏起来；消费者处理完要回一个 ack，队列才真正删掉；如果过了可见性超时还没 ack，队列认为消费者挂了，把消息放回去让别人再拿。Part 3 模拟队列服务重启：所有"被拿走但没 ack"的消息立刻放回队首。

三行小例子（Part 2）：
```
A 在 now=0 被拿走，超时 10 → 截止 10
now=5 再 dequeue → None（A 还没超时，队列里没别的）
now=10 再 dequeue → A（10 >= 10，超时，重投）
```

## 2. 读题：把文字变成模型

- **实体**：消息（id、payload）、消息的状态（待投递 / in-flight / 已完成）。
- **状态**：`ready: deque[id]`、`in_flight: dict[id -> (visible_at, delivery_seq)]`、`payloads: dict[id -> payload]`。
- **输出**：`dequeue` 的 `(id, payload)` 或 `None`；`ack` 的布尔；`CRASH` 的数量。
- **一句话建模**：这是一个 **"待投递 ↔ in-flight 两个集合之间的状态机"**，`dequeue` 是 ready→in-flight，`ack` 是 in-flight→删除，超时是 in-flight→ready 尾，崩溃是 in-flight→ready 头。

> [!note] 为什么 in-flight 要记 `delivery_seq`
> Part 2 超时回队尾按截止时间排序就够了；Part 3 要"最早投递的排最前"，截止时间不等于投递顺序（不同消费者超时参数可以不同），所以单独记一个单调递增的投递序号。

## 3. 下笔顺序

1. **Part 1**：`SimpleQueue` 直接包 `deque`。故意让空队列抛 `IndexError`——先和面试官确认"空了是报错还是返回 None"。
2. **Part 2 状态**：先写 `__init__` 的四个字段，再写 `enqueue`（生成 `m1, m2, …`）。
3. **Part 2 dequeue**：先"扫超时回队尾"，再"弹队首放进 in-flight"。顺序不能反——反了会漏掉刚好到期的消息。
4. **Part 2 ack**：只查 in-flight 表。已经超时回到 ready 的消息 ack 必须失败（迟到的 ack 不能把一条正在排队的消息标成完成）。
5. **Part 3**：in-flight 按 `delivery_seq` 升序，逆序 `appendleft`，最早的就落在最前。
6. **收尾**：跑例 2（超时重投）和例 3（崩溃后 A 在 C 前面、B 永不回来）。

## 4. 代码怎么组织

```
SimpleQueue                        # Part 1：deque 薄封装
MessageQueue._requeue_expired(now) # in-flight 里到期的 → ready 尾
MessageQueue.dequeue / ack         # 状态迁移
MessageQueue.requeue_all_in_flight # Part 3：in-flight 全部 → ready 头
part1/part2/part3(lines)           # 命令流解析
```
所有状态迁移都在 `MessageQueue` 的方法里完成，命令流只负责解析与格式化。

## 5. 核心代码骨架

```python
class MessageQueue:
    def __init__(self):
        self._ready = deque(); self._payloads = {}; self._in_flight = {}
        self._enq = 0; self._deliv = 0

    def enqueue(self, payload):
        self._enq += 1; mid = f"m{self._enq}"
        self._payloads[mid] = payload; self._ready.append(mid)
        return mid

    def _requeue_expired(self, now):
        for _, _, mid in sorted((v, s, m) for m, (v, s) in self._in_flight.items() if v <= now):
            del self._in_flight[mid]; self._ready.append(mid)          # 超时 → 队尾

    def dequeue(self, now, timeout):
        self._requeue_expired(now)                                       # 先扫再弹
        if not self._ready:
            return None
        mid = self._ready.popleft(); self._deliv += 1
        self._in_flight[mid] = (now + timeout, self._deliv)
        return mid, self._payloads[mid]

    def ack(self, mid):
        if mid not in self._in_flight:
            return False                                                 # 不在 in-flight 一律失败
        del self._in_flight[mid]; self._payloads.pop(mid, None)
        return True

    def requeue_all_in_flight(self):
        items = sorted((s, m) for m, (_, s) in self._in_flight.items())
        for _, mid in reversed(items):
            self._ready.appendleft(mid); del self._in_flight[mid]        # 崩溃 → 队首
        return len(items)
```

## 6. 每个 part 叠加什么

| Part | 新增状态 | 新增方法 | 改了什么 |
|---|---|---|---|
| 1 | `deque` | enqueue / dequeue / peek / len | — |
| 2 | ready、in_flight、payloads、两个序号 | ack、`_requeue_expired` | dequeue 不再删除，只迁移到 in-flight |
| 3 | — | requeue_all_in_flight | 无（纯增量） |

## 7. 常见坑

- `dequeue` 先弹后扫：刚好 `now == visible_at` 的消息这一轮拿不到。
- `ack` 查的是 `payloads` 而不是 `in_flight`：已超时回队的消息被错误确认。
- 崩溃恢复把消息放队尾：违背"最老的未完成工作优先"。
- 用截止时间而不是投递序号排崩溃恢复顺序：不同超时参数下顺序错。
- Part 1 空队列返回 `None`：与 `deque` 语义不一致（先问清楚）。
- 性能：`_requeue_expired` 每次全表扫 in-flight 是 O(in-flight)；in-flight 很大时要换成按截止时间的最小堆（懒删除已 ack 的），这是一个很好的追问答案。

## 8. 并发追问怎么答

1. **两个消费者同时 dequeue 会拿到同一条吗？** "扫超时 + 弹队首 + 写 in-flight"是一个 check-then-act，必须在同一把锁里；ack 与超时扫描也要互斥，否则一条消息可能同时被 ack 和重投。
2. **锁粒度？** 单队列一把锁足够；吞吐不够时按队列分片（每个 shard 一把锁），而不是细到每条消息。
3. **分布式版本？** in-flight 表放到存储里，`dequeue` 用条件更新（`status=ready → in_flight, owner, visible_at`）做原子认领；ack 带认领时的 receipt（防止旧消费者 ack 掉新一次投递）。
4. **怎么测？** N 个线程并发 dequeue 同一批消息，断言每条消息在任一时刻最多一个持有者；并发 ack 与超时扫描，断言已 ack 的消息计数只增不减。

## 9. 追问怎么接（来源原话的四个方向）

- **enqueue 刚写内存还没落盘就挂了？** 玩具实现会丢；生产要先写 WAL 确认落盘再返回（和 od01/od05 的持久化同一套）。
- **at-least-once 能不能变 exactly-once？** 队列本身做不到；"至少一次投递 + 消费者按 message_id 幂等"是等价物。
- **多消费者公平 / 优先级？** 按租户分队列轮询，或每条消息带优先级用多级队列。
- **积压怎么办？** 背压：enqueue 端限流或拒绝；监控队列深度与最老消息年龄。

## 10. 自测清单

- [ ] 不看代码写出四条不变量
- [ ] 说清为什么先扫超时再弹队首
- [ ] 说清为什么迟到的 ack 必须失败
- [ ] 说清超时回队尾、崩溃回队首的理由
- [ ] 口述把 in-flight 扫描换成最小堆的改法

## 相关题与 skills

S09 契约先行 · S10 并发正确性 · S13 队列语义 · 相关：`sd05` 分布式队列服务（同一主题的系统设计版）、`od05` cron scheduler 的 lease、`od01` 的持久化 part。
