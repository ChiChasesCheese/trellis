# ld02 · REPORT

## 概要

「交易相关的 OOD」出自 1p3a 一帖的摘要（Junior Engineer 电话面，33 分钟里含简历和 BQ，最后一道不太难的交易相关 OOD，结果被拒）。原题题面没有公开。本 kit 把它补全成四个 Part：订单状态机、仓位盈亏、交易前风控、事件溯源重放。

面试官想看五点：
1. 用类型表达不变量（record 紧凑构造器、sealed 事件、枚举状态）；
2. 状态机写成显式的，非法转移抛异常并且不改状态；
3. 价格和数量用整数，有溢出意识；
4. 失败时默认拒绝（fail closed）；
5. 结果确定，可以重放。

讲义：`study/30-articles/ld02_trading_ood.md`。

## 来源与置信度

置信度：中。只有 1 个来源：`catalog/raw/forums.md` A4，即 1p3a 1136321（2025-07-09），只有摘要；`official_and_process.md` §D4 #16 是同一帖。

相关题族（不计入 #refs）：A9（Put/Delete API）、A8（交易事件编码题）、A5、G2。

(reconstructed)：四个 Part 的划分、状态转移表、FIFO 配对、七条风控规则及其检查顺序、`TradingDesk` 的 journal / replay 语义。能确定的只有：这是一道 OOD，和交易相关，难度不高，实际写代码的时间约 15–20 分钟。

## 逐 Part 思路

1. **OrderManager**：枚举状态 + `switch` 对 sealed `ExecEvent` 做穷尽匹配。
   - `Fill` 依次检查：去重（`execId`）→ 当前状态是否允许 → 是否超量 → 是否越过限价 → 计算累计成交额（`multiplyExact` / `addExact`）。全部通过后才修改状态，所以任何异常路径都不会留下改了一半的状态。
   - 重复的 `Fill` 在状态检查之前就返回 false：订单进入终态之后再收到旧回报，只算重复消息。
   - 因超量被拒的成交，其 `execId` 不记入已见集合。
   - `openCount` 和按「标的 × 方向」统计的 `openLeaves` 在每次状态变化时增量维护，查询 O(1)。
   - `PENDING` 订单计入未完成订单。
2. **PositionBook**：每个标的维护一个同方向 lot 的 FIFO 队列。
   - 同方向成交或当前空仓：追加一个 lot。
   - 反方向成交：从队首开始平仓，实现盈亏 = `方向 × (成交价 − lot 价) × 数量`；平完后还有剩余就翻转，以成交价开一个反方向的 lot。
   - 先只读地把盈亏算完，再一次性提交。乘法溢出时抛 `ArithmeticException`，仓位保持不变。
   - `Position.unrealizedPnl`：多头为 `netQty × mark − openCost`，空头为 `openCost − |netQty| × mark`。
3. **RiskEngine**：检查顺序就是 `RiskReason` 枚举的声明顺序，只报告第一条违反的规则，保证结果确定。
   - 顺序：HALTED → NO_REFERENCE_PRICE（没有参考价时拒绝）→ QTY → NOTIONAL（乘法溢出也算拒绝）→ PRICE_BAND → OPEN_ORDERS → POSITION。
   - PRICE_BAND 用整数交叉相乘判断：`|px − ref| × 10⁴ ≤ ref × bps`，等号算通过。
   - POSITION 按最坏情况算：`净仓 + 未完成买单剩余量（+ 本单）` 和 `净仓 − 未完成卖单剩余量（+ 本单）`。
   - `check` 只读，不改任何状态。
4. **TradingDesk**：每个会改状态的方法，先把输入追加到 journal，再调用同一个 `handle`；`replay` 也调用 `handle`。这样线上路径和恢复路径走的是同一份代码。
   - `risk.check` 必须在 `orders.submit` 之前，否则订单会把自己也算进未完成数量。
   - 被风控拒绝的订单仍然登记，随后在内部应用 `Reject(reason.name())`。这条 `Reject` 是输出，不进 journal。
   - `replay` 会吞掉预期内的业务异常（IAE / ISE / NoSuchElement / Arithmetic），因为第一次执行时这些异常也没有改变状态。

## 隐藏测试会打的坑

* 重复的 `Fill` 先走了状态检查，导致订单 `FILLED` 之后的旧回报抛异常，或者把仓位翻倍。
* 一边校验一边修改：超量成交先加了 `cumQty` 才报错；`execId` 先放进已见集合，之后合法的重发被当成重复吞掉。
* 先登记订单再做风控，导致恰好顶格的订单被误拒。
* 风控只看净仓、不看挂单。例如净仓 2500 + 挂单 2000 + 新买单 501，最坏情况是 5001，应该被拒。卖方向也要对称处理。
* 价格带用除法或浮点计算，参考价是 10007 或 3 时边界会算错；缺参考价时放行；名义金额溢出后绕回一个小数而被放行。
* 翻转时只改了方向、没有计算实现盈亏，或者剩余 lot 的价格取错。
* `journal()` 直接返回内部 list；`replay` 不吞异常；`PENDING` 订单没计入未完成。
* 聚合量在某个终态路径上漏了更新。这种 bug 只有用「随机事件流 + 逐单重算」做对照才能抓到。

## 复杂度 + 实测时间

- 每个事件 O(1)。
- `PositionBook.onFill` 摊还 O(1)：每个 lot 只入队一次、出队一次。
- `get` / `netQty` 要遍历该标的的 lot 队列，O(lot 数)。
- 风控 `check` 是 O(1)，加上 `netQty` 的那次 lot 遍历。
- `open()` / `all()` 要排序，O(n log n)，只用于查询。

