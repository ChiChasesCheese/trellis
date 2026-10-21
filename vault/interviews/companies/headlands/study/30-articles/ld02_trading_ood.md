# ld02 · 交易相关的 OOD：订单状态机、仓位盈亏、交易前风控、事件溯源 —— 讲义

> 读者：只会基本 Java（类、方法、循环、`ArrayList` / `HashMap`），不懂交易，也没学过状态机和事件溯源。覆盖这类题最可能的四个形态；真面试先问清楚题目。

---

## 1. 问题是什么

### 1.1 用大白话

交易员（或策略程序）**下单**：「买 100 股 AAPL，最高出 150 块」。订单发给交易所后陆续收到**回报**：

```text
你 ──下单──▶ 交易所
你 ◀──"收到了"────  (Ack)
你 ◀──"成交了 60 股，价格 149"──  (Fill)
你 ◀──"又成交了 40 股，价格 150"──  (Fill)  → 订单全部成交
```

程序要回答：**订单现在什么状态、还能成交多少**（订单状态机）；**持有多少股、赚了多少**（仓位与盈亏）；**新订单能不能发**——会不会打错价格、让仓位超过公司上限（交易前风控）；以及**程序崩了怎么恢复到一模一样的状态**——所有变化都来自一串"输入事件"，重放即可（事件溯源）。

### 1.2 手算一遍

风控规则：单笔最多 1,000 股、仓位最多 3,000 股。参考价 AAPL = 100。

```text
① 下单 #1：买 100 股，限价 100            风控：数量 100 ≤ 1000，价格没偏离参考价 → 通过
   订单 #1 状态 PENDING（已发出，交易所还没回话）
② 回报 Ack(#1)                            PENDING → WORKING
③ 回报 Fill(#1, 成交号 10, 60 股, 价 99)   WORKING → PARTIALLY_FILLED，已成交 60，剩余 40
   仓位：多 60 股，成本 60×99 = 5,940
④ 回报 Fill(#1, 成交号 11, 40 股, 价 100)  → FILLED
   仓位：多 100 股，成本 5,940 + 4,000 = 9,940
⑤ 下单 #2：卖 100 股，限价 101，Ack，Fill(#2, 12, 100 股, 价 105)
   FIFO 平仓：先平先买的 60 股@99：赚 60×(105−99)=360；再平 40 股@100：赚 40×(105−100)=200
   已实现盈亏 560，仓位回到 0
⑥ 下单 #3：买 5,000 股 → 风控：5,000 > 1,000 → 拒绝 QTY_LIMIT；订单 #3 状态 REJECTED
```

### 1.3 四个 Part

1. **Part 1 `OrderManager`**：状态机——哪些转移合法，非法的、重复的回报怎么办。
2. **Part 2 `PositionBook`**：成交 → 仓位与盈亏，FIFO 配对，**翻转**。
3. **Part 3 `RiskEngine`**：检查顺序、整数价格带、最坏情况仓位、熔断。
4. **Part 4 `TradingDesk`**：所有变化来自输入事件，先记日志再处理，`replay` 重放。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 订单、成交、仓位、盈亏

* **限价单（limit order）**：带方向（买 BUY / 卖 SELL）、数量、**限价**（买单「最高出这个价」，卖单「最低收这个价」）。成交价可以比限价**更好**，不能更差。
* **tick**：价格最小变动单位，价格存成整数个 tick（AAPL 150.25 美元、tick 0.01 美元 → 15,025）。
* **成交（fill）**：订单的一部分或全部被对手方接走；一张订单可分多次成交（部分成交）。
* **仓位（position）**：净持有数量，买入为正（**多头 long**），卖空为负（**空头 short**）。
* **已实现盈亏（realized PnL）**：已平掉部分赚了多少；**未实现盈亏**：没平部分按当前市价（mark price）估算。这两个数错了风控就是错的。

**多头和空头的盈亏**

```text
多头：买 10 股 @100，现在市价 120      未实现 = 10×120 − 10×100 = +200
空头：卖 10 股 @100（先卖后买），现在市价 120   未实现 = 10×100 − 10×120 = −200（价格涨了，空头亏）
```

统一：`盈亏 = 方向 × (现价 − 开仓价) × 数量`，多头 +1，空头 −1。代码里 `Side.sign()` 就是方向（BUY=+1，SELL=−1）。

**平仓用哪个开仓价？——FIFO 与平均成本**。分两次买入 10 股@100、10 股@110，再卖 15 股@120，已实现盈亏：

```text
FIFO（先进先出）：先平先买的。10×(120−100) + 5×(120−110) = 200 + 50 = 250        ← 这里用这个
平均成本：平均开仓价 = (1000+1100)/20 = 105，15×(120−105) = 225                   （剩下 5 股的成本仍按 105）
```

都是合法会计方法，结果不同，**面试要主动问"用哪种、舍入怎么处理"**。FIFO 全程整数无舍入；平均成本要除法（`2101/20` 不整除，得定舍入规则）。

**翻转（flip）**：多头 10 股，一笔卖出 25 股：前 10 股**平仓**（实现盈亏），剩 15 股**开空头**——一笔成交里发生两件事，是仓位类题最经典的 bug 来源（§5.2）。

### 2.2 订单的生命周期：有限状态机

