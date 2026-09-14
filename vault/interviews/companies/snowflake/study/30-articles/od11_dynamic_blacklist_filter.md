# od11 · Dynamic Blacklist Filter System：同刻打平顺序 + 引用计数 + 线性一致性

> [!tldr]
> - 这题考的是：两条并发流（黑名单规则增删 / 待检查输入）的类设计——核心契约是"同一时刻既有规
>   则变更又有输入到达时谁先生效"，以及多 owner 引用计数、并发正确性的可测试定义
> - 三步套路：单线程按时间戳重放（先定死同刻打平顺序）→ 换成多 owner 引用计数 + 前缀通配符 →
>   一把锁包住每次操作，同时录一份"线性化日志"证明并发结果等价于某个串行历史
> - 最值得带走的一个模式：**合并两条乱序流时，"同一时刻两件事谁先生效"不是可以模糊带过的实现
>   细节，是必须显式写进契约的规则——这条规则本身决定了整个系统的语义**

## 1. 题目在说什么（人话版）

系统同时接收两条事件流：一条是**过滤规则的增删**（拉黑/取消拉黑某个值），一条是**待检查的输
入值**。每个输入值到达时，看它在**那一刻**是否处于被拉黑状态，是则丢弃，否则放行。两条流各自
按到达顺序给出，但合并在一起未必是按时间戳单调的。

三行小例子：
```
1 ADD a
2 IN a       -> false   (a 已被拉黑)
3 REMOVE a
4 IN a       -> true    (a 已被移除)
```

## 2. 读题：把文字变成模型

- **实体**：全局黑名单状态、`(timestamp, kind, value)` 事件（`kind` 是 `ADD`/`REMOVE`/`IN`）。
- **输入长什么样**：`events: list[tuple[int,str,str]]`，时间戳可能乱序；Part 2 起还带
  `owner`，`value` 可以是字面值或以 `*` 结尾的前缀通配符。
- **输出要什么**：只对 `IN` 事件产生一个 `bool`，顺序是**排序后**事件流中 `IN` 出现的顺序。
- **状态**：Part 1 是一个 `set`；Part 2 是 `(owner,pattern)` 去重集合 + `pattern -> 引用计数`
  字典；Part 3 额外加一把锁和一份按生效顺序追加的日志。
- **一句话建模**：这是一个**按时间戳重放的状态机**，"同刻多事件谁先生效"是必须显式定义、题面
  没给、需要自己补全的契约。

> [!note] 为什么用引用计数而不是布尔标记
> 现实中黑名单往往是"多个子系统各自维护一份规则"：同一个 value 可能被多个 owner 各自拉黑，只
> 要**至少还有一个 owner** 在拉黑它，它就必须保持被拦截。布尔标记做不到"部分 owner 取消后仍然
> 拦截"，必须用 `(owner, pattern)` 贡献引用的计数方式实现。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`BlacklistFilter`（`set`）+ `add`/`remove`/`offer`；`process_events` 只是重放
   这个类。
2. **Part 1 最小可用**：`process_events` 先按 `(timestamp, mutation_before_input)` 稳定排序，
   再顺序重放，只对 `IN` 产生输出——同刻打平顺序（mutation 先于 input）是这一步必须先想清楚的
   契约，不是后补的边界情形。
3. **Part 2 叠加**：把 `BlacklistFilter` 换成 `RefCountedPatternFilter`：`(owner,pattern)` 集
   合去重（防止同一 owner 重复 add 让计数无限增长）+ `pattern -> 引用计数` 字典；`offer` 遍历
   当前引用计数 > 0 的规则做精确匹配或前缀匹配。
4. **Part 3 叠加**：包一层 `RLock`，每次 `add`/`remove`/`offer` 都在锁内完成并追加一条日志
   （`seq` 严格递增 = 真实生效顺序）；写 `replay_sequential` 对着日志单线程重放，断言与并发观
   测到的结果逐一一致。
5. **收尾**：跑一遍边界清单——乱序时间戳、同刻事件、多 owner 引用计数、通配符误匹配、10 万条
   事件的性能预算。

