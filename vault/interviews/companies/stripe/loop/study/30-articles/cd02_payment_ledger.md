# cd02 · PaymentLedger：一个"接口先行"的类设计题，练的是把三种失败分成三种形状

> [!tldr]
> - 这题考的是：给一个单商户的支付/退款账本设计一个类——先记支付、再叠部分退款、最后加区间查询和持久化；难点不在算法，而在**错误契约**（幂等 `False` / `KeyError` / `ValueError`）要三个 Part 一以贯之
> - 三步套路：先把 6 个方法签名和 2 个状态字段写在纸上 → Part 1 用一个 dict 跑通"存 + 查重 + 求和" → 后面每个 Part 只在已有字段上加规则，不加第二份真相
> - 最值得带走的一个模式：**接口先行**——类设计题先写"方法签名 + 状态字段"的空壳，再逐个填实现；实现是可以改的，接口改一次就要动所有调用方

## 1. 题目在说什么（人话版）
Stripe 内部工具组需要一个不依赖数据库的小对象，帮一个商户记账：收了哪些钱、退了多少、现在净收入是多少、某段时间内有哪些支付。
面试官不会一次把需求说完，而是分三段"揭牌"：

1. `add_payment` + `get_total_revenue`：记支付，算总收入；同一个 `payment_id` 再来一次要**当作重试**，静默忽略；
2. `add_refund`：对某笔支付退款，可以分几次退，累计不能超过原金额；
3. `get_payments_by_date` + `export_json` / `load_json`：按时间区间查支付，以及把账本整个序列化再恢复。

小例子：
```
add_payment("p1", 1000, ...)   → True      add_refund("r1", "p1", 300, ...) → True
add_payment("p2",  500, ...)   → True      add_refund("r2", "p1", 400, ...) → True
add_payment("p1",  999, ...)   → False     get_total_revenue()              → 800
```
`p1` 的第二次提交是重试，不改原记录；退了 700 之后 `1500 - 700 = 800`。

和 ps01 那种"读 stdin → 算 → 打印"的流水线题不同，这题**类本身就是交付物**。三个 Part 是同一个对象上累加的方法，不存在"Part 1 的类"和"Part 2 的类"。评估重点（来自源材料）是"面向对象设计、边界处理、代码清晰度、可扩展性"，不是复杂算法。

## 2. 读题：把文字变成模型
- **实体**：支付（`payment_id, amount_cents, ts, customer`）、退款（`refund_id, payment_id, amount_cents, ts`）。退款是"挂在某笔支付上的扣减"，不是独立实体。
- **输入长什么样**：方法调用，参数都是标量。金额是**整数分**；时间戳只有一种固定形状 `YYYY-MM-DDTHH:MM:SS`，不合法就抛 `ValueError`，三个接收时间戳的方法都要校验。
- **输出要什么**：`add_*` 返回 `bool`（`True` 记了 / `False` 幂等忽略），错误情况抛异常；`get_payments_by_date` 返回固定形状的 dict 列表，按 `(ts, payment_id)` 排。
- **状态**：一个 `dict[payment_id -> Payment]`（每条带 `refunded_cents` 累计值），加一个 `set[refund_id]`。第二个集合是这题最容易漏的状态——没有它，退款重试就会被记两次。
- **一句话建模**：这是一个 **按 payment_id 索引的记录表 + 已处理事件 id 集合** 的幂等账本，三个 Part 只是往同一份状态上加读写规则。

> [!note] 为什么选这个数据结构
> 候选是"一个 list 按时间顺序存所有事件，每次查询重放"（事件溯源），或"一个 dict 存每笔支付的当前状态"。前者更通用（追问里的审计日志就是它），但 Part 1/2 的每个操作都要先在 list 里找到那笔支付，O(n)。后者让 `add_payment` / `add_refund` 都是 O(1) 的 dict 操作，退款累计值直接挂在记录上。面试先选后者，把事件溯源留作追问时的口头升级。`refund_ids` 单独用一个 `set` 而不是存在每笔支付下面，是因为幂等检查发生在"找到那笔支付"**之前**（顺序见 Part 2 规则）。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先把类的空壳写出来——6 个方法的签名（参数名、类型、返回值）+ `__init__` 里的两个状态字段，每个方法体 `raise NotImplementedError`。花 2 分钟，和面试官对一遍："重复 id 返回 `False` 还是抛异常？金额是分？时间戳格式固定？"这一步定下来，后面三个 Part 都不用改签名。
2. **时间戳校验器**：`_validate_ts(ts) -> ts`，正则查形状 + `strptime` 查日历合法性。这是三个方法共用的第一行，先写它。
3. **Part 1 最小可用**：`add_payment` = 校验 → `in` 查重 → 存 `Payment`；`get_total_revenue` = 对 `net_cents` 求和。用样例 1 自测（三次 `add_payment` 返回 `True/True/False`，revenue 1500）。
4. **Part 2 叠加**：`add_refund` 按固定顺序写四个检查（时间戳 → `refund_id` 重复 → `payment_id` 不存在 → 超额），成功路径两行：累加 `refunded_cents`、把 `refund_id` 放进 set。`get_total_revenue` **一行不改**——因为 Part 1 就把它写成了 `amount - refunded` 的和。
5. **Part 3 叠加**：`get_payments_by_date` = 校验两个边界 → 过滤 → 排序 → `asdict`；`export_json` 把两个状态字段原样倒出来，`load_json` 原样装回去。
6. **收尾**：跑样例 4 的命令流；对着 `add_refund` 的四个检查再念一遍顺序；确认排序 key 写全了 `(ts, payment_id)`。

