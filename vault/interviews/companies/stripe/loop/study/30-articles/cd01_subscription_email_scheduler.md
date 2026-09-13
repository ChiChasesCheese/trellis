# cd01 · Subscription Email Scheduler：一条"丢弃-重排"规则贯穿四种事件，练的是"状态机 + 规则复用"

> [!tldr]
> - 这题考的是：把"用户订阅生命周期"建模成一个小状态机（plan / expire / canceled），四种事件
>   （subscribe / change / renew / cancel）各自更新状态，但**共用同一条"丢弃未来邮件再重排"规则**
> - 三步套路：先抽出 `(plan, expire, canceled)` 这个状态 → Part 1 只用 `subscribe` 跑通"生成排程"→
>   Part 2/3 每加一种事件，只加一个"怎么算新 `expire`"的小函数，公共规则原样复用
> - 最值得带走的一个模式：**先写清楚"谁改状态、谁读状态、公共规则是什么"，再给每种事件写一个独立的
>   小函数**——这比把四种事件的逻辑堆进一个大 `if/elif` 更容易在面试里边写边讲清楚

## 1. 题目在说什么（人话版）
一个订阅产品会在三个时间点给用户发邮件：订阅开始发 `welcome`，快到期发两次 `expiring`，到期发
`expired`。用户中途还能换 plan（`change`）、提前续费（`renew`）、取消（`cancel`）。题目给一串事件
（可能乱序），你要按事件发生的先后顺序处理它们，最后打印在某个日期区间内会实际发出的邮件。

小例子：
```
2026-01-01,alice,subscribe,monthly
2026-01-01..2026-12-31
```
```
2026-01-01 alice welcome
2026-01-24 alice expiring
2026-01-30 alice expiring
2026-01-31 alice expired
```
`monthly` 的周期是 30 天，所以 `expire = 2026-01-31`，`expiring` 分别是到期前 7 天和 1 天。

## 2. 读题：把文字变成模型
- **实体**：用户的订阅状态——`plan`（当前套餐）、`expire`（当前到期日）、`canceled`（是否已取消）。
  这三个字段就是整道题的"状态"，四种事件全部读写它们。
- **输入长什么样**：`date,user,action[,plan]`，`action` 决定要不要第四个字段；最后一行如果长得像
  `FROM..TO` 就是查询窗口，否则不过滤。事件**不保证按日期排列**，必须按 `(date, 输入序号)` 重排后
  再处理。
- **输出要什么**：`date user email_type`，按 `(date, user, 固定的邮件类型优先级)` 排序——**不是**按
  事件处理顺序，这一点最容易在写完之后忘记单独测。
- **状态**：每个用户一份 `(plan, expire, canceled)`，外加一份"这个用户目前还没发生的待发邮件列表"
  （最多 3 条：两个 `expiring` + 一个 `expired`，或者一个 `renewed`/`canceled`）。
- **一句话建模**：这是一个 **每用户一个小状态机、四种事件各自算出新状态、但共用一条"丢弃未来邮件
  再重排"规则** 的问题。

> [!note] 为什么选这个数据结构
> 候选方案是"给每个用户维护一个按时间排序的小根堆"或"直接一个 list，反正最多 3 条"。因为一个用户
> 待发邮件数量的上界是常数（≤3），排序/过滤 3 条数据用 list 完全够，堆是过度设计。真正的复杂度不在
> 数据结构上，而在"状态转移规则"——这也是为什么这题的核心是设计清楚 `_apply_change` /
> `_apply_renew` / `_apply_cancel` 这几个函数的边界条件，而不是选什么容器。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：不看实现，先把"这个类/这组函数需要哪些字段、哪些方法"写下来（见第 4 节）。哪怕只
   是空函数体 + `pass`，也要先让面试官看到你已经想清楚了状态怎么存、谁改它。
2. **骨架先行**：`main()` 读 stdin → 分离查询窗口 → 解析成事件列表 → 按日期排序 → 调
   `part1/2/3`。先让"空实现"跑起来，确认解析和分发没问题。
