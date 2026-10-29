# 支付类设计：五道练习题

类设计（OOD，面向对象设计）这一轮考的不是新算法，而是把几种数据结构拼成一个类：每个操作都够快，几份结构之间始终一致，面试官一条一条加需求时只改一处就能接住。支付味道的类设计多了四条硬约束：金额用整数最小货币单位，时间从外部注入，重复调用只产生一次效果，每个结果都能追溯到产生它的规则和版本。下面五道题覆盖这个组最可能出的形状：带规则的计费 / 计税引擎、复式账本、幂等转账、分期计划、按商户限流。每道题给题面、数据结构和原因、不变量、一份不超过 40 行的 Python 骨架、追问和一行回答要点。

## 一道题怎么走（30–45 分钟）

1. **澄清**（3 分钟）：金额单位和币种、并发吗、要持久化吗、错误怎么报。
2. **接口**（2 分钟）：先写方法签名和返回值，让面试官确认。
3. **数据结构**（5 分钟）：每个操作用哪个结构、复杂度多少、为什么不用另一个。
4. **不变量**（2 分钟）：说出一两条「任何时候都成立」的性质，并在代码里检查它。
5. **核心方法**（15–20 分钟）：先写最关键的一个方法，能跑。
6. **测试**（5 分钟）：正常、边界、重复调用、非法输入各一个。
7. **追问**（剩下的时间）：每条新需求说清改哪一处。

## 五道题一览

| # | 题 | 核心结构 | 组合骨架 | 相邻的编码题 |
|---|---|---|---|---|
| 1 | 计费 / 计税引擎 | 每个商户一列按生效时间排序的规则版本 + 二分 | 有序数组 + 二分；规则链 | 时间戳 KV、OrderValidator |
| 2 | 复式账本 | 只追加的分录列表 + 按 ID 的哈希表 + 余额索引 | 主存储 + 派生索引 | 快照 KV |
| 3 | 幂等转账 | 幂等键表 + 账本 | 进行中表（合并重复请求） | 幂等的版本化更新 |
| 4 | 分期计划生成器 | 纯函数 + 不可变的分期列表 | 无状态计算 | 汇率换算 |
| 5 | 按商户限流 | 哈希表 + 访问顺序队列（LRU）+ 令牌桶 | 哈希表 + 链表 | 限流器、带 TTL 的 LRU |

- 组合骨架的总览在 Anki `LeetCode Tops::26 工具里的数据结构与算法` 的 `12 数据结构组合` 分支，Obsidian 入口 [[domains/under-the-hood/map/compose.patterns|组合模式总览]]。
- 编码题在 Anki `LeetCode Tops::24 TikTok 字节高频 · 整题答案`，Obsidian 入口 [[interviews/core/leetcode/tiktok/map/patterns.design|数据结构设计题]] 和 [[interviews/core/leetcode/tiktok/map/python.classes-design|设计题的 Python 写法]]。

## 1. 计费 / 计税引擎

**题面**：给每个商户配置一组费用规则（例如「2.9% + 0.30」），再在费用之上收税（例如费用的 10%）。`quote(txn)` 返回每一行费用：规则 ID、规则版本、金额。商户的规则会改，新规则从某个时间点起生效；历史交易必须按**交易发生时**生效的规则计算。

**数据结构和原因**：

- 每个商户一个按生效时间升序的列表 `starts`，和一个同下标的规则版本列表。查某个时间点生效的版本 = 在 `starts` 上二分，O(log V)。这和「基于时间的键值存储」是同一个结构。
- 规则版本只能追加、时间只能往后：修正历史定价靠发布新版本，不改旧版本，这样任何一行费用都能复现。
- 一个版本里的规则是**有序的链**：每条规则拿到交易和「前面各行的合计」，所以「税算在费用之上」只是链上靠后的一条规则。规则是可调用对象，加一种规则不用改引擎。
- 金额用整数分，规则内部用 `Decimal` 全精度计算，每一行只取整一次（银行家舍入）。

**不变量**：

- 每一行费用都带规则 ID 和版本号，能复现。
- 没有生效规则时**报错**，而不是返回 0（返回 0 就是「有交易没费用」的静默 bug）。
- 同一笔交易、同一版本，结果永远相同（纯函数）。

