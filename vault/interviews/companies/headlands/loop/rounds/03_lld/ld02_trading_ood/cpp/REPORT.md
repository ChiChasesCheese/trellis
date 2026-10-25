# ld02 · 思路与追问（C++20 版）

这是一道建模题，评分点不是算法，而是你怎么用类型表达不变量、怎么让非法操作不留下半个状态、怎么让结果可以重放。下面按 Part 写清三件事：怎么写、面试官在探什么（所有权、不变量、为什么这样排顺序）、该说出口的那句话。C++ 版额外的重点是有符号溢出是 UB。完整的推导和可运行的示例在讲义 [[ld02_trading_ood_cpp]]。

## 30 秒版本

- **类型表达不变量**：`Order` 只有一个带校验的构造函数、没有默认构造函数；事件是 `std::variant`，处理用 `std::visit(Overloaded{...})`，漏一种事件编译不过。
- **先验证、后修改**：所有检查和可能溢出的计算都在改状态之前做完；`exec_id` 在所有检查通过之后才记录；这样任何异常路径都不留下半个状态。
- **去重在状态检查之前**：订单已经 `Filled` 之后收到的旧回报只是重复消息，返回 `false`，不是非法转移。
- **聚合量增量维护**：`open_count`、`open_leaves` 在每次状态变化时更新，风控每张订单都要问，不能扫描。
- **风控**：检查顺序 = 枚举声明顺序；无参考价就拒绝（fail closed）；价格带用整数交叉相乘；最坏情况仓位含未完成订单；任何一步放不进 `long long` 都算超限。
- **事件溯源**：先写 journal 再处理，`handle` 是决定性的，`replay` 走同一份 `handle`；风控检查在登记之前；内部产生的 `Reject` 是输出，不进 journal。

## Part 1 · `OrderManager`

**写法**

```cpp
[&](const Fill& f) {
    if (seen_exec_ids_.contains(f.exec_id())) return false;           // 1 去重：先于状态检查
    require(s.status == Working || s.status == PartiallyFilled, ...);  // 2 状态
    if (f.qty() > s.leaves()) throw IllegalTransitionException(...);  // 3 超量
    /* 4 价格是否越过限价 */
    const long long new_notional = add_exact(s.cum_notional, mul_exact(f.qty(), f.px()));  // 5 可能溢出，仍未改任何东西
    seen_exec_ids_.insert(f.exec_id());                               // 6 全部通过之后才记录
    s.cum_qty += f.qty();  s.cum_notional = new_notional;  reduce_open(s, f.qty());
    /* 状态转到 Filled 或 PartiallyFilled，Filled 时 --open_count_ */
    return true;
}
```

`apply` 是对 `ExecEvent` 的 `std::visit(Overloaded{...})`，四个 lambda 都返回 `bool`。聚合量是 `open_count_` 加上 `symbol → {买剩余, 卖剩余}` 的 map，每个状态变化处同步更新。

**面试官在探什么**

1. **为什么这个检查顺序**。去重在最前：同一份回报交付两次是常态，第二次不该报错。接着是状态、超量、价格、溢出，最后才改。顺序保证「抛异常 ⟹ 什么都没变」；`exec_id` 放在最后记录，是因为超量被拒的成交之后用合法数量重发应该成功，提前记录会把它当成重复吞掉。
2. **状态机显式化**。转移表写出来，非法的一律抛 `IllegalTransitionException` 且不改状态；`Cancel` 是撤单**确认**，`Pending` 收到它非法。
3. **聚合量为什么增量维护**。风控对每张订单都要问 `open_count` 和 `open_leaves`，扫描所有订单是 O(n)，吞吐会随订单数下降。代价是每个终态路径（成交完、撤销、拒绝）都要记得更新，漏一处就错：所以用「随机事件流 + 逐单重算」对照测试。
4. **聚合量也会溢出**。`submit` 里用 `add_exact` 先算出新的剩余量，再登记订单。放在登记之后，溢出抛出时订单已经进了 map，`open_count` 却没加。
5. **所有权与快照**。`OrderManager` 独占内部的订单状态；`get` 返回的 `OrderView` 是拷贝（含一个 `std::string`），调用方拿着它，之后订单怎么变都不受影响，改它也碰不到 manager。代价是每次 `get` 拷贝一次，热路径要避免。
6. **`PENDING` 为什么算未完成**。订单已经发出去，回报还没回来，随时可能成交；风险按「已经在市场里」算。

