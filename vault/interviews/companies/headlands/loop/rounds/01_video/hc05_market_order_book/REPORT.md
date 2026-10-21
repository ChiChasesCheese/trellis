# hc05 · 思路与追问

## 概要

订单簿 / 撮合是电面里最集中的一类。题目本身不难，面试官要看的是：数据结构选得对不对（有序 Map + 带序队列 + id 索引），
规则说得清不清楚（价格-时间优先、成交价取谁的、减量保优先级），以及一路追问下去（性能、溢出、测试）你还站不站得稳。

## 逐 Part 思路

1. **维护（不撮合）**：买卖各一个 `TreeMap<价格, 价位>`（买盘 `reverseOrder`，两边的最优价都是 `firstEntry`）；价位内 `LinkedHashMap<id, Node>` 做 FIFO 且 O(1) 按 id 摘除；`HashMap<id, Node>` 让撤单 / 改量不必知道价格。
   价位上缓存 `total`。所有会抛异常的检查（`addExact`）放在修改之前。
2. **撮合 + 事件**：`sweep` 循环：取对面最优档队头 → 成交 `min(left, maker.qty)` → 成交价取 maker 价 → maker 吃光就 `pollFirstEntry`，档空了连价位一起删。市价单 = 限价设成无穷，复用同一循环。
   结果用 sealed `Event`，命令用 sealed `Command`，校验和渲染都是穷尽 switch。溢出检查在撮合之前（原子拒绝）。
3. **批量撮合**：先整体校验行，再当作 `Limit` 依次执行，事件流里挑出 `Trade`（`mapMulti`），名义金额用 `multiplyExact` / `addExact`。
4. **性能（`TickBook`）**：价格是有界 `long` tick → 价位用数组下标；订单池 = 结构数组 + 侵入式双向链表 + free list；id 表 = 开放寻址（回移删除）；
   最优价靠位图 + `numberOfTrailingZeros` / `numberOfLeadingZeros`；成交走回调。代价：价格带和容量是固定的。

## 隐藏测试会打的坑

* `add` 去撮合了（Part 1 要求只挂不撮）。
* 成交价取了 taker 的限价；部分成交的 maker 被丢到队尾。
* 增量 modify 不丢优先级 / 减量却丢了；`modify(未知 id, 0)` 该先报参数错。
* 价位空了没从 `TreeMap` 删，`bestBid` 返回一个空档。
* 总量溢出：`total += qty` 回绕成负数；先改后查导致簿被改了一半。
* 限价单溢出检查放在撮合之后：成交已发出，却报 overflow。
* 批量撮合：`price × qty` 溢出（`4e9 × 3e9`）；`rows[i]` 长度不是 3；`side` 不是 0/1。
* Part 4：开放寻址删除直接置 0（断探测链）；最优价被吃光 / 撤光后没更新（要跨过上万个空价位）；池满时仍然撮合。

## 复杂度

L = 价位数，n = 订单数，k = 一次下单产生的成交笔数。量级参考：

| 操作 | 复杂度 | 耗时 |
|---|---|---|
| `add` / `cancel` / `modify`（Part 1） | O(log L) | 20 万次 add + 10 万次 cancel：约 65–80 ms |
| `execute(Limit)`（Part 2） | O(k + 吃光的档数 · log L) | 30 万条混合命令（70% 限价、20% 撤单、10% 改量）：约 60 ms |
| `BatchMatcher.run`（Part 3） | 同上，另加 O(n) 校验 | 20 万行：约 65–85 ms |
| `TickBook.limit` / `cancel`（Part 4） | O(k) / O(1)（+ 最优价变空时位图扫描 ≤ maxTicks/64 字） | 200 万次操作：约 100–115 ms（约 2000 万次/秒） |

分配（同一串随机命令）：Part 2 的 `OrderBook` 约 **84 MB / 20 万条命令 ≈ 420 字节/条**；
`TickBook` 预热后 60 万条命令 **0 字节**。

## Java 21 特性