3. **Part 1 最小可用**：只处理 `subscribe`：算 `expire`，追加 `welcome` + 两个 `expiring` + 一个
   `expired`。立刻用题面样例自测。
4. **Part 2 叠加**：写"丢弃未来邮件"这条公共规则（一个函数，所有事件类型共用），再写 `change` 的
   比例重算。**先把公共规则抽出来，再写第一个使用它的事件**，这样 Part 3 加 `renew`/`cancel` 时不用
   再抽一次。
5. **Part 3 叠加**：`renew`/`cancel` 各自算新 `expire`（或者压根没有新 `expire`），调用同一条公共
   规则收尾。
6. **收尾**：确认排序 key 写全（含固定的邮件类型优先级）、空输入直接返回、`main` 只做 I/O。

## 4. 代码怎么组织
**接口先行**：在填任何一行状态转移逻辑之前，先把这几件事定下来——

```python
class _Sub:                    # 状态字段：一个用户当前的订阅
    plan: str; expire: date; canceled: bool

def _discard_future(lst, cutoff) -> None: ...      # 公共规则的签名，四个事件都要调用它
def _apply_subscribe(d, user, plan, state, emails) -> None: ...
def _apply_change(d, user, plan, state, emails) -> None: ...
def _apply_renew(d, user, state, emails) -> None: ...
def _apply_cancel(d, user, state, emails) -> None: ...
def _render(emails, lo, hi) -> list[str]: ...       # 只管过滤 + 排序 + 格式化
```
把这些签名写出来再填实现，好处是：面试官一眼就能看出"你的四个事件处理函数吃同样的两份状态
（`state`、`emails`），而且都要调用同一个 `_discard_future`"——这正是这题要考的设计能力，比直接扎进
`change` 的比例公式更重要。

最终的文件结构：
```
_Sub                                       # 状态：plan / expire / canceled
_parse(lines) -> (events, lo, hi)          # 只管解析 + 按 (date, 输入序号) 排序 + 拆查询窗口
_discard_future(lst, cutoff) -> None       # 公共规则：丢弃严格晚于 cutoff 的待发邮件
_apply_subscribe/_change/_renew/_cancel    # 每个事件一个函数，只管"怎么算新状态、发什么邮件"
_render(emails, lo, hi) -> list[str]       # 只管过滤窗口 + 排序 + 格式化
_run(lines, allow_change, allow_renew_cancel) -> list[str]   # 分发循环，10 行
part1/2/3(lines) -> list[str]              # 各自开关 allow_* 调 _run
main(stdin, stdout)                        # 只做分发
```
拆分原则：**状态转移和公共规则分开、每种事件一个函数、渲染单独一层**。`part1/2/3` 之间只靠两个布尔
开关区分行为，没有代码重复；后面每加一种事件类型，只需要新增一个 `_apply_*` 函数，`_run` 的分发循环
本身不用大改。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：状态转移 + 公共规则 + 分发。省略 _parse、_add_schedule 的邮件生成细节。
class _Sub:
    __slots__ = ("plan", "expire", "canceled")
    def __init__(self, plan, expire, canceled=False):
        self.plan, self.expire, self.canceled = plan, expire, canceled

def _discard_future(lst, cutoff):                  # 公共规则：四个事件都调用它
    lst[:] = [e for e in lst if e[0] <= cutoff]     # 只丢弃严格晚于 cutoff 的，同日的算已提交

def _apply_change(d, user, plan, state, emails):    # 事件处理函数的代表：change
    sub = state.get(user)
    if sub is None or sub.canceled or d >= sub.expire:
        return                                       # 未知用户 / 已取消 / 已过期：静默忽略
    lst = emails.setdefault(user, [])
    _discard_future(lst, d)
    remaining_old = (sub.expire - d).days
    remaining_new = remaining_old * PERIOD_DAYS[plan] // PERIOD_DAYS[sub.plan]  # 向下取整
    new_expire = d + timedelta(days=remaining_new)
    _add_schedule(lst, new_expire, d)
    sub.plan, sub.expire = plan, new_expire

