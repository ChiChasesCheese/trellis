---
nodes: [problems.marketplaces.stock-brokerage, structure.storage, concurrency.primitives]
tags: [problem]
---
# Drill：股票交易系统（Stock Brokerage）

一个单场所、进程内的经纪与撮合系统：用户账户里有现金和持仓，能报限价单和市价单，系统按
**价格-时间优先**把它们撮合成交。几百只股票、每只股票的簿子上几万张挂单、撤单笔数远超成交
笔数。金额一律是**整数最小货币单位（分）**，股数是整数股。行情源、手续费、真实交收周期都不在
这道题里。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：账户、订单与校验。买单看购买力（可用现金），卖单看可用持仓。动手前
  先决定两件事：钱用什么类型（别用 `float`，想清楚为什么），以及**允不允许卖空**——说得出
  允许会把「够不够股」的整数比较变成什么。不合法的报单（数量非正、限价单不带价、市价单带价、
  股票没挂牌、账户不存在）当场拒绝，而且**什么都不留下**。
- 第 2 关（约 15 分钟）：真正的限价订单簿。价格优先、同价时间优先、支持部分成交。**这一关的
  分数全在数据结构的取舍上**：每侧一个堆，还是「有序价位表 + 每价位一个 FIFO」？把**撤单**
  的代价算给面试官看，再决定。然后回答一个必被追问的问题：两张单交叉时，成交打在谁报的价上？
- 第 3 关（约 15 分钟）：生命周期与结算。NEW → PARTIALLY_FILLED → FILLED / CANCELLED /
  REJECTED；撤单与成交的竞争谁说了算；一笔成交必须**原子地**搬动两个账户的钱和股。写一个
  随机会话测试：固定种子、几百次随机报单与撤单，**每一步之后**都断言全场现金总额与总股数不变。
  再用 `threading.Barrier` 让二十个买家同时抢一张有限的卖单——断言的那个数要**推导**出来
  （供给与需求的较小者），不是跑一遍看到的。
- 第 4 关（选做）：盘口行情（top of book）推送给订阅者，或者止损单（stop order）。评分点不是
  「写出来了」，而是**加它有没有动到撮合循环的任何一行**；以及推送该在锁内还是锁外。

**怎么练**：把 `vault/domains/low-level-design/problems/stock-brokerage/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/stock-brokerage -q`。

**评分点**
- 订单簿**只认股数不认钱**：撮合输出一串 `(对手挂单, 成交价, 成交股数)`，结算由门面做；说得出这一刀换来了什么（[[problems-stock-brokerage-book-knows-no-money]]）。
- 数据结构是「有序价位表 + 每价位一个 FIFO」而不是堆，理由是**撤单**与惰性删除的垃圾；说得出 Python 的 `dict` 既是 FIFO 又白送 O(1) 删除，因此不需要序号字段（[[problems-stock-brokerage-price-level-dict-fifo]]）。
- 成交价取**挂单方**的价，差额退给来单方；说得出「一律按卖单价」在买单先挂时为什么是错的（[[problems-stock-brokerage-trade-at-resting-price]]）。
- 资金校验发生在**报单那一刻的冻结**，不是撮合之后的扣款加回滚；终态订单锁着的额度必为 0（[[problems-stock-brokerage-reserve-before-match]]、[[structure-storage-chm-compound-ops]]）。
- 市价买单靠**锁内的一次试算**按最差价冻结，而不是拿最新成交价估；市价单永远不挂单，空簿子上的市价单是 CANCELLED 而不是异常（[[problems-stock-brokerage-market-buy-buying-power]]）。
- 状态是 `Enum` 加一个 `is_terminal`，不是每状态一个类；买卖是一个 `Side` 枚举，不是 `BuyOrder`/`SellOrder` 两个子类；没有「半成交又撤单」这第六个状态（[[problems-stock-brokerage-status-enum-not-state-classes]]、[[structure-state-table-vs-state-pattern]]）。
- 撤单与成交的竞争由同一把锁裁定；说得出 GIL 和并发容器在这里都无能为力，以及真实引擎为什么改成每股票单线程（[[problems-stock-brokerage-cancel-races-a-fill]]、[[concurrency-check-then-act]]）。
- 行情事件**自带内容**、在锁内生成、在锁外推送；加它没有动撮合的任何一行（[[problems-stock-brokerage-feed-and-shrinking-containers]]、[[concurrency-lock-while-calling-out]]）。
- 每个容器都有出口：空价位立刻消失、终结订单被 purge 清出、订阅者表靠退订函数缩小（[[problems-stock-brokerage-feed-and-shrinking-containers]]）。

**题解**：[[solution-stock-brokerage]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