## 4. 代码怎么组织
```
_validate_ts(ts) -> ts                       # 只管校验，三个方法共用；不合法抛 ValueError
@dataclass Payment                           # 一条记录：4 个输入字段 + refunded_cents 累计；net_cents property
class PaymentLedger:
    _payments: dict[str, Payment]            # 状态 1：按 payment_id 索引
    _refund_ids: set[str]                    # 状态 2：已处理的退款 id（幂等 + 持久化都靠它）
    add_payment / get_total_revenue          # Part 1
    add_refund                               # Part 2：四个检查按固定顺序
    get_payments_by_date / export_json / load_json   # Part 3
_cmd_pay / _cmd_refund / _cmd_revenue / _cmd_range   # 命令流 harness：异常 → 文本，只在这一层
COMMANDS = {"PAY": _cmd_pay, ...}            # 动词 → 处理函数的分发表
run_commands(lines) / main(stdin, stdout)    # 只做分发
```
**接口先行**的具体做法：先写 `class PaymentLedger` 的方法签名和 `__init__` 里的两个字段，然后写 `Payment` 的字段列表，最后才填方法体。签名是和面试官的合同，字段是你对"要记住什么"的回答，两者定了，实现就是填空。**记录用 `dataclass` 而不是 dict**：`p.refunded_cents` 比 `p["refunded"]` 少一类拼写 bug，`asdict(p)` 直接就是 `get_payments_by_date` 要的输出形状，`Payment(**row)` 直接就是 `load_json` 的反序列化。**类不知道 CLI**：`add_refund` 抛 `KeyError`，把它翻译成 `REFUND r1 ERROR unknown_payment p1` 这件事发生在 `_cmd_refund` 里——面试官问"换成 HTTP API 怎么办"，你指着 harness 层说"只换这几个函数"。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
@dataclass
class Payment:                                    # 一条记录；refunded_cents 是 Part 2 唯一新增的状态
    payment_id: str; amount_cents: int; ts: str; customer: str; refunded_cents: int = 0
    @property
    def net_cents(self) -> int:                   # 既是"还能退多少"也是"贡献多少 revenue"
        return self.amount_cents - self.refunded_cents

class PaymentLedger:
    def __init__(self) -> None:
        self._payments: dict[str, Payment] = {}   # 状态 1：按 payment_id 索引
        self._refund_ids: set[str] = set()        # 状态 2：没有它，退款重试会记两次

    def add_payment(self, payment_id, amount_cents, ts_iso, customer) -> bool:
        _validate_ts(ts_iso)                      # 先校验再碰状态：重复 id + 坏时间戳照样抛
        if payment_id in self._payments:
            return False                          # 幂等重试，原记录不动
        self._payments[payment_id] = Payment(payment_id, amount_cents, ts_iso, customer)
        return True

    def get_total_revenue(self) -> int:
        return sum(p.net_cents for p in self._payments.values())   # Part 2 来了也不用改

    def add_refund(self, refund_id, payment_id, amount_cents, ts_iso) -> bool:
        _validate_ts(ts_iso)                      # 1. 坏时间戳 → ValueError
        if refund_id in self._refund_ids:
            return False                          # 2. 重复 refund_id → 幂等 False
        payment = self._payments.get(payment_id)
        if payment is None:
            raise KeyError(payment_id)            # 3. 支付不存在 → KeyError（调用方 bug）
        if amount_cents > payment.net_cents:
            raise ValueError("refund exceeds remaining balance")   # 4. 超额；刚好退完允许
        payment.refunded_cents += amount_cents
        self._refund_ids.add(refund_id)
        return True

    def get_payments_by_date(self, start_iso, end_iso) -> list[dict]:
        lo, hi = _validate_ts(start_iso), _validate_ts(end_iso)        # 先校验边界
        rows = [p for p in self._payments.values() if lo <= p.ts <= hi]  # 固定宽度串：字符串序 == 时间序
        rows.sort(key=lambda p: (p.ts, p.payment_id))                    # tie-break 写全
        return [asdict(p) for p in rows]
