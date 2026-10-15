# ld02 · 交易相关的 OOD（订单状态机 · 仓位 PnL · 交易前风控 · 事件溯源与重放）

> 阶段：1p3a 技术电面（Junior Engineer，33 分钟 = 简历 + 行为题 + **一道不是很难的 OOD，trading 相关**，该帖作者被拒）· 置信度：**中**（1 个来源，只有摘要，没有题面）
> **题面完全没有**。能确定的只有：(1) 面向对象设计（OOD）；(2) 与交易相关；(3) "不是很难"；(4) 在一次 33 分钟的电话面里和简历、行为题一起出现，所以**实际编码时间大约 15–20 分钟**。
> 下面的四个 Part、API 形状、状态转移表、风控规则、journal/replay 都是 **(reconstructed)**——是本 kit 为了覆盖"交易相关 OOD"最可能出现的几种形态而设计的。真面试以面试官为准：**先问清题目再动手**。
> 与同类题的关系：forums Q3「订单 / 交易事件处理」家族——A9「Put/Delete(unique_id, quantity) 等 4 个 API」、A8「trading events coding challenge」、A5「订单区间重叠 + 按买卖方处理撤单」（`catalog/raw/forums.md`）。本题是这个家族里偏**建模**（而不是偏算法）的一支。

## 背景

交易系统里最基础的三个对象，几乎任何"交易相关 OOD"都绕不开：

1. **订单（Order）**：一个有生命周期的东西——发出去、被确认、部分成交、全部成交、被撤销、被拒绝。非法的状态转移必须被拒绝。
2. **仓位（Position）与盈亏（PnL）**：成交（Fill）改变仓位；平仓时实现盈亏；翻转（从多头直接卖到空头）是经典的 off-by-one 陷阱。
3. **风险检查（Risk Check）**：订单发出去之前必须过一组规则。规则会变、会增加，所以要**可组合**；任何无法判断的情形都要**拒绝**（fail closed）。

第四个 Part 把它们装配成一个**事件溯源**的 `TradingDesk`：所有状态变化都来自一串输入事件；把这串事件重放一遍，必须得到逐位相同的状态。这是交易系统里崩溃恢复、复盘、回测共用的基础（见 `loop/rounds/04_sd/00_how_to_run.md` §5.2 与 sd03）。

## 读题前你需要知道

讲义 `study/30-articles/ld02_trading_ood.md`（从零讲：什么是订单 / 成交 / 仓位 / 盈亏、状态机怎么建模、FIFO 与平均成本、风控为什么这样写、事件溯源）。最少要先懂：

* **record / sealed / 模式匹配 switch**：`study/10-java21/J01_record.md`、`J02_sealed.md`、`J03_pattern_switch.md`、`J04_record_patterns.md`——本题的事件类型是 sealed 层级，状态转移是穷尽的 `switch`；
* **整数算术与溢出**：`study/10-java21/J15_math_string_utils.md`（`Math.multiplyExact` 等）；
* 订单簿与撮合的背景（可选）：`study/30-articles/hc05_market_order_book.md`。

## 概述

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `OrderManager` | 订单状态机：`PENDING → WORKING → PARTIALLY_FILLED → FILLED`，`CANCELED`，`REJECTED`；回报去重；聚合量增量维护 | 非法转移不改状态；重复回报幂等；超量成交；成交价越过限价 |
| 2 | `PositionBook` (`Position`) | 按标的维护仓位：FIFO 配对，已实现 / 未实现盈亏，**翻转** | 平仓 + 开反向仓一笔成交里完成；全整数；溢出不留半个状态 |
| 3 | `RiskEngine` (`RiskLimits`, `RiskResult`, `RiskReason`) | 交易前风控：数量 / 名义金额 / 价格带 / 未完成订单数 / **最坏情况仓位**，熔断开关 | 检查顺序即确定性；整数价格带；fail closed；最坏情况含未完成订单 |
| 4 | `TradingDesk` | 把 1–3 装配起来；输入先进 journal 再处理；`replay` | 决定性；异常输入也进 journal；重放时吞掉同样的异常 |