有限状态机（finite state machine，FSM）= 一组**状态** + 一组**事件** + 一张"在状态 S 收到事件 E 变成 S'"的表；表里没有的格子**非法**。

不显式写表，状态散落在一堆 `if` 里：订单已 `FILLED` 又收到 `Fill`（重复投递或 bug），代码悄悄把已成交数量加第二遍，仓位翻倍；已 `CANCELED` 却又被成交。状态机让每种"不可能的事"都有明确的、会被测试抓到的结果。

这里的状态转移（实际 FIX 协议状态更多，这里是教学版）：

```text
          Ack              Fill(部分)             Fill(吃满)
 PENDING ─────▶ WORKING ──────────────▶ PARTIALLY_FILLED ───────▶ FILLED
    │              │  │                       │  ▲   └─Fill(部分)─┘
    │              │  └──────────Fill(吃满)───┼──┼─────────────────▶ FILLED
    │              │                          │
    │              └─Cancel──▶ CANCELED ◀─Cancel┘
    └─Reject──▶ REJECTED
```

终态 `FILLED`、`CANCELED`、`REJECTED` 不再变。Java：状态用 `enum`，事件用 `sealed interface` + `record`，转移用 `switch` 表达式（编译器检查处理了每种事件）。

### 2.3 整数算术与溢出：为什么不用 `double` 表示钱

`0.1` 在二进制里是无限循环小数，`double` 只能存近似值。

```java
System.out.println(0.1 + 0.2);        // 0.30000000000000004
System.out.println(0.1 + 0.2 == 0.3); // false
```

几十万笔成交每笔带点误差就对不上；更要命的是**重放**——运算顺序不同得到不同 `double`，两次结果不逐位相等，事件溯源的核心保证就破了。整数加减乘精确且满足结合律。

**溢出**：`long` 范围 ±9.22×10¹⁸，`px × qty` 超过它时 Java **默默回绕成负数**：

```java
long big = Long.MAX_VALUE;
System.out.println(big + 1);                    // -9223372036854775808，回绕了
System.out.println(Math.addExact(big, 1));      // 抛 ArithmeticException，看得见的失败
```

风控里特别危险：名义金额溢出成负数的订单会"小于上限"被放行。所以用 `multiplyExact` / `addExact`，溢出抛异常（风控里当"拒绝"）。

### 2.4 交易前风控（pre-trade risk check）

订单发出前必须通过的一组规则：出了交易所错单就是真金白银，所以在自己系统里先拦。著名事故都缺少或绕过了这类检查（如 2012 年 Knight Capital 软件事故，45 分钟亏损约 4.4 亿美元）；美国 SEC 市场准入规则（Rule 15c3-5）要求预交易风控。

**这里的七条规则**（按声明顺序检查，报告第一条违反的）：

| 规则 | 防什么 | 例子（限额：数量 1000，名义 100 万，仓位 5000，未完成 3 张，价格带 5%） |
|---|---|---|
| `HALTED` 熔断 | 出事了全部停 | 熔断开关（kill switch）打开 → 一律拒绝 |
| `NO_REFERENCE_PRICE` | 没参考价没法判断价格是否离谱 | **fail closed**：拿不准就拒绝，不是放行 |
| `QTY_LIMIT` | 多打了几个 0 的数量 | 买 100,000 股 |
| `NOTIONAL_LIMIT` | 数量 × 价格太大 | 买 1,000 股 × 150,000 |
| `PRICE_BAND` | **胖手指**：150 打成 15 或 1500 | 参考价 100，买入限价 200 |
| `OPEN_ORDERS_LIMIT` | 失控程序狂下单 | 已有 3 张未完成订单，再下一张 |
| `POSITION_LIMIT` | 持仓超过公司允许 | 见下 |

**最坏情况仓位**最易想漏：净持仓 2,500，还挂着 2,000 股买单随时可能成交，真实风险 4,500。新买单 500 股：`2500 + 2000 + 500 = 5000 ≤ 5000` 通过；501 股拒绝。

**检查顺序**：订单同时违反多条时报告哪一条？不固定顺序（如遍历 `HashMap` 的规则）则两次运行报告的原因可能不同，重放不一致。

**价格带用整数交叉相乘**：`|px − ref| / ref ≤ 0.05` 涉及除法和浮点；整数写法 `|px − ref| × 10_000 ≤ ref × 500`（5% = 500 基点），无舍入，恰好 5.00% 精确通过。

### 2.5 事件溯源（event sourcing）与决定性

不直接保存"当前状态"，而保存**所有改变状态的事件**（输入）；当前状态 = 对事件序列的一遍归约（fold）。

```text
状态₀ ──事件₁──▶ 状态₁ ──事件₂──▶ 状态₂ ── … ──▶ 状态ₙ        状态ₙ = f(f(f(状态₀, e₁), e₂), … eₙ)
```

好处：**崩溃恢复**（读日志重放，状态原样回来）；**复盘**（当天事件喂给调试版本）；**回测**（同一份代码喂历史行情，研究和生产同一份逻辑）；**主备一致**（备机重放同一日志）。

这一切成立的前提是 `f` **决定性**：同样输入永远同样输出。破坏者：