**C++ 专属坑**

- 用 `switch` 加 `default` 处理事件：新增一种事件时编译器不提醒。用 `std::visit` 加 `Overloaded`，漏一个 lambda 就编译失败。
- `std::visit` 各分支的返回类型必须一致（都是 `bool`）；一个分支返回 `int`、一个返回 `bool` 编译不过。
- `unordered_map` 的遍历顺序不确定：`open()` / `all()` 输出前要按 id 排序，否则输出顺序在不同运行、不同标准库之间可能不同。

**该说出口的话**：「先查重复，再查状态、数量、价格、溢出，全部通过才改状态并记 `exec_id`；任何异常路径都不会留下改了一半的订单。」

## Part 2 · `PositionBook`

**写法**

```cpp
// 反方向成交：先只读地把盈亏算完
long long remaining = qty, pnl = 0;
for (const Lot& lot : b.lots) {
    if (remaining == 0) break;
    const long long c = std::min(remaining, lot.qty);
    pnl = add_exact(pnl, mul_exact(b.dir * (px - lot.px), c));
    remaining -= c;
}
const long long new_realized = add_exact(b.realized, pnl);   // 到这里都可能抛，状态还没动
// 提交：从队首消耗 lot；剩余 > 0 则以成交价开反方向的新 lot，dir 翻转
```

每个标的一个 `std::deque<Lot>`、一个方向 `dir`（+1 / -1 / 0）、已实现盈亏。`Side` 用 `sign()` 变成 ±1，多头空头共用一套算术，不写两份 if/else。

**面试官在探什么**

1. **翻转**。一笔成交平掉旧仓之后还有剩余，剩余部分以成交价成为新方向的第一个 lot。例：买 10@100、买 10@110、卖 15@120 得 `(5, 550, 250)`；再卖 25@130，平 5@110（+100）后翻成空头 20 手 @130，得 `(-20, 2600, 350)`；`unrealized_pnl(120) = 2600 - 2400 = 200`。
2. **为什么先算后提交**。盈亏在循环里累加，乘法和加法都可能溢出。边算边改，抛出时队列已经消耗了一半、`realized` 还没更新，仓位就坏了。先只读算完、一次性提交，抛异常时状态不变。
3. **FIFO 与整数**。FIFO 平仓全程整数，没有舍入。换成平均成本法要除以 `net_qty`，盈亏出现舍入，要先问业务用哪种成本法、怎么舍入。
4. **复杂度**。`on_fill` 摊还 O(1)：每个 lot 入队一次、出队一次；`get` / `net_qty` 要遍历该标的的 lot，O(lot 数)。
5. **符号列表为什么用 `std::map`**。要字典序输出，`std::map` 遍历天然有序，不需要再排序；`unordered_map` 则要排序，否则输出不确定。
6. **验证**。随机成交与「把每笔拆成单手、逐手 FIFO」的模型逐笔对照，是抓翻转和部分平仓 bug 最可靠的办法。

**C++ 专属坑**

- 错误写法：先 `books_[symbol]` 取引用、再检查 `qty <= 0` → 抛异常时这个符号已经被创建，`symbols()` 多出一个。改法：参数检查放在取引用之前，和 reference 一样。

**该说出口的话**：「平仓用 FIFO，翻转时剩余部分以成交价开新方向的 lot；盈亏先只读算完再一次性提交，所以溢出不会留下半个仓位。」

## Part 3 · `RiskEngine`

**写法**

```cpp
RiskResult check(const Order& o, const PositionBook& pos, const OrderManager& ord) const {
    if (halted_) return reject(Halted);
    auto it = ref_px_.find(o.symbol());  if (it == ref_px_.end()) return reject(NoReferencePrice);
    if (o.qty() > limits_.max_order_qty()) return reject(QtyLimit);
    long long notional;
    if (__builtin_mul_overflow(o.px(), o.qty(), &notional) || notional > limits_.max_order_notional()) return reject(NotionalLimit);
    /* |px - ref| * 10000 > ref * bps  ->  PriceBand ；这两个乘法溢出同样拒绝 */
    if (ord.open_count() >= limits_.max_open_orders()) return reject(OpenOrdersLimit);
    /* net + 买剩余(+本单) 和 net - 卖剩余(+本单)，四次加减全用 __builtin_*_overflow，溢出 || 越界 -> PositionLimit */
    return RiskResult::accepted();
}
```

