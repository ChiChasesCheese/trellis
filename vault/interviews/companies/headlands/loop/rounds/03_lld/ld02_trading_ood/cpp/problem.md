# ld02 · 交易相关的 OOD（C++20 版）

交易系统里最基础的三个对象：**订单**（一个有生命周期的东西，发出去、被确认、部分成交、全部成交、被撤销、被拒绝，非法转移必须被拒绝）、**仓位与盈亏**（成交改变仓位，平仓时实现盈亏，从多头直接卖到空头的「翻转」是经典陷阱）、**交易前风控**（订单发出去之前要过一组规则，拿不准就拒绝）。第四个 Part 把它们装配成一个事件溯源（event sourcing）的 `TradingDesk`：所有状态变化都来自一串输入事件，把这串事件重放一遍，必须得到逐项相同的状态。C++ 版的看点是怎么用类型表达不变量（带校验构造函数的类、`std::variant` 加 `std::visit`），以及**有符号溢出是 UB**，所以每一处可能很大的乘法和加法都要先检查。签名都在 `starter.hpp`（命名空间 `trading`）。

## 读题前你需要知道

- **事件溯源**：状态不直接修改，只由一串事件按顺序推导出来；因此重放同一串事件必定得到同一状态。要做到这点，处理事件的函数必须是决定性的：不读时钟、不用随机数、不依赖哈希表的遍历顺序。
- **`std::variant` 与 `std::visit`**：`variant` 是封闭的「几选一」类型。`std::visit(Overloaded{lambda1, lambda2, ...}, v)` 对每个选项各写一个 lambda，少写一个就编译不过，对应「对封闭的事件集合做穷尽处理」。`Overloaded` 已在 starter 里给出。
- **整数价格与数量**：价格是整数 tick，数量是整数股数，没有浮点，所以 PnL 逐位可验证。名义金额 = `px * qty`，可能溢出，用 starter 里的 `mul_exact / add_exact / sub_exact`（溢出抛 `std::overflow_error`）；在风控里溢出是一个业务结论，直接用 `__builtin_mul_overflow` 返回拒绝。
- **异常对应**：非法参数 `std::invalid_argument`；未知订单 `std::out_of_range`；非法状态转移 `IllegalTransitionException`（`std::logic_error` 的子类）；算术溢出 `std::overflow_error`。

## 公共类型（starter 已给出）

```cpp
enum class Side { Buy, Sell };                       // sign(Side) = +1 / -1，opposite(Side)
enum class OrderStatus { Pending, Working, PartiallyFilled, Filled, Canceled, Rejected };

class Order {                                        // 限价单；构造函数保证 id>0、qty>0、px>0、symbol 非空白，否则 invalid_argument
public:
    Order(long long id, std::string symbol, Side side, long long qty, long long px);
    // id() symbol() side() qty() px()，operator== 默认
};
struct OrderView { Order order; OrderStatus status; long long cum_qty, cum_notional;
                   std::optional<std::string> reject_reason;
                   long long leaves_qty() const; };   // 撤销 / 拒绝为 0；FILLED 因 cum_qty == qty 也是 0

// 事件：每种一个小类，各有 order_id() 等访问器
class Ack;  class Fill;  class Cancel;  class Reject;          // Fill(order_id, exec_id, qty, px)；Reject(order_id, reason)
using ExecEvent = std::variant<Ack, Fill, Cancel, Reject>;
class Submit;  class SetReferencePrice;  struct Halt;  struct Resume;
using DeskEvent = std::variant<Submit, SetReferencePrice, Halt, Resume, Ack, Fill, Cancel, Reject>;   // desk 的全部输入

class RiskLimits { RiskLimits(long long max_order_qty, long long max_order_notional, long long max_position,
                              int max_open_orders, long long price_band_bps); /* 任何一个 <= 0 抛 invalid_argument */ };
enum class RiskReason { Halted, NoReferencePrice, QtyLimit, NotionalLimit, PriceBand, OpenOrdersLimit, PositionLimit };
class RiskResult { static accepted(); static rejected(RiskReason); bool is_accepted() const;
                   std::optional<RiskReason> reason() const; };

struct Position { std::string symbol; long long net_qty, open_cost, realized_pnl;
                  static Position flat(std::string); long long unrealized_pnl(long long mark_px) const; };
```

另有 `to_string(RiskReason)`（返回 `"QTY_LIMIT"` 这样的名字）、`to_desk_event(const ExecEvent&)`、`order_id_of(const ExecEvent&)`。`DeskEvent` 是**平铺**的 8 个选项（`variant` 不能继承另一个 `variant`），四种回报在两个 `variant` 里下标差 4。

