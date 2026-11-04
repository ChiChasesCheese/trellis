---
slug: beverage-vending-system
kind: low-level-design
---

## Q
**多地点饮品自助售卖系统**｜低层设计

设计一个由中心平台统一接单的饮品自动售卖系统：很多台机器分布在不同地点，机器内部存放原料（咖啡豆、牛奶、糖浆、杯子等），能现场制作新鲜饮品；顾客在手机或网页上下单，选择取货地点，到机器前凭取货码取走饮品；机器日常无人值守，只有原料不足时才需要人工补货。要求画出类与职责，说明库存、订单状态、并发下单、机器故障和补货通知是怎么处理的，并写出核心类的代码。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 核心是「库存预留」：下单时先在目标机器上预留原料，制作成功才真正扣减，失败则释放；订单是状态机；补货是对库存水位的监听，而不是人工巡检。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定接口 |
| 8–15 分 | 画类与职责，定订单状态 |
| 15–42 分 | 写核心实现：库存、订单、下单、制作回调 |
| 42–48 分 | 跑例子，包括抢最后一杯 |
| 48–60 分 | 追问：取货码和超时、故障、菜单、补货 |

**需求。**
- 功能：
  1. 查看某地点当前可点的饮品（由该机器的库存决定）。
  2. 下单并支付，系统选择机器、预留原料，返回取货码。
  3. 机器制作饮品，完成后顾客凭取货码取走；超时未取则作废。
  4. 原料低于阈值时自动生成补货任务并通知运维人员；补货后库存更新。
  5. 机器离线或制作失败时订单自动退款，原料预留释放。
- 非功能：
  - 同一台机器同时有多笔订单竞争同一份原料，不允许超卖（预留总量不得超过库存）。
  - 假设 5000 台机器，高峰每台每分钟 2 单，系统约 170 单每秒，中心服务可以水平扩展，机器本地一次只制作一杯。
  - 状态变更幂等：重复的支付回调、重复的取货请求不会产生副作用。

**核心实体与接口。**
- `Recipe`：饮品配方，原料到用量的映射，不可变。
- `Inventory`：一台机器的原料库存，维护实际量和已预留量，提供 `reserve`、`commit`、`release`。线程安全是这个类的责任。
- `Machine`：地点、在线状态、`Inventory`；通过 `MachineController` 接口驱动硬件，便于用假实现测试。
- `Order`：状态机 `CREATED → RESERVED → BREWING → READY → PICKED_UP`，另有 `FAILED`、`EXPIRED`、`CANCELLED`；持有取货码。
- `OrderService`：中心入口，选机器、预留、建单、推动状态变化。
- 关键接口：`place_order(location, drink)`、`on_brewed(order_id, ok)`、`pickup(order_id, code)`；扩展里再加 `menu(location)`、`refill`。

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
<text x="170" y="26" font-size="12">顾客下单(手机)</text>
<text x="170" y="76" font-size="12">OrderService: 选机器</text>
<text x="170" y="126" font-size="12">Inventory.reserve 预留原料</text>
<text x="170" y="176" font-size="12">机器队列制作 -> on_brewed</text>
<text x="170" y="226" font-size="12">commit 扣减 / release 归还</text>
<text x="170" y="276" font-size="12">取货码出杯 | 水位 -> 补货任务</text>
</g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="302" font-size="11">订单与库存各有状态机</text></g>
</g></svg>
```
- 下单：`OrderService` 选机器，调用 `Inventory.reserve`；成功才创建订单并返回取货码，失败则换下一台或提示不可点。
- 制作：机器的制作队列串行消费（一次一杯）；`MachineController` 调硬件，完成后回调 `on_brewed`。
- 取货：顾客输入取货码，匹配且状态为 `READY` 才开门，同时标记 `PICKED_UP`。
- 补货：库存每次 `commit` 后检查水位，低于阈值就建补货任务通知运维（逐步扩展 3）。

**核心实现。** 约 30 分钟，下面是全部要写的代码：库存的预留、提交、释放，订单状态机，下单，制作回调。取货放在逐步扩展 2。

```python
import secrets
from dataclasses import dataclass, field
from enum import Enum
from threading import RLock


@dataclass(frozen=True)
class Recipe:
    name: str
    parts: dict[str, int]          # 原料 -> 单杯用量


class Inventory:
    """一台机器的库存。可用量 = 实际量 - 已预留量。"""
    def __init__(self, stock: dict[str, int]) -> None:
        self._stock, self._reserved = dict(stock), {}
        self._lock = RLock()       # 检查与预留必须在同一把锁内，否则两单会同时看到“够”

    def reserve(self, r: Recipe) -> bool:
        with self._lock:           # 全有或全无：先整体检查，再整体预留
            if any(self._stock.get(i, 0) - self._reserved.get(i, 0) < q
                   for i, q in r.parts.items()):
                return False
            for i, q in r.parts.items():
                self._reserved[i] = self._reserved.get(i, 0) + q
            return True

    def commit(self, r: Recipe) -> None:      # 制作成功：预留转为真实消耗
        with self._lock:
            for i, q in r.parts.items():
                self._reserved[i] -= q
                self._stock[i] -= q

    def release(self, r: Recipe) -> None:     # 制作失败：只归还预留
        with self._lock:
            for i, q in r.parts.items():
                self._reserved[i] -= q


