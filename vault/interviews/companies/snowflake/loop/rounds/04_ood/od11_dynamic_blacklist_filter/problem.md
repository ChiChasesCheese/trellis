# od11 · Dynamic Blacklist Filter System — 双流黑名单过滤器

> TrueInterview 同步清单第 10 题 "Dynamic Blacklist Filter System"（LLD，2026-06 报告），题面
> 付费只见标题与格式标签；1point3acres 面经索引另有一条同名标题 "Dynamic Blacklist Filter
> System"（无法读到正文，日期不详）。**两条来源都只到标题级**——除"两条流：过滤器增删 + 输入
> 值，输入到达时未被拉黑就放行"这一最小骨架外，本题几乎全部规则细节都是 **(reconstructed)**，
> 逐条标注。

## 背景

系统同时接收两条事件流：一条是**过滤规则的修改**（新增/移除黑名单项），一条是**待检查的输入
值**。每个输入值到达时，看它在**那一刻**是否处于被拉黑状态，是则丢弃，否则放行——这是一个典型
的"状态随时间演化 + 按时间点查询"的类设计题，直接对应 Snowflake JD 里"并发正确性"这条技能线
（`skills_matrix.md` S10）。

## 输入

Part 1/2 用一份按到达顺序给出、但**时间戳可能乱序**的事件列表重放；每行：
```
<timestamp:int> ADD <value>
<timestamp:int> REMOVE <value>
<timestamp:int> IN <value>
```
Part 2 额外要求 `owner`（谁发起的这次增删）：
```
<timestamp:int> ADD <owner> <value_or_pattern>
<timestamp:int> REMOVE <owner> <value_or_pattern>
<timestamp:int> IN <value>
```
`value_or_pattern` 要么是字面值，要么是以 `*` 结尾的前缀通配符（如 `10.0.*`）。

## API 契约（英文签名）

```python
class BlacklistFilter:                              # Part 1
    def add(self, v: str) -> None: ...
    def remove(self, v: str) -> None: ...
    def offer(self, v: str) -> bool: ...             # True = passed, False = blacklisted

def process_events(events: list[tuple[int, str, str]]) -> list[bool]: ...   # Part 1 merged log

class RefCountedPatternFilter:                       # Part 2
    def add(self, owner: str, pattern: str) -> None: ...
    def remove(self, owner: str, pattern: str) -> None: ...
    def offer(self, v: str) -> bool: ...

class ThreadSafeBlacklistFilter:                     # Part 3
    def add(self, owner: str, pattern: str) -> None: ...
    def remove(self, owner: str, pattern: str) -> None: ...
    def offer(self, v: str) -> bool: ...
    def linearization_log(self) -> list[tuple[int, str, str, str]]: ...

def replay_sequential(log: list[tuple[int, str, str, str]]) -> list[bool]: ...
```

## 规则

### Part 1 — 单线程、按时间戳重放

- `add(v)` / `remove(v)`：简单集合成员操作；`remove` 对不存在的值是空操作，不报错。
- `offer(v)`：`v` 当前不在黑名单里 → `True`（放行），否则 `False`（拦截）。
- `process_events(events)`：`events` 可能**不是按时间戳排好序**给出的（两条流各自到达顺序，
  合并后未必单调）；必须先按 `timestamp` 稳定排序再重放。**(reconstructed)** 排序打平规则：
  **同一时间戳上，过滤器修改（ADD/REMOVE）排在输入（IN）前面**——即"某个时刻既有黑名单变更又
  有输入到达"时，输入总能看到这次变更之后的状态。这是本题唯一无法从预览文本推出、必须自己定
  好写进契约的边界。
- 返回值：只对 `IN` 事件产生一项结果，顺序 = 排序后事件流中 `IN` 出现的顺序（不是原始输入顺
  序）。

### Part 2 — 多 owner 引用计数 + 前缀通配符 **(reconstructed)**

- 现实中黑名单往往是"多个子系统各自维护一份规则"：同一个 `value`/`pattern` 可能被多个
  `owner` 各自拉黑；只要**至少还有一个 owner** 在拉黑它，它就必须保持被拦截——用引用计数
  （每个 `(owner, pattern)` 贡献 1 个引用）而不是布尔标记实现。
- 同一个 owner 对同一个 pattern 重复 `add` 是幂等的（不会让引用计数无限增长）；`remove` 一个
  从未被该 owner 拉黑过的 pattern 是空操作，不报错。
- Pattern 支持字面值精确匹配，或以 `*` 结尾的前缀匹配（如 `10.0.*` 匹配所有以 `10.0.` 开头的
  值）；`offer(v)` 命中任意一条当前引用计数 > 0 的规则（精确或前缀）即拦截。
- 排序/打平规则与 Part 1 相同（时间戳排序，同刻 mutation 先于 input）。

### Part 3 — 并发：读写锁 / 线性一致性 **(reconstructed)**

- 多个生产者线程可以同时对两条流发号施令（并发调用 `add`/`remove`/`offer`）。参考实现用一把
  可重入锁保护每次读写——在这个数据规模下，"每次操作都在锁内完成"就是最简单、可证明正确的读写
  锁（也可以用 copy-on-write 快照实现，见"追问"）。
- 正确性定义为**线性一致性**：并发跑出来的每个 `offer` 结果，必须等于把所有操作按实际生效顺
  序排成一条串行历史后重放的结果——`linearization_log()` 记录这条串行历史（每次操作在锁内追加
  一条日志，天然有序），`replay_sequential()` 对着这条日志重放，测试断言两者的 `offer` 结果逐
  一相同。

### 命令流