所有类在默认包。以下类型 starter 里**已给出**（和 reference 完全一样）：`Side`、`OrderStatus`、`Order`、`OrderView`、`IllegalTransitionException`、`ExecEvent`（sealed）、`DeskEvent`（sealed）、`RiskLimits`、`RiskReason`、`RiskResult`。你要写的是 `OrderManager`、`PositionBook`（+ `Position.unrealizedPnl`）、`RiskEngine`、`TradingDesk`。

## 共同约定

* **价格是整数 tick，数量是整数股数**（`long`）。没有浮点，所以 PnL 逐位可验证。名义金额 = `px * qty`，用 `Math.multiplyExact`；溢出是异常而不是回绕。
* `Order(id, symbol, side, qty, px)` 是限价单（没有市价单）；紧凑构造器保证 `id > 0`、`qty > 0`、`px > 0`、`symbol` 非空白。
* 输出确定：所有列表按 id 升序 / 符号字典序。
* **先验证、后修改**：任何抛异常的路径都不能改变状态（Part 4 的重放依赖这一点）。
* 单线程使用，不要加锁。

## Part 1 · `OrderManager`（订单状态机）

```java
public final class OrderManager {
    public void submit(Order order)                   // 登记，状态 PENDING；重复 id → IllegalArgumentException；null → NPE
    public boolean apply(ExecEvent event)             // true = 已应用；false = 重复的 Fill（execId 见过）
    public boolean contains(long orderId)
    public OrderView get(long orderId)                // 未知 → NoSuchElementException
    public List<OrderView> open()                     // 未终结订单，按 id 升序
    public List<OrderView> all()                      // 全部，按 id 升序
    public int openCount()                            // O(1)
    public long openLeaves(String symbol, Side side)  // 该标的该方向所有未终结订单的剩余数量之和，O(1)
}
public record OrderView(Order order, OrderStatus status, long cumQty, long cumNotional, String rejectReason) {
    public long leavesQty()      // 已撤销 / 已拒绝为 0；FILLED 为 0（因为 cumQty == qty）
}
```

### 状态转移表 (reconstructed)

| 当前状态 | `Ack` | `Fill` | `Cancel` | `Reject` |
|---|---|---|---|---|
| `PENDING` | → `WORKING` | **非法** | **非法** | → `REJECTED` |
| `WORKING` | **非法** | → `PARTIALLY_FILLED` 或 `FILLED` | → `CANCELED` | **非法** |
| `PARTIALLY_FILLED` | **非法** | → `PARTIALLY_FILLED` 或 `FILLED` | → `CANCELED`（已成交部分保留） | **非法** |
| `FILLED` / `CANCELED` / `REJECTED` | **非法** | **非法**（重复 Fill 例外，见下） | **非法** | **非法** |

“非法”= 抛 `IllegalTransitionException`，**订单状态不变**。

### 规则

* `Fill(orderId, execId, qty, px)`：
  * **去重在状态检查之前**：`execId` 已见过 ⟹ 返回 `false`，无任何效果——即使订单已经 `FILLED`（旧回报重放不是错误）。
  * `qty > leaves` ⟹ `IllegalTransitionException`（超量成交），并且这个 `execId` **不能**被记为已见过（之后用合法数量重发应当成功）。
  * 成交价不得越过限价：买单 `px > 限价` 非法，卖单 `px < 限价` 非法；等于限价、价格改善合法。
  * `cumNotional += qty * px`，溢出抛 `ArithmeticException`，**且订单状态不变**。
  * `cumQty == order.qty` ⟹ `FILLED`，否则 `PARTIALLY_FILLED`。
* `Cancel` 是**撤单确认**（不是撤单请求）。`PENDING` 状态下收到 `Cancel` 非法（真实系统里这是个竞态，本题简化）。
* `Reject` 带原因字符串，存进 `rejectReason`。
* **聚合量增量维护**：`openCount`、`openLeaves` 在每次状态变化时更新，**不要**在查询时扫描所有订单——风控每个订单都要调用它们。
* `PENDING` 订单计入未完成（它已经发出去了，可能随时成交）。

