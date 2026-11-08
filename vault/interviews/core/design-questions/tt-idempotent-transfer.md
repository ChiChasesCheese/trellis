---
slug: tt-idempotent-transfer
kind: low-level-design
---
## Q
**幂等转账服务**｜低层设计

实现 `transfer(client, key, src, dst, amount, currency)`，把钱从一个钱包转到另一个钱包。客户端会因为超时而重试，同一个 `key` 可能先后到达多次，也可能同时到达多次。要求：同一个键只转一次，重试拿到和第一次完全相同的结果；同一个键配了不同的请求要拒绝；余额不足时拒绝，并且这个拒绝结果也要被记住；并发到达的重复请求不会各执行一遍。面试官接着会问：处理到一半进程崩溃怎么办、第二步要调外部支付渠道怎么办、键存多久、多实例部署怎么办、同一个账户被高并发转出怎么办。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 幂等不是"检查一下是否做过"，而是"先用唯一约束原子地占住键，再把业务动作和结果保存放进同一个事务"，并让并发的重复请求合并到第一个请求上，而不是各自再执行一遍。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求（同键同请求、同键异请求、余额不足、并发重复），定 `transfer` 接口 |
| 8–13 分 | 两步：先占键，再在一个临界区里检查、记账、存结果 |
| 13–43 分 | 写核心实现：`KeyRecord`、`TransferService.transfer / _run` |
| 43–48 分 | 跑例子：8 个线程同一个键、余额不足、同键异请求 |
| 48–60 分 | 追问：崩溃恢复、外部支付渠道、键保留期、多实例 |

**需求。**
功能：
1. 同一个（调用方，键）只产生一次转账；重试返回第一次的结果。
2. 同一个键配不同的金额、账户或币种：拒绝（调用方的错误）。
3. 余额不足：返回拒绝结果，且该结果被记住（同一个键再来，仍是同一个拒绝）。
4. 并发的重复请求：只有一个真正执行，其余等待并拿到同样的结果；等不到就返回"稍后重试"。
5. 转账最终体现为账本里的一条平衡分录。

非功能：
- **余额检查与扣款不可插队：** 余额检查和扣款之间不能插入别的转账（否则会透支）。
- 键按调用方隔离：不同客户端可能生成相同的字符串。
- 一个键最多产生一条账本分录，分录 ID 由键派生，账本层再兜一次底。

**核心实体与接口。**
- **KeyRecord 三个字段：** `KeyRecord(fingerprint, done, result)`：键表里的一条记录。`fingerprint` 是请求内容的哈希，用来发现"同键不同请求"；`done` 是一个事件，第一个请求结束时唤醒等待者；`result` 为空表示第一个请求还没有出结果。
- `TransferService`：键表 `_keys`、保护键表的短锁 `_mu`、保护"检查余额 + 记账"的 `_money`、一个账本。对外只有 `transfer(...)`。
- `Ledger`：复式账本，借方为正、贷方为负；用户钱包是负债账户，所以可用余额 = −账本余额。
- 异常：`KeyReuse`（同键不同请求，对应 HTTP 422）、`StillRunning`（第一个请求还没结束，对应 HTTP 409）。
- 模式：幂等接收者（idempotent receiver）；合并重复请求（等同于 singleflight）；分录 ID 由键派生，把幂等一路带到账本。

**整体设计。**
调用分两步：
1. 占键。在 `_mu` 下查键表：不存在就插入一条新记录，调用者成为"拥有者"；已经存在就是重复请求。这一步在生产里是对唯一约束的一次插入，数据库保证两个并发插入只有一个成功。
2. 区分情况。指纹不同，直接报 `KeyReuse`。是拥有者就进入执行；不是拥有者就在记录的事件上等待：等到了并且记录里有结果，原样返回；等待超时，返回 `StillRunning`；如果醒来时记录里没有结果（拥有者异常退出并释放了键），回到循环重新竞争。
3. 执行。在 `_money` 下做三件事：检查可用余额、写账本分录、保存结果。余额不足也是一种结果，同样保存。结果保存完毕后才唤醒等待者，所以等待者永远看得到结果。
4. 失败。如果执行过程中抛出异常（此时还没有记账），拥有者把键从表里删掉再抛出，等待者醒来后重新竞争，其中一个成为新的拥有者。

**核心实现。** 约 30 分钟，一个代码块写完：占键、合并重复请求、检查余额与记账、保存结果。账本是一个只追加的复式账本 `Ledger`（模块 `ledger`；`post` 写入借贷平衡的分录并返回序号，`balance` 读余额，借方为正）。

