# ld02 · 交易相关的 OOD：订单状态机、仓位盈亏、交易前风控、事件溯源 —— 讲义

> 题面：`loop/rounds/03_lld/ld02_trading_ood/problem.md` · 代码：同目录 `reference/`（`OrderManager` `PositionBook` `RiskEngine` `TradingDesk` 与若干数据类型）· 测试：`test/`（56 个）
> 实验代码：`study/30-articles/examples/ld02/DeskBench.java`（事件处理速度）。本文的"实测"来自它和测试套件在本机（Apple M 系列，12 核，JDK 21.0.12）的运行。
> 写法说明见 `study/TEXTBOOK.md`。读者设定：只会基本 Java（类、方法、循环、`ArrayList` / `HashMap` 的基本用法），不懂交易，也没学过状态机和事件溯源。
> **题面是 (reconstructed)**：证据只有「1p3a 一帖摘要：33 分钟电话面里一道不是很难的、与交易相关的 OOD」。本讲义覆盖这类题最可能出现的四个形态。真面试先问清楚题目。

---

## 1. 这道题在问什么

### 1.1 用大白话

想象你在一家交易公司写后台。交易员（或者策略程序）会**下单**：「我要买 100 股 AAPL，最高出 150 块」。这张**订单**发给交易所以后，会陆续收到交易所的**回报**：

```text
你 ──下单──▶ 交易所
你 ◀──"收到了"────  (Ack)
你 ◀──"成交了 60 股，价格 149"──  (Fill)
你 ◀──"又成交了 40 股，价格 150"──  (Fill)  → 订单全部成交
```

你的程序要回答三类问题：

1. **这张订单现在是什么状态？**还能成交多少？（订单状态机）
2. **我现在持有多少股？赚了多少钱？**（仓位与盈亏）
3. **这张新订单可以发出去吗？**会不会一手打错价格、会不会让仓位超过公司允许的上限？（交易前风控）

最后一个问题：**如果程序崩了，怎么恢复到崩溃前一模一样的状态？**——只要所有变化都来自一串"输入事件"，把这串事件重放一遍就行（事件溯源）。

### 1.2 手算一遍

公司的风控规则（后面会详细讲）：单笔最多 1,000 股、仓位最多 3,000 股。参考价 AAPL = 100。

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

对应测试 `TradingDeskTest.fullLifecycleUpdatesOrderAndPosition`（那里的数字略有不同，逻辑一样）。

### 1.3 四个 Part 怎么递进

1. **Part 1 `OrderManager`**：订单状态机。哪些转移合法，非法的怎么办，重复回报怎么办。
2. **Part 2 `PositionBook`**：成交 → 仓位与盈亏。FIFO 配对，**翻转**（从多头一笔卖成空头）。
3. **Part 3 `RiskEngine`**：交易前风控。检查顺序、整数价格带、最坏情况仓位、熔断。
4. **Part 4 `TradingDesk`**：把三者装起来，所有变化都来自输入事件，先记日志再处理，`replay` 重放。

---

## 2. 前置知识

### 2.1 订单、成交、仓位、盈亏

**是什么**

* **限价单（limit order）**：带方向（买 BUY / 卖 SELL）、数量、**限价**。买单的意思是「最高出这个价」，卖单的意思是「最低收这个价」。成交价可以比限价**更好**（买得更便宜、卖得更贵），不能更差。
* **tick**：价格的最小变动单位。我们把价格存成"多少个 tick"的整数，比如 AAPL 的 150.25 美元，tick 是 0.01 美元，就存成 15,025。
* **成交（fill / execution）**：订单的一部分或全部被对手方接走。一张订单可以分多次成交（部分成交）。
* **仓位（position）**：你现在持有的净数量。买入为正（**多头 long**），卖空为负（**空头 short**）。
* **已实现盈亏（realized PnL）**：已经平掉的那部分赚了多少。
* **未实现盈亏（unrealized PnL）**：还没平的那部分，按当前市价（mark price）估算赚了多少。

**为什么需要它**：交易公司的一切决策都建立在"我现在持有什么、赚了多少"之上。这两个数错了，风控就是错的。

**怎么工作：多头和空头的盈亏**

```text
多头：买 10 股 @100，现在市价 120      未实现 = 10×120 − 10×100 = +200
空头：卖 10 股 @100（先卖后买），现在市价 120   未实现 = 10×100 − 10×120 = −200（价格涨了，空头亏）
```

两者可以统一：`盈亏 = 方向 × (现价 − 开仓价) × 数量`，多头方向 +1，空头 −1。代码里 `Side.sign()` 就是这个方向（BUY=+1，SELL=−1）。

**平仓时用哪个开仓价？——FIFO 与平均成本**

你分两次买入：10 股@100、10 股@110。然后卖 15 股@120。已实现盈亏是多少？

```text
FIFO（先进先出）：先平先买的。10×(120−100) + 5×(120−110) = 200 + 50 = 250        ← 本题用这个
平均成本：平均开仓价 = (1000+1100)/20 = 105，15×(120−105) = 225                   （剩下 5 股的成本仍按 105）
```

两种都是合法的会计方法，只是结果不同。**面试时要主动问"用哪种、舍入怎么处理"**。FIFO 的好处是全程整数，没有除法和舍入；平均成本要做除法，`2100/20` 恰好整除，但 `2101/20` 不整除，就得决定舍入规则。

