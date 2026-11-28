---
slug: credit-token-balance
kind: low-level-design
---
## Q
**设计用户额度（Token / Credit）账本服务**｜低层设计

设计一个按量计费的额度账本：用户会被发放额度包（credit grant），每个包有金额、生效时间和过期时间；使用时要扣额度，而且先扣快到期的，免得白白过期；还要能查询任意时间点的余额。难点在于请求可能乱序到达：先收到时间戳为 2 的扣费，再收到时间戳为 1 的发放，扣费仍然应当成功。常见接口是三个操作：发放（创建额度包）、扣费、查余额（带时间戳）。面试官看重的是：为什么不能"收到就直接扣减"、乱序怎么处理、同一时刻的先后规则、重复请求的幂等，以及这套做法的代价。

给出完整解答：需求、核心实现、逐步扩展、深入问题、取舍、不同级别的期望。

## A
**一句话。** 账本只存事件（额度包和扣费），余额和"每笔扣费用了哪些包"都是把事件按时间排序后重放出来的结果；接受新事件之前先在副本上重放，所有已接受的扣费仍能全额扣下才提交，乱序、迟到、作废就都变成"改事件表再重放"，没有回滚逻辑。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清语义：区间开闭、同一时刻谁先、不够扣怎么办、乱序是否允许、要不要幂等 |
| 8–15 分 | 定接口，说出"存事件、重放出结果"和排序键；画重放的小例子 |
| 15–42 分 | 写核心实现：事件、`_expiry_key`、`_replay`、账本 |
| 42–47 分 | 跑例子：先到期先扣、跨包、乱序迟到、余额 |
| 47–60 分 | 追问：幂等与冲突、作废、重放代价与增量、不够扣时的策略 |

**需求。**
- 功能：
  - `grant(id, amount, at, expires_at=None)`：额度包从 `at`（含）起可用，到 `expires_at`（不含）失效，`None` 永不过期；
  - `charge(id, amount, at)`：在时刻 `at` 扣 `amount`，只能用 `at` 时刻有效的包；先到期的先扣，永不过期的最后；同一时刻到期的先发放的先扣，再按 `id`；一笔可以跨多个包，返回按扣减顺序排列的分配；
  - `balance(at)`：`at` 这一刻可用的额度，只算 `at` 及之前发生的事件；
  - 请求可以乱序到达：账本的行为等同于所有事件按 `(时间, 额度包先于扣费, id)` 排好序后处理；
  - 额度不够：扣费抛 `InsufficientCreditsError`，账本原封不动。
- 非功能：
  - 金额用整数，没有浮点；时间由调用方传入，账本不读系统时钟；
  - 已经告诉调用方成功的扣费，不会被后来的迟到事件"饿死"；
  - 事件很多时的代价要能说清：每个新事件都要重放一遍（见深入）。
- 区间约定：额度包在 `[at, expires_at)` 内可用。若题目写成"包在 `[t, t + 有效期]` 内都可用"，换算成 `expires_at = t + 有效期 + 1`。

**核心实体与接口。**
- `Grant`、`Charge`：事件，`frozen=True, slots=True` 的数据类，不可变，可比较。
- **Allocation 记录取了多少：** `Allocation(grant_id, amount)`：`NamedTuple`，一笔扣费从某个包里取了多少。
- `_expiry_key(g)`：包的扣减优先级，`(永不过期?, 到期时间, 发放时间, id)`。
- **_replay 纯函数重放：** `_replay(grants, charges, until)`：纯函数，输入事件表，输出每笔扣费的分配和每个包的剩余额度。
- `CreditLedger`：`grant`、`charge`、`balance`、`allocations`；内部只有两张事件表和 `_commit`。

**整体设计。** 一次写操作（以 `charge` 为例）：
1. 校验参数（金额为正），失败直接抛出；
2. 在事件表的副本里加入新事件，调用 `_replay` 试跑：任何一笔已接受的扣费凑不够，`_replay` 就抛 `InsufficientCreditsError`，真实状态没动；
3. **试跑通过才 _commit：** 试跑通过才替换真实的事件表（`_commit`）；
4. 返回这笔扣费在重放结果里的分配。

重放的内部：事件按 `(时间, 额度包先于扣费, id)` 排序；一个按 `_expiry_key` 排的最小堆放着已发放的包；遇到扣费，先把堆顶已过期的包弹出（惰性删除），再从堆顶取包扣减，用完的包弹出。重放里时间只往前走，所以弹出过期包永远是对的，每个包最多进出堆一次。

**核心实现。** 约 30 分钟，下面是全部要写的代码：

