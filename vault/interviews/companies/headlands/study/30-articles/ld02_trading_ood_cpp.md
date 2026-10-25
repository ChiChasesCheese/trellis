# ld02 · 交易相关的 OOD：订单状态机、仓位盈亏、交易前风控、事件溯源（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

交易员（或策略程序）**下单**：「买 100 股 AAPL，最高出 150」。订单发给交易所后陆续收到**回报**（execution report）：先是「收到了」（Ack），然后「成交 60 股，价格 149」（Fill），再「又成交 40 股，价格 150」。程序要回答四个问题：订单现在是什么状态、还能成交多少（订单状态机）；持有多少股、赚了多少（仓位与盈亏）；一张新订单能不能发——价格是不是打错了、仓位会不会超过公司上限（交易前风控，pre-trade risk check）；程序崩了怎么恢复成一模一样的状态（所有变化都来自一串输入事件，重放即可，叫事件溯源，event sourcing）。

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `OrderManager` | 订单状态机 `PENDING → WORKING → PARTIALLY_FILLED → FILLED`，`CANCELED`，`REJECTED`；回报去重；聚合量增量维护 | 非法转移不改状态；重复回报幂等；超量成交；成交价越过限价 |
| 2 | `PositionBook`、`Position` | 按标的维护仓位，FIFO 配对，已实现 / 未实现盈亏，**翻转** | 平仓加开反向仓在一笔成交里完成；全整数；溢出不留半个状态 |
| 3 | `RiskEngine`、`RiskLimits`、`RiskResult`、`RiskReason` | 数量 / 名义金额 / 价格带 / 未完成订单数 / **最坏情况仓位**，熔断开关 | 检查顺序即确定性；整数价格带；fail closed；有符号溢出是 UB |
| 4 | `TradingDesk` | 把 1–3 装配起来；输入先进 journal 再处理；`replay` | 决定性；异常输入也进 journal；重放时吞掉同样的异常 |

共同约定：

* **价格是整数 tick，数量是整数股数**（`long long`）。没有浮点，所以盈亏逐位可验证。名义金额 `px * qty` 溢出时**抛异常**，不静默回绕。
* `Order(id, symbol, side, qty, px)` 是限价单；构造函数保证 `id > 0`、`qty > 0`、`px > 0`、`symbol` 不是空白，否则 `std::invalid_argument`。
* 输出确定：列表按 id 升序 / 符号字典序。
* **先验证、后修改**：任何抛异常的路径都不能改变状态（Part 4 的重放依赖这一点）。
* 单线程使用，不加锁。

```
TradingDesk desk(RiskLimits(1'000, 10'000'000, 3'000, 50, 1'000));
desk.set_reference_price("A", 100);
desk.submit(Order(1, "A", Side::Buy, 100, 100));      // accepted
desk.on_exec(Ack(1));
desk.on_exec(Fill(1, 10, 60, 99));                    // true；position("A").net_qty == 60
desk.submit(Order(2, "A", Side::Buy, 5'000, 100));    // rejected(QtyLimit)；order(2).status == Rejected
auto copy = TradingDesk::replay(limits, desk.journal());   // 状态与 desk 逐项相等
```

## 2. C++ 怎么建模：类型表达不变量

这类 OOD 题的评分点是**建模的质量**：让不可能的状态无法存在，让漏掉一种情况变成编译错误。Java 用 `record` + `sealed interface` + 穷尽 `switch`；C++20 对应：

| 想表达的 | C++ 写法 |
|---|---|
| 一个值类型，有不变量（`qty > 0`） | `class` + 私有数据 + 校验的构造函数 + `friend bool operator==(...) = default;` |
| 一个值类型，没有不变量 | `struct` + 公有字段（`OrderView`、`Position`），默认 `operator==` |
| 一组固定的状态 | `enum class OrderStatus { Pending, Working, ... }`（不会隐式转成 `int`） |
| 一组封闭的事件类型 | `std::variant<Ack, Fill, Cancel, Reject>` |
| 「对每种事件分别处理，漏一种就编译不过」 | `std::visit(Overloaded{[&](const Ack&){...}, [&](const Fill&){...}, ...}, event)` |
| 「通过」或「带原因拒绝」 | `RiskResult`：内部是 `std::optional<RiskReason>`（`nullopt` = 通过） |
| 没有 `null` | 值语义：函数拿到的就是一个 `Order`，不会是空引用；Java 的 `NullPointerException` 测试在这里不存在 |

