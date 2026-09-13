# cd01 · Subscription email scheduler（订阅邮件调度器）

**类型：** 现场 coding / "Programming Exercise"（60 分钟，3 个部分）· **阶段：** 现场技术 coding round
· **最近一次出现：** 2025-12-08（linkjob 实习生面经；主题持续到 2026 年）
**频率：** 3 份独立来源交叉印证（linkjob 实习生 2025、linkjob「2026 Java NG VO — Email
Subscription」2025-12-08、Simplify 2026 摘要），加上第四份措辞不同的 1point3acres 记录
（「Subscription Email Scheduler」，三步目录）· **置信度：** 中等——三部分结构（排程基础 → 计划变更 →
续费）和领域（订阅生命周期邮件）有四份独立记录相互印证，但没有一份公布精确的字段名或输出格式；本
problem.md 是本套题自己给出的具体重建方案。**本题有意使用与 `problems/q07_subscription_notifications`
不同的字段/动作/输出格式（天数偏移、`[Changed]`/`[Renewed]` 标签）**——这是同一主题家族下的日历日期、
单动词单行"VO"变体；不要把两套规则混为一谈。

## 背景
一个订阅产品会发送三种生命周期邮件：订阅开始时的 `welcome`，到期前不久的 `expiring` 提醒，以及到期时的
`expired` 通知。客户也可以在订阅期内换计划、在到期前续费，或直接取消。给定一串订阅事件流，你需要打印出
系统在指定日期窗口内会发送的确切邮件集合。

## 输入（stdin）
第一行 `PART n`（`n ∈ {1,2,3}`；缺失该头部时默认使用完整的 Part 3 规则集——它是一个严格超集）。其余行，
顺序任意：

* **事件行**：`date,user,action[,plan]` —— `date` 为 `YYYY-MM-DD`。`action ∈ {subscribe,
  change, renew, cancel}`。`subscribe` 和 `change` 带第四个字段 `plan ∈ {monthly,
  annual}`；`renew` 和 `cancel` 没有第四个字段（续费保持当前计划不变）。
* **查询行**（永远是最后一个非空行）：`FROM..TO`，两个用 `..` 连接的 `YYYY-MM-DD` 日期，中间无空格。
  两端都是闭区间。如果最后一个非空行不符合这个格式，则不施加窗口过滤（等价于无界范围）——下面有几个
  测试就是只关心排程本身、不关心过滤而用到这一点。

事件在文件中**不保证按日期顺序排列**；它们始终按 `(date, 输入行序)` 处理，从不按文件顺序处理。空行会被
忽略；逗号周围的空格会被容忍。最多 10^5 条事件行。

## 输出
每一条落在 `[FROM, TO]` 区间内的邮件占一行：`date user email_type`
（`email_type ∈ {welcome, expiring, expired, renewed, canceled}`）。排序依据是 **`date`，然后 `user`
（按普通字符串顺序），然后一个固定的邮件类型优先级** —— `welcome`(0) < `expiring`(1) <
`expired`(2) < `renewed`(3) < `canceled`(4) —— **绝不按事件处理顺序排序。** 排程为空时不打印任何内容。

## 规则

### Part 1 —— 排程基础
只处理 `subscribe` 事件；`change`/`renew`/`cancel` 行在 Part 1 中会被解析但完全忽略（无影响、无输出）。
`period_days(monthly) = 30`，`period_days(annual) = 365`。对于 `date,user,subscribe,plan`：
`expire = date + period_days(plan)`；排程 `welcome@date`、`expiring@(expire-7)`、
`expiring@(expire-1)`、`expired@expire`。同一个用户可以多次 subscribe（各自独立排程；一旦引入
cancel/renew，"多次"的含义参见 Part 3）。

### Part 2 —— 带比例计算的计划变更
`change` 生效。**每一个改变状态的事件都要遵守的一条规则，永远如此：** 在事件日期 `d`，首先**丢弃该用户
所有日期严格晚于 `d` 的已排程邮件**（尚未到期——只有这些会被撤销；日期 `<= d` 的一切，包括来自更早事件、
恰好也是 `d` 的邮件，都视为已确定，*永不*撤销），然后附加基于新状态新计算出的排程。这一条规则就是
change（以及 Part 3 中的 renew 或 cancel）之后"重新排程待发的 `expiring`/`expired` 邮件"的全部逻辑。

