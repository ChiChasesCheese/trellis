# cd01 Subscription email scheduler — 报告

## 概述
这是订阅生命周期邮件系列的一次现场"Programming Exercise"实现，该系列在 Stripe 的 coding round 中反复
出现（另见 `problems/q07_subscription_notifications`）。本题版本使用日历日期和单一的可变的按用户状态机，
而不是 q07 的天数偏移量和显式的 `[Changed]`/`[Renewed]` 公告行——两者是同一主题下的姐妹题而非重复题，
两份 problem.md 文件中都互相交叉引用，避免读者混淆。核心难点在于吃透一条规则（"严格晚于事件日期的待发
邮件要丢弃，然后重新排程"），并将其统一应用到四种不同的事件类型上。

## 来源与置信度
中等。有四份独立记录相互印证（`loop/raw/en_forums.md` §6.2 C1：linkjob intern 2025、linkjob「2026
Java NG VO」2025-12-08、Simplify 2026）以及三部分结构（基础 -> 计划变更 -> 续费）与领域背景
（`loop/raw/cn_forums.md` 第 99 行：1point3acres「Subscription Email Scheduler」目录）。但没有任何来源
公布精确的字段名、输出格式或比例计算公式——这些都是本 problem.md 自己给出的具体、内部自洽的重建方案，
并在"变体"一节中明确标注。`cn_forums.md` 第 264 行的追问清单（「Email Notification Scheduler」，
去重/限流/排序/乱序/取消）确有其事，被直接折入"面试官会怎么追问"而非作为基础需求实现——原始来源本身
就将它们定位为讨论型追问，而非已实现的规则。

## 各部分思路
1. **Part 1**：纯粹的排程生成。`expire = date + period_days(plan)`
   (`monthly=30, annual=365`)；生成 `welcome@date`、`expiring@(expire-7)`、`expiring@(expire-1)`、
   `expired@expire`。
2. **Part 2**：一条规则，应用一次，Part 3 中处处复用——在事件日期 `d`，丢弃所有日期*严格晚于* `d` 的
   待发邮件（不是 `>=`；当天的邮件已经算"已确定"），然后基于新状态重新排程。`change` 的比例计算是整数
   向下取整：`remaining_new = remaining_old * period_days(new) // period_days(old)`。
3. **Part 3**：`renew` 要么从*旧*到期日延长期限（仍在有效期内），要么——如果期限已经过——变成一次全新
   的 `subscribe`（welcome，而非 renewed）。`cancel` 应用丢弃规则且无需重新排程任何新内容，并且是幂等的。

## 隐藏测试针对的坑
- **同一天、不撤销的邮件**：`change`/`renew`/`cancel` 恰好落在已排程的 `expiring` 邮件所在日期，不会撤销
  它（用 `> d`，而非 `>= d`）——会产生两行日期相同的输出，一条来自旧排程，一条来自新排程。这是本题最
  微妙的一条规则，由 `test_change_causing_immediate_expiry_keeps_same_day_old_emails` 直接验证。
- 输出顺序是**固定的类型优先级**（`welcome<expiring<expired<renewed<canceled`），而不是事件处理顺序——
  `test_same_day_cancel_then_resubscribe_orders_by_type_not_event_order` 展示了一个 `canceled` 打印在
  同一天的 `welcome` 之后，即便 cancel 先被处理。
- `change` 恰好在用户自身到期日当天，或针对未知/已取消用户，会被静默忽略（不报错、不崩溃）。
- 比例计算使用整数向下取整，绝不四舍五入——用一个 `remaining_old == period_days(old)`（正好整除，无损失）
  的用例，和一个取整到 0 的立即到期用例做对照验证。
- 重复的 `subscribe` 行故意**不去重**（这是一个已命名的追问方向，不是 bug）——
  `test_duplicate_subscribe_lines_are_not_deduplicated` 明确锁定这一点，防止候选人把它当成 bug"修掉"，
  违背既定契约。
- 输入文件中乱序的事件，仍必须按日期顺序解析处理。

## 复杂度与实测开销
事件排序为 O(n log n)；丢弃/重排步骤每个事件均摊 O(1)，因为单个用户的待发列表从不超过约 3 条。
100k 个事件、20k 个用户，输入乱序：远低于 2 秒 / 256 MB 的性能预算（见 `test_perf_100k_events`）。

## 测试清单
23 个测试 —— part1：7 个，part2：6 个，part3：10 个（含 1 个 io，1 个 perf）；edge 11 个，fmt 2 个，
io 2 个，perf 1 个。

## 考察的技能
S01 阅读多部分题面 . S02 带可选尾字段的行解析 . S03 按用户维护可变状态 . S08 带固定 tie-break 的确定性
多键排序 . S09 精确格式化 . S10 会回溯改变早期决策的事件流 . S12 日历日期运算 . S19 增量式设计

