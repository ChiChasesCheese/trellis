---
nodes: [problems.machines.vending-machine, patterns.state, structure.state-machines]
tags: [problem]
---
# Drill：自动售货机（Vending Machine）

一台放在写字楼大堂的自动售货机：几个货道各装一种商品，一个币箱，面额是 5／10／25／100 分。
顺路径谁都会写，这道题的全部分数在机器**必须拒绝**的那些时刻——以及拒绝之后买家的钱在哪。
照真实机考的节奏分关来做，做完一关再看下一关。金额一律用整数分，代码里不许出现浮点。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：购买流程的状态机 IDLE → 已投币 → 出货中 → 找零待取 → IDLE，并且
  **每一个非法动作都被显式拒绝**：没投币就按选择、出货过程中再投币、货已经在路上了还要退币。
  报错要说得出机器此刻在等什么。投进来的硬币在成交前单独托管，按退币退回的必须是原来那几枚。
- 第 2 关（约 15 分钟）：加库存和币箱，让机器能因为两种不同的理由失败——货道空了、币箱凑
  不出零钱——而且两者都必须**整笔拒绝**：库存不减、币箱不动、钱还在买家名下，他可以补零钱
  或者退币。注意"找不开"必须在货出来**之前**被发现。
- 第 3 关（约 10 分钟）：用真实面额做找零。先写贪心，再自己找出一个"明明有解却报找不开"的
  币箱，然后写一个一定找得到解的版本，并让算法能整体替换而不改机器。
- 第 4 关（选做）：补货与装币这类管理动作（交易进行中必须拒绝），以及读卡器作为第二种支付
  方式。判分点只有一个：加这些东西**不许动状态机**——如果你发现自己在往状态枚举里加成员，
  回头看动作的命名。

**怎么练**：把 `vault/domains/low-level-design/problems/vending-machine/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/vending-machine -q`。

**评分点**
- 合法性做成一张 `dict[(状态, 动作), 新状态]` 的数据，并能写出一个遍历全部状态×动作组合的穷举测试（[[problems-vending-machine-table-vs-state-classes]]、[[patterns-state-enum-table]]）。
- 说得出什么时候该翻到"一状态一个类"：每个状态有成套的进入／退出副作用时，而不是"状态多"时（[[patterns-state-class-form]]、[[patterns-state-explosion]]）。
- 非法动作和守卫失败用两种不同的机制、两种不同的异常，守卫失败时状态原地不动（[[problems-vending-machine-guard-vs-illegal]]、[[structure-state-guards-and-illegal-events]]）。
- 投币先托管，退币原样退回；成交时先把托管硬币并入币箱再取找零（[[problems-vending-machine-escrow]]）。
- 找零方案在出货前算好，算不出来整笔拒绝，绝不半成交（[[problems-vending-machine-plan-change-before-dispensing]]）。
- 举得出贪心找零的反例："币箱只有 25 分和 10 分、要找 30 分"，并给出一定找得到解的做法（[[problems-vending-machine-greedy-change-fails]]）。
- 币箱里被取空的面额从字典里删掉，不留计数为 0 的幽灵面额（[[problems-vending-machine-bank-drops-empty-denomination]]）。
- 加读卡器时动作叫 `PAY` 而不是 `INSERT_COIN`，付款抽成一个真有两个实现的协议（[[problems-vending-machine-second-payment-method]]、[[patterns-state-vending]]）。
- 并发下用一把粗锁保护"查状态→查守卫→改状态"，说得清为什么不按货道细化、GIL 为什么不够（[[problems-vending-machine-lock-granularity]]）。
- 对外只给不可变快照（库存、币箱），从不把内部字典交出去（[[structure-api-leaking-internals]]）。

**题解**：[[solution-vending-machine]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
