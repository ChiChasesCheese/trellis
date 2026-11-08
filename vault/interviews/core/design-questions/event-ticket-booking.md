---
slug: event-ticket-booking
kind: low-level-design
---

## Q
**活动票务预订后端（防超卖的 REST 服务）**｜低层设计

设计并实现一个活动票务系统的后端 RESTful 服务：主办方创建和修改活动，设置多种票型（VIP、普通）、价格、容量和开售与停售时间；用户先限时保留（reserve）票，再付款购买；多个用户同时抢票时库存必须准确，不能超卖；保留超时或付款失败要释放库存；支持取消订单与退款，查看个人订单历史。技术要求写明：乐观锁或悲观锁、ACID 事务、失败回滚、付款状态跟踪、接口限流、错误场景处理。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 核心是库存计数器的并发安全加上"保留—购买—过期"三态的状态机：用一条带条件的原子更新同时完成"检查够不够"和"占住"，付款这种慢的外部调用放在数据库事务之外，并让所有释放动作都具备幂等保护，避免同一份库存被释放两次。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定实体和接口 |
| 8–15 分 | 讲状态机和条件更新，画整体设计 |
| 15–45 分 | 写核心实现：`TicketType`、`Reservation`、`BookingService` |
| 45–50 分 | 跑例子：并发抢票、付款、过期 |
| 50–60 分 | 追问：幂等键、退款、锁的选择、限流 |

**需求。**
- 功能：
  1. 活动管理：创建与更新活动（名称、描述、时间、场馆与容量），按票型设定价格、数量、开售与停售时间。
  2. 查询：活动详情与各票型实时可售数量。
  3. 保留：用户选择票型与数量，系统占住库存并给出过期时间（例如 10 分钟）。
  4. 购买：在保留有效期内付款，成功后出票；失败或超时释放库存。
  5. 取消与退款；个人订单历史。
- 非功能：
  - 不超卖：任何时刻 `已售 + 已保留 ≤ 总量`。
  - 并发：热门活动开售瞬间数万人同时请求，单个票型的库存是一个热点计数器。
  - 原子性：保留与计数更新同事务；购买中途失败可回滚到保留状态。
  - 接口：幂等（重试不重复扣库存）、限流（防刷）、错误码清晰（409 售罄、410 保留过期、422 未开售、429 限流）。

**核心实体与接口。**
- 实体：
  - `Event`：活动。`TicketType`：票型，字段 `total`、`sold`、`held`、`price_cents`、`sale_start`、`sale_end`。可售数 = `total - sold - held`。
  - `Reservation`：保留记录，状态 `HELD → CONFIRMED / EXPIRED / CANCELLED`，字段 `qty`、`expires_at`、`idempotency_key`。
  - `Booking`：购买完成后的订单，含 `payment_status`（PENDING、PAID、FAILED、REFUNDED），保存下单时的价格快照。`Refund`：退款记录。
- 接口：
  - `POST /events`、`PUT /events/{id}`、`GET /events/{id}`（含各票型可售数量）。
  - `POST /events/{id}/reservations {ticketTypeId, qty}`，头部 `Idempotency-Key`，成功 201，返回 `reservationId` 与 `expiresAt`。
  - `POST /reservations/{id}/purchase {paymentToken}`；`DELETE /bookings/{id}` 取消并退款；`GET /users/me/bookings`。
- 类的职责：`BookingService` 编排流程，`TicketType` 封装库存的原子操作（数据库版是仓储层的一条条件 `UPDATE`），`PaymentGateway` 是外部支付的接口（可换成假实现），`HoldSweeper` 定时释放过期保留，`RateLimiter` 是接口层的令牌桶。

