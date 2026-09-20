---
nodes: [problems.marketplaces.food-delivery, structure.state-machines]
tags: [problem]
---
# Drill：外卖配送（Food Delivery）

一个像 Swiggy / 美团那样的外卖平台：顾客点餐，餐厅做菜，骑手送达。**参与方是三个，不是两个**
——这是这道题和网约车最根本的差别。城市里同时有几千家店、几万张单。**地图不在这道题里**：
坐标是平面点，距离是直线距离。金额一律是整数最小货币单位（分）。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：餐厅、菜单、顾客下单，以及订单跨三方的生命周期——PLACED → ACCEPTED
  或 REJECTED（餐厅说了算）→ READY（餐厅）→ PICKED_UP（骑手）→ DELIVERED（骑手），外加
  CANCELLED。**每一条边都要写明允许的角色**，这是本题的设计核心。动手前先决定两件事：
  角色写在哪里（和转移表放一起，还是另起一张许可表）？菜品可售状态随时会变，你在哪一刻校验、
  缺货了少送一道还是整单失败？
- 第 2 关（约 15 分钟）：骑手派单。**餐厅接单之前一个骑手都不派**；接单那一刻算出预计出餐
  时间，派单是一个由注入时钟驱动的拉取动作。写完之后必须能回答一句话：**派早了谁买单、
  派晚了谁买单，你的策略在优化哪一个？**
- 第 3 关（约 15 分钟）：把两三单拼给同一位骑手。给出一条能直接对顾客讲的规则，保证拼单不会
  把第一单耽误太久；想一想能不能用**一条**不等式同时管住「两家店要近」和「两单要差不多时候
  出餐」。并发上：几个线程同时派单，一位骑手不能拿到两个批次，一张订单不能进两个批次。
- 第 4 关（选做）：定时单（预约几点送到）与餐厅中途打烊。评分点不是实现，而是**加它们有没有
  动到派单、批次合并里的任何一行代码**；以及「已经接下的单，打烊后还算不算数」你怎么答。

**怎么练**：把 `vault/domains/low-level-design/problems/food-delivery/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/food-delivery -q`。

**评分点**
- 状态机的每一条边都带着「允许的角色」，而不是把权限散成十个方法里的十个 `if`；说得出「例外用第二张表，通例进第一张表」这条判据（[[problems-food-delivery-role-on-every-edge]]、[[structure-state-transition-table]]）。
- 边不存在和边存在但越权抛**两个不同**的异常，并说得出它们给客服、给监控的含义不同（[[problems-food-delivery-illegal-vs-unpermitted]]、[[structure-state-guards-and-illegal-events]]）。
- 餐厅接单之前不派骑手；预计出餐时间在接单那一刻算，且等于「基础准备 + 最慢的那道菜」而不是相加（[[problems-food-delivery-dispatch-after-acceptance]]）。
- 派单时机是一个显式的取舍，能用一行判据写出来，并说得出没有空闲骑手时的失败模式（[[problems-food-delivery-dispatch-timing-tradeoff]]）。
- 拼单的规则直接写成对顾客的承诺（第一单最多晚多久），一条不等式顶三个阈值；锚单先送（[[problems-food-delivery-batch-one-inequality]]）。
- 批次不另起一套状态机，「送完了吗」是一次对订单状态的查询；批次表在最后一单送达时被删（[[problems-food-delivery-batch-has-no-state-machine]]、[[patterns-extensibility-followup]]）。
- 可售校验、开店判断与抄价在餐厅的一次加锁里完成，缺货整单失败，且餐厅仍保留最终拒单权（[[problems-food-delivery-menu-check-is-atomic]]、[[concurrency-check-then-act]]）。
- 骑手分配是锁内的一次比较并交换，一位骑手不会同时拿到两个批次（[[problems-food-delivery-batch-has-no-state-machine]]、[[concurrency-lock-while-calling-out]]）。
- 打烊只拒未接的单、已接的单照常做完；定时单只加一个状态和一条边，派单一行不改（[[problems-food-delivery-closing-is-not-cancelling]]）。

**题解**：[[solution-food-delivery]]——先做，再看。相邻的[[solution-ride-sharing]]讲的是同一族问题
的另一半（要约、独占、超时顺延），两题对照着看收获最大。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