```
只放类本身：状态 → 三个 Part 的规则。省略了 `_validate_ts`（正则 + `strptime`）、`export_json` / `load_json`（把两个状态字段原样倒出/装回）和命令流 harness。

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先把接口定下来：金额用整数分；时间戳只接受 `YYYY-MM-DDTHH:MM:SS`，不合法抛 `ValueError`；重复的 `payment_id` 我当成重试，返回 `False` 不抛异常——分布式系统里重试太常见，接口应该对它宽容。这几条如果您有不同意见我现在改签名。」
- 写 Part 1 时：「状态就一个 dict，按 `payment_id` 索引。`get_total_revenue` 我直接写成 `amount - refunded` 的和，虽然现在 refunded 恒为 0——这样等会儿加退款的时候这个方法不用动。」
- 写 Part 2 时：「退款可能有三种失败，我用三种形状区分：重复 `refund_id` 是重试，返回 `False`；`payment_id` 不存在是调用方 bug，抛 `KeyError`；超额是业务规则，抛 `ValueError`。检查顺序是固定的——先校验时间戳，再查重，再查支付，最后比金额。查重放在比金额前面，是为了让一个已经成功过的退款重放时永远不报错。」
- 被追问"部分退款/多次退款"时：「累计值挂在 `Payment.refunded_cents` 上，`net_cents` 就是还能退的额度，所以多次退款天然支持；刚好退完允许，多一分抛异常。」不要现场去改成"每笔退款单独存一条"——那是审计追问的答案，口头带过即可。
- 被追问"持久化到数据库"时：「`export_json` / `load_json` 是内存版的等价物，关键是**两个状态字段都要序列化**——只存 `refunded_cents` 恢复不出'哪些 refund_id 处理过'，重放会被记两次。换成真数据库，'先查后写'要变成唯一约束 + 捕获冲突异常，否则并发下两个 `add_payment` 都会读到'不存在'。」说到这里就够了，不要真的开始写 SQL。
- 被追问"海量数据查询"时：「现在是线性扫描，10^5 没问题。要支撑高频区间查询，我会维护一个按 `ts` 排序的列表，用 `bisect` 定位两端，插入时 `insort`——但那是索引层的事，类的接口不变。」
- 交付时：「四个样例都过了。`get_total_revenue` 我保持每次求和而不维护 running total，避免两份真相不同步；如果读远多于写，把它换成 O(1) 只需在 `add_*` 里各加一行。」

## 7. 常见跑偏（方法层面，3 条）
- **没定接口就开始写实现**：一上来在 `add_payment` 里写 dict 操作，写到 Part 2 发现"重复 id 到底返回什么"没定，回头改签名、改测试、改调用方。先花两分钟写空壳，把返回值和异常类型和面试官对齐，再填。
- **三种失败用一个 `Exception`**：重复、不存在、超额全抛 `Exception("error")`，调用方无法区分"该重试"和"该报警"。错误契约是这题的评估点之一，不同情况用不同形状，并且顺序固定。
- **状态越写越多、越写越散**：Part 2 加一个 `_refund_totals` dict，Part 3 加一个 `_by_ts` list，每个 dict 都是一份要同步的真相。回到"要记住什么"这个问题：一张记录表 + 一个 id 集合就够，累计值放在记录上，排序在查询时做。

## 8. 同族题 / 延伸
- OA 侧：q13 `account_balance_ledger` 与 q27 是同一个"按 id 索引的记录 + 幂等去重"骨架（S11/S17）；LC 2043 Simple Bank System（A08）是它的裸算法版——转账/存取的校验顺序和这题的四步检查一模一样。
- 其他轮：cd03 `account_scheduler_lru` 同样是"接口先行"的类设计题，只是状态换成了 `OrderedDict`；ps06 `receivables_registration` 的幂等注册和这题的 `refund_ids` 集合是同一个念头。
- 延伸思考：把 `Payment` 改成"支付 + 退款事件列表"就是追问 #6 的审计版本，`net_cents` 变成对事件求和，`get_total_revenue` 不用改；把 `_validate_ts` 换成"多格式尽量兼容、明确拒绝"的解析器是追问 #3，类的其他部分一行不动。
- 练习命令：`python3 loop/mock.py start cd02`