对于用户当前周期为 `[.., expire)` 时的 `date,user,change,new_plan`：
* 如果用户未知、已取消，或 `date >= expire`（已到/过了自己的到期日——对已过期订阅做 change 是空操作），
  则忽略。
* `remaining_old = expire − date`（天数）。`remaining_new = remaining_old * period_days(new_plan)
  // period_days(old_plan)` —— **永远是整数向下取整**，不做四舍五入。`new_expire = date +
  remaining_new`。
* 用 `new_expire` 应用上面的丢弃-重排规则。`change` 本身从不产生任何邮件——它只是静默地重塑未来的排程
  （这是 cd01 与 `q07` 最大的区别，后者会打印一条明确的 `[Changed]` 行）。

### Part 3 —— 续费与取消
`renew` 和 `cancel` 在 Part 2 的基础上生效。

* `date,user,renew`：如果用户未知或已取消，则忽略。否则：
  * 如果 `date < expire`（在期限到期前续费）：`new_expire = expire +
    period_days(current_plan)` —— **从旧的到期日延长**，而不是从续费当天延长。在 `date` 发出
    `renewed`。
  * 如果 `date >= expire`（在用户自己的到期日当天或之后续费）：视为在同一计划上、从 `date` 开始的
    **全新订阅**（`new_expire = date + period_days(plan)`）。在 `date` 发出 `welcome`，而非 `renewed`。
  * 无论哪种情况，都用 `new_expire` 应用丢弃-重排规则。
* `date,user,cancel`：如果用户未知或已经取消，则忽略（幂等——再次 cancel 是静默空操作）。否则：应用
  丢弃规则（单凭这一步就能清空所有待发的 `expiring`/`expired`），在 `date` 发出 `canceled`，并将该用户
  标记为已取消。已取消用户之后的 `change`/`renew` 事件会被忽略；对该用户的一次全新 `subscribe` 会无条件
  重新开始（不检查取消标记），并且*不会*被取消状态阻止。
* 对一个当前处于活跃状态（未取消、未过期）的用户执行 `subscribe`，是一次**重新订阅**：丢弃-重排规则会
  像对待其他任何事件一样应用——它会清空旧排程中待发的未来邮件，并开启一个全新排程。

## 示例
均已用 `solution.py` 实际运行验证。

### 示例 1（Part 1）
```
PART 1
2026-01-01,alice,subscribe,monthly
2026-01-10,bob,subscribe,annual
2026-01-01..2026-12-31
```
```
2026-01-01 alice welcome
2026-01-10 bob welcome
2026-01-24 alice expiring
2026-01-30 alice expiring
2026-01-31 alice expired
```
（alice：`expire = 2026-01-31`。bob：`expire = 2027-01-10` —— annual，2026 非闰年 —— 所以 bob 的
`expiring`/`expired` 全部落在 2027 年，被查询窗口截断；只剩他的 `welcome`。）

### 示例 2（Part 2 —— 比例计算）
```
PART 2
2026-01-01,alice,subscribe,monthly
2026-01-11,alice,change,annual
2026-01-01..2026-12-31
```
```
2026-01-01 alice welcome
2026-09-04 alice expiring
2026-09-10 alice expiring
2026-09-11 alice expired
```
（`expire = 2026-01-31`；`2026-01-11` 的 `change` → `remaining_old = 20` 天；
`remaining_new = 20 * 365 // 30 = 243`；`new_expire = 2026-01-11 + 243 天 = 2026-09-11`。原本按月度
周期排程的 `expiring`/`expired` 全都晚于 `2026-01-11`，所以三条全部被丢弃并替换。）