## 共同约定

- 输出确定：所有列表按订单 id 升序、符号字典序。
- **先验证、后修改**：任何抛异常的路径都不能改变状态（Part 4 的重放依赖这一点）。
- 单线程使用，不要加锁。

## Part 1 · `OrderManager`（订单状态机）

| 签名 | 要求 |
|---|---|
| `void submit(const Order&)` | 登记，状态 `Pending`；重复 id 抛 `std::invalid_argument` |
| `bool apply(const ExecEvent&)` | `true` = 已应用；`false` = 重复的 `Fill`（`exec_id` 见过） |
| `bool contains(long long) const`、`OrderView get(long long) const` | 未知订单 `get` / `apply` 抛 `std::out_of_range` |
| `std::vector<OrderView> open() const`、`all() const` | 未终结订单 / 全部订单，按 id 升序 |
| `int open_count() const` | O(1) |
| `long long open_leaves(const std::string&, Side) const` | 该标的该方向所有未终结订单的剩余数量之和，O(1)，`Pending` 也计入 |

状态转移表（「非法」= 抛 `IllegalTransitionException`，订单状态不变）：

| 当前状态 | `Ack` | `Fill` | `Cancel` | `Reject` |
|---|---|---|---|---|
| `Pending` | → `Working` | 非法 | 非法 | → `Rejected` |
| `Working` | 非法 | → `PartiallyFilled` 或 `Filled` | → `Canceled` | 非法 |
| `PartiallyFilled` | 非法 | → `PartiallyFilled` 或 `Filled` | → `Canceled`（已成交部分保留） | 非法 |
| `Filled` / `Canceled` / `Rejected` | 非法 | 非法（重复 `Fill` 例外） | 非法 | 非法 |

- **去重在状态检查之前**：`exec_id` 见过 ⟹ 返回 `false`，无任何效果，即使订单已经 `Filled`。
- 超量成交（`qty > leaves`）抛 `IllegalTransitionException`，且这个 `exec_id` 不能被记为已见过：之后用合法数量重发应当成功。例：限量 10，已成交 6，`Fill(exec 2, qty 5)` 抛异常，`cum_qty` 仍是 6；再发 `Fill(exec 2, qty 4)` 返回 `true`，订单变 `Filled`。
- 成交价不得越过限价：买单 `px > 限价` 非法，卖单 `px < 限价` 非法；等于限价、价格改善合法。限价 100 的买单：成交价 101 抛异常，100 和 90 通过。
- 累计成交额 `cum_notional += qty * px`，溢出抛 `std::overflow_error`，且订单状态和 `exec_id` 都不变。例：限量 `LLONG_MAX/2`、限价 `LLONG_MAX/2` 的买单，一笔 `LLONG_MAX/2 @ LLONG_MAX/2` 的成交抛 `std::overflow_error`，`cum_qty` 仍是 0；之后 `Fill(exec 1, qty 1, px 1)` 成功。
- 例：限量 100 的买单，`Ack` 后成交 30 @ 149：`PartiallyFilled`，`cum_qty = 30`，`cum_notional = 30 * 149`，`leaves_qty() = 70`；再成交 70 @ 150 → `Filled`，`cum_notional = 30 * 149 + 70 * 150`。
- 撤销部分成交的订单：`cum_qty` 保留，`leaves_qty()` 为 0，`open_leaves` 释放剩余。`Reject` 的原因字符串存进 `reject_reason`。
- 随机 4000 个事件（300 张订单）下，O(1) 聚合量和逐单重算的结果始终一致；非法事件不改任何东西。
- C++ 专属测试：
  - `Order` 没有默认构造函数；`ExecEvent` 有 4 个选项，`DeskEvent` 有 8 个（`static_assert`）。
  - 聚合量也要防溢出：`submit(买 LLONG_MAX/2+1 @ 1)` 两次，第二次抛 `std::overflow_error`，订单没有登记（`contains` 为 `false`，`open_count()` 仍是 1）；同一标的的卖方向是另一个桶，不受影响。
  - `get` 返回的 `OrderView` 是快照：之后订单变化不会影响已取出的副本，改副本也不会影响 manager。

## Part 2 · `PositionBook`（仓位与盈亏）