**翻转（flip）**：你多头 10 股，一笔卖出 25 股。前 10 股是**平仓**（实现盈亏），剩下 15 股是**开空头**——一笔成交里发生两件事。这是仓位类题最经典的 bug 来源。

**Java 里怎么写**：见 §5.2。

### 2.2 订单的生命周期：有限状态机

**是什么**：有限状态机（finite state machine，FSM）= 一组**状态** + 一组**事件** + 一张"在状态 S 收到事件 E 变成状态 S'"的表。表里没有的格子就是**非法**。

**为什么需要它**：如果不显式写这张表，状态就散落在一堆 `if` 里。后果举例：

* 订单已经 `FILLED`，又收到一个 `Fill`（也许是重复投递，也许是 bug）——你的代码悄悄把已成交数量加了第二遍，仓位翻倍。
* 订单已经 `CANCELED`，却又被成交。

有了状态机，每一种"不可能的事"都有一个明确的、会被测试抓到的结果。

**怎么工作**：本题的状态转移（实际的 FIX 协议状态更多，这里是教学版）：

```text
          Ack              Fill(部分)             Fill(吃满)
 PENDING ─────▶ WORKING ──────────────▶ PARTIALLY_FILLED ───────▶ FILLED
    │              │  │                       │  ▲   └─Fill(部分)─┘
    │              │  └──────────Fill(吃满)───┼──┼─────────────────▶ FILLED
    │              │                          │
    │              └─Cancel──▶ CANCELED ◀─Cancel┘
    └─Reject──▶ REJECTED
```

终态：`FILLED`、`CANCELED`、`REJECTED`——到了终态就不会再变。

**Java 里怎么写**：状态用 `enum`；事件用 `sealed interface` + `record`（§6）；转移用 `switch` 表达式（编译器检查你处理了每一种事件）。

### 2.3 整数算术与溢出：为什么不用 `double` 表示钱

**是什么**：计算机用二进制表示小数，`0.1` 在二进制里是无限循环小数，`double` 只能存近似值。

```java
System.out.println(0.1 + 0.2);        // 0.30000000000000004
System.out.println(0.1 + 0.2 == 0.3); // false
```

**为什么需要整数**：一天有几十万笔成交，每笔都带一点误差，加起来仓位和盈亏就对不上；更要命的是**重放**——不同的运算顺序得到不同的 `double`，两次运行的结果不逐位相等，事件溯源的核心保证就破了。整数加减乘是精确的、满足结合律。

**怎么工作：溢出**。`long` 的范围是 ±9.22×10¹⁸。`px × qty` 如果超过它，Java **默默回绕成负数**（不会报错）：

```java
long big = Long.MAX_VALUE;
System.out.println(big + 1);                    // -9223372036854775808，回绕了
System.out.println(Math.addExact(big, 1));      // 抛 ArithmeticException，看得见的失败
```

风控里这特别危险：一张名义金额溢出成负数的订单，会"小于上限"而被放行。所以用 `Math.multiplyExact` / `addExact`，溢出抛异常（在风控里把溢出当作"拒绝"）。参见 `study/10-java21/J15_math_string_utils.md`。

### 2.4 交易前风控（pre-trade risk check）

**是什么**：订单发出去之前必须通过的一组规则。出了交易所，错单就是真金白银；所以公司在自己系统里先拦。

**为什么需要它**：几个著名的事故都是缺少或绕过了这类检查（例如 2012 年 Knight Capital 的软件事故，45 分钟亏损约 4.4 亿美元——这是公开报道的量级，具体细节以 SEC 报告为准）。监管上，美国 SEC 的市场准入规则（Rule 15c3-5）要求设置预交易风控，（通识，细节以法规为准）。

**怎么工作：本题的七条规则**（按声明顺序检查，报告第一条违反的）：

| 规则 | 防什么 | 例子（限额：数量 1000，名义 100 万，仓位 5000，未完成 3 张，价格带 5%） |
|---|---|---|
| `HALTED` 熔断 | 出事了，全部停 | 熔断开关（kill switch）打开 → 一律拒绝 |
| `NO_REFERENCE_PRICE` | 没有参考价就没法判断价格是否离谱 | **fail closed**：拿不准就拒绝，不是放行 |
| `QTY_LIMIT` | 多打了几个 0 的数量 | 买 100,000 股 |
| `NOTIONAL_LIMIT` | 数量 × 价格太大 | 买 1,000 股 × 150,000 |
| `PRICE_BAND` | **胖手指**：150 打成 15 或 1500 | 参考价 100，买入限价 200 |
| `OPEN_ORDERS_LIMIT` | 失控的程序狂下单 | 已有 3 张未完成订单，再下一张 |
| `POSITION_LIMIT` | 持仓超过公司允许 | 见下 |

**最坏情况仓位**是最容易想漏的一条：你现在净持仓 2,500，但还挂着 2,000 股的买单没成交。这些买单随时可能成交，所以你的真实风险是 4,500，不是 2,500。检查一张新买单（比如 500 股）要看 `2500 + 2000 + 500 = 5000 ≤ 5000`？通过；501 股？拒绝。