```cpp
class Order {
public:
    Order(long long id, std::string symbol, Side side, long long qty, long long px)
        : id_(id), symbol_(std::move(symbol)), side_(side), qty_(qty), px_(px) {
        if (id <= 0) throw std::invalid_argument("id must be > 0");
        // ... symbol 空白、qty <= 0、px <= 0 同理
    }
    long long id() const { return id_; }  // ... 其余只读访问器
    friend bool operator==(const Order&, const Order&) = default;
private:
    long long id_; std::string symbol_; Side side_; long long qty_, px_;
};
static_assert(!std::is_default_constructible_v<Order>);   // 没有「空订单」
```

没有默认构造函数、字段私有、只有一个入口：持有 `Order` 的任何代码都不必再检查 `qty > 0`。`friend ... = default` 的比较是 C++20 起的写法，可以访问私有成员；有了它，测试可以直接比较两个 desk 的全部订单。

事件的封闭集合与 `Overloaded`：

```cpp
using ExecEvent = std::variant<Ack, Fill, Cancel, Reject>;
template <class... Ts> struct Overloaded : Ts... { using Ts::operator()...; };

return std::visit(Overloaded{
    [&](const Ack&)    { ...; return true; },
    [&](const Fill& f) { ...; },
    [&](const Cancel&) { ...; },
    [&](const Reject& r) { ...; },
}, event);        // 少写任何一个 lambda：编译错误
```

Java 里 `ExecEvent extends DeskEvent`，一个 sealed 接口可以继承另一个。`std::variant` 不能继承另一个 variant，所以 `DeskEvent` 是**平铺**的八个选项（`Submit`、`SetReferencePrice`、`Halt`、`Resume` 加上四种回报），`to_desk_event(const ExecEvent&)` 做转换，下标正好差 4（`d.index() == e.index() + 4`）。

异常对应关系：

| Java | C++ |
|---|---|
| `IllegalArgumentException` | `std::invalid_argument` |
| `NoSuchElementException`（未知订单） | `std::out_of_range` |
| `IllegalTransitionException extends IllegalStateException` | `struct IllegalTransitionException : std::logic_error` |
| `ArithmeticException`（`multiplyExact` 溢出） | `std::overflow_error` |

### 2.1 有符号溢出是 UB：自己写 `mul_exact`

Java 的 `Math.multiplyExact` 溢出时抛 `ArithmeticException`，普通的 `*` 则静默回绕。C++ 里有符号整数溢出是**未定义行为**（undefined behaviour，UB）：编译器可以假设它不发生，结果不是「回绕」，而是任意。UBSan 开着时直接中止进程。所以每一处乘法 / 加法，只要输入可能很大，就必须先检查：

```cpp
inline long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error("long overflow");
    return r;
}
```

`__builtin_mul_overflow` / `__builtin_add_overflow` 是 GCC / Clang 的内建函数：算出结果并返回「是否溢出」，不产生 UB。（C++ 标准库目前没有现成的检查算术；C23 的 `ckd_add` 一类还没进 C++。）在风控里不用抛异常的版本，直接 `if (__builtin_mul_overflow(...)) return reject(...)`——溢出是一个**业务结论**，不是错误。

## 3. Part 1：`OrderManager`

### 3.1 状态转移表

| 当前状态 | `Ack` | `Fill` | `Cancel` | `Reject` |
|---|---|---|---|---|
| `Pending` | → `Working` | **非法** | **非法** | → `Rejected` |
| `Working` | **非法** | → `PartiallyFilled` 或 `Filled` | → `Canceled` | **非法** |
| `PartiallyFilled` | **非法** | → `PartiallyFilled` 或 `Filled` | → `Canceled`（已成交部分保留） | **非法** |
| 终态 | **非法** | **非法**（重复 Fill 例外） | **非法** | **非法** |

「非法」= 抛 `IllegalTransitionException`，**订单状态不变**。`Cancel` 是撤单**确认**，不是撤单请求（`Pending` 时收到 `Cancel` 非法，真实系统里这是个竞态，这里简化）。

