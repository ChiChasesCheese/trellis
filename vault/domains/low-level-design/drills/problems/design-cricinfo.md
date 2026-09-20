---
nodes: [problems.games.cricinfo, patterns.observer]
tags: [problem]
---
# Drill：体育比分系统（Cricinfo）

一个像 Cricinfo 那样的板球实时比分系统：一球一球地记录比赛，随时能查总分、每位击球手的
个人成绩、每位投手的经济率。这道题的题眼是事件溯源（event sourcing），只是题面从不这么
说——**球是唯一的事件**，其余所有数字都应该是从这条事件日志现算出来的，不是被维护的字段。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：一场比赛由若干局（innings）组成，一局是一条按顺序追加的球事件
  日志。总分、击球手个人得分、投手的失分与经济率都是对这条日志的一次重放，不是增量更新
  的字段。动手前先想清楚：如果统计是被维护的字段，"改判"这个需求会有多难写？
- 第 2 关（约 20 分钟）：实现四种额外球——wide、no ball 不算合法球，bye、leg bye 算合法
  球；四者是否记到击球手个人得分、是否记到投手失分，规则两两不同。出局要换上下一位击球手。
  单数跑动和一个 over 投完，各自独立触发一次击球手轮转。
- 第 3 关（约 15 分钟）：支持第三裁判改判——只能改最近记的那一球，改完之后，wickets、
  当前击球手、投手的失分统计要全部自动跟上，不能手写任何一条"撤销"逻辑。
- 第 4 关（选做）：给一局比赛加上直播订阅，任何一球记录或改判都要通知订阅者；或者证明
  T20 换成 ODI、换成不限 over 数的 Test 赛制，除了一个数字之外不需要改动任何记分代码。
  评分点不是实现本身，而是**这两样有没有碰到第 1、2、3 关写的记分逻辑一行**。

**怎么练**：把 `vault/domains/low-level-design/problems/cricinfo/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/cricinfo -q`。

**评分点**
- 总分、wickets、击球手个人得分不是被增量维护的字段，而是对球事件日志的一次重放；说得出
  这个选择在"改判"这条路径上换来了什么（[[problems-cricinfo-derive-not-maintain]]）。
- 四种额外球的规则被整理成 `BallOutcome` 上的几个只读属性，而不是散落在重放循环里的一串
  `if`（[[problems-cricinfo-ball-outcome-properties]]）。
- 说得出 wide 和 no ball 虽然都不算合法球，为什么只有 wide 完全不计入击球手个人得分，
  no ball 打出去的分却要正常记给击球手（[[problems-cricinfo-wide-noball-simplification]]）。
- 击球手轮转是两条独立生效的规则（单数跑动、over 结束），而不是为"末球单数跑动时两次抵消"
  这个巧合场景写的一条合并特例（[[problems-cricinfo-strike-rotation-two-independent-rules]]）。
- 改判只能修正最近一球，说得出为什么允许修正任意历史事件会引入一个真实比赛里不会出现的
  问题（[[problems-cricinfo-amend-last-ball-only]]）。
- 直播订阅做成一个包住 `Innings` 的外部类，绕开它直接记分时订阅者完全收不到通知——证明
  它真的没有侵入记分核心（[[problems-cricinfo-commentary-feed-wrapper]]、[[patterns-extensibility-followup]]）。
- 给订阅者发通知时不持有自己的锁，说得出订阅者在回调里反过来调用
  `subscribe`/`unsubscribe` 会发生什么（[[problems-cricinfo-notify-outside-lock]]、[[concurrency-lock-while-calling-out]]）。
- T20/ODI/Test 三种赛制之间的差异被压缩成一个数字（每局限定几个 over），说得出为什么两局
  制的 Test 不需要任何新代码（[[problems-cricinfo-format-is-one-number]]）。

**题解**：[[solution-cricinfo]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