| 签名 | 要求 |
|---|---|
| `void on_fill(const std::string&, Side, long long qty, long long px)` | `qty <= 0` 或 `px <= 0` 抛 `std::invalid_argument`，且不能因此创建这个符号 |
| `Position get(const std::string&) const` | 没出现过 → `Position::flat(symbol)` |
| `long long net_qty(const std::string&) const`、`total_realized() const` | |
| `std::vector<std::string> symbols() const` | 字典序 |
| `long long Position::unrealized_pnl(long long mark_px) const` | 多头 `net_qty * mark - open_cost`；空头 `open_cost - |net_qty| * mark`；flat 为 0；溢出抛 `std::overflow_error` |

FIFO 配对：每个标的维护一队同方向的未平仓 lot（qty, px）。

- 新成交与当前方向相同（或当前 flat）⟹ 追加一个 lot。
- 相反 ⟹ 从队首开始平仓，每平 `c` 手实现 `方向 * (成交价 - lot价) * c`；平完还有剩余 ⟹ **翻转**：剩余部分以成交价作为新方向的第一个 lot。
- `open_cost` = 未平仓 lot 的 `qty * px` 之和（恒 ≥ 0）；`net_qty` = 方向 × 未平仓手数之和。
- 全程整数。**溢出抛 `std::overflow_error`，仓位保持原样**：先只读地算出盈亏，再一次性提交。
- 例：买 10@100，买 10@110（`net_qty = 20`，`open_cost = 2100`），卖 15@120 ⟹ 先平 10@100（+200），再平 5@110（+50），得 `Position{"A", 5, 550, 250}`。再卖 25@130 ⟹ 平 5@110（+100），翻成空头 20 手 @130，得 `Position{"A", -20, 2600, 350}`；`unrealized_pnl(120) = 2600 - 20 * 120 = 200`。
- 空头：卖 10@100，买 4@90 实现 `4 * 10 = 40`；再买 6@130 实现 `6 * (100 - 130)`，`net_qty = 0`。
- 买 7@10 再卖 7@10 恰好平完：`net_qty = 0`，`realized_pnl = 0`；之后从 flat 开任一方向都可以。
- 多头买 10@100、买 10@120：`unrealized_pnl(130) = 20 * 130 - 2200`；空头卖 5@200：`unrealized_pnl(190) = 1000 - 5 * 190`。
- 溢出例：买 `1'000'000'000 @ 1` 之后，`unrealized_pnl(LLONG_MAX / 2)` 抛 `std::overflow_error`。另一例：持有多头后，用 `qty = 3'000'000'000`、`px = LLONG_MAX / 2` 的卖单平仓，`(px - lot价) * qty` 溢出，抛异常，`get` 返回的仓位和之前相等。
- 随机 2000 笔成交（数量 1 到 8，价格 90 到 110）与「把每笔成交拆成单手、逐手 FIFO 配对」的模型逐笔对照，`net_qty`、`realized_pnl`、`open_cost` 都一致。
- 30 万笔成交、50 个标的在 2 秒内完成（`perf` 标签，无 sanitizer 的 `-O2` 构建）。

## Part 3 · `RiskEngine`（交易前风控）

| 签名 | 要求 |
|---|---|
| `explicit RiskEngine(RiskLimits)` | |
| `void set_reference_price(const std::string&, long long px)` | `px <= 0` 抛 `std::invalid_argument` |
| `void halt()`、`resume()`、`bool halted() const` | 熔断开关 |
| `RiskResult check(const Order&, const PositionBook&, const OrderManager&) const` | 只读，不改任何状态 |

**检查顺序 = `RiskReason` 的声明顺序**，报告第一条违反的（同时违反多条时结果必须确定）：

1. `Halted`：熔断中，拒绝一切，包括减仓单。
2. `NoReferencePrice`：该标的没设过参考价 ⟹ 拒绝（fail closed）。
3. `QtyLimit`：`qty > max_order_qty`（`==` 通过）。
4. `NotionalLimit`：`px * qty > max_order_notional`（`==` 通过）；`px * qty` 溢出 ⟹ 也算 `NotionalLimit`，不能回绕成小数而通过。
5. `PriceBand`：`|px - ref| * 10'000 <= ref * price_band_bps` 才通过（整数交叉相乘，等于通过，没有除法和舍入）。
6. `OpenOrdersLimit`：`orders.open_count() >= max_open_orders`（所有标的合计，`Pending` 也算，这一单本身尚未登记）。
7. `PositionLimit`：**最坏情况净仓**：`net + 未完成买单剩余(+本单若为买) <= max_position`，且 `net - 未完成卖单剩余(+本单若为卖) >= -max_position`。

例（`RiskLimits(1'000, 1'000'000, 5'000, 3, 500)`，标的 A 的参考价 100，即 5% 的价格带）：

