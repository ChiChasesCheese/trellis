---
slug: tt-double-entry-ledger
kind: low-level-design
---
## Q
**复式账本（类设计）**｜低层设计

实现一个复式账本（double-entry ledger）：`post(entry)` 写入一条分录，分录由若干条腿（posting）组成，每条腿是（账户、币种、带符号金额）；`balance(account, currency)` 返回余额；`reverse(entry_id)` 冲正一条已有的分录；同一条分录被重复提交时只记一次。面试官会继续追问：冻结与可用余额、不允许透支、并发、每秒几万次写入的热点账户、历史某一时刻的余额、怎么证明账没有被改过、跨币种转账。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 账本由两样东西构成：一份只追加、永不修改的分录日志（唯一的事实来源），和一组随每次写入同步更新的派生索引（余额、历史余额）；所有正确性都落在三条不变量上：每条分录借贷平衡、余额等于腿之和、纠错只靠新分录。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求（币种、幂等、冲正），定 `post / reverse / balance` 接口 |
| 8–13 分 | 日志加派生索引，带符号金额，三条不变量 |
| 13–43 分 | 写核心实现：`Posting`、`Entry`、`Ledger.post / reverse / balance` |
| 43–48 分 | 跑例子：充值、送礼、冲正、重复提交 |
| 48–60 分 | 追问：历史余额、冻结与不透支、并发与热点、防篡改、跨币种 |

**需求。**
功能：
1. `post(entry)`：写入一条至少两条腿的分录；各币种分别借贷平衡，否则拒绝。
2. 同一个分录 ID 重复提交是无操作，返回第一次的结果；同一个 ID 带不同的内容要报错。
3. **balance 查余额 O(1)：** `balance(account, currency)`：当前余额，O(1)。
4. **reverse 生成取反分录：** `reverse(entry_id, new_id)`：生成一条把原分录每条腿取反的新分录，不修改原分录。
5. 追问：`balance_at(account, currency, seq)` 某个分录序号时刻的历史余额；`verify()` 从日志重算余额并与索引比较（逐步扩展 1、2）。

非功能：
- 金额是整数最小货币单位，同一账户可以有多个币种的余额，币种之间不混算。
- 写入是原子的：分录和余额索引要么都更新，要么都不更新。
- 读余额 O(1)；历史余额 O(log n)（追问）。

**核心实体与接口。**
- **Posting 是借正贷负的一条腿：** `Posting(account, currency, amount)`：一条腿。约定借方为正、贷方为负，所以一条分录所有腿（按币种）之和为 0。资产和费用账户通常余额为正；负债（用户钱包里的钱是平台欠用户的）、权益和收入账户的余额为负，展示给用户时取反。
- **Entry 的 id 由业务意图派生：** `Entry(id, postings, reverses)`：一条分录。`id` 由业务意图派生（例如"转账 + 客户端 + 幂等键"），`reverses` 指向被冲正的那一条。
- `Ledger`：持有日志 `_journal`、去重表 `_by_id`、当前余额 `_bal`；对外是 `post / reverse / balance`，之后再加 `balance_at / verify`。
- 模式：事件溯源（日志是事实，状态是推导）；主存储加派生索引；不可变值对象（`frozen=True` 的数据类）。

**整体设计。**
写入路径：`post` 先查 `_by_id`，重复就返回（内容不一致则报错）；否则按币种汇总各腿，检查腿数不少于 2 且每个币种的合计为 0；通过后在同一个临界区内追加到 `_journal`、登记到 `_by_id`、更新每条腿对应账户的 `_bal`。

冲正路径：`reverse` 取出原分录，每条腿取反，用一个新 ID 作为新分录写入，`reverses` 指回原分录。原分录原样保留，所有读过旧状态的下游都能从日志里看到"错了、改了、改成什么"。

**核心实现。** 约 28 分钟，下面是全部要写的代码：不可变的分录、带去重和平衡检查的 `post`、冲正、余额。