## Part 2 · `PositionBook`（仓位与盈亏）

```java
public record Position(String symbol, long netQty, long openCost, long realizedPnl) {
    public static Position flat(String symbol)
    public long unrealizedPnl(long markPx)     // 多头 netQty*mark - openCost；空头 openCost - |netQty|*mark；flat → 0
}
public final class PositionBook {
    public void onFill(String symbol, Side side, long qty, long px)   // qty/px <= 0 → IAE
    public Position get(String symbol)         // 未出现过 → Position.flat(symbol)
    public long netQty(String symbol)
    public long totalRealized()
    public List<String> symbols()              // 字典序
}
```

### 规则：FIFO 配对 (reconstructed)

* 维护每个标的的一队**未平仓 lot**（`qty`, `px`），队内所有 lot 方向相同。
* 新成交与当前方向**相同**（或当前为 flat）⟹ 追加一个 lot。
* **相反** ⟹ 从队首开始平仓：每平一段 `c` 手，实现 `方向 * (成交价 - lot价) * c`（多头：卖价 − 买价；空头：开仓价 − 回补价）。
* 平完还有剩余 ⟹ **翻转**：剩余部分以成交价作为新方向的第一个 lot。
* `openCost` = 未平仓 lot 的 `qty * px` 之和（恒 ≥ 0）；`netQty` = 方向 × 未平仓手数之和。
* 全程整数；**溢出抛 `ArithmeticException`，仓位保持原样**（先只读地算出盈亏，再一次性提交）。

### 样例

```java
var b = new PositionBook();
b.onFill("A", Side.BUY, 10, 100);
b.onFill("A", Side.BUY, 10, 110);          // netQty 20, openCost 2100
b.onFill("A", Side.SELL, 15, 120);         // 先平 10@100（+200）再平 5@110（+50）
// get("A") == Position("A", 5, 550, 250)

b.onFill("A", Side.SELL, 25, 130);         // 平 5@110（+100），翻成空头 20 @130
// get("A") == Position("A", -20, 2600, 350)
b.get("A").unrealizedPnl(120);             // 2600 - 20*120 = 200
```

## Part 3 · `RiskEngine`（交易前风控）

```java
public record RiskLimits(long maxOrderQty, long maxOrderNotional, long maxPosition, int maxOpenOrders, long priceBandBps)
public enum RiskReason { HALTED, NO_REFERENCE_PRICE, QTY_LIMIT, NOTIONAL_LIMIT, PRICE_BAND, OPEN_ORDERS_LIMIT, POSITION_LIMIT }
public sealed interface RiskResult { RiskResult ACCEPTED; record Accepted(); record Rejected(RiskReason reason); boolean isAccepted() }

public final class RiskEngine {
    public RiskEngine(RiskLimits limits)
    public void setReferencePrice(String symbol, long px)     // px <= 0 → IAE
    public void halt();  public void resume();  public boolean halted()
    public RiskResult check(Order o, PositionBook positions, OrderManager orders)   // 只读，不改任何状态
}
```

### 规则 (reconstructed)

**检查顺序 = `RiskReason` 的声明顺序**，报告**第一条**违反的。同时违反多条时结果必须确定（回放要得到同一个原因）。

1. `HALTED`：熔断中，拒绝一切（包括减仓单——kill switch 不挑单）。
2. `NO_REFERENCE_PRICE`：该标的没有设过参考价 ⟹ 拒绝（**fail closed**：无法判断价格带，就不放行）。
3. `QTY_LIMIT`：`qty > maxOrderQty`（`==` 通过）。
4. `NOTIONAL_LIMIT`：`px * qty > maxOrderNotional`（`==` 通过）；`px * qty` 溢出 ⟹ 也算 `NOTIONAL_LIMIT`（不能回绕成小数而通过）。
5. `PRICE_BAND`：`|px - ref| / ref > priceBandBps / 10000` 则拒绝，**边界含等于通过**。用整数交叉相乘：`|px - ref| * 10_000 <= ref * priceBandBps`，不做除法，没有舍入。
6. `OPEN_ORDERS_LIMIT`：`orders.openCount() >= maxOpenOrders`（所有标的合计；`PENDING` 也算；这一单本身尚未登记）。
7. `POSITION_LIMIT`：**最坏情况净仓**——假设该标的所有未完成买单都成交，或所有未完成卖单都成交（含本单）：
   `net + 未完成买单剩余(+本单若为买) <= maxPosition` 且 `net - 未完成卖单剩余(+本单若为卖) >= -maxPosition`。