## 边写边说什么
1. **拿到题面先问**：`renew`/`cancel` 事件里没有 `plan` 字段，说明 renew 永远续同一个 plan——这个假
   设要不要跟面试官确认？如果 renew 也能顺便换 plan，规则会变成 `change`+`renew` 的组合。
2. **写 Part 1 时**：先把 `period_days` 定死成一个查表函数，说明"到期前 7 天/1 天"是从 `expire`
   往回算而不是从 `start` 往前数——这样以后无论是 `change` 还是 `renew` 改了 `expire`，公式都不用
   改，只要重新调用同一个"生成排程"的小函数。这是本题唯一值得刻意抽出来复用的地方。
3. **过渡到 Part 2 时**：提前说清楚"丢弃-重排"这一条规则要在 `change`、`renew`、`cancel` 之间完全
   复用，不要三个事件各写一套——面试官通常会在 Part 3 追问"你这段逻辑是不是可以和 Part 2 共享"，主
   动说出来能提前拿分。
4. **写比例重算时**：显式说"我用整数向下取整，不四舍五入"，并举一个"正好整除"和一个"取整到 0"的例
   子（`test_change_causing_immediate_expiry_keeps_same_day_old_emails`)，证明自己想清楚了边界。
5. **Part 3 renew 的两条分支**：讲清楚"到期前 renew = 续期"和"到期后 renew = 新订阅"是两种完全不同
   的邮件（`renewed` vs `welcome`），并且解释为什么用 `date >= expire` 而不是 `>` 做分界——因为
   `expired` 邮件本身就是在 `expire` 这一天发的，所以那一天已经算"过期状态"。
6. **收尾追问**：参考 problem.md 末尾"面试官会怎么追问"，挑 2-3 条主动展开（去重/幂等设计、流式处
   理下"决定不可撤销"假设失效、时区/DST），展示系统设计视角。

## 待解决的问题
- 比例计算公式（`remaining_old * period_new // period_old`）和"同一天邮件不撤销"规则是本套题自己的设计
  选择，追求简单、确定、可手工验证——并未对照 Stripe 真实评分标准核实（没有任何来源公布这道题的确切评分
  标准）。如果之后有更精确的题面记录出现，应优先复核这两条规则。
- `renew`/`cancel` 行按设计不携带 `plan` 字段（renew 永远保持当前 plan）；这一点在"边写边说什么" #1 中
  已标注为候选人应主动提出的开放问题。

## 复盘（2026-09-02）
**改了什么**
- `solution.py`：`_run` 原本是一个 ~56 行的大函数（四个事件类型的逻辑全部内联），超出 checklist 的
  "函数 ≤ 40 行" 建议，可读性也差（陌生人要通读整个函数才能看清一个事件类型的规则）。拆成
  `_discard_future`（"丢弃-重排"公共规则单独一个函数，供四个 handler 共用）+ `_apply_subscribe` /
  `_apply_change` / `_apply_renew` / `_apply_cancel`（每个 handler 对应 problem.md 里的一条规则，
  10 行左右）+ `_render`（过滤窗口 + 排序 + 格式化）。`_run` 现在只剩一个 10 行的分发循环，60 秒内能
  从 `main` 追到任意一个 Part 的核心规则。新增 `State`/`Emails` 类型别名和函数级 docstring
  （每个 handler 一句话说清"什么时候生效、做什么"）；`_parse` 补了返回类型标注和 docstring。公共 API
  （`part1/2/3`、`main`）未变，`starter_template.py`/`starter.py`/`test_cd01.py` 无需同步签名改动。
- `test_cd01.py`：修了 3 处 flake8 `E741`（循环变量名 `l` 与数字 `1` 易混淆），改名为 `line`；其余是
  `black -l 110` 的自动换行（长断言列表拆成多行、`import datetime` 前补空行），无语义变化。
- 三个 worked examples 逐字喂给 `python3 solution.py`，输出与 problem.md 完全一致（未改动）。
**为什么**：`_run` 超长是 S 项（可读性/函数拆分），按 checklist "S 函数 ≤ 40 行；一个函数一件事" 修；
拆分后每个 handler 直接对应题面里 `change`/`renew`/`cancel` 各自的小节，面试官对照 problem.md 读代码
更快。`E741` 是 flake8 会拦的裸红线（虽不属于 F 类，但 `loop/lint.sh` 不区分类别，全量 flake8 通过才算
过）。题面语义、排序 key、边界规则（同日邮件不撤销、`change` 恰好到期日是 no-op、幂等 cancel）均未变。
**遗留**：无。`solution.py` 已是可复用的规则表结构；problem.md"面试官会怎么追问"里的幂等去重/流式重构/
时区等追问均未实现（按设计，仅口头讨论，见 REPORT 原有"边写边说什么" #6）。