```python
import hashlib
import json
import threading
from dataclasses import dataclass, field

from ledger import Entry, Ledger, Posting


class KeyReuse(Exception):
    """同一个幂等键配了不同的请求：调用方的 bug，对应 HTTP 422。"""


class StillRunning(Exception):
    """第一个请求在等待时间内没有结束：让调用方稍后重试，对应 HTTP 409。"""


@dataclass
class KeyRecord:
    fingerprint: str                                          # 请求内容的哈希
    done: threading.Event = field(default_factory=threading.Event)
    result: dict | None = None                                # None = 第一个请求还没出结果


class TransferService:
    def __init__(self, ledger: Ledger, wait: float = 5.0) -> None:
        self._ledger = ledger
        self._wait = wait
        self._keys: dict[tuple[str, str], KeyRecord] = {}     # (调用方, 键) -> 记录；生产里是唯一约束
        self._mu = threading.Lock()                           # 只保护键表
        self._money = threading.Lock()                        # 检查余额 + 记账，代替账户行锁

    def transfer(self, client: str, key: str, src: str, dst: str, amount: int, ccy: str) -> dict:
        if amount <= 0 or src == dst:
            raise ValueError("非法转账")
        fp = hashlib.sha256(json.dumps([src, dst, amount, ccy]).encode()).hexdigest()
        k = (client, key)
        while True:
            with self._mu:                                    # 第一步：占键（相当于唯一键插入）
                rec = self._keys.get(k)
                owner = rec is None
                if owner:
                    rec = self._keys[k] = KeyRecord(fp)
            if rec.fingerprint != fp:
                raise KeyReuse("同一个键不能用于不同的请求")
            if owner:
                return self._run(k, rec, src, dst, amount, ccy)
            if not rec.done.wait(self._wait):                 # 合并：等第一个请求，而不是再执行一次
                raise StillRunning("第一个请求仍在处理")
            if rec.result is not None:
                return rec.result                             # 原样返回第一次的结果
            # 第一个请求异常退出并释放了键：回到循环重新竞争

    def _run(self, k, rec: KeyRecord, src, dst, amount, ccy) -> dict:
        try:
            with self._money:                                 # 第二步：检查 + 记账 + 存结果
                if -self._ledger.balance(src, ccy) < amount:  # 钱包是负债账户：可用 = -余额
                    result = {"status": "rejected", "reason": "insufficient_funds"}
                else:
                    legs = (Posting(src, ccy, amount), Posting(dst, ccy, -amount))
                    seq = self._ledger.post(Entry(f"tr:{k[0]}:{k[1]}", legs))   # 分录 ID 派生自键
                    result = {"status": "succeeded", "ledger_seq": seq}
            rec.result = result                               # 业务拒绝也会被记住
            return result
        except BaseException:
            with self._mu:
                del self._keys[k]                             # 还没记账就失败：释放键，允许重试
            raise
        finally:
            rec.done.set()                                    # 先存结果，后唤醒等待者
```

**运行。**
- 钱包 a 先充值 10000 分。8 个线程同时用同一个键转 3000 分给 b：只产生一条转账分录，8 个调用拿到完全相同的结果，a 的余额是 −7000（可用 70.00），b 是 −3000。
- 再用新键转 8000 分：可用余额 7000 不足，返回 `insufficient_funds`；充值之后用同一个键重试，仍是这个拒绝，不会变成成功。
- 同一个键配不同金额：抛出 `KeyReuse`。

**深入。**

1. 【必讲】为什么要有"进行中"状态和合并，而不是只做"完成后去重"。
- 问题：只在完成后记录键，会有一个窗口：两个相同请求同时到达，都查不到记录，都去执行，转账两次。
- 选项：给整个 `transfer` 加一把全局锁，简单但所有转账串行；对每个键加锁，粒度合适但要管理锁的生命周期；占位记录加事件，第一个请求持有占位，其他请求等待。
- 选择：占位记录。它同时解决两件事：只执行一次，以及重复请求拿到的是第一次的结果而不是一个"冲突"错误，客户端体验更好。`done.wait` 带超时，避免第一个请求卡住时拖垮所有重试者。