def _run(lines, allow_change, allow_renew_cancel):   # 分发循环：谁调用哪个 _apply_*
    events, lo, hi = _parse(lines)
    state, emails = {}, {}
    for d, _, user, action, plan in events:
        if action == "subscribe":
            _apply_subscribe(d, user, plan, state, emails)
        elif action == "change" and allow_change:
            _apply_change(d, user, plan, state, emails)
        elif action == "renew" and allow_renew_cancel:
            _apply_renew(d, user, state, emails)
        elif action == "cancel" and allow_renew_cancel:
            _apply_cancel(d, user, state, emails)
    return _render(emails, lo, hi)

def part1(lines):
    return _run(lines, allow_change=False, allow_renew_cancel=False)
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：`renew`/`cancel` 没有 `plan` 字段，说明续费一定续同一个 plan——这个假设对
  吗？」
- 写接口时：「我先把状态定成 `(plan, expire, canceled)`，四种事件都是读它、改它；再定义一条公共的
  '丢弃未来邮件'规则，等下 `change`/`renew`/`cancel` 都会调用它，这样我不用在每个事件里重复写一遍
  过滤逻辑。」
- 写 `change` 时：「比例重算我用整数向下取整，不四舍五入；如果面试官问'为什么不是四舍五入'，我会说
  金额/天数类的计算一般默认向下取整，除非题面另有说明。」
- 被问"如果要加第五种事件、比如'暂停'"：「我只需要新写一个 `_apply_pause`，签名跟其他事件一样吃
  `(d, user, state, emails)`，内部改 `state` 再调 `_discard_future` 就行——不用碰 `_run` 的分发循环
  之外的东西，因为公共规则已经抽出来了。」这是接口先行带来的好处：新增状态转移不需要重新设计。
- 交付时：「三个样例都过了；如果时间允许，我会把'同一用户同一天多条重复事件是否去重'这个追问的方案
  说一下，但不现场实现，因为题面没要求。」

## 7. 常见跑偏（方法层面，3 条）
- **把四种事件的逻辑全塞进一个大 `if/elif` 函数**：能跑，但函数很快超过 40-50 行，面试官读起来要
  在一个函数里同时跟踪四套状态转移条件。先把"公共规则"和"每种事件"拆成独立函数，再用一个薄的分发
  循环把它们接起来。
- **公共规则写了四遍**：`change` 里写一次"丢弃未来邮件"，`renew`/`cancel` 各自再写一遍——第三遍开始
  就是复制粘贴，后来改一处漏一处。第一次用到这条规则时就应该把它抽成函数。
- **状态字段想到哪加到哪**：先不定义 `_Sub` 有哪些字段，写 `change` 时才发现还需要记"是否取消"，
  回头改数据结构。花两分钟先把状态字段列全（这题就是 `plan`/`expire`/`canceled` 三个，不多不少），
  比边写边加字段省时间。

## 8. 同族题 / 延伸
- OA 侧：`problems/q07_subscription_notifications` 是同一主题的兄弟题——用整数天偏移量代替日历日期，
  且每次 `change`/`renew` 会显式打印 `[Changed]`/`[Renewed]` 公告行，而 cd01 是"静默重排"，两题共享
  "多 part 递进 + 状态机"的骨架但规则不同，不要混用。
- 其他轮：cd02 `payment_ledger`、cd03 `account_scheduler_lru` 都是"接口先行"同一方法论的另一种应用——
  先定状态字段和方法签名，再填实现。
- 延伸思考：如果输入是真正的实时流（事件到达顺序不可控，不能整批重排），"当前决定不能被撤销"这个
  假设会被打破；`_discard_future` 这条规则本身需要改成"允许一个宽限期内的迟到事件"。
- 练习命令：`python3 loop/mock.py start cd01`