| 破坏者 | 例子 | 这里的办法 |
|---|---|---|
| 读时钟 | `System.currentTimeMillis()` | 状态机不读时钟（时间戳作为事件字段） |
| 遍历顺序 | 遍历 `HashMap` 决定先处理谁 | 输出前排序（`open()` 按 id 排序），检查顺序写死 |
| 浮点 | 运算顺序不同结果不同 | 全整数 |
| 随机数 | 无种子 `Random` | 不用 |
| 多线程竞态 | 线程交错顺序每次不同 | 单线程使用（单写者），线程交错顺序要记进日志 |

**"先记日志，后处理"（journal before process）**：每个输入先追加到日志，再改内存状态——任何状态改变都有日志里一条事件对应；先改状态再记日志，崩在中间就丢一条事件。（撮合引擎也这样；`TradingDesk` 是缩小版。我们作为交易所客户，订单真相在交易所，日志主要用于重建和复盘。）

**异常输入**：非法输入（如对不存在的订单发 `Ack`）已在日志里，处理时抛异常，**状态未变**；重放时同样抛，必须像第一次一样**吞掉**，否则一个坏输入让整个恢复失败。这依赖"先验证、后修改"：抛异常的路径不改任何状态。

### 2.6 Java 21 语法前置

`record`（紧凑构造器里写校验）、`sealed`（让 `switch` 可查穷尽）、模式匹配 `switch` 与 record 模式（`case Fill(var id, var qty) -> …` 一步完成类型判断和解构）、`switch` 表达式 + `yield`（直接产生值，无 fallthrough）。详见第 6 节。

---

## 3. 从最笨的解法开始

大多数人的第一反应（刻意写得"天真"）：

```java
class Order { String id; String symbol; String side; double qty; double price; String status = "NEW"; double filled; }

Map<String, Order> orders = new HashMap<>();
Map<String, Double> position = new HashMap<>();

void onFill(String id, double q, double px) {
    Order o = orders.get(id);
    o.filled += q;
    if (o.filled >= o.qty) o.status = "FILLED"; else o.status = "PARTIAL";
    position.merge(o.symbol, o.side.equals("BUY") ? q : -q, Double::sum);
}

boolean riskOk(Order o) {
    if (o.qty > 1000) return false;
    double pos = position.getOrDefault(o.symbol, 0.0);
    return Math.abs(pos + (o.side.equals("BUY") ? o.qty : -o.qty)) <= 3000;
}
```

**错 / 慢的输入**：

| 输入 | 暴露的问题 |
|---|---|
| 同一个 `Fill` 投递两次 | 仓位翻倍；`filled` 超过 `qty` |
| `CANCELED` 的订单又收到 `Fill` | 悄悄改回 `PARTIAL`——幽灵订单 |
| `side = "buy"`（小写）/ 拼错状态 | `equals` 不匹配，被当卖单；编译器不提醒 |
| 数量 0.1 + 0.2 | `double` 误差，订单永不到 `FILLED` |
| 多头 10 股，卖 25 股 | `merge` 只得 −15，**盈亏没算**：无"平 10 股的实现盈亏"，无"新空头的成本" |
| 风控：已有挂单 | 只看 `position` 不看未成交挂单——最坏情况仓位漏了 |
| 风控检查时订单 `o` 已登记 | 把自己算进未完成数量，顶格订单被误拒 |
| 订单数很多 | 每次扫描所有订单求未完成数量，总 O(n²) |
| 重启 | 状态全丢，无恢复手段 |

---

## 4. 一步一步改进

### 步骤 1：用类型表达"不可能"

字符串状态、`double` 数量、`side = "buy"`：让非法值**无法构造**，由编译器 / 构造器拦，而非靠每个方法记得检查。

```java
public enum Side { BUY, SELL }                                  // 不是字符串
public record Order(long id, String symbol, Side side, long qty, long px) {
    public Order {                                              // 紧凑构造器：非法订单造不出来
        if (qty <= 0) throw new IllegalArgumentException(...);
        ...
    }
}
```

价格和数量改 `long`。复杂度不变，但消除一整类 bug。

### 步骤 2：显式状态机，非法转移抛异常且不改状态

转移表写成代码；`switch` 对事件类型穷尽匹配；每个分支先验证（`require(...)`）、后修改——异常路径无副作用，是之后 `replay` 成立的前提（`OrderManager.apply`，§5.1）。

### 步骤 3：Fill 去重放在状态检查之前

回报是 **at-least-once** 投递：同一笔成交可能到两次。每笔成交有全局唯一 `execId`，记在 `Set`，见过的直接返回 `false`。

**为什么在状态检查之前**：订单已 `FILLED` 后旧回报过来，先检查状态会被当"终态后又来 Fill"的**非法转移**抛异常，但它只是重复消息，应安静忽略。**细节**：**验证通过之后**才记 `execId`；超量成交被拒后其 `execId` 不能算"已处理"，否则之后用合法数量重发会被当重复吞掉。

### 步骤 4：风控要的聚合量，增量维护

风控每个订单都问"这个标的未完成买单总量"和"几张未完成订单"，扫描所有订单 O(n)。把这两个量作为状态，每次状态变化同步更新：`submit` +qty；`Fill` −成交量；`Cancel`/`Reject` −剩余量；终态 `openCount--`。查询 O(1)。**代价**：所有会改变订单的地方都要记得更新，漏一处就漂移，所以用随机事件流做对照校验（"逐单重算"检查一致）。

### 步骤 5：仓位用 FIFO lot 队列