### 示例 3（Part 3 —— 到期前续费、到期后续费、取消）
```
PART 3
2026-02-01,bob,subscribe,monthly
2026-02-20,bob,renew
2026-01-01,carol,subscribe,monthly
2026-02-15,carol,renew
2026-01-01,dave,subscribe,monthly
2026-01-15,dave,cancel
2026-01-01..2026-12-31
```
```
2026-01-01 carol welcome
2026-01-01 dave welcome
2026-01-15 dave canceled
2026-01-24 carol expiring
2026-01-30 carol expiring
2026-01-31 carol expired
2026-02-01 bob welcome
2026-02-15 carol welcome
2026-02-20 bob renewed
2026-03-10 carol expiring
2026-03-16 carol expiring
2026-03-17 carol expired
2026-03-26 bob expiring
2026-04-01 bob expiring
2026-04-02 bob expired
```
（bob 在 `2026-02-20` 续费，仍早于他的 `2026-03-03` 到期日 → `renewed`，期限从旧的结束日延长到
`2026-04-02`。carol 的月度订阅在 `2026-01-31` 到期；她在 `2026-02-15` "续费"，*已经过了*到期日，所以
这是一次全新订阅——是 `welcome`，不是 `renewed`——运行到 `2026-03-17`；她一月份的原始
`welcome`/`expiring`/`expiring`/`expired` 都不受影响，因为它们日期都早于续费事件。dave 在
`2026-01-15` 取消，早于他任何 `expiring`/`expired` 到期，全部清空；只剩下 `welcome` + `canceled`。）

## 隐藏测试已知会针对的边界情况
- **change/renew/cancel 恰好落在旧计划已排程 `expiring` 邮件的同一天，不会撤销它** —— 只有严格未来的
  日期才会被丢弃。具体来说：`2026-01-01` 订阅 annual（`expire = 2027-01-01`，
  `expiring@2026-12-25`，`expiring@2026-12-31`），然后在 `2026-12-31`（旧周期还剩一天）执行
  `change,monthly` → `remaining_new = 1*30//365 = 0` → `new_expire = 2026-12-31`（当天立即到期）——
  但两条旧的 `expiring` 邮件（`2026-12-25`、`2026-12-31`）都会保留，因为它们都不*严格晚于*事件日期；
  输出中 `2026-12-31` 这一天会有**两条**记录（按 TYPE_ORDER 先 `expiring` 后 `expired`），再加上未受
  影响的 `2026-12-25 expiring`。
- `change` 恰好落在用户自己的 `expire` 那天，是空操作（忽略，不报错）。
- 对未知用户或已取消用户的 `change`/`renew`，静默忽略。
- 对已取消用户再次 `cancel` 是空操作（幂等）。
- 在已经活跃时重新订阅，会清空旧的待发排程（Part 3）。
- 同一用户在同一天出现两条完全相同的 `subscribe` 行，**不会去重**——两条 `welcome` 邮件都会打印（第二个
  事件的 `<=d` 截断规则会保留第一条的同日 welcome）；这是故意为之——见"面试官会怎么追问" #2。
- `remaining_old == period_days(old_plan)`（在 subscribe 当天本身执行 change）恰好化简为在新计划上的
  一次全新订阅，向下取整不损失任何东西。
- 输入文件中乱序给出的事件，仍必须按日期顺序应用。
- 查询窗口边界：日期恰好等于 `FROM` 或恰好等于 `TO` 的邮件会被包含；超出任一边界一天的邮件会被排除。
- 10^5 条事件行、跨多个用户、单个查询窗口——必须保持接近线性。

## 变体
- **天数偏移 / `[Changed]`+`[Renewed]` 变体**：见 `problems/q07_subscription_notifications` ——
  同样是三部分结构（基础 → 变更 → 续费），但用整数天数偏移而非日历日期，用明确的
  `[Changed]`/`[Renewed]` 公告行而非 cd01 的静默重排。把两者当作姐妹题，而非重复题。
- linkjob 的「2026 Java NG VO — Email Subscription」提到一种"灵活的 `send_schedule` 结构，可处理多种
  触发类型"——一种泛化方案，把 `(-7, -1, 0)` 偏移量和 `{welcome, expiring, expired}` 消息集合变成可配置
  的，类似 q07 的 `schedule=` 参数。
- Simplify 的一句话概述"带订阅生命周期管理的通知调度系统"，与上述内容一致，但没有额外细节。