- 买 10 @105 通过（+5.00% 恰好等于带宽）；买 @106 → `PriceBand`；卖 @94 → `PriceBand`；卖 10 @1（少打一个零）→ `PriceBand`。
- 标的 `ZZZ` 没有参考价 → `NoReferencePrice`。
- 数量 1000 通过，1001 → `QtyLimit`。
- 价格带用整数运算：参考价 10007 时，买价 10507 通过、10508 拒绝；参考价 3 时，只有买价 3 通过，4 拒绝。
- 已有净仓 4500：买 500 通过（恰好 5000），买 501 → `PositionLimit`；卖 1000 通过。
- 未完成买单 2 张各 1000，净仓 2500：再买 500 通过（2500 + 2000 + 500 = 5000），买 501 → `PositionLimit`（只看净仓 2500 + 501 会误放行）。其中一张完全成交，风险敞口总量不变，结论不变；撤掉另一张之后买 1000 通过。
- 空头一侧对称：净仓 -2500、未完成卖单 2000，再卖 500 通过（-5000），再卖 1 → `PositionLimit`；买单不增加空头敞口。
- 风控限额按标的分别算：A 的净仓 5000 不影响 B 的买单。
- 同时违反多条：数量、名义金额、价格带都超 → `QtyLimit`；名义金额和价格带超 → `NotionalLimit`；熔断 + 无参考价 → `Halted`。
- 未完成订单数限额 3：登记 3 张（含 `Pending` 和另一个标的的）后，新单 → `OpenOrdersLimit`；其中一张被拒绝（进入终态）释放名额后通过。
- `check` 调用 10 次，manager 里的订单和 `open_count()` 都不变。
- C++ 专属测试：
  - 最坏情况仓位的加法不能溢出：限额都是 `LLONG_MAX`，已有一张 `LLONG_MAX` 的未完成买单，再来 `1` 手的买单 → `PositionLimit`（Java 会回绕成巨大的负数而放行，C++ 里是 UB）；卖方向同理。
  - `RiskResult` 是值：`accepted()` 没有 reason，`rejected(QtyLimit)` 的 `reason()` 等于 `QtyLimit`，两者 `!=`；`to_string(RiskReason::OpenOrdersLimit)` 是 `"OPEN_ORDERS_LIMIT"`。

## Part 4 · `TradingDesk`（事件溯源 + 重放）

| 签名 | 要求 |
|---|---|
| `explicit TradingDesk(RiskLimits)` | |
| `RiskResult submit(const Order&)` | 重复 id 抛 `std::invalid_argument` |
| `bool on_exec(const ExecEvent&)` | `false` = 重复 `Fill`；非法 → `IllegalTransitionException` / `std::out_of_range` |
| `void set_reference_price(const std::string&, long long)`、`halt()`、`resume()` | |
| `OrderView order(long long) const`、`all_orders() const` | |
| `Position position(const std::string&) const`、`symbols() const` | |
| `std::vector<DeskEvent> journal() const` | 按值返回，输入顺序 |
| `static TradingDesk replay(const RiskLimits&, const std::vector<DeskEvent>&)` | |

- **每个变更方法先把输入追加到 journal，再处理**：即使处理会抛异常，输入也已经在 journal 里。
- `submit`：重复 id 抛异常（状态不变）；先 `risk.check`（在登记**之前**，否则这张单把自己算进未完成数量）；通过 ⟹ `orders.submit`；被拒 ⟹ 仍然 `orders.submit`，然后立刻应用 `Reject(id, 原因名)`，所以 `order(id)` 是 `Rejected`，`reject_reason` 是 `"QTY_LIMIT"` 这样的名字。**这个内部 `Reject` 不进 journal**（它是输出，不是输入）。
- `on_exec`：成功应用的 `Fill` 同步更新 `PositionBook`（用订单里的标的和方向，成交里的数量和价格）；重复 `Fill` 不更新仓位。
- `replay`：新建 desk，按顺序处理 journal 里的每个输入；原来抛过异常的输入，重放时同样会抛，同样被吞掉（只捕获 `std::logic_error` 和 `std::overflow_error`，不要 `catch (...)`）。结果的 `all_orders()`、`position(s)`、`journal()` 必须与原 desk 逐项相等。
- 例（`RiskLimits(1'000, 10'000'000, 3'000, 50, 1'000)`，A 参考价 100，B 参考价 50）：
  - 提交买 100 @100 → 通过；`Ack`；`Fill(1, exec 10, 60, 99)` 返回 `true`，`position("A").net_qty == 60`，`open_cost == 60 * 99`；再成交 40 @100 → 订单 `Filled`，净仓 100。再卖 100 @101 并以 105 全部成交，`net_qty = 0`，`realized_pnl = 60 * (105 - 99) + 40 * (105 - 100)`。
  - 买 2000 @100 → `Rejected(QtyLimit)`，`order(1).status == Rejected`，`reject_reason == "QTY_LIMIT"`，不占用未完成名额：之后可以提交 3 张各 1000 的买单（总敞口 3000 恰好顶格），再买 1 → `PositionLimit`。
  - 单笔恰好顶格的订单不能被误拒：连续两张买 1000 @100 都通过（不把自己算两遍）。
  - `halt()` 之后 `submit` → `Halted`，`resume()` 之后通过。
  - 同一个 `Fill`（同一个 `exec_id`）收到两次：第二次返回 `false`，净仓只算一次（30，不是 60）。