每个标的维护一队**未平仓 lot**（数量，价格），同一时刻所有 lot 方向相同。新成交：
* 同向（或 flat）→ 追加 lot；
* 反向 → 从队首起平仓，每平一段实现 `方向 × (成交价 − lot价) × 数量`；平完还有剩余 → 剩余部分**以成交价作为新方向的第一个 lot**（翻转）。

全是整数加减乘；翻转不是特例，只是"平完队列后还有剩余"的自然结果。每个 lot 最多入队、出队一次，`onFill` 摊还 O(1)。

### 步骤 6：风控整数交叉相乘，溢出视为拒绝

§2.4。`PRICE_BAND` 和 `NOTIONAL_LIMIT` 都用 `multiplyExact`，`catch ArithmeticException` 当拒绝。

### 步骤 7：最坏情况仓位

§2.4。`net + 未完成买单剩余 (+本单)`、`net − 未完成卖单剩余 (+本单)` 与 ±`maxPosition` 比较。

### 步骤 8：装配成 `TradingDesk`，输入先记日志

定义 `DeskEvent`（`Submit`、`SetReferencePrice`、`Halt`、`Resume` 以及 `ExecEvent`）为**全部输入**；每个变更方法先 `journal.add(event)` 再 `handle(event)`；`replay` 对新 desk 重复 `handle`。输出（风控结论、被拒订单、仓位）全是输入的函数，不在日志里，重放时重算——两次不相等就是有非决定性的东西混进来了。

### 步骤 9：重放吞掉同样的异常

日志里有第一次就抛异常的输入（重复 id、非法转移、未知订单）。`replay` 里 `try { handle(e) } catch (...) {}`——状态本来就没变，吞掉是对的。只吞**预期的**业务异常（`IllegalArgumentException`、`IllegalStateException`、`NoSuchElementException`、`ArithmeticException`）；其他（`NullPointerException`、`OutOfMemoryError`）说明有 bug，应让它崩。

---

## 5. 逐段讲解法

### 5.1 数据类型和状态机（`Order`、`ExecEvent`、`OrderManager.apply`）

```java
public record Order(long id, String symbol, Side side, long qty, long px) {
    public Order {
        Objects.requireNonNull(symbol, "symbol");
        Objects.requireNonNull(side, "side");
        if (id <= 0) throw new IllegalArgumentException("id must be > 0: " + id);
        if (symbol.isBlank()) throw new IllegalArgumentException("symbol is blank");
        if (qty <= 0) throw new IllegalArgumentException("qty must be > 0: " + qty);
        if (px <= 0) throw new IllegalArgumentException("px must be > 0: " + px);
    }
}
```

* 紧凑构造器无参数列表，直接写校验，字段赋值由编译器在末尾补上；`requireNonNull` 抛 NPE，其余抛 `IllegalArgumentException`。

```java
public sealed interface ExecEvent extends DeskEvent permits ExecEvent.Ack, ExecEvent.Fill, ExecEvent.Cancel, ExecEvent.Reject {
    long orderId();

    /** 交易所收下了这张单。 */
    record Ack(long orderId) implements ExecEvent {}

    /** 一笔成交。execId 全局唯一：回报可能重复投递（at-least-once），靠它去重。 */
    record Fill(long orderId, long execId, long qty, long px) implements ExecEvent {
        public Fill {
            if (qty <= 0) throw new IllegalArgumentException("fill qty must be > 0: " + qty);
            if (px <= 0) throw new IllegalArgumentException("fill px must be > 0: " + px);
        }
    }

    /** 撤单已确认（不是「撤单请求」）。 */
    record Cancel(long orderId) implements ExecEvent {}

    /** 交易所拒绝（或本地风控拒绝）。 */
    record Reject(long orderId, String reason) implements ExecEvent {
        public Reject {
            java.util.Objects.requireNonNull(reason, "reason");
        }
    }
}
```

* `sealed ... permits`：只有这四个实现，`apply` 里的 `switch` **穷尽**——新增回报不改 `switch` 就编译不过。
* `ExecEvent extends DeskEvent`：回报也是 desk 的输入事件。

```java
    public boolean apply(ExecEvent event) {
        Objects.requireNonNull(event, "event");
        State s = orders.get(event.orderId());
        if (s == null) throw new NoSuchElementException("unknown order " + event.orderId());
        return switch (event) {
            case ExecEvent.Ack a -> {
                require(s.status == OrderStatus.PENDING, s, "Ack");
                s.status = OrderStatus.WORKING;
                yield true;
            }
            case ExecEvent.Fill f -> {
                if (seenExecIds.contains(f.execId())) yield false;     // 重复投递：先于状态检查（FILLED 之后重放的旧回报也只是重复）
                require(s.status == OrderStatus.WORKING || s.status == OrderStatus.PARTIALLY_FILLED, s, "Fill");
                if (f.qty() > s.leaves()) throw new IllegalTransitionException("overfill on order " + s.order.id());
                boolean outside = s.order.side() == Side.BUY ? f.px() > s.order.px() : f.px() < s.order.px();
                if (outside) throw new IllegalTransitionException("fill px " + f.px() + " outside limit " + s.order.px());
                long notional = Math.multiplyExact(f.qty(), f.px());
                long newCumNotional = Math.addExact(s.cumNotional, notional);   // 可能抛 ArithmeticException：在修改任何东西之前
                seenExecIds.add(f.execId());
                s.cumQty += f.qty();
                s.cumNotional = newCumNotional;
                reduceOpen(s, f.qty());
                if (s.cumQty == s.order.qty()) {
                    s.status = OrderStatus.FILLED;
                    openCount--;
                } else {
                    s.status = OrderStatus.PARTIALLY_FILLED;
                }
                yield true;
            }
            case ExecEvent.Cancel c -> {
                require(s.status == OrderStatus.WORKING || s.status == OrderStatus.PARTIALLY_FILLED, s, "Cancel");
                reduceOpen(s, s.leaves());
                s.status = OrderStatus.CANCELED;
                openCount--;
                yield true;
            }
            case ExecEvent.Reject r -> {
                require(s.status == OrderStatus.PENDING, s, "Reject");
                reduceOpen(s, s.leaves());
                s.status = OrderStatus.REJECTED;
                s.rejectReason = r.reason();
                openCount--;
                yield true;
            }
        };
    }
```