class Status(Enum):
    CREATED = 1; RESERVED = 2; BREWING = 3; READY = 4
    PICKED_UP = 5; FAILED = 6; EXPIRED = 7; CANCELLED = 8


# 合法迁移集中在一张表，非法迁移直接报错
ALLOWED = {
    Status.CREATED: {Status.RESERVED, Status.CANCELLED, Status.FAILED},
    Status.RESERVED: {Status.BREWING, Status.CANCELLED, Status.FAILED},
    Status.BREWING: {Status.READY, Status.FAILED},
    Status.READY: {Status.PICKED_UP, Status.EXPIRED},
}


@dataclass
class Order:
    order_id: str
    machine_id: str
    recipe: Recipe
    pickup_code: str = field(default_factory=lambda: secrets.token_hex(3))
    status: Status = Status.CREATED

    def move(self, to: Status) -> bool:
        if self.status == to:
            return False                       # 幂等：已在目标状态，不再产生副作用
        if to not in ALLOWED.get(self.status, set()):
            raise ValueError(f"{self.status.name} -> {to.name} not allowed")
        self.status = to
        return True


class Machine:
    def __init__(self, machine_id: str, location: str, stock: dict[str, int]) -> None:
        self.machine_id, self.location = machine_id, location
        self.inventory, self.online = Inventory(stock), True


class OrderService:
    def __init__(self, machines: list[Machine], recipes: dict[str, Recipe]) -> None:
        self.machines = {m.machine_id: m for m in machines}
        self.recipes, self.orders = recipes, {}

    def place_order(self, location: str, drink: str) -> Order:
        recipe = self.recipes[drink]
        for m in self.machines.values():       # 选机策略可替换：这里取第一台能做的
            if m.location == location and m.online and m.inventory.reserve(recipe):
                order = Order(secrets.token_hex(4), m.machine_id, recipe)
                order.move(Status.RESERVED)
                self.orders[order.order_id] = order
                return order
        raise LookupError("该地点暂时无法制作，请换一杯或换地点")

    def on_brewed(self, order_id: str, ok: bool) -> None:
        o = self.orders[order_id]
        inv = self.machines[o.machine_id].inventory
        if ok and o.move(Status.READY):
            inv.commit(o.recipe)               # 成功才真正扣减
        elif not ok and o.move(Status.FAILED):
            inv.release(o.recipe)              # 失败归还预留；退款由支付服务订阅 FAILED 事件
```

机器开始制作时要先调用 `order.move(Status.BREWING)`，之后才能 `on_brewed`。

**运行。** 一台咖啡机在 `SF`，牛奶 `200`，拿铁要牛奶 `150`：
- **第一单成功、第二单抛错：** 第一单 `place_order("SF", "latte")` 成功，第二单抛 `LookupError`：可用牛奶只剩 `50`，预留挡住了超卖。
- 第一单开始制作后失败，`on_brewed(id, False)` 后订单为 `FAILED`，预留归还，再下单成功。
- **重复 on_brewed 不再释放：** 重复调用 `on_brewed(id, False)` 不再释放第二次。
- 32 个线程同时抢最后一杯：只有 1 个成功。

**逐步扩展。**
1. 【追问再讲】菜单由库存推导，不单独维护，避免「菜单上有、实际做不了」；下单仍以 `reserve` 结果为准。

```python
def can_make(self, r: Recipe) -> bool:         # Inventory 新增
    return all(self._stock.get(i, 0) - self._reserved.get(i, 0) >= q
               for i, q in r.parts.items())


def menu(self, location: str) -> set[str]:     # OrderService 新增
    return {n for n, r in self.recipes.items()
            for m in self.machines.values()
            if m.location == location and m.online and m.inventory.can_make(r)}
```

2. 【追问再讲】取货：顾客凭取货码取杯，做好后保留 15 分钟，超时作废。`Order` 加字段 `ready_at: float | None = None`，`on_brewed` 的成功分支加 `o.ready_at = time.time()`（文件头加 `import time`），`OrderService` 加：

```python
PICKUP_TTL = 15 * 60                           # 类属性：做好后保留 15 分钟

def pickup(self, order_id: str, code: str) -> bool:
    o = self.orders[order_id]
    if o.status is Status.READY and time.time() - o.ready_at > self.PICKUP_TTL:
        o.move(Status.EXPIRED)                 # 超时作废；是否退款由政策决定
        return False
    return o.status is Status.READY and secrets.compare_digest(o.pickup_code, code) \
        and o.move(Status.PICKED_UP)