```python
from bisect import bisect_right
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN
from typing import Callable

@dataclass(frozen=True)
class Txn:
    merchant: str
    amount: int                # minor units
    ts: int                    # event time, epoch seconds

Rule = Callable[[Txn, int], Decimal | None]   # (txn, sum of earlier lines) -> fee, None = n/a

def percent_plus_fixed(bps: int, fixed: int) -> Rule:     # 290 bps = 2.9 %
    return lambda t, prior: Decimal(t.amount) * bps / 10_000 + fixed if t.amount > 0 else None

def tax_on_fees(bps: int) -> Rule:
    return lambda t, prior: Decimal(prior) * bps / 10_000

class FeeEngine:
    def __init__(self) -> None:
        self._starts: dict[str, list[int]] = {}
        self._versions: dict[str, list[tuple[tuple[str, Rule], ...]]] = {}
    def publish(self, merchant: str, effective_from: int, rules: tuple[tuple[str, Rule], ...]) -> int:
        starts = self._starts.setdefault(merchant, [])
        if starts and effective_from <= starts[-1]:
            raise ValueError("versions only move forward")
        starts.append(effective_from)
        self._versions.setdefault(merchant, []).append(rules)
        return len(starts)                                 # version number
    def quote(self, t: Txn) -> list[tuple[str, int, int]]:  # (rule id, version, amount)
        v = bisect_right(self._starts.get(t.merchant, []), t.ts)
        if v == 0:
            raise LookupError(f"no schedule for {t.merchant} at {t.ts}")  # fail loudly
        lines: list[tuple[str, int, int]] = []
        for rule_id, rule in self._versions[t.merchant][v - 1]:
            amt = rule(t, sum(a for _, _, a in lines))
            if amt is not None:
                lines.append((rule_id, v, int(amt.quantize(Decimal(1), ROUND_HALF_EVEN))))
        return lines
```

**追问**：

- **加阶梯费率、封顶和保底？** 新写一种规则；封顶 / 保底可以是包在另一条规则外面的装饰规则，引擎不动。
- **规则之间有依赖，顺序不是简单列表？** 把规则依赖建成有向无环图，发布时做一次拓扑排序，得到链的顺序；有环就拒绝发布。这就是 OrderValidator 那道题。
- **多币种？** 交易带币种，固定费用按币种配置；取整按该币种的小数位。
- **发布了错的规则，已经算出的费用怎么办？** 不改旧行：发布新版本，再对受影响的交易写**调整行**，差额 = 新版本结果 − 旧行。
- **规则热更新、多实例一致？** 规则是版本化数据，实例按版本号拉取；费用行记下版本号，所以即使两个实例短暂不一致也能事后核对。
- **线程安全？** 读多写少：发布时构造新列表再整体替换引用，读路径不加锁。

**相关**：[[interviews/core/leetcode/tiktok/map/a.time-based-key-value-store|时间戳 KV（同样的二分）]] · [[interviews/core/leetcode/tiktok/map/a.tt-ai-assisted-order-validator|OrderValidator（规则 DAG）]] · [[domains/under-the-hood/map/compose.interceptor-chain|拦截器链：列表 + 游标]]

## 2. 复式账本

**题面**：实现一个账本。`post(entry)` 写入一条分录，分录有若干条腿（账户、币种、带符号金额）；`balance(account, currency)` 返回余额；`reverse(entry_id)` 冲正一条分录。同一条分录被重复提交时只记一次。

**数据结构和原因**：

- `_journal`：只追加的分录列表，是唯一的事实来源；审计和重算都从它出发。
- `_by_id`：分录 ID → 分录的哈希表，O(1) 判断重复提交，并检查「同一个 ID 不能带不同的腿」。
- `_bal`：(账户, 币种) → 余额的哈希表，是从分录**派生出来的索引**，每次写分录时在同一步更新，读余额 O(1)。代价：它必须和分录同时更新，生产里就是同一个数据库事务。
- 这里用带符号金额的简写：一条分录所有腿之和为 0。正数让账户余额增加，负数让它减少；各腿之和为 0，所以钱只会从一个账户移到另一个账户，不会凭空出现。要对应会计的借贷方向，只需给每类账户标一个正常余额方向。

**不变量**：

- 每条分录至少两条腿，并且**按币种**分别求和为 0。
- 任何账户的余额 = 该账户所有腿之和；`_bal` 随时可以从 `_journal` 重算。
- 分录写入后不修改；纠错只靠反向的新分录。

