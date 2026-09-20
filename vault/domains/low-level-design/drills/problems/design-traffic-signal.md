---
nodes: [problems.machines.traffic-signal, structure.state-machines]
tags: [problem]
---
# Drill：交通信号灯（Traffic Signal）

一个四进口道的十字路口的信号控制器：相位轮转、可配置时序、紧急车辆抢占。这道题看着最简单，
却最容易写出一份**没法测试**的答案——只要你在状态处理函数里写下 `time.sleep(green)` 再开一个
后台线程，这一轮就基本结束了。时间必须靠 `step()` 一格一格推进，真实时间只通过注入的时钟
进入时间戳；代码里不许出现 `sleep`。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：一个路口，四个进口道，相位序列 南北绿 → 清空 → 全红 → 东西绿 →
  清空 → 全红 → ……；`step()` 推进一个 tick。把**安全不变式**显式写出来并在每一 tick 末尾
  复核：两个互相冲突的流向永不同时放行。动手之前先想清楚「冲突」该写在哪——写成东西南北的
  分支，还是写成一张与方向无关的数据？这个选择在第 4 关会被兑现。
- 第 2 关（约 15 分钟）：配时方案可以整体替换——定周期，以及感应式（最短绿之后只要车还在
  陆续到达就延长，直到最长绿）。写完之后回答一个问题：**为什么全红清空段才是不变式在相位
  切换那一瞬间仍然成立的原因？**顺便说清最短绿和最长绿各自守的是什么。
- 第 3 关（约 15 分钟）：紧急车辆抢占。某个流向请求放行，控制器**仍然要走完最短绿、清空段
  和全红**才切过去；紧急车辆通过后恢复到原来的方案。再回答两个问题：抢占要不要上限？
  「恢复」到底是跳回被打断的相位，还是从被抢占到的相位继续环？
- 第 4 关（选做）：加一个行人相位（走 / 闪烁禁止通行 / 禁止通行 三段），或者一个保护左转
  箭头。判分点只有一个：**不许动相位引擎**。如果你发现自己在往引擎里写 `if 是行人`，
  回头看流向能不能自己回答「我现在该显示什么」。

**怎么练**：把 `vault/domains/low-level-design/problems/traffic-signal/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/traffic-signal -q`。

**评分点**
- 安全定义做成一张冲突图而不是方向分支，并在启动时校验每个相位内部无冲突（[[problems-traffic-signal-conflict-graph-not-directions]]）。
- 时间靠 tick 推进、时钟注入，代码里没有 `sleep`、没有后台线程，因此也不需要锁——而且说得出这是主动选择（[[problems-traffic-signal-tick-driven-no-sleep]]）。
- 相位切换必经清空段 + 全红段，并说得出物理理由；黄灯与闪烁禁止通行都不算放行（[[problems-traffic-signal-all-red-clearance]]、[[structure-state-transition-table]]）。
- 配时方案收敛成「绿灯还要不要再保持一个 tick」这一个布尔问题，两个真实实现；最短绿是安全参数、最长绿是防饿死上限（[[problems-traffic-signal-timing-plan-strategy]]）。
- 抢占不跳间隔、有上限、恢复是继续环这三条都答得出（[[problems-traffic-signal-preemption-three-rules]]）。
- 流向自己回答 go / clear / stop，于是行人相位和左转箭头都是只改数据（[[problems-traffic-signal-movement-go-clear-stop]]）。
- 拒绝「一个颜色一个状态类」和单例控制器，并说得出判据（[[problems-traffic-signal-refuse-state-class-per-color]]、[[structure-state-table-vs-state-pattern]]）。
- 拿得出多种子随机演练的性质测试：每一 tick 冲突为空，且等待不超过一个**从控制器参数推导出来**的饿死上界（不是跑一遍观察到的数字）；不变式用显式异常而不是裸 `assert`（[[problems-traffic-signal-property-test-and-assert]]）。
- 对外只给不可变快照（当前各流向的显示），从不把内部字典交出去（[[structure-api-leaking-internals]]）。

**题解**：[[solution-traffic-signal]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