```python
import heapq
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple


class LedgerError(Exception): ...
class InsufficientCreditsError(LedgerError): ...       # 这笔扣费，或因它而扣不下的某笔已有扣费
class UnknownChargeError(LedgerError): ...


class Allocation(NamedTuple):                          # 既能拆包比较，又有字段名
    grant_id: str
    amount: int


@dataclass(frozen=True, slots=True)
class Grant:
    id: str
    amount: int
    at: datetime                                       # 从这一刻起可用（含）
    expires_at: datetime | None = None                 # 到这一刻失效（不含）；None 永不过期


@dataclass(frozen=True, slots=True)
class Charge:
    id: str
    amount: int
    at: datetime


def _expiry_key(g: Grant) -> tuple:
    """先到期的先扣；永不过期的排最后；同一时刻到期的，先发放的先扣，再按 id。"""
    return (g.expires_at is None, g.expires_at, g.at, g.id)


def _replay(grants: dict[str, Grant], charges: dict[str, Charge],
            until: datetime | None = None) -> tuple[dict[str, tuple[Allocation, ...]], dict[str, int]]:
    """纯函数：事件按 (时间, 额度包先于扣费, id) 排好，从头重放。返回每笔扣费的分配、每个包的剩余额度。
    某笔扣费凑不够就抛 InsufficientCreditsError。"""
    events = sorted([*grants.values(), *charges.values()], key=lambda e: (e.at, isinstance(e, Charge), e.id))
    heap, remaining, allocations = [], {}, {}
    for event in events:
        if until is not None and event.at > until:
            break
        match event:
            case Grant():
                remaining[event.id] = event.amount
                heapq.heappush(heap, (_expiry_key(event), event.id))
            case Charge():
                need, taken = event.amount, []
                while need and heap:
                    _, gid = heap[0]
                    expires = grants[gid].expires_at
                    if expires is not None and expires <= event.at:
                        heapq.heappop(heap)            # 惰性删除：重放里时间只往前走，过期的包不会再有效
                        continue
                    use = min(need, remaining[gid])
                    remaining[gid] -= use
                    need -= use
                    taken.append(Allocation(gid, use))
                    if remaining[gid] == 0:
                        heapq.heappop(heap)
                if need:
                    raise InsufficientCreditsError(f"charge {event.id} is short by {need}")
                allocations[event.id] = tuple(taken)
    return allocations, remaining


class CreditLedger:
    def __init__(self) -> None:
        self._grants: dict[str, Grant] = {}            # 账本只存事件，余额和分配都是重放出来的
        self._charges: dict[str, Charge] = {}

    def grant(self, grant_id: str, amount: int, at: datetime, expires_at: datetime | None = None) -> None:
        if amount <= 0 or (expires_at is not None and expires_at <= at):
            raise ValueError("amount must be positive and expiry must be after the grant time")
        self._commit(grants={**self._grants, grant_id: Grant(grant_id, amount, at, expires_at)})

    def charge(self, charge_id: str, amount: int, at: datetime) -> tuple[Allocation, ...]:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._commit(charges={**self._charges, charge_id: Charge(charge_id, amount, at)})
        return self.allocations(charge_id)

    def balance(self, at: datetime) -> int:
        """at 这一刻可用的额度：只重放到 at，已过期的包不算。"""
        _, remaining = _replay(self._grants, self._charges, until=at)
        return sum(left for gid, left in remaining.items()
                   if (exp := self._grants[gid].expires_at) is None or exp > at)

    def allocations(self, charge_id: str) -> tuple[Allocation, ...]:
        """这笔扣费在"所有事件排好序"的结果里用了哪些包：迟到的事件可能改变它，但总额不变。"""
        if charge_id not in self._charges:
            raise UnknownChargeError(charge_id)
        return _replay(self._grants, self._charges)[0][charge_id]

    def _commit(self, *, grants: dict[str, Grant] | None = None, charges: dict[str, Charge] | None = None) -> None:
        """先在副本上重放：所有已接受的扣费都仍能全额扣下才替换真实状态，失败时账本原封不动。"""
        grants = self._grants if grants is None else grants
        charges = self._charges if charges is None else charges
        _replay(grants, charges)
        self._grants, self._charges = grants, charges
```

