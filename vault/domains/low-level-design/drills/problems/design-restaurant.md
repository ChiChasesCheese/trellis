---
nodes: [problems.booking.restaurant, structure.state-machines]
tags: [problem]
---
# Drill：餐厅管理（Restaurant Management）

一家线下餐厅的点单系统：客人到店要有位子坐，坐下点菜要送进后厨，做好了端上桌，吃完要能
结账、还能拆着付。和外卖最大的不同是**客人就坐在店里**：一张桌子上的所有人共享同一份账单，
后厨要按课程顺序上菜，外带外送则完全不占桌子。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：桌子按容量建模；散客到店挑坐得下的**最小**空桌；按时段预订要提前
  锁定桌子，同一张桌子的预订时段不能重叠；坐不下时进候位名单；预订没人认领要在一个宽限期
  之后自动让位，桌子回到可分配的池子里，候位名单有机会顶上。动手前先想清楚两件事：候位
  名单空出一张桌子时，该服务队首那一位，还是队伍里第一个坐得下这张桌子的人？没人认领的
  预订要怎么让它过期——用后台定时任务，还是在每次读写时顺手检查？
- 第 2 关（约 20 分钟）：点单里每道菜有自己的状态（已下单、制作中、已备好、已上桌），
  非法的状态跳转要报错。账单只认已经上桌的菜。写三种拆账方式——平摊、按份额、按菜——
  取整产生的零头必须分配得确定、可复现。想清楚一件事：一桌人先付清一部分账，之后又点了
  菜，账单要怎么继续正确增长？
- 第 3 关（约 15 分钟）：后厨是一条队列，开胃菜要先于主菜就绪；一道菜中途没货了，还没
  开始做的那部分要能被撤下来，已经在做或做好的不受影响；前厅要能看到"哪张桌子还在等哪些
  菜"。
- 第 4 关（选做）：加一种不占桌的点单（外带或外送），复用后厨那条流水线。评分点不是
  实现本身，而是**加它有没有碰到第 1 关写的桌位管理代码一行**。

**怎么练**：把 `vault/domains/low-level-design/problems/restaurant/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/restaurant -q`。

**评分点**
- 散客和预订共用"挑能坐下这拨人的最小桌子"这条规则，但入座依据的是"此刻谁空着"，预订依据的
  是"那段时间有没有人订"，两者不能混用同一次校验（[[problems-restaurant-smallest-fitting-table]]）。
- 没人认领的预订过了宽限期会自动从预订表里消失，说得出为什么用懒惰重算而不是后台定时任务
  （[[problems-restaurant-reservation-grace-lazy-sweep]]）。
- 候位名单空出桌子时，会跳过坐不下的团体、服务队伍里第一个坐得下的，而不是死板地按队首处理
  （[[problems-restaurant-waitlist-skip-too-big]]）。
- 账单是对"已上桌"这个状态的一次实时查询，不是下单时就锁定、之后累加扣减的一个字段——这也是
  "先付一部分、再加菜"不需要专门状态就能正确工作的原因（[[problems-restaurant-served-total-is-query]]）。
- 拆账的三种方式是三个纯函数而不是三个策略类，说得出策略模式在这里为什么不成立
  （[[problems-restaurant-split-functions-not-classes]]、[[patterns-extensibility-followup]]）。
- 按份额拆账的取整零头用最大余数法逐分整数分配，不用浮点数，两次运行同样的输入给出同样的
  结果（[[problems-restaurant-largest-remainder-method]]）。
- 课程门禁用一条"课程序号更小的兄弟菜必须先就绪"的通用规则，而不是给每一对课程写一条特判
  的 `if`（[[problems-restaurant-course-gating-ordinal]]）。
- 一道菜中途缺货，只有还没开始做的同款菜转为不可用，已经在做或做好的不受影响
  （[[problems-restaurant-mark-unavailable-partial]]）。
- 点单里有一道菜缺货，整批提交失败且不留下部分行——校验和入队钉在同一次加锁里完成，失败时
  把已经加进点单的行整批撤回（[[problems-restaurant-atomic-submit-rollback]]、[[concurrency-check-then-act]]）。

**题解**：[[solution-restaurant]]——先做，再看。相邻的[[solution-food-delivery]]讲的是"点菜
送到"这条主线在多方协调下的另一种形态，两题对照着看能看清"客人在不在店里"这一件事如何改变
整个设计。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