实测：全套 56 个测试约 0.2 s。

`DeskBench`（JIT 预热后取 5 次中位数）：

| 项目 | 规模 | 耗时 | 速率 |
|---|---|---|---|
| 实时处理 | 40 万事件 | 17.7 ms | 22.6 M 事件/s（44 ns/事件） |
| 重放 | 40 万事件 | 17.1 ms | 23.4 M 事件/s（43 ns/事件） |
| `PositionBook.onFill` | 300 万次成交 | 103 ms | 29 M 次/s（含 `"S"+i` 的字符串分配） |

这些是平均吞吐的量级，不包括 GC 造成的尾延迟。reference 用了 `HashMap<Long,…>`、装箱和 record 分配，没有做零分配优化。

## 测试清单（脚本数）

共 56 个，0 失败：part1 15、part2 11、part3 17、part4 13；edge 23、perf 2；没有 conc / io。

- **OrderManagerTest**（15）：全部合法与非法转移、去重、超量、限价约束、聚合量、溢出、随机事件流对照。
- **PositionBookTest**（11）：FIFO、空头镜像、翻转、恰好平仓、多标的、未实现盈亏、溢出时不留半个状态、与逐手模型对照（2000 笔）、30 万笔 perf。
- **RiskEngineTest**（17）：每条规则在 `==` 和 `+1` 处的边界、整数价格带、多空两侧的最坏情况仓位、熔断、检查顺序、`check` 不改状态、限额参数校验。
- **TradingDeskTest**（13）：完整生命周期、拒绝的订单也登记、不把自己算两遍、halt / resume、重复 id、重复 Fill、非法事件仍进 journal、journal 不可变、replay 结果相等、replay 吞异常、25 个随机种子 × 600 步、5 万订单 × 4 事件 + 重放 perf。

变异检查（每次只改 reference 的一处，测试都变红）：

| 变异 | 结果 |
|---|---|
| 去掉 `execId` 去重 | 2 个测试失败 |
| 名义金额 `>` 改成 `>=` | 1 个测试失败 |
| 空头仓位限额放宽 1 | 1 个测试失败 |
| `b.dir * qty` 改成 `qty` | 3 个测试失败 |
| 风控检查移到登记之后 | 1 个测试失败 |

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J01 record | `Order`、`ExecEvent.*`、`DeskEvent.*`、`Position`、`OrderView`、`RiskLimits` 的紧凑构造器校验 | 非法对象根本造不出来；自带结构相等，测试可以直接比较两个 desk 的状态 |
| J02 sealed | `ExecEvent`、`DeskEvent`、`RiskResult` | 编译器知道全部子类型，新增事件类型没处理就编译不过 |
| J03 switch 模式匹配 | `OrderManager.apply`、`TradingDesk.handle` | 不需要 `default` 和强制转换，穷尽性由编译器检查 |
| J04 record 模式 | `case DeskEvent.SetReferencePrice(var symbol, var px)`、`x instanceof ExecEvent.Fill(var orderId, …)`、`r instanceof RiskResult.Rejected(var reason)` | 一步解构，不用一串 getter |
| J05 switch 表达式 + yield | `apply` 的每个分支 `yield true` | 没有 fall-through，每个分支都必须给出值 |
| J15 Math.*Exact | 名义金额、盈亏、累计成交额 | 溢出直接抛异常，不会悄悄绕回 |
| J14 Stream.toList() | `OrderManager.open()` | 返回不可变列表 |
| J18 / 集合工厂 | `List.copyOf(journal)` | 防御性的不可变拷贝 |

## 面试官可能的追问

1. **新增一条风控规则要改哪里？** 加一个 `RiskReason` 枚举值（它的位置就是优先级）和一个 `if`。想要可组合，可以重构成 `List<RiskCheck>` 责任链，但热路径上保持内联。和时间有关的规则（比如速率限制）要把时间作为事件传进来，不能在代码里读时钟，否则重放结果就不确定了。
2. **多线程怎么办？** 用单写者：一个线程独占 desk，其他线程把命令投递到它的队列。加锁会带来竞争，而且线程交错的顺序每次不同，会破坏重放。需要并行时按标的分片。
3. **为什么 `PENDING` 订单算未完成？** 交易所的回报会滞后，但风险不会：订单已经发出去了，可能已经成交。
4. **为什么重复 Fill 的去重放在状态检查之前？** 订单进入终态后再收到的旧回报只是重复消息，不是非法转移；另外，因超量被拒的成交不能把 `execId` 记成已见。
5. **FIFO 换成平均成本法？** 需要除法和舍入规则，要先问业务方。实现上只存 `netQty` 和 `costBasis`，平仓时按比例取整，余数留在 `costBasis` 里。FIFO 的好处是全程整数，不需要舍入。
6. **重放结果和线上不一致，怎么排查？** 对日志做二分，比较状态摘要，找到第一个产生分叉的事件。常见原因：读了时钟或随机数、依赖 `HashMap` 的遍历顺序、用了浮点、多线程。预防：线上定期记录状态摘要；发布前用生产日志做一次重放回归。
7. **撤单请求和撤单确认之间怎么处理？** 加一个 `PENDING_CANCEL` 状态：这期间订单仍可能成交，所以风控的最坏情况仓位仍要算上它的剩余数量。
8. **性能够吗？** 平均约 2200 万事件/s，吞吐足够。要做到微秒级尾延迟，需要零分配：原始类型哈希表、预分配槽位、journal 用环形缓冲或 mmap。先测量再优化。
9. **市价单怎么支持？** 转成带保护价的限价单，这样风控规则不需要特殊处理。