```

3. 【追问再讲】补货通知（观察者模式）：`on_brewed` 里 `commit` 之后调用 `monitor.check(machine)`。同一机器同一原料只保留一个未完成任务，补货后水位恢复才关闭。

```python
# Inventory 新增
def refill(self, items: dict[str, int]) -> None:
    with self._lock:
        for i, q in items.items():
            self._stock[i] = self._stock.get(i, 0) + q

def low_items(self, thresholds: dict[str, int]) -> list[str]:
    return [i for i, t in thresholds.items()
            if self._stock.get(i, 0) - self._reserved.get(i, 0) < t]


class RefillMonitor:
    def __init__(self, thresholds: dict[str, int], notify) -> None:
        self.thresholds, self.notify = thresholds, notify
        self.open: set[tuple[str, str]] = set()      # (machine_id, item) 未完成的任务

    def check(self, m: Machine) -> None:             # 每次 commit 之后调用
        for item in m.inventory.low_items(self.thresholds):
            if (m.machine_id, item) not in self.open:    # 去重
                self.open.add((m.machine_id, item))
                self.notify(m.machine_id, item)

    def on_refilled(self, m: Machine) -> None:       # 补货后关闭已恢复的任务
        low = set(m.inventory.low_items(self.thresholds))
        self.open = {k for k in self.open if k[0] != m.machine_id or k[1] in low}
```

4. 【加分】库存放在数据库、多进程下单时，`reserve` 变成一条带条件的更新，每种原料一条：

```sql
UPDATE inventory SET reserved = reserved + :q
WHERE machine_id = :m AND item = :i AND stock - reserved >= :q
```

受影响行数必须等于配方的原料种数，否则回滚整个事务，保证全有或全无。

**深入。**
1. 【必讲】并发下单与库存正确性。
   - 先查后扣：两个订单同时读到「还剩一杯的量」，都通过，实际超卖。
   - 预留与扣减分离（选用）：`reserve` 在锁内整体检查并占用；`commit` 和 `release` 只改已预留量，制作期间别的订单看到的可用量已经扣掉了这份。
2. 【必讲】订单状态机与幂等。
   - 合法迁移集中在迁移表，任何服务都不能直接改状态。
   - 支付回调、机器回调可能重复，`move` 对「已在目标状态」返回 `False`，调用方据此不再执行副作用。
3. 【追问再讲】制作失败和机器离线。
   - 制作失败：释放预留，订单 `FAILED`，退款服务订阅事件执行退款（事件至少一次，退款以订单号为幂等键）。
   - 机器离线：定时心跳，超时标记离线，其 `RESERVED` 订单批量转 `FAILED` 或重新路由到同地点其他机器。
   - 中心与机器断网：机器只执行已下发的订单，不接受离线新单。
4. 【追问再讲】菜单与机器选择。选择策略抽成接口（策略模式）：最近优先、库存最充裕优先、排队最短优先，运行时可换。
5. 【追问再讲】补货通知。阈值按原料配置（例如牛奶低于 3 杯用量）；也可以按「预计耗尽时间」提醒。路线优化属于运维调度，不在本设计范围。
6. 【追问再讲】取货与安全。取货码随机、一次性、限定机器；比较用常量时间函数，限制错误尝试次数。超时未取，饮品作废，出口格需要清空。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 为什么不下单时就扣减：制作失败还要加回库存，并且制作期间库存的真实状态与账面不一致；预留后提交把「承诺」和「消耗」分开，故障恢复简单。
- 支付放在预留前还是后：先预留后支付，支付超时则释放预留；预留设置 TTL，防止占着库存不付款。
- 怎么测试：`MachineController` 假实现可注入失败；并发测试里让几十个线程抢最后一杯的原料，断言只有一个成功。
- 一台机器能同时做多杯吗：多数硬件一次一杯，用单消费者队列；若能并行，按资源（磨豆机、蒸汽）建模，配方声明所需资源。
- 配方有可选项（加糖、换奶）：配方加定制参数，预留量由配方加参数计算得出；价格同理。
- 成千上万台机器：库存按机器分片，订单服务无状态；机器与中心之间用消息队列下发订单和上报状态。

**级别期望。**
- 中级：配方、库存、订单、机器几个类，基本下单流程和库存扣减。
- 高级：预留与提交分离、订单状态机、幂等、故障时的释放与退款、策略与观察者模式的使用。
- 资深（staff）：多进程下库存条件更新、机器离线重路由、预留 TTL、可测试性（硬件抽象）、从单机到全局的分片与调度设计。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-concurrency-intro|并发入门]]

**同类题。** [[solution-vending-machine]]（本库完整题解）、[[solution-coffee-machine]]、[[hi-low-level-design-problem-breakdowns-inventory-management|库存管理]]、[[solution-amazon-locker]]
