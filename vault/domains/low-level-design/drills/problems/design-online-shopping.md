---
nodes: [problems.marketplaces.online-shopping, structure.state-machines, structure.storage]
tags: [problem]
---
# Drill：在线购物（Online Shopping）

一个像 Amazon 那样的商城：商品有多个卖家在卖，用户加购、下单，库存必须正确扣减，订单要能
跟踪状态。一次下单会跨库存、支付、履约三个各自会失败、又不在同一个事务里的系统。金额一律
是整数最小货币单位（分）。**商品搜索不在这道题里**，那是另一道完整的题。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：商品目录、购物车、结账产出一张订单。订单行要抄下**下单那一刻**的
  价格，卖家事后改价不追溯已下的单；购物车某一行数量减到 0 要整行消失，对外只给快照。
  动手前先决定：价格和库存挂在商品上，还是挂在"某个卖家对某件商品的挂牌"上？
- 第 2 关（约 15 分钟）：库存加一个"预留"的中间态，带过期时间，**过期由注入的时钟判定**
  （测试不许 `sleep`）。预留必须整笔成立或整笔失败。说清楚"加购时预留"和"下单时预留"各自
  漏掉了什么，并说出你选哪个、代价是什么。
- 第 3 关（约 15 分钟）：订单生命周期写成一张**显式的转移表**，非法转移抛异常；结账编排成
  "预留—扣款—扣减—发货"四步，任何一步失败，已经发生的部分都要被补偿掉。再想一想：
  扣款成功但回执丢了，你的回滚会怎么处理那笔钱？
- 第 4 关（选做）：同一件商品出现第二个卖家；加一条"满 300 减 10%"的促销。评分点不是实现，
  而是**加它们有没有动到下单流程、订单、库存里的任何一行代码**。

**怎么练**：把 `vault/domains/low-level-design/problems/online-shopping/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/online-shopping -q`。

**评分点**
- 说得出加购即锁库存是"少卖"、扣款后再扣现货是"超卖"，并为自己的选择给出代价（[[problems-online-shopping-reserve-timing]]）。
- 预留的过期是被**执行**的而不是被记录的：注入时钟、读写前清扫、提交已过期的预留直接失败（[[problems-online-shopping-reservation-expiry]]）。
- 预留表和它的额度计数表都会缩小，三条删除路径（过期／释放／提交）数得清（[[problems-online-shopping-reservation-expiry]]、[[structure-storage-secondary-index]]）。
- 订单状态是枚举加一张显式转移表，既不是布尔汤也不是每状态一个类，并说得出判据（[[problems-online-shopping-transition-table]]、[[structure-state-table-vs-state-pattern]]）。
- 非法转移抛异常而不是被忽略；状态只读，唯一改法是一次受检的转移，并留下历史（[[problems-online-shopping-illegal-transition-raises]]、[[structure-state-guards-and-illegal-events]]）。
- 结账写成"动作 + 补偿"成对声明的 Saga，而不是一串嵌套 `try/except`（[[problems-online-shopping-saga-vs-try-except]]）。
- 失败的那一步自己也被补偿，且每个补偿幂等、能容忍"什么都还没发生"（[[problems-online-shopping-compensate-failed-step]]）。
- 退款按调用方生成的幂等键寻址，不依赖可能根本没拿到的回执号（[[problems-online-shopping-idempotency-key]]）。
- 价格和库存挂在挂牌上，第二个卖家只是目录里多一行（[[problems-online-shopping-price-on-listing]]）。
- 促销规则是普通函数，不为无状态的一次性计算建抽象基类；折扣向下取整（[[problems-online-shopping-pricing-rule-function]]）。

**题解**：[[solution-online-shopping]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