### 3.2 `Fill` 的规则

1. **去重在状态检查之前**。回报可能重复投递（至少一次，at-least-once），靠全局唯一的 `exec_id` 去重。订单已经 `Filled` 之后旧回报再来一次，只是重复（返回 `false`），不是非法转移。
2. `qty > leaves`（超量成交）抛异常，并且这个 `exec_id` **不能**被记为已见过：之后用合法数量重发应当成功。
3. 成交价不得越过限价：买单 `px > 限价`、卖单 `px < 限价` 非法；等于限价、价格改善合法。
4. `cum_notional += qty * px` 溢出抛 `std::overflow_error`，订单状态不变。
5. `cum_qty == order.qty` ⇒ `Filled`，否则 `PartiallyFilled`。

做法：**先把所有检查做完，把可能抛异常的算术算出来，最后才修改**：

```cpp
[&](const Fill& f) {
    if (seen_exec_ids_.contains(f.exec_id())) return false;     // 重复：先于状态检查
    require(s.status == Working || s.status == PartiallyFilled, s, "Fill");
    if (f.qty() > s.leaves()) throw IllegalTransitionException("overfill ...");
    // ... 成交价越过限价 ⇒ 抛
    const long long new_cum = add_exact(s.cum_notional, mul_exact(f.qty(), f.px()));   // 可能抛：此时什么都没改
    seen_exec_ids_.insert(f.exec_id());                           // 全部通过之后才记录
    s.cum_qty += f.qty();   s.cum_notional = new_cum;   reduce_open(s, f.qty());
    // ... 状态 ⇒ Filled / PartiallyFilled，Filled 时 --open_count_
    return true;
}
```

这就是**强异常保证**（strong exception guarantee）：操作要么完全成功，要么抛异常且状态不变。做法永远是「先算后改」（copy-and-swap 是另一种）。

### 3.3 聚合量增量维护

风控每张订单都要问「这个标的这个方向还有多少未完成数量」「一共有多少未完成订单」。如果每次扫描所有订单，是 O(n)。所以 `open_count_` 和 `open_leaves_`（`symbol → {buy, sell}`）在每次状态变化时**增量**更新，查询 O(1)。`Pending` 也算未完成（已经发出去，可能随时成交）。`submit` 里 `open_leaves_` 的累加用 `add_exact`：两张数量接近 `LLONG_MAX/2` 的订单会让聚合量溢出，必须在登记订单**之前**抛 `std::overflow_error`，订单不留痕迹。

容器选择：订单用 `std::unordered_map<long long, State>`（查找 O(1)），`all()` 返回前按 id 排序——保证输出确定，不依赖哈希表的遍历顺序。

## 4. Part 2：`PositionBook`（FIFO）

每个标的维护一队**未平仓 lot**（`qty`, `px`），队内所有 lot 方向相同（`dir = +1` 多头 / `-1` 空头 / `0` 空仓）。

* 新成交与当前方向相同（或空仓）⇒ 追加一个 lot。
* 相反 ⇒ 从队首开始平仓，每平一段 `c` 手实现 `dir * (成交价 - lot价) * c`。
* 平完还有剩余 ⇒ **翻转**：剩余部分以成交价为新方向的第一个 lot。

```
on_fill(A, BUY, 10, 100)    lots: [10@100]
on_fill(A, BUY, 10, 110)    lots: [10@100, 10@110]      net 20, cost 2100
on_fill(A, SELL, 15, 120)   平 10@100 (+200)，平 5@110 (+50)   lots: [5@110]   realized 250
on_fill(A, SELL, 25, 130)   平 5@110 (+100)，剩 20 翻成空头   lots: [20@130]   net -20, cost 2600, realized 350
unrealized(120) = 2600 - 20*120 = 200
```

用 `std::deque<Lot>`：从队首删、从队尾加都是 O(1)。`openCost` = 各 lot 的 `qty * px` 之和（恒 ≥ 0）。

### 4.1 溢出不留半个状态

`dir * (px - lot.px) * c` 的乘积可能溢出。平仓是**多步**修改（改多个 lot、改 `realized`、可能翻转），如果算到一半抛异常，仓位就是半个状态。做法：**第一遍只读**：遍历 lot 算出总盈亏（溢出就抛，此时一个字节没改）；第二遍才真正修改，且第二遍里没有任何会抛的操作。