```python
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class Posting:
    account: str
    currency: str
    amount: int                       # signed minor units; legs of one entry sum to 0

@dataclass(frozen=True)
class Entry:
    id: str
    postings: tuple[Posting, ...]
    reverses: str | None = None

class Ledger:
    def __init__(self) -> None:
        self._journal: list[Entry] = []                   # append-only
        self._by_id: dict[str, Entry] = {}
        self._bal: dict[tuple[str, str], int] = defaultdict(int)
    def post(self, e: Entry) -> Entry:
        if e.id in self._by_id:                           # replay of the same entry: no-op
            if self._by_id[e.id] != e:
                raise ValueError("entry id reused with different legs")
            return self._by_id[e.id]
        net: dict[str, int] = defaultdict(int)
        for p in e.postings:
            net[p.currency] += p.amount
        if len(e.postings) < 2 or any(net.values()):
            raise ValueError(f"unbalanced entry {e.id}: {dict(net)}")
        self._journal.append(e)
        self._by_id[e.id] = e
        for p in e.postings:
            self._bal[(p.account, p.currency)] += p.amount
        return e
    def reverse(self, entry_id: str, new_id: str) -> Entry:  # correct by a new entry, never by editing
        legs = tuple(Posting(p.account, p.currency, -p.amount) for p in self._by_id[entry_id].postings)
        return self.post(Entry(new_id, legs, reverses=entry_id))
    def balance(self, account: str, currency: str) -> int:
        return self._bal.get((account, currency), 0)
```

**追问**：

- **冻结和可用余额？** 加一个冻结表 (账户, 冻结 ID) → 金额；可用余额 = 余额 − 冻结合计；冻结和释放各自幂等。
- **不允许透支？** 在 `post` 里对用户类账户检查「写入后余额 ≥ 0」，检查和写入必须在同一把锁或同一个事务里。
- **并发？** 按账户加锁，多个账户时按账户 ID 排序加锁，避免死锁；数据库里用 `SELECT … FOR UPDATE` 或带条件的 `UPDATE`。
- **热点账户每秒几万次写？** 不更新单行余额：只追加分录，余额按时间片汇总，读时取最近快照加之后的增量。
- **怎么证明账没被改过？** 定期从 `_journal` 重算全部余额和 `_bal` 比对；所有账户总和按币种为 0；分录按块加哈希链。
- **跨币种转账？** 两组腿，各自平衡：用户 USD 减少、FX 中间账户 USD 增加；FX 中间账户 MYR 减少、对方 MYR 增加。

**相关**：[[domains/under-the-hood/map/compose.k8s-indexer|主存储 + 二级索引]] · [[interviews/core/leetcode/tiktok/map/a.tt-kv-store-snapshot-restore|快照与恢复 KV]] · [[sd09-wallet-ledger]]

## 3. 幂等转账服务

**题面**：`transfer(client, key, src, dst, amount, currency)` 从一个钱包转钱到另一个。客户端会因超时重试，同一个 `key` 可能到达多次、甚至同时到达。要求：同一个键只转一次，重试拿到和第一次相同的结果；同一个键配不同的请求要拒绝；余额不足时拒绝，并且这个拒绝结果也要被记住。

**数据结构和原因**：

- 幂等键表：(调用方, 键) → 记录（请求指纹、结果）。键按调用方隔离，因为不同客户端可能生成相同的字符串。
- 请求指纹 = 请求内容的哈希，用来发现「同一个键、不同请求」的客户端 bug。
- 结果为空表示第一次请求还在处理中：并发到达的重复请求直接返回「请稍后重试」，不会执行第二次。
- 两步走：第一步「占键」（生产里是对唯一约束的插入）；第二步「检查余额 + 记账 + 保存结果」放在**同一个事务**里，所以要么都发生，要么都不发生。

**不变量**：

- 一个键最多产生一条账本分录（分录 ID 由键派生，账本层再兜一次底）。
- 已完成的键，返回的结果永远和第一次相同，包括「余额不足」。
- 余额检查和扣款之间没有其他转账插进来。

```python
import hashlib, json, threading
from dataclasses import dataclass
from ledger import Entry, Ledger, Posting

@dataclass
class KeyRecord:
    fingerprint: str
    result: dict | None = None        # None while the first request is still running

class Conflict(Exception): ...

class TransferService:
    def __init__(self, ledger: Ledger) -> None:
        self._ledger = ledger
        self._keys: dict[tuple[str, str], KeyRecord] = {}   # (client, key) -> record
        self._lock = threading.Lock()                       # stands in for DB transactions

    def transfer(self, client: str, key: str, src: str, dst: str, amount: int, ccy: str) -> dict:
        if amount <= 0:
            raise ValueError("amount must be positive")
        body = json.dumps([src, dst, amount, ccy]).encode()
        fp = hashlib.sha256(body).hexdigest()
        with self._lock:                                    # step 1: claim the key (unique insert)
            rec = self._keys.get((client, key))
            if rec is not None:
                if rec.fingerprint != fp:
                    raise Conflict("key reused with a different request")   # 422
                if rec.result is None:
                    raise Conflict("first request still in progress")       # 409, retry later
                return rec.result                                         # replay stored answer
            self._keys[(client, key)] = KeyRecord(fp)
        with self._lock:                                    # step 2: check + post + store, one transaction
            if self._ledger.balance(src, ccy) < amount:
                result = {"status": "rejected", "reason": "insufficient_funds"}
            else:
                legs = (Posting(src, ccy, -amount), Posting(dst, ccy, amount))
                self._ledger.post(Entry(f"tr:{client}:{key}", legs))
                result = {"status": "succeeded"}
            self._keys[(client, key)].result = result
        return result
```