* 未知订单抛 `NoSuchElementException`——**在任何修改之前**。
* `Fill` 分支顺序很讲究：①去重（`seenExecIds`）→ ②状态是否允许 → ③是否超量 → ④是否越过限价 → ⑤算新累计成交额（`multiplyExact`/`addExact` 可能抛）→ **全部通过之后**才 ⑥ 记 `execId`、改 `cumQty`、改聚合量、改状态。前五步只读不写，任何一步失败状态都没动。
* `reduceOpen(s, f.qty())` 同步减少未完成剩余；`Cancel` 一次性减掉全部剩余（`s.leaves()`）。`openCount--` 只在到达终态时（`FILLED`、`CANCELED`、`REJECTED`）。

### 5.2 仓位（`PositionBook.onFill`）

```java
    public void onFill(String symbol, Side side, long qty, long px) {
        Objects.requireNonNull(symbol, "symbol");
        Objects.requireNonNull(side, "side");
        if (qty <= 0 || px <= 0) throw new IllegalArgumentException("qty and px must be > 0");
        Book b = books.computeIfAbsent(symbol, k -> new Book());
        int s = side.sign();
        if (b.dir == 0 || b.dir == s) {
            b.lots.addLast(new Lot(qty, px));
            b.dir = s;
            return;
        }
        long remaining = qty;
        long realized = b.realized;
        // 先只读地算出实现盈亏（溢出会在这里抛，此时还没改任何东西），再一次性提交
        long pnl = 0;
        for (Lot lot : b.lots) {
            if (remaining == 0) break;
            long c = Math.min(remaining, lot.qty);
            pnl = Math.addExact(pnl, Math.multiplyExact((long) b.dir * (px - lot.px), c));
            remaining -= c;
        }
        long newRealized = Math.addExact(realized, pnl);
        // 提交（以下不会再抛异常）
        remaining = qty;
        while (remaining > 0 && !b.lots.isEmpty()) {
            Lot lot = b.lots.peekFirst();
            long c = Math.min(remaining, lot.qty);
            lot.qty -= c;
            remaining -= c;
            if (lot.qty == 0) b.lots.pollFirst();
        }
        b.realized = newRealized;
        if (remaining > 0) {
            b.lots.addLast(new Lot(remaining, px));
            b.dir = s;                       // 翻转
        } else if (b.lots.isEmpty()) {
            b.dir = 0;
        }
    }
```

* `b.dir`：+1 多头 / −1 空头 / 0 平；`s = side.sign()`。同向或 flat：追加 `Lot`，设方向，返回。
* 反向：**先只读地**遍历队列算出实现盈亏 `pnl`（`(long) b.dir * (px - lot.px) * c`，`multiplyExact`/`addExact`），溢出在这里抛，此时什么都没改；再遍历一次真正消耗 lot，`remaining > 0` 即翻转，追加新方向的 lot。
* 算两遍是为"溢出不留半个状态"：边算边改的话第三个 lot 溢出时前两个已被消耗。代价是常数倍遍历，一次成交涉及的 lot 通常很少。

### 5.3 风控（`RiskEngine.check`）

```java
    public RiskResult check(Order o, PositionBook positions, OrderManager orders) {
        if (halted) return reject(RiskReason.HALTED);
        Long ref = refPx.get(o.symbol());
        if (ref == null) return reject(RiskReason.NO_REFERENCE_PRICE);      // fail closed
        if (o.qty() > limits.maxOrderQty()) return reject(RiskReason.QTY_LIMIT);
        try {
            if (Math.multiplyExact(o.px(), o.qty()) > limits.maxOrderNotional()) return reject(RiskReason.NOTIONAL_LIMIT);
            // |px - ref| / ref <= bps / 10000   <=>   |px - ref| * 10000 <= ref * bps    （整数交叉相乘，不做除法）
            long dev = Math.multiplyExact(Math.abs(o.px() - ref), 10_000L);
            if (dev > Math.multiplyExact(ref, limits.priceBandBps())) return reject(RiskReason.PRICE_BAND);
        } catch (ArithmeticException overflow) {
            return reject(RiskReason.NOTIONAL_LIMIT);
        }
        if (orders.openCount() >= limits.maxOpenOrders()) return reject(RiskReason.OPEN_ORDERS_LIMIT);
        // 最坏情况净仓：假设所有未完成买单都成交 / 所有未完成卖单都成交（含这一单）
        long buyLeaves = orders.openLeaves(o.symbol(), Side.BUY) + (o.side() == Side.BUY ? o.qty() : 0);
        long sellLeaves = orders.openLeaves(o.symbol(), Side.SELL) + (o.side() == Side.SELL ? o.qty() : 0);
        long net = positions.netQty(o.symbol());
        if (net + buyLeaves > limits.maxPosition() || net - sellLeaves < -limits.maxPosition())
            return reject(RiskReason.POSITION_LIMIT);
        return RiskResult.ACCEPTED;
    }
```