**整体设计。**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 328">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="170" y1="36" x2="170" y2="53"/>
<line x1="170" y1="86" x2="170" y2="103"/>
<line x1="170" y1="136" x2="170" y2="153"/>
<line x1="170" y1="186" x2="170" y2="203"/>
<line x1="170" y1="236" x2="170" y2="253"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="12" y="8" width="316" height="28" rx="3"/>
<rect x="12" y="58" width="316" height="28" rx="3"/>
<rect x="12" y="108" width="316" height="28" rx="3"/>
<rect x="12" y="158" width="316" height="28" rx="3"/>
<rect x="12" y="208" width="316" height="28" rx="3"/>
<rect x="12" y="258" width="316" height="28" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="170,58 167,52 173,52"/>
<polygon points="170,108 167,102 173,102"/>
<polygon points="170,158 167,152 173,152"/>
<polygon points="170,208 167,202 173,202"/>
<polygon points="170,258 167,252 173,252"/>
</g>
<g fill="currentColor">
<text x="170" y="26" font-size="12">POST 保留(幂等键 + 限流)</text>
<text x="170" y="76" font-size="12">原子条件 UPDATE 占库存</text>
<text x="170" y="126" font-size="12">事务一: 锁保留行校验</text>
<text x="170" y="176" font-size="12">支付网关(事务外, 幂等键)</text>
<text x="170" y="226" font-size="12">事务二: held 转 sold 出票</text>
<text x="170" y="276" font-size="12">Sweeper: 过期 HELD 条件释放</text>
</g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="302" font-size="11">状态迁移都用条件更新</text></g>
</g></svg>
```
- 保留：事务内执行下面的条件更新并插入 `reservation`（HELD，带过期时间）。受影响行数为 0 就是售罄或未开售。
- 购买：事务一读取并锁定 `reservation` 行，确认 HELD 且未过期；提交后调用支付网关（带预订号作幂等键）；事务二把 `held` 转为 `sold`，保留改为 CONFIRMED，插入 `booking`。付款与确认之间崩溃时，用付款幂等键查询支付状态对账。
- 过期：`HoldSweeper` 每几十秒扫描 `HELD` 且过期的记录，用条件更新改为 EXPIRED，成功才释放 `held`。

```sql
UPDATE ticket_type
SET held = held + :qty
WHERE id = :id
  AND now() BETWEEN sale_start AND sale_end
  AND total - sold - held >= :qty;
-- 受影响行数 = 1 才继续插入 reservation；同一个事务内完成
```

**核心实现。** 约 90 行，下面的内存版和上面的数据库版一一对应。并发正确性集中在 `TicketType` 一个类里，其余代码只调它的原子方法，容易审查也容易压测。用到的模式：状态机（保留的生命周期）、服务与仓储分层、支付网关接口（可替换，便于测试注入失败）。

```python
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from typing import Protocol
import time, uuid


class RStatus(Enum):
    HELD = 1; CONFIRMED = 2; EXPIRED = 3; CANCELLED = 4


class SoldOut(Exception): ...
class HoldExpired(Exception): ...
class NotOnSale(Exception): ...


@dataclass
class TicketType:
    total: int
    sale_start: float
    sale_end: float
    sold: int = 0
    held: int = 0
    _lock: Lock = field(default_factory=Lock, repr=False)  # 内存版的“行锁”；数据库版由一条带条件的 UPDATE 承担

    def try_hold(self, qty: int, now: float) -> None:
        """检查 + 占住必须在同一个原子步骤内，否则两个请求会同时看到“还剩 1 张”。"""
        if not (self.sale_start <= now <= self.sale_end):
            raise NotOnSale()
        with self._lock:
            if self.total - self.sold - self.held < qty:
                raise SoldOut()
            self.held += qty

    def release_hold(self, qty: int) -> None:
        with self._lock:
            self.held -= qty

    def confirm(self, qty: int) -> None:  # 保留 -> 已售，总占用量不变，所以不会超卖
        with self._lock:
            self.held -= qty
            self.sold += qty


@dataclass
class Reservation:
    rid: str
    tt: TicketType
    qty: int
    expires_at: float
    status: RStatus = RStatus.HELD


class PaymentGateway(Protocol):
    def charge(self, token: str, amount: int, idem_key: str) -> bool: ...