```cpp
long long remaining = qty, pnl = 0;
for (const Lot& lot : b.lots) {                          // 只读：溢出在这里抛，状态原样
    if (remaining == 0) break;
    const long long c = std::min(remaining, lot.qty);
    pnl = add_exact(pnl, mul_exact(b.dir * (px - lot.px), c));
    remaining -= c;
}
const long long new_realized = add_exact(b.realized, pnl);
// 提交：下面不会再抛
```

容器：`std::map<std::string, Book>`。符号数很少，`std::map` 的遍历自带字典序，`symbols()` 不需要再排序；代价是查找 O(log n)，对几十个标的无所谓。几千个标的的热路径应该换 `unordered_map` + 排序输出。

## 5. Part 3：`RiskEngine`

`check(order, positions, orders)` 是 `const` 方法：**只读，不改任何状态**——类型系统直接表达了这一点。检查顺序 = `RiskReason` 的声明顺序，报告**第一条**违反的（同时违反多条时结果确定，重放才会得到同一个原因）：

1. `Halted`：熔断中，拒绝一切（包括减仓单——kill switch 不挑单）。
2. `NoReferencePrice`：没设过参考价 ⇒ 拒绝。**fail closed**：无法判断价格带，就不放行。
3. `QtyLimit`：`qty > max_order_qty`（`==` 通过）。
4. `NotionalLimit`：`px * qty > max_order_notional`；乘积溢出也算 `NotionalLimit`（不能回绕成小数而通过）。
5. `PriceBand`：`|px - ref| / ref > bps / 10000` 则拒绝，**含等于通过**。用整数交叉相乘：`|px - ref| * 10'000 <= ref * bps`，不做除法，没有舍入。
6. `OpenOrdersLimit`：`orders.open_count() >= max_open_orders`（所有标的合计，`Pending` 也算；这一单本身尚未登记）。
7. `PositionLimit`：**最坏情况净仓**。

### 5.1 最坏情况仓位，以及它的溢出

假设该标的所有未完成买单（含本单若为买）都成交，或所有未完成卖单都成交：

```
net + buy_leaves  <= max_position
net - sell_leaves >= -max_position
```

只看当前净仓是不够的：净仓 2500，未完成买单 2000，再买 500 恰好顶格，501 就超了——而 `2500 + 501` 看起来完全没问题。

这里有三次加减法，限额可以设成 `LLONG_MAX`，未完成数量也可以接近 `LLONG_MAX`，所以**每一步都可能溢出**。Java 的 `long` 会回绕成一个巨大的负数，于是 `> maxPosition` 不成立，**被放行**。C++ 里这是 UB。正确的结论：任何一步放不进 `long long`，就是超限：

```cpp
long long buy_leaves, sell_leaves, high, low;
const bool overflow =
    __builtin_add_overflow(orders.open_leaves(sym, Side::Buy),  o.side() == Side::Buy  ? o.qty() : 0, &buy_leaves)  ||
    __builtin_add_overflow(orders.open_leaves(sym, Side::Sell), o.side() == Side::Sell ? o.qty() : 0, &sell_leaves) ||
    __builtin_add_overflow(positions.net_qty(sym), buy_leaves, &high) ||
    __builtin_sub_overflow(positions.net_qty(sym), sell_leaves, &low);
if (overflow || high > limits_.max_position() || low < -limits_.max_position()) return reject(RiskReason::PositionLimit);
```

`||` 短路求值：前一个溢出了，后面的不会再算（也不会读到没赋值的变量）。

## 6. Part 4：`TradingDesk`（事件溯源）

所有状态变化都来自 `DeskEvent`。每个变更方法按固定顺序做三件事：

1. 把输入**先追加到 journal**；
2. 调 `handle` 修改内存状态；
3. 返回结果。

`replay(limits, journal)` 对一个新 desk 重复第 2 步，必须得到逐位相同的状态——这就是崩溃恢复、复盘、回测共用的基础。因此 `handle` 必须是**决定性的**：不读时钟、不用随机数、不依赖哈希表遍历顺序。

