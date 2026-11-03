# 幂等转账服务（Idempotent Transfer）

钱包服务提供 `transfer`，把钱从一个钱包转到另一个钱包。客户端会因为超时而重试，同一个幂等键（idempotency key）
可能先后到达多次，也可能同时到达多次；响应丢了不代表转账没成功。要保证：同一个键只转一次，重试拿到和第一次完全相同的结果。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：同一个（调用方，键）只转一次，重试返回第一次的结果；同键配不同的请求内容要拒绝；
  余额不足是一个"被拒绝"的结果，不是异常，而且这个拒绝也要被记住；不合法的请求直接报错，不占用键。
- 第 2 关（约 15 分钟）：并发到达的重复请求只有一个真正执行，其余的等它并拿到同样的结果，等太久就报 `StillRunning`；
  拥有者在做一个很慢的外部步骤（风控）时，别的键的转账不能被卡住；不同的键并发转出同一个账户，不能透支。
- 第 3 关（约 20 分钟）：外部步骤失败（动钱之前）要释放键，之后可以用同一个键重试，等待者重新竞争；
  结果只保留 `ttl` 秒，之后同一个键视为新请求；`purge()` 清理过期结果；还在执行的请求不受 `ttl` 影响。
- 第 4 关（选做）：租约（lease）。拥有者崩溃或卡死后，键会永远停在"执行中"。超过 `lease` 秒还没出结果，
  允许别的重复请求接手；无论旧拥有者之后是否醒来，钱都最多动一次。

**接口**

```python
class TransferError(Exception)             # 以下全是它的子类
class InvalidRequest(TransferError, ValueError)   # 金额不是正整数、src == dst、client 或 key 为空
class KeyReuse(TransferError)              # 同一个 (client, key) 配了不同的请求
class StillRunning(TransferError)          # 第 2 关：等第一个请求超过 wait 秒
class LeaseLost(TransferError)             # 第 4 关：这一轮的租约已被收回，且没有动钱

@dataclass(frozen=True) class TransferResult: status: str; reason: str | None = None; seq: int | None = None
    # status 是 "succeeded"（seq 为成功转账的序号，从 1 起）或 "rejected"（reason 为 "insufficient_funds"）
@dataclass(frozen=True) class TransferRecord: seq: int; client: str; key: str; src: str; dst: str; amount: int; currency: str

class TransferService:
    def __init__(self, balances: Mapping[tuple[str, str], int] | None = None, *, wait: float = 5.0,
                 ttl: float | None = None, lease: float | None = None,
                 clock: Callable[[], float] = time.monotonic,
                 on_execute: Callable[[str, str], None] | None = None) -> None
    def transfer(self, client: str, key: str, src: str, dst: str, amount: int, currency: str) -> TransferResult
    def balance(self, account: str, currency: str) -> int       # (账户, 币种) 没出现过是 0
    def transfers(self) -> tuple[TransferRecord, ...]           # 成功的转账，按序号排列
    def purge(self) -> int                                      # 第 3 关
```

- `balances` 的键是 `(账户, 币种)`；`transfer` 的币种是请求的一部分，指纹是 `(src, dst, amount, currency)`。
- 余额恰好等于金额是允许的；余额不足返回 `TransferResult("rejected", "insufficient_funds")`，不改任何余额，不占转账序号。
- `on_execute(client, key)`：占键之后、动钱之前调用一次的外部步骤（比如风控）。它可能阻塞很久，也可能抛异常；
  抛出的异常原样传给调用方。调用它时不能持有会卡住别的键的锁。
- `ttl`：结果完成后保留多少秒；到点（`>=`）即过期。`lease`：执行中的记录开始后超过多少秒没出结果即视为失联。`clock` 注入时间。
- `wait`：重复请求等第一个请求的最长秒数，超时抛 `StillRunning`。

例子：

```python
svc = TransferService({("alice", "USD"): 10000})
svc.transfer("c1", "k1", "alice", "bob", 3000, "USD")   # TransferResult("succeeded", None, 1)
svc.transfer("c1", "k1", "alice", "bob", 3000, "USD")   # 同一个结果；alice 还是 7000
svc.transfer("c1", "k1", "alice", "bob", 3001, "USD")   # 抛 KeyReuse
svc.transfer("c1", "k2", "alice", "bob", 9000, "USD")   # TransferResult("rejected", "insufficient_funds", None)
```

**评分点**

- 先占键、再执行：说得出"只在完成后记录键"为什么会让两个同时到达的相同请求各转一次。
- 重复请求合并到第一个请求（占位记录加事件），等待带超时；拿到的是第一次的结果而不是一个冲突错误。
- 业务拒绝（余额不足）与技术失败（外部步骤抛异常）分开处理：前者是结果，要记住；后者没有结论，要释放键。
- "检查余额 + 扣款 + 保存结果"是一个原子步骤；外部慢调用不持有全局锁；两把锁各管什么、持有多久。
- 同键异请求用指纹拒绝；键按调用方隔离；不合法的请求不占键。
- 保留期的代价能讲清：过期后迟到的重试会再转一次，所以 `ttl` 至少要覆盖客户端最长的重试窗口。
- 租约接手时钱最多动一次：沿用同一条记录、提交时检查"已有结果"，以及接手的一轮失败后旧拥有者不能再动钱。
- 能口述：数据库唯一约束与条件更新、事务外盒（outbox）与外部渠道的结果未知、三层幂等（客户端到平台、平台到渠道、崩溃重放）。
