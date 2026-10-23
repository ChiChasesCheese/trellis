---
id: hl-hc05-java21-features
node: problems.hc05-market-order-book
type: qa
step: 18
---
## Q
订单簿实现用到了哪些 Java 21 特性？各自比旧写法好在哪？

## A
- **record + 紧凑构造器**：`Order`（校验）、`Level`、全部命令和事件、`Summary`；非法订单构造不出来，`equals` 按字段，测试直接比较事件列表。需要可变状态时不该用（`Node` 的 `qty` 会变，所以是普通类）。
- **sealed**：`Command permits Limit, Market, Cancel, Modify`、`Event permits Trade, Rested, Cancelled, Modified, Rejected`；新增一种时所有 switch 编译报错。
- **switch 模式匹配 + `when` 守卫**：`case Limit l when l.price() <= 0`，代替 `instanceof` 链加强转；穷尽性由编译器检查，**sealed switch 里别写 `default`**（会丧失穷尽检查）。
- **record 模式**：`case Trade(var taker, var maker, var side, var px, var q) ->`。
- **switch 表达式 + `yield`**：无 fallthrough，多行分支也能当表达式。
- **`instanceof` 模式**：`e instanceof OrderBook.Trade t`。
- **Sequenced Collections**：`TreeMap` / `LinkedHashMap` 都是 `SequencedMap`：`firstEntry / pollFirstEntry / putLast`；旧写法取队头 `map.entrySet().iterator().next()` 长且易忘判空。
- **未命名模式 `_`**（预览）：`case Limit _, Market _ ->` 一个 case 并列多个模式（JDK 22 正式）。
- **`mapMulti` / `toList()`**、`addExact / multiplyExact`、`formatted`、文本块、`var`。
- 把 `case` 守卫顺序写对：第一个匹配的生效。