**为什么检查顺序重要**：当一张订单同时违反多条，报告哪一条？如果不固定顺序（比如遍历 `HashMap` 的规则），两次运行报告的原因可能不同——重放就不一致了。所以顺序固定。

**价格带为什么用整数交叉相乘**：「偏离不超过 5%」用小数写是 `|px − ref| / ref ≤ 0.05`，涉及除法和浮点。整数写法：`|px − ref| × 10_000 ≤ ref × 500`（5% = 500 个基点，1 基点 = 0.01%）。两边都是整数，没有舍入，边界（恰好 5.00%）精确通过。

### 2.5 事件溯源（event sourcing）与决定性

**是什么**：不直接保存"当前状态"，而是保存**所有改变状态的事件**（输入）；当前状态 = 对事件序列做一遍归约（fold）。

```text
状态₀ ──事件₁──▶ 状态₁ ──事件₂──▶ 状态₂ ── … ──▶ 状态ₙ        状态ₙ = f(f(f(状态₀, e₁), e₂), … eₙ)
```

**为什么需要它**：

* **崩溃恢复**：内存里的状态丢了？读事件日志，重放，状态原样回来。
* **复盘**：线上出了问题，把当天的事件喂给调试版本，一步步看。
* **回测**：同一份代码，喂历史行情，就是回测——研究和生产用同一份逻辑。
* **主备一致**：备机重放同一份日志，状态和主机一样。

**怎么工作：决定性**。上面的一切成立的前提是 `f` 是**决定性的**：同样的输入，永远同样的输出。以下东西会破坏它：

| 破坏者 | 例子 | 本题的办法 |
|---|---|---|
| 读时钟 | `System.currentTimeMillis()` | 状态机里不读时钟（时间戳作为事件的字段） |
| 遍历顺序 | 遍历 `HashMap` 决定先处理谁 | 输出前排序（`open()` 按 id 排序），检查顺序写死 |
| 浮点 | 运算顺序不同结果不同 | 全整数 |
| 随机数 | 无种子的 `Random` | 不用 |
| 多线程竞态 | 两个线程的交错顺序每次不同 | 单线程使用（单写者），线程交错的顺序要记进日志 |

**"先记日志，后处理"（journal before process）**：每个输入事件先追加到日志，再去改内存状态。这样内存里任何一个状态改变，都有日志里的一条事件对应。反过来先改状态再记日志，崩在中间就丢了一条事件。（参见 trellis 卡片 `problems-stock-exchange-journal-before-match-replay-recovery` 对撮合引擎的讲解；本题的 `TradingDesk` 是它的缩小版。注意区分：交易所自己必须先落盘再处理；我们作为交易所的客户，订单的真相在交易所，所以日志主要用于重建和复盘，见 sd03。）

**异常输入怎么办**：一个非法输入（比如对不存在的订单发 `Ack`）——它已经在日志里了（因为先记日志），处理时抛异常，**状态没有改变**。重放时这个输入又会抛同样的异常——重放必须像第一次一样**吞掉**它，否则一个坏输入会让整个恢复失败。这依赖于"先验证、后修改"：抛异常的路径不改任何状态。

### 2.6 Java 21 语法前置（只列链接）

* `record`（含紧凑构造器）：[J01](../10-java21/J01_record.md)；`sealed`：[J02](../10-java21/J02_sealed.md)；模式匹配 `switch`：[J03](../10-java21/J03_pattern_switch.md)；record 模式：[J04](../10-java21/J04_record_patterns.md)；`switch` 表达式 + `yield`：[J05](../10-java21/J05_switch_expressions.md)。

---

## 3. 从最笨的解法开始

大多数人第一反应是这样写（刻意写得"天真"）：

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

**它在哪些输入上错 / 慢**（每一条都对应一个隐藏测试）：

| 输入 | 暴露的问题 |
|---|---|
| 同一个 `Fill` 投递两次 | 仓位翻倍；`filled` 超过 `qty` |
| `CANCELED` 的订单又收到 `Fill` | 悄悄把状态改回 `PARTIAL`——幽灵订单 |
| `side = "buy"`（小写）/ 拼错的状态字符串 | `equals` 不匹配，被当成卖单；编译器不会提醒 |
| 数量 0.1 + 0.2 | `double` 误差：`filled >= qty` 偏差一个极小量，订单永远不到 `FILLED` |
| 多头 10 股，卖 25 股 | `position.merge` 只会得到 −15，**但**盈亏没有算：既没有"平仓 10 股的实现盈亏"，也没有"新空头的成本" |
| 风控：已有挂单 | 只看 `position`，不看未成交的挂单——最坏情况仓位漏了 |
| 风控检查时订单 `o` 已经被登记 | 把自己算进未完成数量，顶格订单被误拒 |
| 订单数很多 | 如果风控每次扫描所有订单求未完成数量，每次 O(n)，n 个订单总共 O(n²) |
| 重启 | 状态全丢，没有恢复手段 |

---

## 4. 一步一步改进

### 步骤 1：用类型表达"不可能"

**问题**：字符串状态、`double` 数量、`side = "buy"`。
**想法**：让非法值**无法构造**。
**为什么有效**：编译器 / 构造器帮你拦，而不是靠每个方法记得检查。
**代码变化**：