### 样例

```java
var risk = new RiskEngine(new RiskLimits(1_000, 1_000_000, 5_000, 3, 500));   // 5% 价格带
risk.setReferencePrice("A", 100);
risk.check(new Order(1, "A", Side.BUY, 100, 105), positions, orders);   // ACCEPTED（+5.00% 恰好等于带宽）
risk.check(new Order(2, "A", Side.BUY, 100, 106), positions, orders);   // Rejected(PRICE_BAND)
risk.check(new Order(3, "B", Side.BUY, 1, 1), positions, orders);       // Rejected(NO_REFERENCE_PRICE)
```

## Part 4 · `TradingDesk`（事件溯源 + 重放）

```java
public final class TradingDesk {
    public TradingDesk(RiskLimits limits)
    public RiskResult submit(Order order)               // 重复 id → IllegalArgumentException
    public boolean onExec(ExecEvent event)              // false = 重复 Fill；非法 → IllegalTransitionException / NoSuchElementException
    public void setReferencePrice(String symbol, long px)
    public void halt();  public void resume()
    public OrderView order(long id);  public List<OrderView> allOrders()
    public Position position(String symbol);  public List<String> symbols()
    public List<DeskEvent> journal()                    // 不可变拷贝，按输入顺序
    public static TradingDesk replay(RiskLimits limits, List<DeskEvent> journal)
}
```

### 规则

* **每个变更方法先把输入追加到 journal，再处理**——即使处理会抛异常，输入也已经在 journal 里（真实系统里输入先被排序、记录，决定性的校验在记录之后）。
* `submit`：重复 id 抛异常（不改状态）；先 `risk.check`（在登记**之前**，否则这张单把自己算进未完成数量）；通过 ⟹ `orders.submit`；被拒 ⟹ 仍然 `orders.submit`，然后立刻应用 `Reject(id, reason.name())`，所以 `order(id)` 返回 `REJECTED`，`rejectReason` 是原因枚举名。**这个内部 Reject 不进 journal**（它是输出，不是输入）。
* `onExec`：成功应用的 `Fill` 同步更新 `PositionBook`（用订单里的标的和方向，成交里的数量和价格）；重复 `Fill` 不更新仓位。
* `replay(limits, journal)`：新建 desk，按顺序处理 journal 里的每个输入；**原来抛过异常的输入，重放时同样会抛，同样被吞掉**（状态没变）。结果的 `allOrders()`、`position(s)`、`journal()` 必须与原 desk 逐项相等。
* `journal()` 返回的是快照：之后的操作不会改变已取出的列表。

### 样例

```java
var desk = new TradingDesk(new RiskLimits(1_000, 10_000_000, 3_000, 50, 1_000));
desk.setReferencePrice("A", 100);
desk.submit(new Order(1, "A", Side.BUY, 100, 100));     // ACCEPTED
desk.onExec(new ExecEvent.Ack(1));
desk.onExec(new ExecEvent.Fill(1, 10, 60, 99));         // true；position("A").netQty() == 60
desk.submit(new Order(2, "A", Side.BUY, 5_000, 100));   // Rejected(QTY_LIMIT)；order(2).status() == REJECTED

var copy = TradingDesk.replay(limits, desk.journal());
// copy.allOrders().equals(desk.allOrders())，copy.position("A").equals(desk.position("A"))
```

## 边界清单（隐藏测试会打）