```python
import threading
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Posting:
    account: str
    currency: str
    amount: int                  # 带符号的最小货币单位：借方为正、贷方为负


@dataclass(frozen=True)
class Entry:
    id: str                      # 由业务意图派生（如 "tr:client:key"），重复提交靠它去重
    postings: tuple[Posting, ...]
    reverses: str | None = None  # 冲正分录指向被冲正的那一条


class Ledger:
    def __init__(self) -> None:
        self._journal: list[Entry] = []                            # 唯一事实来源，只追加
        self._by_id: dict[str, tuple[int, Entry]] = {}             # 去重索引：分录 ID -> (序号, 分录)
        self._bal: dict[tuple[str, str], int] = defaultdict(int)   # 派生索引：当前余额
        self._lock = threading.Lock()                              # 代替数据库事务

    def post(self, e: Entry) -> int:
        """写入一条分录，返回它的序号（从 1 开始）；重复提交返回原序号。"""
        with self._lock:
            hit = self._by_id.get(e.id)
            if hit is not None:
                if hit[1] != e:
                    raise ValueError(f"分录 {e.id} 被复用但内容不同")
                return hit[0]
            net: dict[str, int] = defaultdict(int)
            for p in e.postings:
                net[p.currency] += p.amount
            if len(e.postings) < 2 or any(net.values()):           # 每个币种各自借贷平衡
                raise ValueError(f"分录 {e.id} 不平衡: {dict(net)}")
            self._journal.append(e)
            seq = len(self._journal)
            self._by_id[e.id] = (seq, e)
            for p in e.postings:                                   # 与分录在同一个临界区内更新
                self._bal[(p.account, p.currency)] += p.amount
            return seq

    def reverse(self, entry_id: str, new_id: str) -> int:
        """纠错只靠新分录：把原分录每条腿取反。"""
        orig = self._by_id[entry_id][1]
        legs = tuple(Posting(p.account, p.currency, -p.amount) for p in orig.postings)
        return self.post(Entry(new_id, legs, reverses=entry_id))

    def balance(self, account: str, currency: str) -> int:
        return self._bal.get((account, currency), 0)
```

**运行。**
- **例：充值与送礼两条分录：** 充值 100.00 美元写一条分录（PSP 应收 +10000，用户钱包 −10000），序号为 1；用户给主播送 30.00 美元，（用户钱包 +3000，主播待结算 −3000），序号为 2。
- 此时用户钱包余额是 −7000，展示为"可用 70.00 美元"。
- 重复提交 ID 为 `e1` 的分录返回序号 1，余额不变；同一个 ID 带不同内容抛 `ValueError`；腿不平衡的分录抛 `ValueError`。
- 冲正序号 2 的分录返回序号 3，余额回到 −10000，日志里有 3 条记录，没有任何一条被改动。
- 50 个线程并发各写一条分录：全账户之和仍为 0。

**逐步扩展。**
1. 【追问再讲】历史余额 `balance_at`：每次更新余额时，把「序号，更新后的余额」追加到该账户的历史列表。因为序号严格递增，列表天然有序，用二分找序号不大于给定值的最后一项。上面的例子里 `balance_at(用户钱包, 1)` 是 −10000。

```python
from bisect import bisect_right

# __init__ 里加一行：
#   self._hist: dict[tuple[str, str], tuple[list[int], list[int]]] = {}   # 账户 -> (序号列表, 余额列表)
# post 里 `self._bal[...] += p.amount` 改成下面四行：
for p in e.postings:
    k = (p.account, p.currency)
    self._bal[k] += p.amount
    seqs, bals = self._hist.setdefault(k, ([], []))
    seqs.append(seq)                       # 序号严格递增，所以列表天然有序
    bals.append(self._bal[k])


# 新增方法
def balance_at(self, account: str, currency: str, seq: int) -> int:
    """历史余额：二分找到序号 <= seq 的最后一条腿。"""
    seqs, bals = self._hist.get((account, currency), ([], []))
    i = bisect_right(seqs, seq)
    return bals[i - 1] if i else 0
```

2. 【加分】核对 `verify`：从日志从头重算每个账户的余额和各币种的总和，与 `_bal` 比较，并要求各币种全账户之和为 0。它是独立于写入路径的第二把尺子，定期运行，能发现索引与日志分叉的缺陷。上面的例子冲正后 `verify()` 为真。

```python
def verify(self) -> bool:
    """从分录重算全部余额并与索引比对；每个币种全账户之和必须为 0。"""
    fresh: dict[tuple[str, str], int] = defaultdict(int)
    total: dict[str, int] = defaultdict(int)
    for e in self._journal:
        for p in e.postings:
            fresh[(p.account, p.currency)] += p.amount
            total[p.currency] += p.amount
    same = all(fresh[k] == self._bal.get(k, 0) for k in set(fresh) | set(self._bal))
    return same and not any(total.values())
```

**深入。**

1. 【必讲】为什么是"日志 + 派生索引"，而不是一个余额字段。
- 问题：只存余额字段，改错无法追溯；两次更新之间崩溃，钱凭空出现或消失；无法证明总账是平的。
- 选项：只存日志，读余额时求和，读是 O(腿数)；只存余额字段，读快但没有审计；日志加余额索引，读快也可审计。
- 选择：日志加索引。代价是索引必须和日志同时更新，因此写入放在同一个临界区（生产中是同一个数据库事务）；`verify` 负责在出现偏差时发现它。