```cpp
RiskResult submit(const Order& order) {
    journal_.emplace_back(Submit(order));        // (1) 先写日志，即使后面抛异常，输入也已经在里面
    return handle_submit(order);                 // (2)
}

RiskResult handle_submit(const Order& o) {
    if (orders_.contains(o.id())) throw std::invalid_argument("duplicate order id ...");
    const RiskResult r = risk_.check(o, positions_, orders_);   // 必须在登记之前：否则这张单把自己算进未完成数量
    orders_.submit(o);
    if (!r.is_accepted()) orders_.apply(Reject(o.id(), std::string(to_string(*r.reason()))));   // 内部 Reject 是输出，不进 journal
    return r;
}
```

* **被风控拒绝的单仍然登记**，状态 `Rejected`，`reject_reason` 是原因名（`"QTY_LIMIT"`）。这个内部 `Reject` 是**输出**不是输入，所以不进 journal；重放时 `Submit` 会再产生同样的拒绝。
* **风控检查在登记之前**：先登记再检查，单笔恰好顶格的订单会把自己算两遍而被误拒。
* `on_exec`：成功应用的 `Fill` 同步更新 `PositionBook`（用订单里的标的和方向，成交里的数量和价格）；重复 `Fill` 不更新仓位。

`handle` 是对 `DeskEvent` 的 `std::visit`，新增一种事件不写处理就编译不过。四种回报用一个带约束的泛型 lambda 统一处理：

```cpp
std::visit(Overloaded{
    [&](const Submit& s) { (void)handle_submit(s.order()); },
    [&](const SetReferencePrice& r) { risk_.set_reference_price(r.symbol(), r.px()); },
    [&](const Halt&)   { risk_.halt(); },
    [&](const Resume&) { risk_.resume(); },
    [&]<class E>(const E& x) requires std::is_constructible_v<ExecEvent, const E&> { (void)handle_exec(ExecEvent(x)); },
}, e);
```

### 6.1 重放只吞「自己的」异常

原来抛过异常的输入，重放时同样会抛——而且调用方第一次已经看到过，状态当时没有改变，所以重放时吞掉。**吞什么**很重要：

```cpp
try { d.handle(e); }
catch (const std::logic_error&) {}        // invalid_argument、out_of_range、IllegalTransitionException
catch (const std::overflow_error&) {}
```

不用 `catch (...)`：那会连 `std::bad_alloc` 或者你自己的 bug 抛出的别的东西一起吞掉，重放"成功"了，状态却是错的。

### 6.2 `journal()` 与值语义

* `journal()` 返回 `std::vector<DeskEvent>` **按值**：调用方拿到的是一份拷贝，之后 desk 的活动不会改变它，改它也不会影响 desk。Java 用 `List.copyOf` 得到不可变列表；C++ 的对应物是「拷贝」而不是「不可变」。
* 整个 `TradingDesk` 是纯值成员（`OrderManager`、`PositionBook`、`RiskEngine`、`vector`），所以**默认的拷贝构造就是一个完整、独立的快照**：`TradingDesk what_if = desk;` 之后随便在副本上试成交、熔断，原 desk 不受影响。Java 里要自己写深拷贝或者重放 journal。代价是拷贝 O(状态大小)。

## 7. 和 Java 版的差异（以及为什么）

| Java | C++ | 为什么 |
|---|---|---|
| `record` | `class` + 校验构造函数 + `friend operator== = default`；无不变量的用 `struct` | C++ 没有 record；构造函数是唯一入口 |
| `sealed interface` + 穷尽 `switch` | `std::variant` + `std::visit(Overloaded{...})` | 封闭集合 + 编译期穷尽检查 |
| `ExecEvent extends DeskEvent` | `DeskEvent` 平铺 8 个选项 + `to_desk_event` | variant 不能继承 variant |
| `Math.multiplyExact` | 自己写 `mul_exact`（`__builtin_mul_overflow`） | 标准库没有检查算术；有符号溢出是 UB |
| 普通 `long` 溢出回绕 | 溢出是 UB：风控、聚合量全要显式检查 | 回绕被「碰巧放行」的 bug，在 C++ 里是 UB |
| `null` / `NullPointerException` | 值语义，没有空引用；`std::optional` 表示「可能没有」 | 少了一整类错误和测试 |
| `String rejectReason`（可 `null`） | `std::optional<std::string>` | 同上 |
| `List.copyOf(journal)`（不可变） | 返回 `std::vector` 的拷贝 | C++ 用「所有权」而不是「不可变包装」 |
| desk 共享引用 | 值语义：拷贝是独立快照 | 默认拷贝就是深拷贝 |
| `HashMap` + 输出时排序 | `unordered_map` + 排序（订单），`std::map`（符号） | 同样要保证输出确定 |
| `catch (IllegalStateException \| ...)` | `catch (const std::logic_error&)` + `catch (const std::overflow_error&)` | 异常类型的继承关系决定怎么写最窄的捕获 |