* 每行 `return reject(...)` 的顺序就是 `RiskReason` 的声明顺序。
* 价格带 `Math.abs(o.px() - ref) * 10_000` 与 `ref * limits.priceBandBps()` 比较，两边 `multiplyExact`；`catch (ArithmeticException overflow) { return reject(NOTIONAL_LIMIT); }`：乘法溢出一律拒绝。
* 最坏情况仓位：`orders.openLeaves(...)` O(1)，`positions.netQty` 遍历该标的 lot（通常很短；成为瓶颈可缓存 `netQty`）。
* `check` 不改状态：可在"登记订单之前"调用，也可单独验证。

### 5.4 装配与重放（`TradingDesk`）

```java
    public RiskResult submit(Order order) {
        DeskEvent e = new DeskEvent.Submit(order);
        journal.add(e);
        return handleSubmit((DeskEvent.Submit) e);
    }
```

```java
    public boolean onExec(ExecEvent event) {
        journal.add(Objects.requireNonNull(event, "event"));
        return handleExec(event);
    }
```

```java
    public static TradingDesk replay(RiskLimits limits, List<DeskEvent> journal) {
        TradingDesk d = new TradingDesk(limits);
        for (DeskEvent e : journal) {
            d.journal.add(e);
            try {
                d.handle(e);
            } catch (IllegalArgumentException | IllegalStateException | NoSuchElementException | ArithmeticException sameAsBefore) {
                // 第一次执行时调用方已经看到过这个异常，且状态没有改变
            }
        }
        return d;
    }
```

```java
    private Object handle(DeskEvent e) {
        return switch (e) {
            case DeskEvent.Submit s -> handleSubmit(s);
            case DeskEvent.SetReferencePrice(var symbol, var px) -> { risk.setReferencePrice(symbol, px); yield null; }
            case DeskEvent.Halt h -> { risk.halt(); yield null; }
            case DeskEvent.Resume r -> { risk.resume(); yield null; }
            case ExecEvent x -> handleExec(x);
        };
    }
```

```java
    private RiskResult handleSubmit(DeskEvent.Submit s) {
        Order o = s.order();
        if (orders.contains(o.id())) throw new IllegalArgumentException("duplicate order id " + o.id());
        RiskResult r = risk.check(o, positions, orders);      // 必须在 submit 之前：否则这张单把自己算进未完成数量
        orders.submit(o);
        if (r instanceof RiskResult.Rejected(var reason)) orders.apply(new ExecEvent.Reject(o.id(), reason.name()));
        return r;
    }
```

```java
    private boolean handleExec(ExecEvent x) {
        boolean applied = orders.apply(x);
        if (applied && x instanceof ExecEvent.Fill(var orderId, var ignoredExecId, var qty, var px)) {
            Order o = orders.get(orderId).order();
            positions.onFill(o.symbol(), o.side(), qty, px);
        }
        return applied;
    }
```

* `handle` 是**唯一**修改状态的地方，`submit/onExec/...` 是"先记日志、再调 handle"的薄包装；`replay` 也调同一个 `handle`——实时与恢复同一份代码，不会悄悄分叉。
* `handleSubmit`：先检查重复 id；再 `risk.check`（**登记之前**）；再登记；被拒则立即应用一条 `Reject`——这条内部 `Reject` 不进 journal（是**输出**，重放时由同样的风控重新产生）。
* `handleExec`：`orders.apply` 返回 `true`（不是重复）且是 `Fill` 才更新仓位；`x instanceof ExecEvent.Fill(var orderId, var ignoredExecId, var qty, var px)` 是 record 模式的 `instanceof` 形式。

### 5.5 数据

事件处理速度（JIT 预热后取 5 次中位数）：

```text
live  : 400,000 events in 17.7 ms (median of 5) => 22.63 M events/s, 44 ns/event
replay: 400,000 events in 17.1 ms (median of 5) => 23.43 M events/s, 43 ns/event
PositionBook.onFill: 3,000,000 fills in 103.3 ms => 29.03 M fills/s（含 "S"+i 字符串拼接的分配）
```

这是**吞吐量级**，不是延迟指标：测平均值，不含 GC 停顿尾部；实现为清晰用了 `HashMap<Long, …>`、装箱、record 分配，未为零分配优化。用在 µs 级热路径需：原语哈希表、预分配订单槽位、不为每个事件创建 record。重放速度与实时几乎一样（同一份 `handle`）。

---

## 6. Java 21 特性小课