```java
public enum Side { BUY, SELL }                                  // 不是字符串
public record Order(long id, String symbol, Side side, long qty, long px) {
    public Order {                                              // 紧凑构造器：非法订单造不出来
        if (qty <= 0) throw new IllegalArgumentException(...);
        ...
    }
}
```

价格和数量改成 `long`。**新复杂度**：无变化，但消除了一整类 bug。

### 步骤 2：显式状态机，非法转移抛异常且不改状态

**问题**：幽灵订单、重复 Ack。
**想法**：转移表写成代码；`switch` 对事件类型穷尽匹配；每个分支先验证（`require(...)`）、后修改。
**为什么有效**：「先验证后修改」保证异常路径没有副作用——这是之后 `replay` 能成立的前提。
**代码**：`OrderManager.apply`（§5.1）。

### 步骤 3：Fill 去重要放在状态检查之前

**问题**：交易所/网关的回报是 **at-least-once**（至少一次）投递：同一笔成交可能到两次。
**想法**：每笔成交有全局唯一的 `execId`，记在 `Set` 里；见过的直接返回 `false`。
**为什么放在状态检查之前**：订单已 `FILLED` 后，旧回报重放过来——如果先检查状态，它会被当作"终态后又来 Fill"的**非法转移**而抛异常；但它其实只是一条重复消息，应该安静地忽略。
**一个细节**：只有**验证通过之后**才把 `execId` 记进 `Set`。超量成交的 `Fill` 被拒绝了，它的 `execId` 就不能算"已处理"——否则之后用合法数量重发会被当成重复而吞掉（测试 `overfillRejectedAndNotRecorded`）。

### 步骤 4：风控要的聚合量，增量维护

**问题**：风控每个订单都要问"这个标的未完成的买单总量"和"一共几张未完成订单"。扫描所有订单是 O(n)。
**想法**：把这两个量作为状态的一部分，在**每次状态变化**时同步更新：
`submit` +qty；`Fill` −成交量；`Cancel`/`Reject` −剩余量；到达终态时 `openCount--`。
**为什么有效**：查询变成 O(1) 的 map 查找。代价：**所有会改变订单的地方都要记得更新**——漏一处聚合量就漂移。所以测试里有一个随机事件流的对照测试（每隔一阵用"逐单重算"校验聚合量，`randomEventsKeepAggregatesConsistent`）。
**新复杂度**：每次事件 O(1)；风控查询 O(1)。

### 步骤 5：仓位用 FIFO lot 队列

**问题**：平仓用哪个成本？翻转怎么处理？
**想法**：每个标的维护一队**未平仓 lot**（数量，价格），同一时刻所有 lot 方向相同。新成交：
* 同向（或 flat）→ 追加 lot；
* 反向 → 从队首起平仓，每平一段实现 `方向 × (成交价 − lot价) × 数量`；平完还有剩余 → 剩余部分**以成交价作为新方向的第一个 lot**（翻转）。

**为什么有效**：全是整数加减乘；翻转不是特例，只是"平完队列后还有剩余"的自然结果。
**新复杂度**：每个 lot 最多被入队一次、出队一次；`onFill` 摊还 O(1)（一次成交可能平掉多个 lot，但每个 lot 只会被完全消耗一次）。

### 步骤 6：风控用整数交叉相乘，溢出视为拒绝

见 §2.4。`PRICE_BAND` 和 `NOTIONAL_LIMIT` 都用 `multiplyExact`，`catch ArithmeticException` 当作拒绝。

### 步骤 7：最坏情况仓位

见 §2.4。`net + 未完成买单剩余 (+本单)`、`net − 未完成卖单剩余 (+本单)` 与 ±`maxPosition` 比较。

### 步骤 8：装配成 `TradingDesk`，输入先记日志

**问题**：怎么证明状态可恢复？
**想法**：定义 `DeskEvent`（`Submit`、`SetReferencePrice`、`Halt`、`Resume` 以及 `ExecEvent`）作为**全部输入**；每个变更方法先 `journal.add(event)`，再 `handle(event)`；`replay` 对新 desk 重复 `handle`。
**为什么有效**：输出（风控结论、被拒订单、仓位）全部是输入的函数，不在日志里；重放时会重新算出来——如果两次不相等，就是有非决定性的东西混进来了（测试 `replayEqualsOriginalOnRandomEventStreams`：25 个随机种子 × 600 步）。

### 步骤 9：重放吞掉同样的异常

**问题**：日志里有第一次就抛了异常的输入（重复 id、非法转移、未知订单）。
**想法**：`replay` 里 `try { handle(e) } catch (...) {}`——第一次执行时状态没有变化，重放时也不会变化，吞掉是对的。
**注意**：只能吞**预期的**业务异常（`IllegalArgumentException`、`IllegalStateException`、`NoSuchElementException`、`ArithmeticException`）；其他异常（比如 `NullPointerException`、`OutOfMemoryError`）说明有 bug，应该让它崩。

---

## 5. 逐段讲参考解

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

* 紧凑构造器没有参数列表，直接在里面写校验；字段赋值由编译器在末尾自动补上。`requireNonNull` 抛 NPE，其余抛 `IllegalArgumentException`。换成普通类要写 getter / `equals` / `hashCode` / `toString`，还容易漏掉校验。

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