**追问**：

- **第一步之后进程崩溃，键永远停在处理中？** 记录里加开始时间；恢复任务扫描超时的「处理中」键，按同一个键重放第二步（第二步本身幂等）。
- **第二步要调外部 PSP，不能放进数据库事务？** 用 outbox：事务里写「待发送的 PSP 请求」，后台用同一个幂等键发送；PSP 超时记为 unknown，查询有定论后再写结果。
- **幂等键存多久？** 至少覆盖客户端的最长重试窗口（常见 24 小时到几天），过期后按时间分区批量删除。
- **多实例部署？** 内存锁换成数据库的唯一约束和行锁；键表和账本在同一个库里，才能同一事务提交。
- **同一个账户被高并发转出？** 按账户串行化（行锁或按账户分区的队列），检查余额用带条件的更新：`UPDATE … SET balance = balance − x WHERE balance ≥ x`。

**相关**：[[domains/under-the-hood/map/compose.singleflight|singleflight：合并重复请求]] · [[interviews/core/leetcode/tiktok/map/a.tt-idempotent-versioned-update|幂等、带版本号的数据更新]] · [[tiktok-idempotency-transactions]]

## 4. 分期计划生成器

**题面**：给定本金（分）、期数、年化利率（基点，1200 = 12%）和起始日期，生成每月一期的还款计划：每期的到期日、本金、利息。利率为 0 时是免息分期。

**数据结构和原因**：

- 纯函数，输入相同输出相同，方便测试和审计；输出是不可变的 `Instalment` 列表。
- 到期日**每次都从起始日期加 k 个月**，而不是在上一期日期上加 1 个月：1 月 31 日起算时，逐期累加会变成 2 月 28 日、3 月 28 日……永久漂移。月末日期按当月天数截断。
- 免息时用整数除法加余数分配，保证各期本金之和恰好等于本金。
- 有息时按等额本息公式算出每期还款额并取整，利息按剩余本金逐期计算，**最后一期吸收所有取整误差**。

**不变量**：

- 各期本金之和 == 本金，一分不差。
- 到期日严格递增；没有负数金额。
- 例：120000 分、12 期、1200 基点，每期 10662，第 1 期利息 1200、本金 9462，最后一期 10660，总利息 7942。

```python
import calendar
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN

@dataclass(frozen=True)
class Instalment:
    seq: int
    due: date
    principal: int                     # minor units
    interest: int

def add_months(d: date, k: int) -> date:  # Jan 31 + 1 month = Feb 28/29, clamped
    y, m = divmod(d.month - 1 + k, 12)
    year, month = d.year + y, m + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))

def schedule(principal: int, n: int, apr_bps: int, start: date) -> list[Instalment]:
    if principal <= 0 or n <= 0:
        raise ValueError("principal and n must be positive")
    due = [add_months(start, i + 1) for i in range(n)]   # always from start: no drift
    if apr_bps == 0:                                     # pay-in-n, interest free
        base, extra = divmod(principal, n)
        return [Instalment(i + 1, due[i], base + (1 if i < extra else 0), 0) for i in range(n)]
    r = Decimal(apr_bps) / 10_000 / 12
    pay = int((principal * r / (1 - (1 + r) ** -n)).quantize(Decimal(1), ROUND_HALF_EVEN))
    out: list[Instalment] = []
    bal = principal
    for i in range(n):
        interest = int((bal * r).quantize(Decimal(1), ROUND_HALF_EVEN))
        p = bal if i == n - 1 else pay - interest        # last one absorbs rounding
        out.append(Instalment(i + 1, due[i], p, interest))
        bal -= p
    return out
```

**追问**：