2. 【必讲】业务拒绝要不要被记住。
- 问题：余额不足是一个确定的业务结果，而不是错误。如果不记住，那么同一个键第二次到达时恰好有人充了值，就会成功，同一个键两次得到不同的结果，客户端无法推理。
- 做法：拒绝与成功一样保存。想在充值之后再试，必须用新键，因为这是一次新的业务意图。
- 对照：网络错误、超时、数据库暂时不可用是"结果未知或可重试"的错误，不应该当作结论保存。本例的做法是：记账之前失败就释放键；记账之后的失败靠分录 ID 的幂等兜底，重放同一个键不会记两次。

3. 【必讲】余额检查与扣款的原子性。
- 问题：先读余额再写账本，两步之间别的转账可能把钱转走。
- 本例：用 `_money` 把"检查 + 记账"放进一个临界区。
- 生产：同一个数据库事务里，用带条件的更新，例如 `UPDATE wallet SET balance = balance - x WHERE id = ? AND balance >= x`，受影响行数为 0 就是余额不足；或者对账户行加 `SELECT ... FOR UPDATE`，涉及多个账户时按账户 ID 排序加锁，避免死锁。
- 热点账户：高并发转出同一个账户会在行锁上排队，可以按账户把请求路由到单一分区串行处理，或使用分片追加加快照的账本。

4. 【追问再讲】崩溃恢复。
- 占键之后、执行完成之前进程崩溃，键永远停在"进行中"。在真实系统里，键记录带开始时间；恢复任务扫描超过阈值的进行中记录，用同一个键重放第二步。第二步必须幂等：账本分录 ID 由键派生，所以重放要么发现已记账（直接补写结果），要么记账。

5. 【加分】外部支付渠道。
- **外部渠道用发件箱：** 如果第二步要调用外部支付渠道（不能放进数据库事务），用事务外盒（outbox）：事务里写入业务数据和"待发出的渠道请求"，后台进程用同一个幂等键调用渠道。渠道超时视为结果未知，用同一个键去查询或重试，直到有定论才推进状态，绝不当作失败重新下单。
- 三层幂等：客户端到平台靠调用方的键；平台到渠道靠平台生成并传给渠道的键；崩溃窗口靠先记录意图再动手加重放。缺一层就会重复扣款。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- **同键不同请求要拒绝：** 同键不同请求为什么要拒绝而不是覆盖？这几乎总是客户端的 bug（键没有按业务意图生成）。悄悄执行第二个请求会转出错误的金额，悄悄返回第一个结果会让调用方以为第二个请求成功了。
- 响应丢失：转账已成功但响应在网络上丢了，客户端重试得到保存的结果，看到成功，这正是设计目标。
- 返回码设计：新建成功 201，重放返回同样的码和内容；`StillRunning` 用 409 加 `Retry-After`；`KeyReuse` 用 422。
- **键保留要覆盖重试窗口：** 键存多久？至少覆盖客户端最长的重试窗口（常见 24 小时到几天），过期后按时间分区批量清理。过短会让迟到的重试变成第二次转账。
- 多实例部署？内存锁换成数据库的唯一约束与行锁；键表与账本放在同一个库里，才能在同一个事务里提交。等待者不用事件，而是轮询或订阅记录状态的变化。
- 键由谁生成？由客户端在用户发起动作时生成一次，重试沿用；服务端生成没有意义，因为重试时拿不到。
- 如何测试？并发同键 N 次只记一次账；同键异请求被拒；拒绝被记住；拥有者抛异常后键被释放且下一个请求成功；账本 `verify` 始终为真。

**级别期望。**
- 中级：键表加账本，检查是否做过，余额不足拒绝。
- 高级：占位记录合并并发重复，指纹检测同键异请求，检查与扣款原子，拒绝结果也被记住。
- 资深/Staff：崩溃恢复与重放、事务外盒与外部渠道的结果未知、三层幂等、数据库层的唯一约束与条件更新、键的保留期与清理、热点账户的串行化。

**先修概念。** [[hi-low-level-design-concurrency-intro|并发入门]]、[[hi-low-level-design-concurrency-correctness|并发正确性]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-system-design-patterns-multi-step-processes|多步骤流程]]、[[hi-system-design-patterns-dealing-with-contention|处理争用（Contention）]]

**同类题。** [[tt-idempotent-versioned-update|幂等的版本化更新]]、[[tt-double-entry-ledger|复式账本（类设计）]]、[[sd01-payment-system|支付系统（系统设计）]]、[[tiktok-idempotency-transactions|幂等与事务八股]]、[[payment-batch-processing|支付系统（收单、扣款、确认）]]