* `sealed ... permits`：只有这四个实现。`OrderManager.apply` 里的 `switch` 因此是**穷尽**的——以后新增一种回报，不改 `switch` 就编译不过。
* `ExecEvent extends DeskEvent`：回报也是 desk 的输入事件，所以放进同一个 sealed 层级（`DeskEvent` 的 `permits` 里列出 `ExecEvent`）。

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

逐行解释：

* `State s = orders.get(...)`；未知订单抛 `NoSuchElementException`——**在任何修改之前**。
* `return switch (event) { case ExecEvent.Ack a -> {...; yield true;} ... }`：`switch` 是表达式，每个分支用 `yield` 产出值；没有 fall-through。
* `Fill` 分支的顺序很讲究：①去重（`seenExecIds`）→ ②状态是否允许 → ③是否超量 → ④是否越过限价 → ⑤算新的累计成交额（`multiplyExact`/`addExact` 可能抛）→ **全部通过之后**才 ⑥ 记 `execId`、改 `cumQty`、改聚合量、改状态。前五步只读不写，所以任何一步失败，状态都没动。
* `reduceOpen(s, f.qty())`：同步减少该标的该方向的未完成剩余。`Cancel` 时一次性减掉剩余全部（`s.leaves()`）。
* `openCount--` 只在到达终态时：`FILLED`（`Fill` 分支）、`CANCELED`、`REJECTED`。

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

* `b.dir`：+1 多头 / −1 空头 / 0 平。`s = side.sign()`。
* 同向或 flat：追加一个 `Lot`，设定方向，返回。
* 反向：**先只读地**遍历队列，算出这笔成交的实现盈亏 `pnl`（`(long) b.dir * (px - lot.px) * c`，用 `multiplyExact`/`addExact`）；溢出会在这里抛，此时什么都没改。
* 提交：再遍历一次真正消耗 lot；`remaining > 0` 表示翻转，追加新方向的 lot。
* 为什么算两遍：为了"溢出不留半个状态"。如果边算边改，第三个 lot 溢出时前两个 lot 已经被消耗掉了。代价是常数倍的遍历；一次成交涉及的 lot 数通常很少。

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

* 每一行 `return reject(...)` 的顺序就是 `RiskReason` 的声明顺序。
* 价格带：`Math.abs(o.px() - ref) * 10_000` 与 `ref * limits.priceBandBps()` 比较，两边都是 `multiplyExact`。
* `try { ... } catch (ArithmeticException overflow) { return reject(NOTIONAL_LIMIT); }`：名义金额或价格带的乘法溢出，一律拒绝。
* 最坏情况仓位：`orders.openLeaves(...)` 是 O(1)（§4 步骤 4），`positions.netQty` 遍历该标的的 lot（通常很短；若成为瓶颈，可以在 `Book` 里缓存 `netQty`）。
* `check` 不改任何状态：这让风控可以在"登记订单之前"调用，也让它可以单独测试。

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

* `handle` 是**唯一**修改状态的地方，`submit/onExec/...` 只是"先记日志、再调 handle"的薄包装；`replay` 也调同一个 `handle`——所以实时路径和恢复路径用的是同一份代码，不可能出现"重放逻辑和实时逻辑悄悄分叉"。
* `case DeskEvent.SetReferencePrice(var symbol, var px) -> ...`：record 模式把字段直接解构出来（J04）。
* `handleSubmit`：先检查重复 id；再 `risk.check`（**在登记之前**）；再登记；被拒则立即应用一条 `Reject`——这条内部 `Reject` 不进 journal（它是**输出**，重放时会由同样的风控重新产生）。
* `handleExec`：`orders.apply` 返回 `true`（不是重复）并且是 `Fill` 才更新仓位。`x instanceof ExecEvent.Fill(var orderId, var ignoredExecId, var qty, var px)` 是 record 模式的 `instanceof` 形式。

### 5.5 本机实测

`study/30-articles/examples/ld02/DeskBench.java`（JIT 预热后取 5 次中位数）：

```text
live  : 400,000 events in 17.7 ms (median of 5) => 22.63 M events/s, 44 ns/event
replay: 400,000 events in 17.1 ms (median of 5) => 23.43 M events/s, 43 ns/event
PositionBook.onFill: 3,000,000 fills in 103.3 ms => 29.03 M fills/s（含 "S"+i 字符串拼接的分配）
```

怎么读这些数字：

* 这是**吞吐的量级**，不是延迟指标：测的是平均值，不含 GC 停顿的尾部；reference 为清晰用了 `HashMap<Long, …>`、装箱、record 分配，没有为零分配优化。
* 想要在 sd03 那样的 µs 级热路径上用，需要：`long → int` 原语哈希表、预分配的订单槽位、不为每个事件创建 record。见 `loop/rounds/04_sd/sd03_low_latency_trading_system/model_answer.md` §5.2、§12。
* 重放速度与实时速度几乎一样——因为它们是同一份 `handle`；重放比实时快的部分只在于不用等输入。

---

## 6. Java 21 特性小课