```
<ts> ADD <value>                  Part 1
<ts> REMOVE <value>               Part 1
<ts> IN <value>                   Part 1（有输出）

<ts> ADD <owner> <pattern>        Part 2/3
<ts> REMOVE <owner> <pattern>     Part 2/3
<ts> IN <value>                   Part 2/3（有输出）
```
`ADD`/`REMOVE` 无输出；`IN` 输出 `true`/`false`（小写字面量）。

## Worked examples（全部由 `solution.py` 实际运行得出）

```
PART 1
1 ADD a
2 IN a
3 REMOVE a
4 IN a
→ false
   true
```

```
同刻打平（mutation 先于 input）：
5 ADD b
5 IN b
→ false
```

```
乱序到达（先给 IN，再给它之前时间戳的 ADD/REMOVE）：
3 IN a
1 ADD a
2 REMOVE a
→ true            (排序后变成 ADD@1 → REMOVE@2 → IN@3，a 在 t=3 已经被移除)
```

```
PART 2（多 owner 引用计数）
1 ADD u1 a
2 ADD u2 a
3 IN a
4 REMOVE u1 a
5 IN a
6 REMOVE u2 a
7 IN a
→ false
   false           (u2 还在拉黑 a，即使 u1 已经 remove)
   true            (最后一个 owner 也 remove 了)
```

```
PART 2（前缀通配符）
1 ADD u1 10.0.*
2 IN 10.0.9.9
3 IN 10.1.0.0
4 REMOVE u1 10.0.*
5 IN 10.0.9.9
→ false
   true
   true
```

```
main() 端到端：
PART 3
0 ADD u1 a
1 IN a
2 REMOVE u1 a
3 IN a
→ false
   true
```

## 边界清单

- 单线程 `remove` 一个从未 `add` 过的值：不报错，空操作
- `process_events` 输入乱序（时间戳不单调）：必须先排序再重放
- 同一时间戳既有 mutation 又有 input：mutation 先生效（**(reconstructed)** 打平规则，测试会用
  刻意构造的同刻事件验证）
- 空事件列表 / 只有 mutation 没有 input：返回 `[]`
- Part 2：同一 owner 重复 `add` 同一 pattern 不重复计数；`remove` 一个该 owner 从未拉黑过的
  pattern 是空操作
- Part 2：多个 owner 拉黑同一 value，必须全部 `remove` 才真正放行
- Part 2：精确值与前缀通配符可以同时存在于黑名单里，`offer` 命中任意一条即拦截
- Part 2：通配符只匹配"以给定前缀开头"，`"10.0.*"` 不应误匹配 `"10.1.0.0"`
- Part 3：50+ 个并发线程对不相交/相交的 owner+pattern 做 add/remove/offer，最终
  `linearization_log()` 重放结果与实际观测到的 `offer` 返回值逐一一致
- 性能：10 万条事件（含乱序时间戳）2 秒预算内完成排序+重放

## 追问

1. **为什么要"同刻 mutation 先于 input"而不是反过来？** 因为黑名单系统的现实语义是"防御性"
   的——一条新规则生效的时刻，你希望它**立刻**开始拦截，而不是让"恰好同一时刻"到达的输入侥幸
   免检；反过来设计会让整个过滤器在竞态窗口里失去意义。
2. **读写锁 vs copy-on-write 快照，怎么选？** 本题参考实现用一把锁覆盖读和写——写少读多的场景
   下这会让 `offer`（读）互相阻塞；copy-on-write（每次 mutation 生成一份新的不可变规则集，
   `offer` 读一份不变的快照指针）能让读完全无锁，但每次 mutation 的复制成本随规则数线性增长，
   适合"规则数量少、mutation 远少于 offer"的场景——现场应该讲清楚这个吞吐量/内存的权衡，而不
   是默认选一个。
3. **多线程下"引用计数"本身需要额外保护吗？** 需要——`add`/`remove` 对同一个 pattern 的引用计
   数是"读-改-写"，如果不在同一把锁内完成，两个线程并发 `remove` 同一个只剩 1 个引用的 pattern
   会导致计数变成负数（该 pattern 被错误地判定为"未拉黑"或反之），这是并发正确性题里最常见的
   竞态之一。
4. **如果两条流本身通过网络乱序到达（不是本题这种"整批给你重放"），怎么设计？** 需要给每条事件
   一个单调递增的逻辑时间戳（或用来源系统的事件时间 + 到达时的水位线/watermark 机制），迟到的
   mutation 到达后要能"回溯"重算这段时间窗内已经放行/拦截的判断是否仍然成立——这是流处理里
   "乱序事件 + 迟到数据"的标准追问，面试官大概率会问到。

## 来源与置信度

- **MED**：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步清单）第 10 题
  "Dynamic Blacklist Filter System"，LLD，2026-06 报告；正文付费，只见标题与格式标签。见
  `../../../catalog/raw/github_repos.md` §2 第 10 行、§3 "od11" 一条。
- **medium，标题级单一来源**：1point3acres 面经索引标题 "Dynamic Blacklist Filter System"（
  `https://www.1point3acres.com/interview/company/snowflake`，正文未读，日期不详），见
  `../../../catalog/raw/system_design.md` §1.8。两条来源相互印证"这题存在"，但都没有给出任何
  规则细节；本题除最小骨架外全部标注 **(reconstructed)**。

## 考什么

S09 类设计先定契约（"同刻打平顺序"必须先想清楚再写代码）· S10 并发正确性（读写锁 vs
copy-on-write、引用计数的原子性、线性一致性的可测试定义）· 流处理里"乱序事件+按时间点查询"的
通用模式（与 od06 审计日志、pc03 事件流同族）。
