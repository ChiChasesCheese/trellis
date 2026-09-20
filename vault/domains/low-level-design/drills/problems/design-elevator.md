---
nodes: [problems.machines.elevator, structure.state-machines, patterns.strategy, concurrency.hazards]
tags: [problem]
---
# Drill：电梯系统（Elevator System）

一栋二十层的写字楼，四部电梯。楼层外的按钮带方向（在 5 楼按"上"），轿厢里的按钮只有楼层。
照真实机考的节奏分关来做，做完一关再看下一关的要求。**时间不许用 `time.sleep` 模拟**：
一个 `step()` 推进一拍，一拍走一层或者开一次门，时钟从构造函数注入。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：一部梯。显式的状态机 IDLE / MOVING_UP / MOVING_DOWN / DOORS_OPEN，
  不允许用 `is_moving` + `going_up` + `door_open` 这种布尔汤；支持带方向的外呼和不带方向的
  内选；`step()` 推进一拍并返回这一拍发生的事件；门开满若干拍自动关上。整套逻辑必须能在
  不睡眠的前提下被逐拍断言。
- 第 2 关（约 15 分钟）：把"下一站去哪"整体换掉——至少实现经典电梯算法（SCAN／LOOK：朝一个
  方向一路服务到底，再掉头扫回来）和朴素的"最近请求优先"两种，切换策略不许改动第 1 关写好的
  轿厢类。并写一个测试证明后者会饿死远处的楼层、前者不会。
- 第 3 关（约 15 分钟）：四部梯加一个派梯器，把一个外呼指派给其中一部。说清楚它优化什么
  （这位乘客的等待时间），以及它绝不能做什么（同一个外呼被两部梯接走——按两次按钮也不行）。
  外呼从各楼层并发进来，指派必须原子；外呼被服务之后，"派给了谁"的记录必须销掉。
- 第 4 关（选做）：挡门（有人堵住门口）、把一部梯停用去检修、直达梯只停部分楼层。三者都
  不应该要求你回头改第 1 关的状态机：挡门复用已有的开门倒计时，停用是一维正交的标志，
  直达梯是派梯前的一道过滤。停用的那部梯手上没做完的外呼要能被收回重派，同时不能影响
  车里乘客已经按下的内选。

**怎么练**：把 `vault/domains/low-level-design/problems/elevator/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/elevator -q`。

**评分点**
- 时间建模成 tick、时钟靠注入，全程没有 `time.sleep`，因此每一拍都能被断言（[[problems-elevator-tick-not-sleep]]）。
- "此刻在做什么"（状态枚举）和"这一趟朝哪走"（扫描方向）分开存，方向跨越开关门不丢（[[problems-elevator-sweep-outlives-doors]]、[[structure-state-enum-vs-boolean-soup]]）。
- 停靠请求按外呼向上／外呼向下／内选分成三个集合，内选两个方向都停，同层的双向外呼互不吞并（[[problems-elevator-three-stop-sets]]）。
- 说得出 SCAN 的公平性是"一趟扫描最多一个来回"，并能演示"最近请求优先"饿死远处楼层（[[problems-elevator-scan-vs-nearest-starvation]]）。
- 两个可替换点（选下一站、派哪部梯）都是普通函数，不为一次性计算单开抽象基类（[[problems-elevator-policies-as-functions]]、[[patterns-strategy-callable]]）。
- 一个外呼恰好一部梯：分派表放在梯群、幂等处理重复按键，**并且在服务完成时销账**（[[problems-elevator-one-call-one-car]]）。
- "停用"做成和状态机正交的布尔字段而不是第五个状态，说得出状态爆炸是怎么来的（[[problems-elevator-out-of-service-orthogonal]]、[[patterns-state-explosion]]）。
- 并发下锁只包住"查表→挑梯→登记"，事件回调和订阅者通知都在锁外，能说清 GIL 为什么替代不了这把锁（[[problems-elevator-lock-scope]]）。
- 对外只给不可变快照和自描述事件，从不把轿厢内部的停靠集合交出去（[[structure-api-leaking-internals]]）。

**题解**：[[solution-elevator]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