| 特性 | 旧写法（Java 8 风格） | 新写法（本题） | 编译器多做了什么 / 什么时候别用 |
|---|---|---|---|
| **`record` + 紧凑构造器**（[J01](../10-java21/J01_record.md)） | 15 行：私有 final 字段、构造器、getter、`equals`、`hashCode`、`toString` | `record Order(long id, String symbol, ...) { Order { 校验 } }` | 编译器生成全部样板，字段不可变。不要用在需要继承或可变的地方。`record` 的 `equals` 对 `byte[]` 字段是引用比较——本题没有数组字段 |
| **`sealed interface ... permits`**（[J02](../10-java21/J02_sealed.md)） | `interface ExecEvent {}` + 约定「只有这四个实现」 | `sealed interface ExecEvent permits Ack, Fill, Cancel, Reject` | 编译器知道所有子类型，`switch` 才能检查穷尽。不要用在需要外部扩展的 SPI 上 |
| **`switch` 模式匹配**（[J03](../10-java21/J03_pattern_switch.md)） | `if (e instanceof Ack) {...} else if (e instanceof Fill) {...}` 加强制转换，漏一个分支运行时才发现 | `switch (event) { case ExecEvent.Ack a -> ...; case ExecEvent.Fill f -> ...; ... }` | 对 sealed 类型不需要 `default`；少写一个 `case` 编译报错。若加了 `default`，反而会掩盖「新增事件类型忘了处理」 |
| **record 模式**（[J04](../10-java21/J04_record_patterns.md)） | `if (e instanceof Fill) { Fill f = (Fill) e; long q = f.qty(); ... }` | `x instanceof ExecEvent.Fill(var orderId, var execId, var qty, var px)`；`case DeskEvent.SetReferencePrice(var symbol, var px) -> ...` | 解构嵌套的 record；record 模式里不能写常量，要用 `when` 守卫 |
| **`switch` 表达式 + `yield`**（[J05](../10-java21/J05_switch_expressions.md)） | 先声明 `boolean result;` 再在每个 `case` 里赋值，别忘了 `break` | `return switch (event) { case ... -> { ...; yield true; } }` | 没有 fall-through；每个分支必须产出值，漏了编译报错 |
| **`Math.multiplyExact` / `addExact`**（[J15](../10-java21/J15_math_string_utils.md)） | `long r = a * b;`（溢出默默回绕）或手写 `if (a != 0 && r / a != b)` | `Math.multiplyExact(px, qty)` 溢出抛 `ArithmeticException` | 比手写检查短；热路径上有少量开销（JIT 会做内联成溢出标志检查）。「用异常表示拒绝」要像本题一样，在不应改变状态的地方捕获 |
| **`Stream.toList()`**（[J14](../10-java21/J14_stream_api.md)） | `.collect(Collectors.toList())`（可变，类型不保证） | `.sorted(...).toList()`（不可变） | 返回不可修改的列表；若要 `null` 元素也允许 |
| **`List.copyOf`** | `Collections.unmodifiableList(new ArrayList<>(x))` | `List.copyOf(journal)` | 防御性拷贝，返回不可变；元素不能为 `null` |
| **`var`**（[J08](../10-java21/J08_var.md)） | `RiskResult r = ...` / `DeskEvent.Halt e = new DeskEvent.Halt();` | `var e = new DeskEvent.Halt();` | 只在右边已写出类型时使用 |

---

## 7. 追问预演

### Q1：新增一条风控规则（比如「单标的每秒最多 N 笔」），要改哪里？

**思考**：设计的扩展点在哪？现在是 `check` 里一串 `if`。
**答案要点**：reference 为了清晰和可审计用顺序 `if`（检查顺序 = 枚举声明顺序）。扩展有两条路：①直接加一个 `RiskReason` + 一个 `if`（编译器通过 `switch` 穷尽性提醒处理新原因的地方）；②重构为 `List<RiskCheck>`（责任链），每条规则实现 `Optional<RiskReason> check(ctx)`，按固定顺序执行。后者利于测试和组合，代价是多一层间接和虚调用——**热路径**上我会保持前者（内联、可预测）。速率限制需要时间：**时间必须作为事件进来**（`Tick` 事件），不能在检查里读时钟，否则破坏决定性。
**可以说**：「新规则要加在枚举里固定的位置；时间依赖的规则，时间要作为输入事件传进来。」

### Q2：多个线程同时提交订单怎么办？

**答案要点**：这个设计是**单写者**：一个线程拥有 `TradingDesk`，其他线程把命令放进队列（MPSC 队列）。加锁的问题：①锁竞争和上下文切换进入延迟；②多线程交错的顺序每次不同，破坏决定性——除非把"实际处理顺序"记进日志。所以：并行靠**按标的分片**（每个分片一个 desk），而不是一个 desk 里加锁。参见 sd03 §4、`ld01`。
**可以说**：「并发的答案是把可变状态收归一个线程，别把它变成共享的。」

### Q3：市价单怎么支持？

**答案要点**：`px` 没有了。风控的价格带无法检查，要改成：用参考价（或对手方最优价）加保护价（marketable limit）来近似；名义金额用保护价估算；`Fill` 的限价约束改为保护价。很多交易所不支持裸市价单，系统常把市价单转成带保护价的限价单——所以"市价单"在系统内部是一种限价单。
**可以说**：「我会把市价单转成带保护价的限价单，这样风控规则不用特判。」

