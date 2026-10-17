---
nodes: [amazon.amz-discount-engine, patterns.strategy, oop.values]
tags: [problem]
---
# Drill：购物车折扣引擎（Checkout Price Engine）

Amazon OOD 一轮的题：购物车里有若干商品，商家有一批促销规则，写出算总价的引擎，并随着面试官加需求不断扩展。规模是几十行商品、几十条规则；钱用整数分。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：报告里的原话——抽象一个 Discount 基类，`is_eligible` 判断商品是否适用，`apply` 返回折扣金额；`PriceEngine` 遍历购物车每一行、依次检查所有折扣、累加后从原价扣除。先实现 `LineItem`、`Cart`、百分比折扣 `PercentOff`（可限定 SKU 或品类）和 `compute`，钱全程用整数分。
- 第 2 关（约 15 分钟）：加 `BuyXGetY`（它不直接减钱，把送出的件数折成钱）和满减 `ThresholdOff`（推断）。先回答：满减的门槛看原价还是折后价？它为什么不能做成“对每一行 apply”？
- 第 3 关（约 15 分钟）：多个折扣同时命中同一行（推断）：叠加顺序、不能减成负数、写坏的折扣返回负数怎么办，再加“每行只取最大一条”。想清楚为什么这是一个枚举参数而不是第二个引擎类。
- 第 4 关（选做）：返回带标签的账单 `Receipt`，保证“原价 − 全部减免 = 应付”；多线程同时改购物车、同时算价不出错。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-discount-engine/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-discount-engine -q`。

**评分点**
- 说得出面试官会怎么问，并先问出叠加、整车折扣、币种三个澄清问题（[[amz-discount-engine-how-it-is-asked]]）。
- 对象拆分清楚：商品行、购物车、行级折扣、整车折扣、引擎、账单各管一件事（[[amz-discount-engine-objects-and-jobs]]）。
- 主循环正确：先筛 `is_eligible`，再对剩余价格 `apply`，减免钳在剩余价格以内（[[amz-discount-engine-stage-one-flow]]）。
- 金额用整数分、比例用基点、舍入只发生一次（[[amz-discount-engine-integer-cents-single-rounding]]、[[amz-discount-engine-float-money-mistake]]）。
- 能解释折扣为什么分两层，买 X 送 Y 住在哪一层（[[amz-discount-engine-line-level-vs-cart-level]]、[[amz-discount-engine-buy-x-get-y]]）。
- 叠加时后一条看剩余价格，负数用异常拒绝（[[amz-discount-engine-stacking-and-clamp]]）。
- 并发：引擎无状态可共享，购物车的合并要加锁（[[amz-discount-engine-thread-safety]]）。

**题解**：[[solution-amz-discount-engine]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