## 8. 陷阱

1. **去重放在状态检查之后**：订单 `Filled` 后旧回报重放被当成非法转移（3.2）。
2. **超量成交的 `exec_id` 已经记录了**：之后合法数量的重发被当成重复（3.2）。
3. **先改后验**：溢出抛出时订单 / 仓位已经改了一半（3.2、4.1）。
4. **风控扫描所有订单**：O(n)，每张订单都要问一遍（3.3）。
5. **风控检查在登记之后**：订单把自己算两遍（6）。
6. **价格带用除法或浮点**：舍入误差，边界不稳定（5）。
7. **名义金额溢出回绕成小数而通过**；**最坏仓位的加法回绕**：在 C++ 里还是 UB（2.1、5.1）。
8. **`catch (...)` 吞一切**：重放"成功"但状态是错的（6.1）。
9. **journal 不先写**：处理中途抛异常，输入就丢了，重放与原状态不一致（6）。
10. **`handle` 里读时钟 / 用随机数 / 依赖哈希表遍历顺序**：重放不再逐位一致（6）。
11. **内部产生的 `Reject` 也写进 journal**：journal 里多出一条从来没有人输入过的事件，重放时它撞上已经是 `Rejected` 的订单，变成一次非法转移（6）。
12. **`journal()` 返回引用**：调用方持有的东西会随 desk 改变；返回拷贝（6.2）。

## 9. 面试官会追问什么（senior）

**Q1. 新增一条风控规则（如「单标的每秒最多 N 笔」），改哪里？** `RiskReason` 加一个枚举值（位置决定检查顺序），`check` 里加一段；这个规则需要时间——时间必须作为**输入事件**（一个 `Tick` 事件）进入 journal，而不是在 `check` 里读时钟，否则重放不再确定。更进一步把每条规则做成 `std::vector<std::unique_ptr<RiskCheck>>` 的责任链，代价是顺序依赖和虚调用。

**Q2. 多个线程同时提交订单？** 粗粒度加锁，或者**单写者 + 队列**：所有线程把事件放进一个队列，一个线程顺序处理——这与事件溯源天然契合，处理顺序就是 journal 顺序。

**Q3. 市价单怎么支持？** `Order` 的 `px` 变成 `std::optional<long long>`；风控的价格带、名义金额要用参考价估算；成交价检查跳过限价比较。

**Q4. 撤单请求与撤单确认的区别？** 请求发出后订单进入 `PendingCancel`：这期间可能还有成交（竞态）。状态机多一个状态，`Fill` 在 `PendingCancel` 里合法。

**Q5. 为什么 `Pending` 也算未完成？** 订单已经发出，回报还没回来，随时可能成交；风险上必须按「已经在市场里」处理。

**Q6. 为什么 FIFO？换成平均成本要改什么？** 平均成本用 `open_cost / net_qty`，要取整，盈亏出现舍入——要主动问「用哪种成本法、舍入规则是什么」。

**Q7. 怎么持久化，重启后恢复？** journal 写盘（追加写 + `fsync`），重启时 `replay`。journal 太长就定期做快照（snapshot）：保存状态 + 对应的 journal 位置，恢复时从快照开始重放后半段。C++ 里值语义让「快照」就是一次拷贝。

**Q8. 重放结果与线上不一致，怎么排查？** 先找非确定性的因素：时钟、随机数、哈希遍历顺序、浮点、未初始化变量（C++ 特有）、依赖多线程交错。二分 journal：重放前 k 条，比较状态，找到第一个分叉的事件。