| 特性 | 旧写法（Java 8 风格） | 新写法 | 编译器多做了什么 / 什么时候别用 |
|---|---|---|---|
| **`record` + 紧凑构造器** | 15 行：私有 final 字段、构造器、getter、`equals`、`hashCode`、`toString` | `record Order(long id, String symbol, ...) { Order { 校验 } }` | 生成全部样板，字段不可变。不用于需继承或可变处；`byte[]` 字段的 `equals` 是引用比较（这里无数组字段） |
| **`sealed interface ... permits`** | `interface ExecEvent {}` + 约定「只有这四个实现」 | `sealed interface ExecEvent permits Ack, Fill, Cancel, Reject` | 编译器知道所有子类型，`switch` 才能查穷尽。不用于需外部扩展的 SPI |
| **`switch` 模式匹配** | `if (e instanceof Ack) {...} else if ...` 加强转，漏一个运行时才发现 | `switch (event) { case ExecEvent.Ack a -> ...; case ExecEvent.Fill f -> ...; ... }` | sealed 类型不需 `default`；少写 `case` 编译报错。加 `default` 反会掩盖「新增事件类型忘了处理」 |
| **record 模式** | `if (e instanceof Fill) { Fill f = (Fill) e; long q = f.qty(); ... }` | `x instanceof ExecEvent.Fill(var orderId, var execId, var qty, var px)` | 解构嵌套 record；不能写常量，要用 `when` 守卫 |
| **`switch` 表达式 + `yield`** | 先声明 `boolean result;` 再每个 `case` 赋值，别忘 `break` | `return switch (event) { case ... -> { ...; yield true; } }` | 无 fall-through；每分支必须产出值 |
| **`Math.multiplyExact` / `addExact`** | `long r = a * b;`（溢出默默回绕）或手写 `if (a != 0 && r / a != b)` | `Math.multiplyExact(px, qty)` 溢出抛 `ArithmeticException` | 比手写短；热路径少量开销（JIT 内联成溢出标志检查）。「用异常表示拒绝」要在不应改变状态处捕获 |
| **`Stream.toList()` / `List.copyOf`** | `.collect(Collectors.toList())`（可变）/ `Collections.unmodifiableList(new ArrayList<>(x))` | `.sorted(...).toList()` / `List.copyOf(journal)` | 不可变；`copyOf` 是防御性拷贝，元素不能为 `null` |
| **`var`** | `DeskEvent.Halt e = new DeskEvent.Halt();` | `var e = new DeskEvent.Halt();` | 只在右边已写出类型时用 |

---

## 7. 追问预演

### Q1：新增一条风控规则（如「单标的每秒最多 N 笔」），改哪里？

现在是 `check` 里一串 `if`（顺序 = 枚举声明顺序，可审计）。①加一个 `RiskReason` + 一个 `if`（编译器经 `switch` 穷尽性提醒处理新原因处）；②重构为 `List<RiskCheck>`（责任链），每条规则 `Optional<RiskReason> check(ctx)`，固定顺序执行——利于测试组合，但多一层间接，**热路径**保持前者。速率限制需要时间：**时间必须作为事件进来**（`Tick`），不能在检查里读时钟，否则破坏决定性。

### Q2：多个线程同时提交订单？

**单写者**：一个线程拥有 `TradingDesk`，其他线程把命令放进 MPSC 队列。加锁的问题：锁竞争和上下文切换进入延迟；多线程交错顺序每次不同，破坏决定性——除非把"实际处理顺序"记进日志。并行靠**按标的分片**（每片一个 desk），而非一个 desk 里加锁。

### Q3：市价单怎么支持？

`px` 没有了，价格带无法检查：用参考价（或对手方最优价）加保护价（marketable limit）近似；名义金额用保护价估算；`Fill` 的限价约束改为保护价。很多交易所不支持裸市价单，系统常把市价单转成带保护价的限价单，风控规则不用特判。

### Q4：撤单请求和撤单确认的区别？

先有"撤单请求"（我们发出），再有"撤单确认"（交易所回）。中间状态 `PENDING_CANCEL`：订单仍可能被成交（请求和成交在途中交叉）。这里 `Cancel` 只表示**确认**。若加 `PENDING_CANCEL`：`WORKING/PARTIALLY_FILLED --请求--> PENDING_CANCEL`，`--Fill--> 仍可成交`，`--确认--> CANCELED`，`--撤单拒绝--> 回到原状态`。最坏情况仓位在此期间**仍要计入**该订单剩余数量（撤单是个竞态，不是一个瞬间）。

### Q5：为什么 `PENDING` 订单也算未完成？

已发出，交易所可能已成交只是回报没到；风控按"最坏情况"算，否则「连续快速下多张单，每张都通过，合起来超限」。回报是滞后的，风险不是。

### Q6：为什么 FIFO，换成平均成本要改什么？

平均成本需 `openCost / netQty`，不整除，要定义舍入（四舍五入 / 向零 / 向下）；平仓用平均价，剩余保留平均价。实现更简单（不用队列，只存 `netQty` 和 `costBasis`），但要选舍入并解释累积误差——成本存「总成本」（整数），平仓按比例 `costBasis × closeQty / netQty` 取整，余数留在 `costBasis`，总和保持精确。FIFO 全整数无舍入。选哪种是业务/会计决定，我先问。

### Q7：怎么持久化，重启后恢复？

journal 追加写文件；定期快照（序列化当前状态，记下日志位置，须与日志位置原子对应）；恢复 = 读快照 + 重放其后的日志，恢复时间由日志尾长度决定，所以快照要定期。日志格式：定长头 + 二进制载荷、校验和、按大小切段。恢复后要对账交易所（订单真相在交易所）。

### Q8：重放结果与线上不一致，怎么排查？

