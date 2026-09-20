---
nodes: [problems.booking.airline, structure.state-machines]
tags: [problem]
---
# Drill：航班管理（Airline Management）

一家全国性航司：几十个机场、每天几千班航班，热门枢纽机场每天有成百上千条中转组合。旅客搜一天
从 A 到 B 的机票，可能要中转一次，选舱位下单，之后值机、登机，也可能取消或改签。像真实的机器
编码轮一样分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：先想清楚"航班"要不要拆成两个类——一个描述排班规则，一个描述某一天
  真正持有库存的那一班。建出机型、座位表、航班目录，按机场 + 日期 + 舱位查出还有票的航班，
  订一张单段行程的票。座位号不存在、这个舱位已经卖光，都要抛明确的异常。
- 第 2 关（约 15 分钟）：加中转。一条行程要拼成若干航段，中转判定"接得上"需要一个最短衔接时间
  的阈值——想清楚这条规则该挂在哪个对象上，为什么不该挂在航班上。订一条跨两段航班的行程时，
  两段必须**要么都订上，要么一段都不订**，说得出你的多锁方案为什么不会死锁。
- 第 3 关（约 15 分钟）：把订单生命周期做成一张显式的状态转移表（占座 → 出票 → 值机 → 登机，
  以及从合适的状态回到取消）。加超售：某个舱位卖出的票可以超过实际座位数，值机时可能选不到座位，
  登机口按公开规则决定谁被拒载。用真线程测同一舱只剩几个授权名额时被多人同时抢购。
- 第 4 关（选做）：加代码共享——同一架飞机在另一家航司的目录里挂着不同航班号，只是同一份库存的
  另一个市场标签。验收标准很硬：这个功能加进来**不能改动第 2、3 关写好的订座与库存代码一行**。

**怎么练**：把 `vault/domains/low-level-design/problems/airline/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/airline -q`。

**评分点**
- 能说清"航班"为什么要拆成排班规则和某一天的实例两个类，以及库存状态为什么只该长在后者身上
  （[[problems-airline-flight-vs-instance]]）。
- 库存用"订单号→舱位"和"座位号→订单号"两张表而不是一张座位状态表，说得出这两张表分别回答什么
  问题、为什么这样才能表达超售（[[problems-airline-sold-vs-seats-two-tables]]）。
- 跨航段原子订座：按 key 排序、固定顺序拿到全部锁再做两段式检查加写入，说得出这为什么不会死锁
  （[[problems-airline-atomic-cross-segment]]），以及为什么这里不需要两阶段提交或补偿事务
  （[[problems-airline-no-two-phase-commit]]）。
- 最短衔接时间挂在机场而不是航班，说得出理由（[[problems-airline-mct-belongs-to-airport]]）。
- 超售登机口拒载谁，规则要能对旅客解释清楚（[[problems-airline-denied-boarding-rule]]）。
- 改签不是字面意义的"取消再重订"，说得出为什么要先占新段再放旧段
  （[[problems-airline-change-reserve-before-release]]）。
- 代码共享作为一个"不碰订座代码"的扩展加进来，而不是新建一份库存
  （[[problems-airline-codeshare-alias-extension]]）。

**题解**：[[solution-airline]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