## 本题考察内容
技能：S01 阅读多部分题面 · S02 带可选尾字段的行解析 · S03 按用户维护可变状态 · S08 带固定（非输入决定
的）tie-break 的确定性多键排序 · S09 精确格式化 · S10 会回溯改变早期决策的事件流 · S12 日历日期运算
（`timedelta`，非闰年的年度周期）· S19 增量式设计（仅 subscribe → +change/比例计算 → +renew/cancel）

## 来源
- `loop/raw/en_forums.md` §6.2 C1（约第 303-306 行）："Part 1: 按 plan 日期发邮件（welcome、expiration
  notices）。Part 2: 根据用户输入处理 plan 变更。Part 3: 续费/延期。" [linkjob intern, 2025]；「2026
  Java NG VO - Email Subscription」灵活的 `send_schedule` [linkjob technical, 2025-12-08]；
  Simplify 一句话概述 [Simplify, 2026]。
- `loop/raw/cn_forums.md` 第 99 行：一亩三分地「Subscription Email Scheduler」导读，目录 = Part 1
  Scheduling Basics → Part 2 Changing Plans → Part 3 Handling Renewals → Solution Strategy →
  Common Follow-up Questions。[1point3acres.com/interview/post/7100084]
- `loop/raw/cn_forums.md` 第 264 行：一亩三分地「Email Notification Scheduler」（`oj` 类型，正文完整）：
  "常见追问：同一用户+类型在时间窗口内的去重/合并、按用户限流、同 `sendAt` 多任务的排序、乱序到达、
  取消/更新逻辑"。这五个追问方向被折入下面的"面试官会怎么追问"。
- `problems/q07_subscription_notifications/problem.md` —— 本题有意不重复的天数偏移姐妹变体。

## 面试官会怎么追问
1. 如果同一批事件里，同一个 user 同一天出现多条几乎相同的事件（比如客户端重试导致同一个
   `subscribe` 或 `change` 被发送了两次），你现在的实现会不会重复发邮件？上面的"重复 subscribe"边
   界例就是这个问题的答案（会重复）——你会怎么改成幂等的？给事件一个唯一 id 去重，还是在应用状态变
   更前先比较"新状态是否和当前状态相同"？
2. 如果要求"同一个用户同一天最多收 1 封邮件"（合并/限流），你会怎么在现在的排序结果上做后处理？
   直接在最终列表里按 `(date,user)` 分组只保留第一条，还是需要更细的合并规则（比如 `expired` 优
   先于 `expiring`）？
3. 输入目前假设一次性给全量事件、离线批处理；如果改成**流式**处理（事件一条条实时到达，不能重新
   排序整批数据），你的"先丢弃未来邮件再重新排程"这套模型还能用吗？需要什么样的数据结构（比如每
   个用户维护一个按日期排序的小根堆/有序容器）来保证仍然是"当前决定不了未来"的语义？
4. 现在的日期都是"请求处理所在时区"的日历日期；如果客户端传的是 UTC 时间戳，而"到期前 7 天"要按
   用户本地时区（比如美国有夏令时）计算，你的 `timedelta(days=7)` 还成立吗？DST 切换的那一周会怎
   么错位？
5. 10^5 到 10^6 条事件规模下，你的每用户"丢弃未来邮件再重建"操作复杂度是多少？是否会退化（比如一
   个用户反复 change 上千次，每次都线性扫描该用户的 pending 列表）？怎么用堆/平衡树把单用户操作降
   到 `O(log k)`（`k` = 该用户 pending 邮件数，通常 ≤ 3，所以其实已经是常数级——但如果 schedule 表
   项变多，比如从 3 种邮件类型变成 20 种，这个假设还成立吗）？
6. 如果乱序输入不只是"文件里行序打乱"，而是**真的乱序到达**（网络延迟导致一个更早日期的事件在一个
   更晚日期的事件处理完之后才到达），"先处理完的决定不可撤销"这个假设会被打破——你会怎么设计一个
   "宽限期"（grace period）让系统能接受一定程度的迟到事件而不必假装它们没发生？
7. 如果要支持"取消"之外的第四种终止状态，比如"暂停"（pause，之后可以 resume 且到期日顺延暂停天
   数），你的状态机（`plan`, `expire`, `canceled`）要怎么扩展？`resume` 事件的到期日顺延逻辑和
   `change` 的比例重算逻辑有什么本质区别？