class BookingService:
    HOLD_SECONDS = 600

    def __init__(self, pay: PaymentGateway) -> None:
        self.pay = pay
        self.reservations: dict[str, Reservation] = {}

    def reserve(self, tt: TicketType, qty: int, now: float | None = None) -> Reservation:
        now = time.time() if now is None else now
        tt.try_hold(qty, now)
        r = Reservation(uuid.uuid4().hex, tt, qty, now + self.HOLD_SECONDS)
        self.reservations[r.rid] = r
        return r

    def purchase(self, rid: str, token: str, price_cents: int, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        r = self.reservations[rid]
        if r.status is RStatus.CONFIRMED:
            return True  # 重复请求直接返回成功
        if r.status is not RStatus.HELD or now > r.expires_at:
            raise HoldExpired()
        # 外部付款不放进数据库事务里：不要拿着行锁等第三方
        if not self.pay.charge(token, price_cents * r.qty, idem_key=rid):
            return False  # 付款失败：保留仍然有效，用户可以换卡重试
        r.tt.confirm(r.qty)
        r.status = RStatus.CONFIRMED
        return True

    def sweep_expired(self, now: float | None = None) -> None:
        now = time.time() if now is None else now
        for r in list(self.reservations.values()):
            if r.status is RStatus.HELD and r.expires_at < now:
                # 只有状态确实从 HELD 变成 EXPIRED 才归还库存，防止重复释放
                r.status = RStatus.EXPIRED  # 数据库版：UPDATE ... WHERE status='HELD'，看影响行数
                r.tt.release_hold(r.qty)
```

**运行。**

```python
class Pay:  # 假的支付网关，可以让它失败
    def __init__(self, ok=True): self.ok = ok
    def charge(self, token, amount, idem_key): return self.ok

tt = TicketType(total=5, sale_start=0, sale_end=1000)
svc = BookingService(Pay())
# 16 个线程同时抢 20 次，每次 1 张
```

- 20 次保留 → 5 次成功、15 次 `SoldOut`，`held = 5`，没有超卖。
- 购买第一张 → `True`，`sold = 1, held = 4`；重复购买同一个 `rid` → 仍是 `True`，`sold` 不变。
- `t = 700` 时清理过期保留 → `held = 0, sold = 1`。
- 开售窗口外保留 → `NotOnSale`；保留超过 600 秒再付款 → `HoldExpired`。
- 付款失败 → 返回 `False`，保留仍是 `HELD`，用户可以换卡重试。

**复杂度。** 保留、购买、释放都是 `O(1)`；清理任务扫描所有保留，`O(m)`，数据库版建 `(status, expires_at)` 索引后只扫到期的。

**逐步扩展。**
1. 【追问再讲】幂等键：客户端网络超时后重试，同一个键必须得到同一份保留，不能重复占库存。内存版整段放在服务锁内，数据库版是对 `(user_id, idempotency_key)` 加唯一约束。

```python
# __init__ 里加：self.by_idem = {}; self._lock = Lock()
def reserve(self, tt, qty, idem_key, now=None):
    now = time.time() if now is None else now
    with self._lock:  # 整段在锁内：同一个键的两个并发请求只有一个会真的占库存
        if idem_key in self.by_idem:
            return self.reservations[self.by_idem[idem_key]]
        tt.try_hold(qty, now)
        r = Reservation(uuid.uuid4().hex, tt, qty, now + self.HOLD_SECONDS)
        self.reservations[r.rid] = r
        self.by_idem[idem_key] = r.rid
        return r
```

2. 【加分】取消与退款：只有 `CONFIRMED` 才能取消；状态迁移成功才还库存，退款交给异步任务并用幂等键。

```python
def refund(self, qty):  # TicketType
    with self._lock:
        self.sold -= qty

def cancel(self, rid):  # BookingService
    r = self.reservations[rid]
    if r.status is not RStatus.CONFIRMED:
        return False
    r.status = RStatus.CANCELLED  # 数据库版：条件更新 WHERE status='CONFIRMED'
    r.tt.refund(r.qty)
    self.pay.refund(rid)  # PaymentGateway 再加 refund(idem_key)，同样幂等
    return True
```

8 个线程用同一个键保留 2 张 → 只有 1 份保留，`held = 2`；购买后取消 → `True`，`sold = 0`；再取消一次 → `False`，不会重复退款。

**深入。**
1. 【必讲】并发控制：为什么用带条件的原子更新。
   - 悲观锁（`SELECT ... FOR UPDATE` 锁票型行）：简单，但热门票型所有请求排队，持锁必须极短，且不能把付款放在锁内。
   - 乐观锁（`version` 列，更新带 `WHERE version = ?`，失败重试）：冲突少时吞吐高；开售瞬间冲突率极高，大量重试反而浪费。
   - 带条件的原子更新（选用）：一条语句完成检查与更新，锁的时间最短，不需要重试循环，对单计数器最合适。多个资源一起锁（座位、捆绑票型）才回到行锁，并固定加锁顺序避免死锁。
2. 【必讲】事务与外部付款。
   - 付款是外部调用，无法纳入事务，所以拆成两个短事务：「保留 + 计数」和「确认 + 出票」，中间用状态和幂等键衔接。
   - 付款结果不明（超时）：不要贸然释放库存，进入待核实状态，用幂等键向支付方查询；确认失败再释放，确认成功补全订单。
3. 【必讲】状态机与过期释放。
   - 保留的状态迁移只允许 HELD → CONFIRMED / EXPIRED / CANCELLED；每次迁移用条件更新并检查影响行数。
   - 过期任务和购买请求同时到达时，只有一个能改成功，另一个得到明确的错误（410 保留过期）；只有状态确实变化才归还库存，避免同一份库存被释放两次。
   - 读可售数量时可以把过期保留当作已释放，减少用户看到「已售罄」的时间。
4. 【追问再讲】接口错误码：409 售罄、410 保留过期、422 未开售、429 限流。付款失败时保留仍有效。
5. 【追问再讲】开售热点与限流：接口层令牌桶按用户与 IP 限流，返回 429 加 `Retry-After`，超出库存的请求越早失败越好。再升级用前置虚拟等候室把请求匀速放入，避免几万个并发更新压住行锁。防刷：验证码，以及保留时校验该用户该活动已购与已保留的总量。
6. 【加分】选座与容量修改。
   - 选座：从计数改为逐座位行，保留时条件更新 `WHERE status='AVAILABLE'`，检查影响行数等于座位数；固定加锁顺序。
   - 修改票型数量：新 `total` 不能小于 `sold + held`；各票型总量之和不超过场馆容量，同一事务内校验。价格修改不影响已存在的保留与订单。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 库存计数为什么不只放 Redis：库存与订单要同事务一致，Redis 与数据库之间会出现不一致；可以用 Redis 做前置的快速拒绝（明显售罄时直接返回），最终以数据库为准。
- 保留时长多久：太短用户来不及付款，太长占着库存；10 分钟常见，抢手活动可更短并显示倒计时。
- 退款规则：按距开场时间分档，退款金额在订单上保留规则快照；已使用的票不可退。

**级别期望。**
- 中级：活动、票型、订单的表和接口，说出为什么需要事务，知道先扣库存再付款的顺序；核心实现里的保留和购买能跑通。
- 高级：原子条件更新防超卖、保留—购买—过期状态机、过期释放的幂等保护、幂等键、限流。
- 资深（staff）：付款与事务边界的拆分及对账、悲观与乐观锁在热点下的取舍、虚拟等候室、座位级加锁顺序、容量约束的一致性。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-concurrency-intro|并发入门]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-system-design-core-concepts-api-design|API 设计]]、[[hi-system-design-patterns-dealing-with-contention|处理争用（Contention）]]

**同类题。** [[solution-movie-booking]]、[[solution-ticket-booking]]（系统设计版）、[[hi-system-design-problem-breakdowns-ticketmaster|票务预订（Ticketmaster）]]、[[hi-low-level-design-problem-breakdowns-bookmyshow|电影票预订（BookMyShow）]]
