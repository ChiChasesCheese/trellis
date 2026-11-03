# 复式账本（Double-Entry Ledger）

一个钱包业务要自己记账：充值、转账、送礼、退款，每一笔钱的去向都要查得到、对得平、改不掉。
账本里的每条记录叫一条分录（entry），由若干条腿（posting）组成，每条腿是（账户、币种、带符号金额）。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：`post` 写入分录，按币种各自借贷平衡才能写入；同一个分录 ID 重复提交是无操作，
  内容不同则报错；`balance` 查余额；`reverse` 冲正一条分录（生成一条把每条腿取反的新分录，原分录不动）；
  `journal` 返回只读日志。失败的调用不留任何痕迹。
- 第 2 关（约 15 分钟）：`balance_at` 查某条分录写入后的历史余额；`set_floor` 给账户设余额下限（比如 0 表示不许透支），
  不满足就整条分录拒绝，一条腿都不落；`statement` 按页返回对账单。
- 第 3 关（约 20 分钟）：冻结（`hold` / `release` / `available`）：冻结的钱仍在账面上，但不能再被花；
  `post` 可以在同一个原子步骤里释放自己的冻结再写入；多个线程同时写入时，不能一起透支，不能重复记账。
- 第 4 关（选做）：`exchange` 换汇：一条分录里出现两个币种，各币种仍然各自平衡，账本代码不用为它改动。

**接口**

```python
@dataclass(frozen=True) class Posting: account: str; currency: str; amount: int   # 正数增加余额，负数减少
@dataclass(frozen=True) class Entry:   id: str; postings: tuple[Posting, ...]; reverses: str | None = None
@dataclass(frozen=True) class StatementLine: seq: int; entry_id: str; amount: int; balance_after: int

class LedgerError(Exception)       # 以下全是它的子类
class InvalidEntry                 # 腿数少于 2、有金额为 0 的腿、某币种不平、分录或冻结的 ID 为空、冻结金额不是正数
class ConflictError                # 同一个 ID 带了不同的内容；释放已经被用掉的冻结
class UnknownEntry                 # 引用了不存在的分录或冻结
class AlreadyReversed              # 这条分录已经被另一条分录冲正过
class InsufficientFunds            # 写入或冻结会让"余额减冻结"低于账户的下限

class Ledger:
    def post(self, entry: Entry, release_hold: str | None = None) -> int     # 返回序号，从 1 开始
    def balance(self, account: str, currency: str) -> int                    # 没出现过的账户是 0
    def total(self, currency: str) -> int                                    # 全账户余额之和，正确的账本恒为 0
    def reverse(self, entry_id: str, new_id: str) -> int
    def journal(self) -> tuple[Entry, ...]
    def balance_at(self, account: str, currency: str, seq: int) -> int       # seq<1 得 0，超过当前序号得当前余额
    def set_floor(self, account: str, currency: str, floor: int) -> None
    def statement(self, account: str, currency: str, after_seq: int = 0, limit: int = 100) -> list[StatementLine]
    def available(self, account: str, currency: str) -> int                  # 余额 - 冻结合计
    def hold(self, hold_id: str, account: str, currency: str, amount: int) -> None
    def release(self, hold_id: str) -> None
    def exchange(self, entry_id: str, account: str, from_currency: str, from_amount: int,
                 to_currency: str, to_amount: int, fx_account: str = "fx") -> int
```

规则细节：

- 重复提交：同 ID、同内容，返回第一次的序号，不改余额，也不占新序号。
- `reverse`：新分录的 `reverses` 指向原分录；原分录不存在抛 `UnknownEntry`；已被另一个 `new_id` 冲正过抛 `AlreadyReversed`；
  用同一个 `new_id` 重试返回第一次的序号；`new_id` 撞上别的分录抛 `ConflictError`。冲正分录自己也可以被冲正。
- 下限只约束之后的写入，没设下限的账户可以为负（比如充值来源账户）。`floor` 可以是负数（授信额度）。
- `hold`：同一个 `hold_id` 同参数重复调用是幂等的（即使已经释放过），参数不同抛 `ConflictError`。`release` 对已释放的冻结是无操作。
- `post(..., release_hold=h)`：先把 `h` 释放，再检查下限并写入；任一步失败，冻结保持原样。冻结不存在抛 `UnknownEntry`，已用掉抛 `ConflictError`。
- `statement` 每条分录对一个账户一行，同账户的多条腿合并成净额；`limit < 1` 抛 `ValueError`。

例子：

```python
led = Ledger()
led.post(Entry("e1", (Posting("psp", "USD", -10000), Posting("alice", "USD", 10000))))   # 1：充值 100.00
led.post(Entry("e2", (Posting("alice", "USD", -3000), Posting("bob", "USD", 3000))))     # 2：转账 30.00
led.reverse("e2", "e2-undo")                                                             # 3：alice 回到 10000
led.post(Entry("e9", (Posting("psp", "USD", -10000), Posting("alice", "USD", 10001))))   # 抛 InvalidEntry（不平）
led.post(Entry("e1", (Posting("psp", "USD", -999), Posting("alice", "USD", 999))))       # 抛 ConflictError
```

**评分点**

- 日志是唯一事实，余额和历史只是随写入同步更新的派生索引；能说出为什么不是只存一个余额字段。
- 先校验、后修改：任何失败都不留半截状态，序号也不被占用；检查和写入在同一个临界区里。
- 幂等与冲突分得清：同 ID 同内容是重放，同 ID 不同内容是 bug，两者的处理不同。
- 纠错只靠追加新分录，不改旧分录；冲正本身也要幂等，同一条分录不能被冲两次。
- 下限检查和写入不能分成两步（会一起透支）；多条腿的分录要么全落要么全不落；能口述数据库里的条件更新写法。
- 冻结不动账面，只动可用余额；"释放加写入"是一个原子步骤，不是两次调用。
- 币种之间不混算；换汇通过中转账户表达，说明为什么不需要新的账本概念。
- 能口述热点账户（分片追加加快照）、按账户排序加锁避免死锁、哈希链防篡改、对账闭环。