| 特性 | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| record（含紧凑构造器） | `Order`（校验）、`Level`、`Limit` / `Market` / …、全部 `Event`、`Summary` | 非法订单构造不出来；`equals` 按字段，测试直接 `assertEquals(List.of(new Trade(…)), events)` |
| sealed | `Command permits Limit, Market, Cancel, Modify`；`Event permits Trade, Rested, Cancelled, Modified, Rejected` | 类型封闭，新增一种时所有 switch 编译报错，不会漏处理 |
| switch 模式匹配 + `when` 守卫 | `execute`、`validate`（`case Limit l when l.price() <= 0 -> …`）、`render` | 代替 `instanceof` 链 + 强转；守卫让校验顺序一目了然；穷尽性由编译器检查，无 `default` |
| record 模式 | `case Trade(var taker, var maker, var side, var px, var q) ->`；`e instanceof Rejected(var id, var why)` | 判型与拆字段一步完成，省掉 getter 调用 |
| switch 表达式 + `yield` | `execute` 的块分支、`parse` 的 `needArgs` 后 `yield` | 无 fallthrough，多行分支也能当表达式 |
| `instanceof` 模式 | `BatchMatcher` 里 `e instanceof OrderBook.Trade t` | 判断 + 强转 + 绑定一步 |
| Sequenced Collections | `TreeMap` / `LinkedHashMap` 都声明为 `SequencedMap`：`firstEntry` / `pollFirstEntry` / `putLast`；测试里 `getFirst` / `getLast` | 取头尾的统一 API；`putLast` 对已有 key 直接「移到队尾」，旧写法要 remove + put |
| 未命名模式 `_`（预览） | `validate` 里 `case Limit _, Market _ ->`、`case Cancel _, Modify _ ->` | 明说不需要绑定，且一个 case 可并列多个模式 |
| `mapMulti` / `toList()` | `BatchMatcher` 从事件流挑 `Trade`；`depth` 的 `stream().limit(n)…toList()` | 一步完成 filter + 强转；`toList()` 不可变 |
| `addExact` / `multiplyExact` / `formatted` | 价位总量、名义金额、`render` | 溢出直接抛，而不是静默回绕成错数 |
| 文本块 / `var` / Comparator | 多行样例、`var`、`Comparator.reverseOrder()` / `Objects.requireNonNull` | 多行样例原样可读；买盘最优价与卖盘对称 |

## 面试官可能的追问

1. **撤单怎么做到 O(1)（或 O(log L)）？** 要点：`byId` 哈希表给订单 → 订单记着价格和方向 → 价位内 `LinkedHashMap.remove(id)` O(1)；价位变空再从 `TreeMap` 删 O(log L)。进一步 O(1)：价格有界时价位用数组下标（Part 4）。
2. **为什么用 `long` 价格不用 `double`？** 浮点存不准十进制小数，相等的价格可能分到两个价位，比较要 epsilon；整数 tick 精确且可以当数组下标。数量用 `long`，累加用 `addExact`。
3. **GC 很忙怎么办？** 先量：每条命令约 420 字节垃圾。对象图 → 数组：`TreeMap` → 下标，`Node` → 结构数组，`LinkedHashMap` → 侵入式链表，`HashMap<Long,…>` → 开放寻址，`List<Event>` → 回调。代价：有界价格带与容量。JVM 侧：Generational ZGC（亚毫秒级停顿）、预热 JIT、`-Xms=-Xmx` + `AlwaysPreTouch`。
4. **多线程？** 一个品种一个撮合线程（单写者），命令经队列（如 Disruptor 的环形缓冲）串行进入：无锁、可重放、延迟稳定；扩展靠按品种分片。不要给每个方法加 `synchronized`（撮合仍须整体串行，锁只增开销；且 Java 21 里 `synchronized` 会钉住虚拟线程）。
5. **价格范围很大怎么办？** 数组只覆盖中间价附近的一段，远处的价位放一棵 `TreeMap`；或价位少时用有序数组 + 二分（缓存友好）。
6. **怎么测撮合？** 手算样例 + 不变量（不交叉、数量守恒）+ 对拍（快版本 vs 明显正确的慢版本，同一串随机命令）。
7. **self-trade / 冰山单 / 止损单 / FOK、IOC 怎么加？** sealed `Command` 加一个子类，编译器会指出所有要改的 switch；IOC 就是 Market 的限价版（吃不完的作废）；FOK 要先 dry-run 数一下对面总量够不够再下手。