### Q4：撤单请求和撤单确认的区别？

**答案要点**：现实中先有"撤单请求"（我们发出），再有"撤单确认"（交易所回）。中间状态 `PENDING_CANCEL`：此时订单仍可能被成交（请求和成交在途中交叉）。本题的 `Cancel` 只表示**确认**。如果加 `PENDING_CANCEL`：`WORKING/PARTIALLY_FILLED --请求--> PENDING_CANCEL`，`PENDING_CANCEL --Fill--> 仍可成交`，`--确认--> CANCELED`，`--撤单拒绝--> 回到原状态`。风控的最坏情况仓位在 `PENDING_CANCEL` 期间**仍然要计入**该订单的剩余数量。
**可以说**：「撤单是个竞态，不是一个瞬间；在确认之前，订单仍然是风险。」

### Q5：为什么 `PENDING` 订单也算未完成？

**答案要点**：已经发出去，交易所可能已经成交，只是回报还没到。风控按"最坏情况"算，把它当作可能随时成交。若不算，会出现「连续快速下多张单，每张都通过检查，合起来超限」。
**可以说**：「回报是滞后的，风险不是。」

### Q6：为什么 FIFO，换成平均成本要改什么？

**答案要点**：平均成本需要 `openCost / netQty`，不整除，要定义舍入（四舍五入 / 向零 / 向下）；每次平仓用平均价，剩余数量保留平均价不变。实现更简单（不用队列，只存 `netQty` 和 `costBasis`）但要选舍入并解释累积误差——可以把成本存成「总成本」（整数），平仓时按比例 `costBasis × closeQty / netQty` 取整，把余数留在 `costBasis`，使总和保持精确（"最大余数法"的变体）。FIFO 的好处是全整数无舍入。
**可以说**：「选哪种是业务/会计的决定；我会先问，再说明各自的舍入影响。」

### Q7：怎么把状态持久化，重启后恢复？

**答案要点**：落地 journal（追加写文件）；定期快照（把当前状态序列化，记下日志位置）；恢复 = 读快照 + 重放其后的日志。快照必须与日志位置原子对应。日志格式：定长头 + 二进制载荷、校验和、按大小切段。注意恢复后要对账交易所（订单真相在交易所），见 sd03 §8。
**可以说**：「快照加日志尾，恢复时间由日志尾的长度决定，所以快照要定期。」

### Q8：重放结果与线上不一致，怎么排查？

**答案要点**：二分日志：重放前 k 条，比较状态摘要（哈希）与线上同一位置的摘要，找到第一个分叉的事件；常见原因：读了时钟 / 随机数 / `HashMap` 遍历顺序 / 浮点 / 外部可变状态 / 线程。预防：线上周期性记录状态摘要进日志；发布前用生产日志做重放回归。
**可以说**：「决定性要用测试守护，不是靠自觉。」

### Q9：性能：每秒 100 万个事件，这个实现够吗？

**答案要点**：本机实测约 2,200 万事件/s（平均，JIT 预热后），平均吞吐够；但 µs 级尾延迟不够：每个事件分配 record、`HashMap<Long,…>` 装箱、`ArrayList` 增长都会产生垃圾，导致 GC 停顿。改进：原语哈希表（`long→int`）、订单槽位预分配 + 空闲链表、journal 用预分配的环/mmap 而不是 `ArrayList<DeskEvent>`、事件用 flyweight 视图。
**可以说**：「吞吐够，尾延迟要看分配；先测量再优化。」

### Q10：`record` 的 `equals` 让两个 desk 的状态可以直接比较，这有什么风险？

**答案要点**：record 的 `equals` 逐字段比较，对嵌套 record 递归，OK；但包含 `double`（NaN）或数组会有陷阱；`OrderView` 里是 `long`/`String`/枚举，安全。测试里 `assertEquals(a.allOrders(), b.allOrders())` 就依赖它。若字段是可变集合，比较的是当时内容。
**可以说**：「record 相等是结构相等；要留意含数组和浮点的字段。」

---

## 8. 常见误区

1. **先登记订单再做风控检查**。→ 错：订单把自己算进「未完成数量」，恰好顶格的订单被误拒。→ 正确：`check` 在 `submit` 之前（测试 `orderDoesNotCountItselfAgainstPositionLimit`）。
2. **重复回报按状态检查**。→ 订单已 `FILLED` 后的旧回报被当作非法转移抛异常，或更糟——被当成新的成交把仓位翻倍。→ 正确：去重在状态检查之前（测试 `duplicateFillIsIdempotent`）。
3. **边验证边修改**。→ 超量成交先把 `cumQty` 加了再发现超量，抛异常时状态已被破坏；`execId` 先记进了 Set，之后合法重发被吞。→ 正确：所有检查在修改之前（测试 `overfillRejectedAndNotRecorded`）。
4. **用 `double` 或 `int`**。→ `int` 的 `qty × px` 在 21 亿就溢出；`double` 累加有误差。→ `long` + `multiplyExact`（测试 `notionalOverflowIsRejectedNotWrapped`）。
5. **翻转时只改方向、不算盈亏**。→ 多头 10 股，卖 25 股：要先平 10 股实现盈亏，再以成交价开 15 股空头（测试 `flipThroughZeroOpensOppositeLotAtFillPrice`）。
6. **风控只看净仓，不看挂单**。→ 净仓 2,500 + 挂单买 2,000，再买 501，看起来 3,001 没超，其实最坏 5,001（测试 `positionLimitCountsOpenOrdersWorstCase`）。
7. **价格带用除法 / 浮点**。→ 边界（恰好 5%）因舍入被误拒或误放；参考价小（3）时「5% = 0.15」整除出 0（测试 `priceBandUsesIntegerArithmeticNoRounding`）。
8. **缺参考价就放行**。→ 无法判断就放行，是 fail open；正确是拒绝（测试 `missingReferencePriceFailsClosed`）。
9. **replay 里不吞异常**。→ 第一次抛过异常的输入，重放时同样抛，导致恢复失败（测试 `replaySwallowsInputsThatFailedTheFirstTime`）。
10. **`journal()` 返回内部 list**。→ 调用方可以篡改日志；正确：`List.copyOf`（测试 `journalIsAnImmutableCopyInInputOrder`）。