- **免息四期、每两周一期（pay-in-4）？** 到期日改成起始日加 14 × k 天；本金分配逻辑不变。
- **提前还款？** 用剩余本金和剩余期数重新调用同一个函数生成新计划；旧计划标记为被替代，不删除。
- **逾期？** 计划之外再加一个还款记录表；逾期天数 = 今天 − 最早未还清一期的到期日；逾期费是一条新的费用行，不改计划。
- **一笔还款怎么分配？** 按固定顺序冲抵：费用 → 利息 → 本金，从最早一期开始；顺序是配置，不是写死的 if-else。
- **到期日遇到节假日？** 计划里保存合同到期日；扣款日另算（顺延到下一个工作日），两者分开存。
- **按日计息而不是按月？** 利息 = 剩余本金 × APR ÷ 365 × 当期天数，各期天数不同，所以每期还款额不再相等，最后一期仍然吸收误差。

**相关**：[[05-payment-domain]] 第 7 节 · [[interviews/core/leetcode/tiktok/map/a.tt-currency-conversion-queries|汇率换算查询]]

## 5. 按商户限流

**题面**：支付接口按商户限流：每个商户有自己的速率和突发上限（大商户更高），没有配置的用默认值。`allow(merchant, cost)` 返回是否放行。商户数量可能有几十万，大多数长期不活跃，内存不能无限增长。

**数据结构和原因**：

- **令牌桶**（token bucket）：每个商户一个桶，按速率往里加令牌，最多到容量；一次请求消耗 `cost` 个令牌。它允许短时突发（桶是满的），长期速率又不超过上限，适合支付这种有尖峰的流量。
- **惰性补充**：不用定时器给几十万个桶加令牌，而是在请求到来时按「距离上次更新的时间 × 速率」一次补齐，O(1)。
- **`OrderedDict` 做 LRU**：每次访问把商户移到队尾，超过上限时淘汰队头最久没用的桶。这就是「哈希表 + 双向链表」骨架。被淘汰的商户下次进来得到一个满桶，相当于多给一次突发；对长期不活跃的商户可以接受。
- 时钟从外部注入，测试时可以手动拨时间；时间倒退（时钟回拨）时补充量按 0 算。

**不变量**：

- 任何时刻 0 ≤ tokens ≤ burst。
- 任意长度为 T 的时间窗口里放行的总量 ≤ burst + rate × T。
- 桶的数量 ≤ `max_buckets`。

```python
import threading
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Limit:
    rate: float                  # tokens added per second
    burst: int                   # bucket capacity

@dataclass
class Bucket:
    tokens: float
    updated: float

class MerchantRateLimiter:
    def __init__(self, limits: dict[str, Limit], default: Limit,
                 clock: Callable[[], float], max_buckets: int = 100_000) -> None:
        self._limits, self._default, self._clock = limits, default, clock
        self._buckets: OrderedDict[str, Bucket] = OrderedDict()   # oldest use first
        self._max = max_buckets
        self._lock = threading.Lock()

    def allow(self, merchant: str, cost: int = 1) -> bool:
        lim = self._limits.get(merchant, self._default)
        with self._lock:
            now = self._clock()
            b = self._buckets.get(merchant)
            if b is None:
                b = self._buckets[merchant] = Bucket(lim.burst, now)
                if len(self._buckets) > self._max:
                    self._buckets.popitem(last=False)       # evict the idlest merchant
            self._buckets.move_to_end(merchant)
            b.tokens = min(lim.burst, b.tokens + max(0.0, now - b.updated) * lim.rate)
            b.updated = now
            if b.tokens < cost:
                return False
            b.tokens -= cost
            return True
```

**追问**：

- **多实例部署？** 桶放到 Redis，用一个 Lua 脚本原子地完成「读、补充、扣减、写回」；或者按商户 ID 把请求路由到固定实例，桶留在本地内存。
- **滑动窗口和令牌桶怎么选？** 滑动窗口日志精确但每个请求存一条时间戳，内存 O(请求数)；固定窗口计数在窗口边界会放过两倍流量；令牌桶 O(1) 内存且允许突发。
- **单个锁成为瓶颈？** 按商户 ID 哈希分成多个分段，每段一把锁和一个 LRU。
- **被限流的请求怎么办？** 返回 429 和 `Retry-After`（按缺少的令牌数 ÷ 速率算）；支付请求本身带幂等键，客户端重试是安全的。
- **商户配置实时修改？** 下一次 `allow` 读到新配置；如果容量变小，把现有令牌截断到新容量。

**相关**：[[interviews/core/leetcode/tiktok/map/a.tt-rate-limiter-implementation|手写限流器]] · [[interviews/core/leetcode/tiktok/map/a.tt-lru-cache-ttl|带 TTL 的 LRU 缓存]] · [[domains/under-the-hood/map/compose.caffeine|Caffeine：哈希表 + 访问队列]] · [[tiktok-service-protection]]