- 非法事件：订单还在 `Pending` 时 `Fill` 抛 `IllegalTransitionException`；`Ack(99)`（未知订单）抛 `std::out_of_range`；仓位和订单状态都不变，但两条输入都在 journal 里。
- `journal()` 的内容和顺序：先 `set_reference_price("A", 100)`、`set_reference_price("B", 50)`，再提交买 10 @100 并 `Ack(1)`，得到 `[SetReferencePrice A, SetReferencePrice B, Submit, Ack]`，共 4 条。取出的副本之后不受 desk 变化影响，往副本里追加也不影响 desk。
- 重放等价：25 个随机种子、每个 600 步（含重复 `exec_id`、非法事件、熔断），`replay` 之后的订单、符号、仓位都与原 desk 相等；重放得到的 desk 还能继续工作。
- 5 万张订单、每张 4 个事件（共 20 万个事件）加一次重放在 3 秒内完成（`perf` 标签）。
- C++ 专属测试：
  - `TradingDesk what_if = desk;` 是完整、独立的快照：在副本上成交、熔断，原 desk 的仓位、订单状态、journal 长度都不受影响。
  - `IllegalTransitionException`、`std::out_of_range`、`std::invalid_argument` 都是 `std::logic_error` 的子类，而 `std::overflow_error` 不是；`mul_exact(LLONG_MAX, 2)`、`add_exact(LLONG_MAX, 1)`、`sub_exact(LLONG_MIN, 1)` 都抛 `std::overflow_error`。
  - `to_desk_event` 对四种回报都成立：`DeskEvent` 的下标等于 `ExecEvent` 的下标加 4。

## 边界清单

- 状态机：表里每个「非法」格；终态之后的任何事件；重复 `Ack`；`Pending` 收到 `Fill` / `Cancel`；`Working` 收到 `Reject`
- 回报：重复 `exec_id`（含订单 `Filled` 之后）；超量成交后同一 `exec_id` 以合法数量重发；买单成交价 = 限价 / 高 1；卖单对称
- 聚合量：`Pending` 计入；`Cancel` / `Reject` / 全部成交后释放；多标的互不影响；随机事件流下和逐单重算一致
- 溢出：`qty * px` 在 `LLONG_MAX/2` 附近；PnL 乘积溢出后仓位原样；风控名义金额溢出不放行；最坏情况仓位的加法溢出不放行
- 仓位：同向加仓；部分平；恰好平完；翻转；flat 之后反向开仓；空头；多标的
- 风控：每条规则的 `==` 和 `+1`；价格带 `ref` 很小或不整除；未知标的；同时违反多条；`check` 不改状态；`halt` 拒绝减仓单；空头一侧对称
- desk：风控拒绝的单仍登记为 `Rejected`；非法事件抛出但仍在 journal；重放等于原状态；journal 返回拷贝

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/03_lld/ld02_trading_ood                 # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/03_lld/ld02_trading_ood --tag part1
python3 tools/cpptest.py run   loop/rounds/03_lld/ld02_trading_ood --tag cpp       # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/03_lld/ld02_trading_ood                 # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB（比如有符号溢出）就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 订单簿加撮合：把交易所一侧也建模（见 hc05）。
- 平均成本法代替 FIFO：`open_cost / net_qty` 要取整，PnL 出现舍入；先问清楚用哪种成本法、怎么舍入。
- 撤单请求与确认分开（多一个 `PendingCancel` 状态）：这期间还可能有成交。
- 市价单：转成带保护价的限价单，风控规则不需要特殊处理。
- 多线程提交订单：单写者加队列，处理顺序就是 journal 顺序。