方法是 `const`，参数全是 `const&`：类型系统直接表达了「检查只读」。

**面试官在探什么**

1. **检查顺序为什么重要**。同时违反多条时必须报同一条，否则重放得到的原因会不同。顺序就是 `RiskReason` 的声明顺序，加规则时枚举值的位置决定优先级。
2. **fail closed**。没有参考价就无法判断价格带，那就拒绝；熔断拒绝一切包括减仓单。放行一个无法判断的订单，风险是未知的；拒绝一个合法订单，代价是已知且有限的。
3. **价格带为什么交叉相乘**。`|px - ref| / ref <= bps / 10000` 变成 `|px - ref| * 10000 <= ref * bps`，没有除法就没有舍入。参考价 10007、5%：买价 10507 通过、10508 拒绝；参考价 3 时只有 3 本身通过。边界含等于通过。
4. **最坏情况仓位**。只看净仓不够：净仓 2500、未完成买单 2000，再买 501 的净仓看起来是 3001，最坏情况却是 5001 > 5000，应拒绝。多头和空头两个方向各算一遍。
5. **溢出是业务结论**。限额可以设成 `LLONG_MAX`，未完成数量也可能接近它，每一步加法都可能放不进 `long long`。Java 的 `long` 会回绕成负数而放行；C++ 里是 UB。放不进就算超限，直接返回拒绝，而不是抛异常。名义金额同理：乘积回绕成小数会被放行。
6. **新增一条规则改哪里**。加一个枚举值（位置决定优先级）和一段检查。和时间有关的规则（比如每秒最多 N 笔）要把时间作为输入事件传进来，不能在 `check` 里读时钟，否则重放不确定。要做成可组合的责任链，代价是顺序依赖和虚调用。

**C++ 专属坑**

- `||` 短路求值：用一串 `__builtin_add_overflow(...) || ...` 判断溢出，前一个溢出后面的不会再算，也就不会读到没赋值的结果变量。
- `RiskResult` 是值（内部 `std::optional<RiskReason>`）：没有 `null`，「通过」和「带原因拒绝」不会混淆。

**该说出口的话**：「按枚举顺序报第一条违反的规则，结果确定；拿不准就拒绝；最坏情况仓位把未完成订单也算进来，任何一步放不进 `long long` 都当作超限。」

## Part 4 · `TradingDesk`

**写法**

```cpp
RiskResult submit(const Order& order) {
    journal_.emplace_back(Submit(order));   // 1 先写日志：之后抛异常，输入也已经在里面
    return handle_submit(order);            // 2 再处理
}
RiskResult handle_submit(const Order& o) {
    if (orders_.contains(o.id())) throw std::invalid_argument("duplicate order id");
    const RiskResult r = risk_.check(o, positions_, orders_);          // 先于登记
    orders_.submit(o);
    if (!r.is_accepted()) orders_.apply(Reject(o.id(), std::string(to_string(*r.reason()))));  // 输出，不进 journal
    return r;
}
static TradingDesk replay(const RiskLimits& limits, const std::vector<DeskEvent>& journal) {
    TradingDesk d(limits);
    for (const DeskEvent& e : journal) {
        d.journal_.push_back(e);
        try { d.handle(e); } catch (const std::logic_error&) {} catch (const std::overflow_error&) {}
    }
    return d;
}
```

在线路径和恢复路径走同一个 `handle`，它是对 `DeskEvent` 的 `std::visit`；四种回报用一个带 `requires` 约束的泛型 lambda 统一处理。成员全是值（`OrderManager`、`PositionBook`、`RiskEngine`、`std::vector`），所以默认的拷贝就是完整的快照。

**面试官在探什么**