2. 【必讲】冻结、可用余额和不允许透支。
- 问题：用户转账或打款处理期间，金额需要先"占住"，防止被花两次；用户钱包不能出现负的可用余额。
- 做法：另设一张冻结表 `(账户, 冻结 ID) → 金额`；可用余额 = 账面余额的展示值 − 冻结合计。冻结与释放各自幂等（以冻结 ID 为键）。检查"写入后可用余额不小于 0"必须与写入在同一把锁或同一个事务里，否则两个并发转账会各自检查通过、一起透支。
- 在数据库里的写法：对用户账户的余额行用带条件的更新，`UPDATE ... SET balance = balance - x WHERE balance >= x`，受影响行数为 0 就是余额不足，检查与扣减是一条语句。
- 选择：冻结表加条件更新；不允许透支只用于用户类账户，平台内部账户（如应收渠道款）可以为负，因为它们代表的是在途资金。

3. 【追问再讲】并发与热点账户。
- 问题：单把全局锁让所有写入串行；平台手续费收入这类账户每秒被几万笔分录写，单行余额成为锁热点。
- 并发：按账户加锁，一条分录涉及多个账户时按账户 ID 排序依次加锁，避免两个事务以相反顺序加锁而死锁；数据库里对应 `SELECT ... FOR UPDATE` 按固定顺序取行。
- 热点账户：不要在每次写入时更新同一行余额。只追加分录，余额按时间片汇总：写入把腿追加到分片的分录表，后台周期性地把增量折叠进快照；读余额时取最近快照加快照之后的增量。代价是读比单行余额略慢，换来写入可以水平扩展。
- 选择：普通账户行锁加余额索引；已知的热点账户改用分片追加加快照。

4. 【加分】如何证明账没有被改过。
- 日志不可变：存储层只开放追加，不开放更新和删除的权限。
- 定期核对：重算余额，每个币种全账户之和必须为 0，每条分录平衡。
- 防篡改：分录按块计算哈希链（每块包含前一块的哈希），任何历史改动都会让后续哈希对不上；可以定期把最新哈希发布到独立的存储。
- 对外核对：账本里的"应收渠道款"和渠道的结算文件对账，余额应该在结算后回到 0，剩下的差异就是需要解释的项。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 错误的分录怎么办？永远不改。写一条冲正分录，再写一条正确的分录；两条都带上原因和操作人。
- **带符号金额对借贷两列：** 为什么用带符号金额而不是分借方和贷方两个字段？带符号的和为 0 是最容易检查的不变量；缺点是需要为每类账户记住"正常余额方向"，展示时翻转。会计系统常保留借贷两列以便阅读，内部检查仍是等价的。
- 幂等重试的位置？分录 ID 由业务意图派生，账本层再兜一次底；上层的幂等键表负责返回第一次的完整结果。
- 如何测试？不平衡的分录被拒绝；重复提交不改变余额；冲正后余额回到原值；多线程并发转账后各币种总和仍为 0 且 `verify` 为真；`balance_at` 在边界序号上的取值。
- 日志无限增长？按时间分区，旧分区转冷存储；余额索引和快照保证读取不依赖旧分区；审计需要时再读冷存储。
- 数据库实现？分录表和腿表都只插入，腿表上 `(account, currency, seq)` 建索引；余额表与分录在同一个事务里更新；`(分录 ID)` 唯一约束就是去重。
- 跨币种转账？用两组各自平衡的腿，经由一个 FX 中间账户：用户美元账户减少、FX 中间账户美元增加；FX 中间账户林吉特减少、对方林吉特账户增加。分录里记录汇率和报价编号，汇兑差额进入汇兑损益账户，而不是悄悄吃掉。

**级别期望。**
- 中级：只追加的分录列表加余额表，每条分录借贷平衡，能处理重复提交。
- 高级：日志与派生索引的关系，冲正代替修改，历史余额，冻结与可用余额，按账户排序加锁避免死锁。
- 资深/Staff：热点账户的分片追加与快照，哈希链与核对，多币种与 FX 账户，数据库事务与条件更新的写法，冷热分区与对账闭环。

**先修概念。** [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-concurrency-correctness|并发正确性]]、[[hi-system-design-core-concepts-data-modeling|数据建模]]、[[hi-system-design-deep-dives-postgres|PostgreSQL]]

**同类题。** [[solution-digital-wallet|数字钱包]]、[[solution-bank-account|银行账户]]、[[sd09-wallet-ledger|钱包与账本服务（系统设计）]]、[[tt-kv-store-snapshot-restore|KV 快照]]、[[05-payment-domain|支付领域知识]]
