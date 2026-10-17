---
nodes: [amazon.amz-pizza-order, patterns.creational, patterns.strategy, oop.values]
tags: [problem]
---
# Drill：披萨订单（Pizza Order）

披萨店让顾客自选尺寸、饼底和配料，要算出每份的价格，再把一张订单里的多份披萨套上优惠，算出总价。规模是三个尺寸、几种饼底、十几种配料、几条优惠；钱用整数分。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：菜单是数据。实现 `Menu`（尺寸基础价、饼底加价、按尺寸的配料价）、不可变的 `Pizza` 和 `Menu.price`。先回答：配料价格随尺寸变，怎么存？为什么不是每种配料一个类？
- 第 2 关（约 15 分钟）：用 `PizzaBuilder` 收集选择，`build()` 一次性校验：未知选项、小号不能做芝心饼底、奶酪与植物奶酪互斥、配料不重复且不超过上限。失败抛带原因的 `InvalidChoiceError`。
- 第 3 关（约 15 分钟）：优惠。行级规则 `LineRule`（小号九折、同款买二送一）和整单规则 `OrderRule`（满 30 减 3、每 3 份最便宜的一份免费），由 `PriceEngine` 遍历、钳位、记账。想清楚：整单规则读折前价还是折后价？
- 第 4 关（选做）：`Order` 把同样的披萨合并成一行，多线程同时加披萨、同时算价不出错；说出订单怎么存下来、价格为什么要在构建时定格。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-pizza-order/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-pizza-order -q`。

**评分点**
- 说得出披萨订单要设计什么，并先问出配料价格与尺寸、不允许的组合、优惠范围三个澄清问题（[[amz-pizza-order-how-it-is-asked]]）。
- 对象拆分清楚：菜单、Builder、披萨、订单、两层规则、引擎各管一件事（[[amz-pizza-order-objects-and-jobs]]）。
- `build()` 先校验再定价，失败抛带原因的异常（[[amz-pizza-order-stage1-build-and-validate]]）。
- 菜单用数据表达按尺寸的价格，说得出为什么不用装饰器（[[amz-pizza-order-menu-as-data-price-by-size]]、[[amz-pizza-order-decorator-vs-menu-data]]）。
- 优惠分行级和整单两层，新优惠只加一个类（[[amz-pizza-order-followup-discount-layers]]）。
- 整单规则读折后价，免费不超过实际价格（[[amz-pizza-order-cheapest-free-uses-discounted-price]]）。
- 并发：订单合并加锁，引擎无状态可共享（[[amz-pizza-order-concurrency-order-lock]]）；配料排序后同样的披萨才会合并（[[amz-pizza-order-unsorted-toppings-mistake]]）。

**题解**：[[solution-amz-pizza-order]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