## 4. 代码怎么组织

```
BlacklistFilter.add/remove/offer                    # Part1：单线程集合成员操作
process_events(events) -> list[bool]                 # 排序（同刻 mutation 先于 input）+ 重放
RefCountedPatternFilter.add/remove/offer             # Part2：(owner,pattern) 去重 + 引用计数 + 通配符
ThreadSafeBlacklistFilter                            # Part3：RLock 包住每次操作 + 追加线性化日志
replay_sequential(log) -> list[bool]                  # 单线程重放日志，验证线性一致性
```

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
# process_events 的排序 key 是 (timestamp, 0 if ADD/REMOVE else 1)：同刻打平，mutation 先生效。
class RefCountedPatternFilter:
    def __init__(self):
        self._owned = set()          # (owner, pattern) 去重，避免同一 owner 重复计数
        self._refcount = {}          # pattern -> 当前有效引用数

    def add(self, owner, pattern):
        key = (owner, pattern)
        if key in self._owned:
            return                   # 同一 owner 重复 add 同一 pattern 是幂等的
        self._owned.add(key)
        self._refcount[pattern] = self._refcount.get(pattern, 0) + 1

    def remove(self, owner, pattern):
        key = (owner, pattern)
        if key not in self._owned:
            return                   # 从未拉黑过，空操作，不报错
        self._owned.discard(key)
        self._refcount[pattern] -= 1
        if self._refcount[pattern] <= 0:
            del self._refcount[pattern]

    def offer(self, v):
        for pattern in self._refcount:
            if pattern.endswith("*"):
                if v.startswith(pattern[:-1]):
                    return False      # 前缀匹配
            elif pattern == v:
                return False          # 精确匹配
        return True
```

## 6. 并发追问怎么答

- **为什么每次操作都要在同一把锁内完成**：`add`/`remove` 对引用计数是"读-改-写"，如果不在同
  一把锁内完成，两个线程并发 `remove` 同一个只剩 1 个引用的 pattern 会导致计数变成负数——该
  pattern 会被错误地判定为"未拉黑"，这是并发正确性题里最常见的竞态之一。
- **怎么证明并发执行是正确的**：正确性定义为线性一致性——`linearization_log()` 在锁内按真实
  生效顺序追加每次操作，`replay_sequential()` 对着这份日志做单线程重放；测试断言并发跑出来的
  每个 `offer` 结果，都等于把日志按记录顺序重放的结果。
- **读写锁 vs copy-on-write 怎么选**：参考实现用一把锁覆盖读和写，写少读多场景下会让 `offer`
  互相阻塞；copy-on-write（每次 mutation 生成一份新的不可变规则集，`offer` 只读一份不变快照）
  能让读完全无锁，代价是每次 mutation 的复制成本随规则数线性增长——这是吞吐量与内存的权衡，面
  试里应该主动提出来讨论，而不是默认选一个。

## 7. 常见跑偏（方法层面，含并发一条）

- 没有显式定义"同刻既有 mutation 又有 input"时谁先生效，测试用刻意构造的同刻事件一测就翻车。
- **并发相关**：引用计数的 `add`/`remove` 没有做成锁内的原子"读-改-写"，多线程并发操作同一个
  pattern 时计数变成负数或提前归零。
- 前缀通配符用 `pattern in v` 或反过来误判包含关系，而不是 `v.startswith(pattern[:-1])`，导致
  `"10.0.*"` 误匹配 `"10.100.0.0"` 这类不该匹配的值。

## 8. 同族题 / 延伸

- 与 `od06_query_audit_log`、`pc03_recent_event_stream` 同族："乱序事件流 + 按时间点查询"这条
  模式反复出现——本题额外加了"多 owner 引用计数"和"线性一致性的可测试定义"两层。
- 与 `od14_durable_kv_serialization` 同族在"并发正确性"这条技能线：一个靠锁+日志重放验证，一
  个靠"生成号必须从持久层读"避免撞车，都是围绕 S10 的不同侧面。
- 练习命令：`python3 loop/mock.py start od11`