1. **为什么 journal 先于处理**。处理中途抛异常，如果输入还没记录就丢了，重放时这条输入不存在，状态和线上对不上。先写日志，异常的输入也在里面，重放时它会再抛一次，再被吞掉，状态一致。
2. **为什么风控检查在登记之前**。先登记再检查，订单会把自己算进未完成数量和最坏情况仓位。单笔恰好顶格的订单（比如连续两张买 1000，限额 3000）会被误拒。
3. **内部 `Reject` 为什么不进 journal**。它是风控的输出，不是输入；重放时 `Submit` 会再次产生同样的拒绝。如果它也进 journal，重放会多出一条没人输入过的事件，撞上已经是 `Rejected` 的订单，变成非法转移。
4. **为什么重放要吞异常，吞什么**。原来抛过异常的输入，调用方第一次已经看到过，状态当时没变，重放时再抛一次也要吞掉。只捕获 `std::logic_error` 和 `std::overflow_error`（`invalid_argument`、`out_of_range`、`IllegalTransitionException` 都是前者的子类，`overflow_error` 不是）。不用 `catch (...)`：它会连 `std::bad_alloc` 和你自己的 bug 一起吞掉，重放「成功」了，状态却是错的。
5. **决定性**。`handle` 里不读时钟、不用随机数、不依赖哈希表遍历顺序、没有未初始化变量。重放结果和线上不一致时：对 journal 二分，比较状态，找到第一个产生分叉的事件。
6. **所有权**。desk 独占订单、仓位、风控、journal 的全部状态，没有指向外部对象的指针。`journal()` 返回 `std::vector` 的拷贝：之后 desk 的活动不会改变它，改它也不会影响 desk。`TradingDesk what_if = desk;` 是独立的快照，拷贝代价是 O(状态大小)。
7. **多线程怎么办**。单写者加队列：所有线程把事件投递到队列，一个线程顺序处理，处理顺序就是 journal 顺序。加锁会带来竞争，线程交错的顺序每次不同，也会破坏重放。其他线程要读状态，拿快照拷贝，不要直接读 desk。
8. **持久化与恢复**。journal 追加写盘并 `fsync`，重启时 `replay`；journal 太长就定期做快照（保存状态和对应的 journal 位置），从快照开始重放后半段。
9. **撤单请求与确认分开**。多一个 `PendingCancel` 状态：这期间可能还有成交，所以风控的最坏情况仓位仍要算上它的剩余数量。

**C++ 专属坑**

- `DeskEvent` 是平铺的 8 个选项，`variant` 不能继承另一个 `variant`，所以 `to_desk_event` 把四种回报转成 `DeskEvent`（下标差 4）；忘了转换，在线路径写进 journal 的类型就是错的。
- 默认的 `operator==` 比较所有字段：测试里直接比较两个 desk 的订单列表很方便，但以后加一个不该参与业务相等的字段（比如时间戳），比较会悄悄变严格。
- 返回 `const std::vector<DeskEvent>&` 看起来省拷贝，调用方持有的引用会随 desk 追加而失效或改变；要返回拷贝。

**该说出口的话**：「先写 journal 再处理；在线和重放走同一个决定性的 `handle`；风控检查在登记之前；内部的 Reject 是输出，不进 journal；重放只吞自己的异常类型。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 值类型 | `record`，紧凑构造器校验 | `class` + 私有数据 + 校验构造函数 + `friend operator== = default`；无不变量的用 `struct` |
| 封闭的事件集合 | `sealed interface` + 穷尽 `switch` | `std::variant` + `std::visit(Overloaded{...})` |
| 事件继承 | `ExecEvent extends DeskEvent` | `DeskEvent` 平铺 8 个选项 + `to_desk_event` |
| 溢出 | `Math.multiplyExact`；普通 `long` 静默回绕 | 有符号溢出是 UB：`mul_exact` / `__builtin_*_overflow`，风控和聚合量全要显式检查 |
| 空值 | `null`、`NullPointerException` | 值语义；`std::optional` 表示「可能没有」 |
| 异常 | `IllegalArgumentException`、`NoSuchElementException`、`ArithmeticException` | `std::invalid_argument`、`std::out_of_range`、`std::overflow_error`，非法转移是 `std::logic_error` 的子类 |
| journal 快照 | `List.copyOf` | 按值返回 `std::vector` |
| desk 的复制 | 共享引用 | 值语义：默认拷贝就是独立快照 |
| 符号排序 | `HashMap` + 输出时排序 | 仓位用 `std::map`（自带有序），订单用 `unordered_map` + 排序 |