**运行。** 两个包 `soon`（100，第 10 天到期）和 `late`（100，第 30 天到期），都从第 0 天起：
- 第 1 天扣 60，得到 `soon` 60；第 2 天再扣 60，得到 `soon` 40 和 `late` 20；
- `balance` 在第 0 天是 200，第 2 天是 80，第 10 天是 80（`soon` 已用完且到期），第 30 天是 0；
- 第 3 天扣 500，抛 `InsufficientCreditsError`（差 420），余额仍是 80；
- 乱序：`g1`（第 10 天到期）和 `g2`（第 20 天到期）各 100，第 5 天的 `c2` 先到，用的是 `g1`；第 3 天的 `c1` 迟到，`c1` 用 `g1`，`c2` 的分配自动变成 `g2`；再迟到一笔第 4 天的 100 会让 `c2` 扣不下，被拒绝（`charge c2 is short by 100`）；
- 同一时刻：包 `a` 在第 2 天到期、包 `b` 在第 2 天生效，第 2 天的余额是 10（`a` 已失效、`b` 已生效）；
- **示例：发放 10、5、7 后扣 20：** 发放 10、5、7（同一到期日，生效时间递增）后扣 20：分配是 10、5、5，余额 2；若扣费先到而发放 7 的包没到，则差 5 被拒绝，迟到的包到达后扣费成功。

**逐步扩展。**
1. 【追问再讲】幂等与冲突：触发"网络重试，同一个请求发了两次"。同一个 `id` 用相同的参数重试，返回第一次的结果，不再扣第二次；参数不同抛 `ConflictError`，是难查的账务错误，不能悄悄忽略。被拒绝的扣费不入账，所以补了额度之后可以用同一个 `id` 重试。判断就是 `old != new`，因为事件是冻结的数据类。

```python
class ConflictError(LedgerError): ...                  # 同一个 id 用不同的参数提交过


class CreditLedger:  # 只列出新增或替换的方法
    def grant(self, grant_id: str, amount: int, at: datetime, expires_at: datetime | None = None) -> None:
        if amount <= 0 or (expires_at is not None and expires_at <= at):
            raise ValueError("amount must be positive and expiry must be after the grant time")
        new = Grant(grant_id, amount, at, expires_at)
        old = self._grants.get(grant_id)
        if old is not None:                            # 同参数重复提交是幂等的：什么都不做
            if old != new:                             # 冻结数据类自带按值比较，冲突判断就一句
                raise ConflictError(f"grant {grant_id} already exists with different terms")
            return
        self._commit(grants={**self._grants, grant_id: new})

    def charge(self, charge_id: str, amount: int, at: datetime) -> tuple[Allocation, ...]:
        if amount <= 0:
            raise ValueError("amount must be positive")
        new = Charge(charge_id, amount, at)
        old = self._charges.get(charge_id)
        if old is not None:
            if old != new:
                raise ConflictError(f"charge {charge_id} already exists with different terms")
            return self.allocations(charge_id)         # 重试：返回和第一次相同的分配，不再扣第二次
        self._commit(charges={**self._charges, charge_id: new})   # 被拒绝的扣费不入账，补了额度可以用同一个 id 重试
        return self.allocations(charge_id)
```

2. 【加分】作废额度包：触发"撤回一个发放"。等价于把到期时间提前到 `at`：用 `dataclasses.replace` 生成改过到期时间的副本，复用同一套"副本重放、通过再提交"；已经扣掉的不追回；会让某笔已有扣费凑不够就拒绝。

```python
from dataclasses import replace


class UnknownGrantError(LedgerError): ...


class CreditLedger:  # 只列出新增或替换的方法
    def revoke(self, grant_id: str, at: datetime) -> None:
        """从 at 起这个包剩余的额度作废，等价于把到期时间提前到 at；已经扣掉的不追回。"""
        grant = self._grants.get(grant_id)
        if grant is None:
            raise UnknownGrantError(grant_id)
        if at <= grant.at:
            raise ValueError("cannot revoke at or before the grant time")
        if grant.expires_at is not None and grant.expires_at <= at:
            return                                     # 已经更早失效，什么都不用做
        self._commit(grants={**self._grants, grant_id: replace(grant, expires_at=at)})   # 同一套"副本重放、通过再提交"
```

**运行（逐步扩展）。**
- 重试：`c1` 用相同参数再来一次，返回同样的分配；金额改成 61 抛 `ConflictError`；
- 作废：一个 100 的包，第 1 天扣 30，第 2 天作废：第 1 天余额 70，第 2 天余额 0，之后再扣 1 被拒绝；
- 三层整合（核心加逐步扩展 1、2）：对同一套组合代码跑完整的单元测试，共 23 项全部通过；只有核心时通过 17 项，其余 6 项（冲突检测、作废）要加上逐步扩展才过。

**深入。**
1. 【必讲】存事件、重放出结果，而不是"收到就直接扣减":
   - 直接扣减假设事件按时间顺序到达：迟到的事件会让已经做出的分配变错，补救就要回滚再重做，等于临时拼凑一个重放；
   - 账本里只存事件，余额和分配都是对排好序的事件重放得到的结果：乱序、迟到、作废全部变成"改事件表再重放"；
   - `_replay` 是不碰 `self` 的纯函数，所以能对副本试跑；写在方法里就没法试跑，失败时要手工回滚（事件溯源加试运行提交）。