二分日志：重放前 k 条，比较状态摘要（哈希）与线上同位置摘要，找第一个分叉事件；常见原因：读时钟 / 随机数 / `HashMap` 遍历顺序 / 浮点 / 外部可变状态 / 线程。预防：线上周期性记录状态摘要进日志，发布前用生产日志做重放回归——决定性要靠自动化校验守护，不是靠自觉。

### Q9：每秒 100 万个事件，这个实现够吗？

约 2,200 万事件/s（平均，JIT 预热后），吞吐够；µs 级尾延迟不够：每事件分配 record、`HashMap<Long,…>` 装箱、`ArrayList` 增长都产生垃圾导致 GC 停顿。改进：原语哈希表、订单槽位预分配 + 空闲链表、journal 用预分配环 / mmap、事件用 flyweight 视图。先测量再优化。

### Q10：`record` 的 `equals` 让两个 desk 状态可直接比较，有什么风险？

逐字段比较，嵌套 record 递归，OK；含 `double`（NaN）或数组有陷阱；`OrderView` 里是 `long`/`String`/枚举，安全。比较两个 desk 的 `allOrders()` 就依赖它；字段是可变集合则比较当时内容。

---

## 8. 常见误区

1. **先登记订单再做风控检查**。订单把自己算进「未完成数量」，恰好顶格的订单被误拒。→ `check` 在 `submit` 之前。
2. **重复回报按状态检查**。订单已 `FILLED` 后的旧回报被当非法转移抛异常，或更糟——当成新成交把仓位翻倍。→ 去重在状态检查之前。
3. **边验证边修改**。超量成交先加 `cumQty` 再发现超量，抛异常时状态已破坏；`execId` 先记进 Set，之后合法重发被吞。→ 所有检查在修改之前。
4. **用 `double` 或 `int`**。`int` 的 `qty × px` 在 21 亿就溢出；`double` 累加有误差。→ `long` + `multiplyExact`。
5. **翻转时只改方向、不算盈亏**：多头 10 股卖 25 股，要先平 10 股实现盈亏，再以成交价开 15 股空头。
6. **风控只看净仓不看挂单**：净仓 2,500 + 挂单买 2,000，再买 501，看着 3,001 没超，其实最坏 5,001。
7. **价格带用除法 / 浮点**：边界（恰好 5%）因舍入误拒或误放；参考价小（3）时「5% = 0.15」整除出 0。
8. **缺参考价就放行**。无法判断就放行是 fail open；正确是拒绝。
9. **replay 里不吞异常**。第一次抛过异常的输入，重放时同样抛，恢复失败。
10. **`journal()` 返回内部 list**。调用方可篡改日志；→ `List.copyOf`。

---

## 9. 自测题

**Q1（概念）**：为什么重放要求状态机"决定性"？列出至少三种破坏者及对策。

<details><summary>答案</summary>

不决定性则重放结果与崩溃前不同，恢复、复盘、回测都失去意义。破坏者：读时钟（时间作为事件字段）、`HashMap` 遍历顺序（输出前排序，检查顺序写死）、浮点（全整数）、无种子随机数（不用）、多线程交错（单线程，顺序记进日志）。
</details>

**Q2（计算）**：10 股@100、20 股@110 依次买入，然后卖出 25 股@120。FIFO 下已实现盈亏？剩余仓位的 `openCost`？再买 5 股@90 之后呢？

<details><summary>答案</summary>

先平 10@100：10×(120−100)=200；再平 15@110：15×(120−110)=150；已实现 350。剩余 5 股@110，`openCost` = 550，`netQty` = 5。再买 5 股@90：同向追加 lot，netQty = 10，openCost = 550 + 450 = 1000，已实现仍 350。
</details>

**Q3（翻转）**：多头 10 股（均 @100），卖 25 股@110。结果的 `netQty`、`openCost`、`realizedPnl`？

<details><summary>答案</summary>

平 10 股：10×(110−100)=100。剩余 15 股作空头 lot @110：`netQty = −15`，`openCost = 15×110 = 1650`，`realizedPnl = 100`。
</details>

**Q4（风控）**：maxPosition = 5000。净仓 2,500，挂单买 1,000 + 1,000。再买 500 通过吗？买 501？卖 4,000（数量限额放得下）？

<details><summary>答案</summary>

买 500：2500 + 2000 + 500 = 5000 ≤ 5000，通过；买 501：5001，拒绝（`POSITION_LIMIT`）。卖 4,000：`net − 未完成卖 − 本单` = 2500 − 0 − 4000 = −1500 ≥ −5000，通过；买方向暴露 `net + 买挂单` = 4500 ≤ 5000 不变，通过。
</details>

**Q5**：在 `OrderManager` 里新增 `PENDING_CANCEL`，写出需改的三处。

<details><summary>答案</summary>

①`OrderStatus` 加枚举值，`isOpen()` 仍 true；②新增事件 `CancelRequest(orderId)`（编译器会逼你在 `apply` 的 `switch` 里处理）：`WORKING/PARTIALLY_FILLED → PENDING_CANCEL`；③`Fill` 在该状态仍允许；`Cancel`（确认）→ `CANCELED`；`CancelReject` 回到原状态（需记住）。风控的未完成剩余量不能在请求时减，要等确认。
</details>

---

## 延伸阅读

* Martin Fowler「Event Sourcing」。