| 类别 | 例子 |
|---|---|
| 状态机 | 表里每个"非法"格；终态后任何事件；重复 Ack；`PENDING` 收到 `Fill`/`Cancel`；`Reject` 出现在 `WORKING` |
| 回报 | 重复 `execId`（含订单已 `FILLED` 之后）；超量成交后同一 `execId` 以合法数量重发；买单成交价 = 限价 / 高 1 / 低很多；卖单对称 |
| 聚合量 | `PENDING` 计入；`Cancel` / `Reject` / 全部成交后释放；多标的互不影响；随机事件流下与逐单重算一致 |
| 溢出 | `qty * px` 在 `Long.MAX_VALUE/2` 附近；PnL 乘积溢出后仓位原样；风控名义金额溢出不放行 |
| 仓位 | 同向加仓；部分平；恰好平完；翻转；flat 之后反向开仓；空头；多标的；与"逐手模型"对照（随机 2,000 笔） |
| 风控 | 每条规则的 `==` / `+1`；价格带 `ref` 很小或不整除（`10_007`、`3`）；未知标的；同时违反多条的确定顺序；`check` 不改状态；`halt` 拒绝减仓单；最坏情况仓位含未完成买单（净仓本身不超限）；空头一侧对称 |
| desk | 风控拒绝的单仍登记为 `REJECTED`；单笔恰好顶格的单不被误拒（不把自己算两遍）；非法事件抛出但仍在 journal；重放等于原状态（25 个随机种子 × 600 步）；journal 不可变 |
| 性能 | 30 万笔成交 < 2 s；5 万订单 × 4 事件 + 重放 < 3 s |

## 野外变体

* **订单簿 + 撮合**（把交易所一侧也建模）：`hc05`。
* **平均成本法**而不是 FIFO：`openCost / netQty` 要取整，PnL 出现舍入——面试时要主动问"用哪种成本法、舍入规则是什么"。
* **多币种 / 合约乘数 / 手续费**：PnL 加一个 `multiplier`，费用作为单独的事件。
* **撤单请求与确认分开**（`PENDING_CANCEL` 状态）：真实 FIX 状态机里有，竞态更多（撤单请求与成交同时到达）。
* **订单改单（replace）**：新数量 / 新价格，保持 / 丢失时间优先级。
* **策略与风控的接口**：把 `RiskCheck` 做成可组合的责任链（`List<RiskCheck>`），并讨论顺序依赖与短路。
* **并发**：多线程提交订单 ⟹ 加锁（粗粒度）还是单写者 + 队列？（这是 sd03 的核心：单写者。）

## 来源与置信度

`catalog/raw/forums.md` A4（1p3a 1136321，2025-07-09，Junior Engineer，技术电面：「问了33分钟简历和bq然后一道不是很难的ood，trading相关直接挂」；摘要 "an easy trading-related OOD question"，摘要 / 中）· `catalog/raw/official_and_process.md` §D4 #16（同一帖）· 相关家族：`forums.md` A8、A9、A5、G2（「making market order book in c++」）。**没有任何来源给出题面**；Part 划分、状态转移表、FIFO 规则、风控规则、journal/replay 全部是 **(reconstructed)**。

## 考什么

"OOD 题"的评分点是**建模的质量**，不是算法：

1. **用类型表达不变量**：`record` 的紧凑构造器让不可能的订单无法存在；`sealed` 事件 + 穷尽 `switch` 让漏掉一种事件变成编译错误；状态用 `enum` 而不是字符串。
2. **状态机显式化**：合法转移表写出来，非法的明确抛异常且不改状态。
3. **整数与溢出意识**：价格 tick、数量股数；`multiplyExact`；不用 `double` 表示钱。
4. **fail closed**：拿不准就拒绝（无参考价、熔断）。
5. **可扩展**：新增一条风控规则 / 一种事件，要改哪里？（设计的"开闭"程度。）
6. **决定性与可重放**：状态是输入的函数；为什么 `submit` 的风控检查要在登记之前；为什么 journal 先于处理。