**Q9. 每秒 100 万个事件，这个实现够吗？** 瓶颈是 `orders_.get(...)` 里拷贝 `OrderView`（含 `std::string`）和 `unordered_map` 的缓存不友好。优化：`std::string` 换成符号 id（整数）；订单放进预分配的 `vector`、用下标当 id；`handle_exec` 里直接拿内部状态引用，不拷贝 `OrderView`；`journal_` 预留容量。

**Q10. 默认的 `operator==` 比较两个 desk 的状态，有什么风险？** 它比较所有字段，包括不该参与「业务相等」的（比如时间戳、内部序号）；加字段后测试会悄悄变严格或变松。

## 10. 自测

1. `Pending` 状态的订单收到 `Fill`，抛什么？订单状态变了吗？
2. 订单 `Filled` 后，同一个 `exec_id` 的 `Fill` 又来一次，返回什么？
3. 为什么超量成交的 `exec_id` 不能被记为已见过？
4. 买入 10 手 @100，再买入 10 手 @110，卖出 15 手 @120，已实现盈亏是多少？剩余 lot 是什么？
5. `Position::unrealized_pnl` 对空头怎么算？
6. 参考价 10007，bps = 500。`px = 10507` 和 `10508` 的结果？为什么不用除法？
7. 净仓 2500，未完成买单 2000，`max_position = 5000`。再买 500 和 501 的结果？
8. `check` 为什么是 `const` 方法？
9. 为什么 `replay` 只捕获 `std::logic_error` 和 `std::overflow_error`？
10. 为什么被风控拒绝的订单内部的 `Reject` 不进 journal？
11. `__builtin_add_overflow` 相比 `a + b` 再检查结果是否变小，好在哪里？

<details><summary>答案</summary>

1. `IllegalTransitionException`；订单状态不变，`cum_qty` 不变。
2. `false`：去重在状态检查之前，旧回报重放只是重复，不是非法转移。
3. 超量成交被拒绝了，这笔成交实际上没有发生；如果记下 `exec_id`，之后同一个 id 用合法数量重发会被误认为重复而丢掉。
4. 先平 10@100：`10*(120-100) = 200`；再平 5@110：`5*(120-110) = 50`；合计 250。剩余 lot：`5@110`，`net_qty = 5`，`open_cost = 550`。
5. `open_cost - |net_qty| * mark`：空头价格跌了赚钱。
6. 5% × 10007 = 500.35：`|10507-10007| * 10000 = 5'000'000 <= 10007 * 500 = 5'003'500` 通过；`10508`：`5'010'000 > 5'003'500` 拒绝。用整数交叉相乘没有舍入，边界精确。
7. 500：`2500 + 2000 + 500 = 5000 <= 5000` 通过；501：`5001 > 5000` 拒绝（`PositionLimit`）。
8. 它只读取仓位、订单、参考价，不修改任何东西；`const` 让编译器强制这一点，也说明可以放心地对同一个状态反复检查。
9. 这两类就是 desk 的输入能引发的异常，调用方第一次已经看到过且状态没变；`catch (...)` 会连 `std::bad_alloc` 和真正的 bug 一起吞掉。
10. 它是 `Submit` 处理的**输出**：重放时再次处理 `Submit` 会再次产生同样的拒绝；如果也写进 journal，journal 里就多出一条没有人输入过的事件，重放时它撞上已经是 `Rejected` 的订单，成为非法转移。
11. 有符号整数溢出本身是 UB，事后检查「结果是否变小」时编译器可以认为溢出不会发生，把检查优化掉；内建函数返回是否溢出，不产生 UB。

</details>

## 延伸阅读

* [std::variant](https://en.cppreference.com/w/cpp/utility/variant) 与 [std::visit](https://en.cppreference.com/w/cpp/utility/variant/visit)：封闭类型集合与穷尽访问
* [Builtin overflow checking](https://clang.llvm.org/docs/LanguageExtensions.html#checked-arithmetic-builtins)：`__builtin_*_overflow`
* [Exception safety](https://en.cppreference.com/w/cpp/language/exceptions#Exception_safety)：基本保证与强保证
* Martin Fowler, Event Sourcing：<https://martinfowler.com/eaaDev/EventSourcing.html>