---

## 9. 自测题

**Q1（概念）**：为什么重放要求状态机是"决定性的"？列出至少三种破坏决定性的东西，以及本题对其中每一种的对策。

<details><summary>答案</summary>

重放的意义是「同样的输入得到同样的状态」；如果状态机不决定性，重放得到的状态与崩溃前不同，恢复、复盘、回测都失去意义。破坏者：读时钟（时间作为事件字段）、`HashMap` 遍历顺序（输出前排序，检查顺序写死）、浮点运算顺序（全整数）、无种子随机数（不用）、多线程交错（单线程使用，顺序记进日志）。
</details>

**Q2（计算）**：10 股@100、20 股@110 依次买入，然后卖出 25 股@120。FIFO 下已实现盈亏是多少？剩余仓位的 `openCost` 是多少？再买 5 股@90 之后呢？

<details><summary>答案</summary>

先平 10@100：10×(120−100)=200；再平 15@110：15×(120−110)=150；已实现 350。剩余 5 股@110，`openCost` = 550，`netQty` = 5。再买 5 股@90：同向，追加 lot，netQty = 10，openCost = 550 + 450 = 1000，已实现仍是 350。
</details>

**Q3（翻转）**：多头 10 股（均为 @100），卖 25 股@110。结果的 `netQty`、`openCost`、`realizedPnl`？

<details><summary>答案</summary>

平 10 股：10×(110−100)=100。剩余 15 股作为空头 lot @110：`netQty = −15`，`openCost = 15×110 = 1650`，`realizedPnl = 100`。
</details>

**Q4（风控）**：限额：maxPosition = 5000。净仓 2,500，挂单买 1,000 + 1,000（未成交）。再买 500 股，通过吗？买 501 呢？卖 4,000 呢（假设数量限额放得下）？

<details><summary>答案</summary>

买 500：2500 + 2000 + 500 = 5000 ≤ 5000，通过；买 501：5001，拒绝（`POSITION_LIMIT`）。卖 4,000：`net − 未完成卖 − 本单` = 2500 − 0 − 4000 = −1500 ≥ −5000，通过；同时买方向的暴露 `net + 买挂单` = 4500 ≤ 5000 也不变，通过。
</details>

**Q5（小编程）**：在 `OrderManager` 里新增 `PENDING_CANCEL`，请写出需要改的三处。

<details><summary>答案</summary>

①`OrderStatus` 加枚举值，`isOpen()` 仍为 true；②新增事件 `CancelRequest(orderId)`（sealed 层级里加 record，`apply` 的 `switch` 编译器会逼你处理）：`WORKING/PARTIALLY_FILLED → PENDING_CANCEL`；③`Fill` 在 `PENDING_CANCEL` 状态下仍允许；`Cancel`（确认）从 `PENDING_CANCEL → CANCELED`；`CancelReject` 回到原状态（需要记住原状态）。风控的未完成剩余量不能在请求时就减掉，要等确认。
</details>

---

## 10. 延伸阅读

* FIX 协议规范（FIX Trading Community）的 *Order State Change Matrices*——真实世界的订单状态机，比本题的教学版多 `PENDING_CANCEL`、`PENDING_REPLACE`、`SUSPENDED` 等状态。
* Martin Fowler, 「Event Sourcing」（martinfowler.com）——事件溯源的定义与权衡。
* Martin Fowler, 「The LMAX Architecture」（2011）——单线程业务逻辑 + 事件日志 + 重放的工业实例。
* JEP 395（records）、JEP 409（sealed classes）、JEP 441（switch 模式匹配）、JEP 440（record 模式）——本题用到的语言特性的权威说明。
* `java.lang.Math` Javadoc 中的 `multiplyExact` / `addExact`——溢出检测。
* SEC Rule 15c3-5（市场准入规则）——预交易风险控制的法规背景。
* DDIA（Kleppmann）第 11 章「流处理」中关于事件日志与状态派生的部分。
* 本 kit：`loop/rounds/04_sd/sd03_low_latency_trading_system/model_answer.md`（把本题放进完整交易系统）、`study/30-articles/hc05_market_order_book.md`（交易所一侧的订单簿）、`study/30-articles/ld01_spsc_channel.md`（单写者通道）。