2. 【必讲】先到期先扣用堆，过期惰性删除：
   - 最小堆的键是 `(永不过期?, 到期时间, 发放时间, id)`：先到期的先扣，永不过期的最后，平局有确定顺序；
   - 重放里时间只往前走，过期的包浮到堆顶时弹出，每个包最多进出堆各一次；放弃"每笔扣费把所有包排序一遍"，那样每笔扣费 O(g log g)；
   - 排序键 `(at, isinstance(e, Charge), id)`：同一时刻先发放后扣费，保证"发放时刻就能用"；`id` 兜底，让结果与到达顺序无关。
3. 【必讲】接受迟到事件的条件与代价：
   - 条件：重放之后每笔已接受的扣费仍能全额扣下。放弃"迟到事件一律拒绝"，乱序是常态，一律拒绝会丢账；放弃"一律接受，让旧扣费变成欠款"，已经告诉调用方成功的扣费不应该事后失败。代价是迟到的扣费有时会被拒绝；
   - 现象：迟到事件会改变旧扣费用了哪些包，但总额不变；
   - 重放代价：每个新事件都重放全部事件，复杂度 O(E log E)，逐个写入 E 个事件是 O(E² log E)。一次本机实测，交替写入发放和扣费，1,000 个事件约 0.2 秒，2,000 个约 0.8 秒，4,000 个约 3.4 秒（随机器而异）：事件数翻倍，时间约翻四倍。
4. 【追问再讲】区间的开闭要一致：发放时刻含、到期时刻不含，同一时刻先发放后扣费；这几个边界一旦不一致，就会出现"刚发放的额度用不上"或"到期那一刻还能花"。
5. 【追问再讲】幂等和冲突分开：相同参数返回原结果，不同参数报错；只按 `id` 去重会让同 `id` 不同金额被悄悄忽略。核心实现里没有这一层，同 `id` 会直接覆盖，所以要先说明假设 `id` 唯一。
6. 【追问再讲】不够扣时的策略要问清：核心是整笔拒绝并保持账本不变（返回失败）；另一种语义是"能扣多少扣多少，其余忽略"，实现上只要删掉 `_replay` 末尾的 `if need: raise ...` 两行，扣费就只取到手的部分。实测：一个 10 的包上扣 25，得到 10、余额 0；之后迟到一个 5 的包，同一笔扣费的分配变成 10 加 5。这种语义下账本不再拒绝任何扣费。
7. 【加分】增量重放：事件很多时，一个办法是保存重放的检查点（堆和剩余额度），新事件的时间不早于最后一个事件时只喂这一个事件；迟到事件才从最早受影响的时刻重放。迟到事件通常离现在不远，所以代价小。
8. 【加分】持久化与并发：事件追加到日志，按 `id` 去重，重放由单个写入者提交，读者用快照；退款是一种新事件，把额度退回原来被扣的包，包已过期就不再有效，重放时在对应时间点处理。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 为什么 `balance` 只重放到 `at`：这样它是时间的函数，而不是到达顺序的函数，可以回答"上周三的余额"。
- 为什么返回值用 `NamedTuple`：既能像元组一样比较、拆包，又有字段名；普通元组让调用方记位置，数据类又要多写比较。
- 想让迟到的扣费总能成功、宁可让旧扣费失败：重放后不够就把最晚的一笔标成欠款，需要把欠款也作为一种可结算的状态。
- 金额为什么用整数：额度本来就是整数单位；用浮点会累积误差，要小数就用最小单位的整数。
- 想要"到期前一段时间提醒"：到期是确定的事件时间，由单独的扫描任务按到期时间查询包即可，不进入账本核心。

**级别期望。**
- 中级：核心实现中的发放、扣费、先到期先扣、余额，顺序到达即可。
- 高级：乱序到达也正确：存事件、纯函数重放、试跑再提交；堆加惰性删除；开闭区间与同一时刻规则；幂等与冲突。
- 资深/专家：说清为什么迟到事件会改变旧分配而总额不变；不够扣的几种语义；重放的 O(E² log E) 代价与检查点、快照；作废与退款作为新事件。

**先修概念。**
- [[hi-low-level-design-in-a-hurry-delivery|答题框架]]
- [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]
- [[hi-low-level-design-in-a-hurry-design-principles|设计原则]]
- [[hi-system-design-core-concepts-data-modeling|数据建模]]

**同类题。**
- [[solution-digital-wallet|设计题解：数字钱包]]
- [[solution-bank-account|设计题解：银行账户]]
- [[solution-ttl-cache|设计题解：带过期时间的缓存]]
- [[solution-rate-limiter|设计题解：限流器]]
