# 库存管理（Inventory Management）

电商的库存分散在好几个仓库里。下单时要先"预留"库存：占住但不立刻发货，付款成功再确认发货，
放弃或超时就放回去。预留带有效期，过期没人管就自动释放；很多用户同时抢最后几件时，绝不能卖出超过实际库存的数量。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：多仓库存；`reserve` 预留（可能跨仓库、全有或全无）；`confirm` 确认发货；`cancel` 取消；
  可售数量 = 在架 - 被预留占用；各种错误（数量不合法、库存不足、预留不存在、状态不允许）。
- 第 2 关（约 15 分钟）：预留的有效期：`reserve(..., ttl=)`，到点自动释放（不起后台线程）；过期后确认要报错；
  `extend` 延期；已确认、已取消的预留不会被过期处理再碰一次。
- 第 3 关（约 20 分钟）：多个线程同时预留，不能超卖，也不能出现一个预留只占了一半；
  `reserve_many` 一次预留多件商品，全有或全无，两种商品顺序相反的并发请求不会死锁。
- 第 4 关（选做）：`transfer` 在仓库之间调拨没被预留的库存；`snapshot` 返回一致的库存快照。

**接口**

```python
class InventoryError(Exception)              # 以下全是它的子类
class InvalidQuantity(ValueError)            # 数量不是正整数（bool、浮点、字符串都不是）
class OutOfStock                             # 属性 sku、requested、available（当时的可售总量）
class UnknownReservation(LookupError); class ReservationExpired; class InvalidState

class Status(Enum): ACTIVE; CONFIRMED; CANCELLED; EXPIRED
@dataclass(frozen=True, slots=True) class Allocation: warehouse: str; quantity: int
@dataclass(frozen=True, slots=True) class Reservation:
    id: str; sku: str; quantity: int; allocations: tuple[Allocation, ...]; expires_at: float | None; status: Status
@dataclass(frozen=True, slots=True) class StockRow: warehouse: str; sku: str; on_hand: int; reserved: int

class Inventory:
    def __init__(self, clock: Callable[[], float] = time.monotonic)
    def add_stock(self, warehouse: str, sku: str, quantity: int) -> None
    def on_hand(self, sku: str, warehouse: str | None = None) -> int
    def available(self, sku: str, warehouse: str | None = None) -> int
    def reserve(self, sku: str, quantity: int, ttl: float | None = None) -> Reservation
    def confirm(self, reservation_id: str) -> None
    def cancel(self, reservation_id: str) -> None
    def get(self, reservation_id: str) -> Reservation
    def extend(self, reservation_id: str, ttl: float) -> Reservation                       # 第 2 关
    def reserve_many(self, lines: Mapping[str, int], ttl: float | None = None) -> tuple[Reservation, ...]   # 第 3 关
    def transfer(self, sku: str, source: str, target: str, quantity: int) -> None          # 第 4 关
    def snapshot(self) -> tuple[StockRow, ...]
```

规则细节：

- `on_hand` 是实际在架（含被预留占着的）；`available` 是在架减去有效预留占用；没见过的商品和仓库都是 0。
- 分配规则是确定的：先从可售最多的仓库拿，同样多取仓库名小的，拿完为止。因此一个预留可能跨仓库，`allocations` 数量之和等于 `quantity`。
- 库存不足抛 `OutOfStock`，不占任何库存；`available` 属性是当时所有仓库的可售总量。
- `confirm`：在架按分配扣减，预留不再占用；重复确认是无操作；已过期抛 `ReservationExpired`；已取消抛 `InvalidState`。
  `cancel`：库存放回；重复取消、取消已过期的预留是无操作；已发货抛 `InvalidState`。
- 有效期左闭右开：`clock() >= expires_at` 即过期，到点那一刻库存已经可以被新的预留拿走。状态不靠后台线程变化，每次调用时结清。
- `extend`：新的过期时间是"现在 + ttl"，不是在原期限上累加，可以缩短；对没有期限的预留也可以加上期限；已过期抛 `ReservationExpired`；已确认或已取消抛 `InvalidState`。`ttl <= 0` 抛 `ValueError`。
- `reserve_many`：返回按 sku 排序的预留；有不足时抛 `OutOfStock`，报告按 sku 排序的第一件不足的；`lines` 为空抛 `ValueError`。
- `transfer` 只能调可售的部分，已有预留的分配不变；源仓库可售不够抛 `OutOfStock`；两个仓库相同抛 `ValueError`。
- 返回的 `Reservation` 是快照：之后预留的状态变化不会改动已经交出去的对象。

例子：

```python
inv = Inventory(clock=clock)
inv.add_stock("A", "widget", 10); inv.add_stock("B", "widget", 5)
r = inv.reserve("widget", 12, ttl=60)     # allocations: A 取 10，B 取 2；available("widget") == 3
inv.reserve("widget", 4)                  # 抛 OutOfStock（要 4，可售 3）
# 60 秒过去
inv.available("widget")                   # 15：预留过期，库存放回
inv.confirm(r.id)                         # 抛 ReservationExpired
```

**评分点**

- 账只有两个数：在架和被预留占用；每个操作都只是在这两个数上加减，且保持 `0 <= 占用 <= 在架`。
- 先计划、后提交：计划阶段只读，提交阶段只做加法、不会失败，所以"库存不足"不会留下半截预留；多件商品同理。
- 过期不起后台线程：每个操作开头先结清到点的预留；到点预留放在按时间排序的堆里，延期、确认、取消不去堆里删，只让条目作废（惰性删除）。
- 注入时钟，测试里没有 `sleep`；有效期的边界（恰好到点）有明确约定。
- 并发下不超卖：检查和占用在同一个临界区；能说清为什么先用一把锁，什么时候才需要按商品分段加锁。
- 状态机清楚：哪些状态转换合法，重复的确认、取消是无操作还是错误，有明确答案并加以测试。
- 对外只给不可变快照；错误带上调用方需要的信息（`OutOfStock` 报可售数量）。
- 能口述：库存预留的幂等键、预留与订单的关系、安全库存和补货、跨仓调拨的在途库存、分布式下的超卖防护（数据库条件更新、分片）。
