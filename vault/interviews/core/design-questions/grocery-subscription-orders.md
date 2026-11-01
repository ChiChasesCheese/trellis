---
slug: grocery-subscription-orders
kind: low-level-design
---
## Q
**生鲜订阅转订单服务**｜低层设计

设计一个生鲜订阅服务的代码结构：用户可以创建周期性订阅（例如每周送一次牛奶和鸡蛋）；系统到期时把订阅自动转成订单，转换时要同时看用户钱包余额和商品库存是否足够。重点是创建订阅和"订阅转订单"这一步的类划分、状态流转、失败处理和并发正确性，需要能写出可运行的核心代码。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 订阅转订单是一个"跨两个资源的小事务"（库存加钱包）：难点不在类有多少，而在步骤的顺序、失败时的补偿、以及任务重跑时不会重复下单。

**需求。**
功能：
1. 创建订阅：用户、商品及数量、周期（每 N 天）、首次执行日期。
2. 暂停、恢复、取消订阅。
3. 每天（或按调度）找出到期的订阅，转成订单：库存足够并且钱包余额足够才成功。
4. 失败要有明确结果（库存不足、余额不足），不静默丢失，并为后续重试或通知留出位置。
5. 订单与订阅的每一期一一对应，重复执行不产生重复订单。

非功能：并发安全（同一库存被多个订阅同时抢）；金额用整数（分）；扣款与库存的一致性；可测试（日期注入）。

**核心实体与接口。**
- `Subscription`：订阅，含 `items`（商品到数量）、`every_days`、`next_run`、状态。
- `Order`：订单，含 `(sub_id, cycle)` 这对幂等键、明细、总价、状态（成功、因库存跳过、因余额跳过）。
- `Inventory`：`reserve(lines)` 整单预留（全有或全无）、`release(lines)` 归还。
- `Wallet`：`debit(user_id, amount)` 扣款，余额不足返回失败。
- `SubscriptionService`：`create`、`run_due(today)`、内部的 `_convert(sub, cycle)`。
- 模式：事务脚本加补偿（Saga 的最小形式）；仓储（Repository）隔离存储；策略（Strategy）可选——库存不足时"整单跳过"还是"部分发货"做成可替换的履约策略；日期作为参数传入，便于测试。

```python
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


class SubStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class OrderStatus(Enum):
    PLACED = "placed"
    SKIPPED_NO_STOCK = "skipped_no_stock"
    SKIPPED_NO_FUNDS = "skipped_no_funds"


@dataclass
class Subscription:
    id: str
    user_id: str
    items: dict[str, int]            # product_id -> 数量
    every_days: int
    next_run: date
    status: SubStatus = SubStatus.ACTIVE


@dataclass
class Order:
    id: str
    sub_id: str
    cycle: date                      # 对应哪一期；(sub_id, cycle) 唯一，保证幂等
    lines: dict[str, int]
    total: int                       # 以分为单位的整数，避免浮点
    status: OrderStatus


class Inventory:
    """库存：先预留（可撤销），确认扣款后才算最终成交。"""

    def __init__(self, stock: dict[str, int]) -> None:
        self._stock, self._lock = dict(stock), threading.Lock()

    def reserve(self, lines: dict[str, int]) -> bool:
        with self._lock:                         # 一把锁覆盖整单：要么全部预留，要么一件不留
            if any(self._stock.get(p, 0) < q for p, q in lines.items()):
                return False
            for p, q in lines.items():
                self._stock[p] -= q
            return True

    def release(self, lines: dict[str, int]) -> None:
        with self._lock:
            for p, q in lines.items():
                self._stock[p] += q


class Wallet:
    def __init__(self, balances: dict[str, int]) -> None:
        self._bal, self._lock = dict(balances), threading.Lock()

    def debit(self, user_id: str, amount: int) -> bool:
        with self._lock:
            if self._bal.get(user_id, 0) < amount:
                return False
            self._bal[user_id] -= amount
            return True


class SubscriptionService:
    def __init__(self, prices: dict[str, int], inventory: Inventory, wallet: Wallet) -> None:
        self.prices, self.inventory, self.wallet = prices, inventory, wallet
        self.subs: dict[str, Subscription] = {}
        self.orders: dict[tuple[str, date], Order] = {}   # 以 (sub_id, cycle) 为键

    def create(self, sub: Subscription) -> None:
        self.subs[sub.id] = sub

    def run_due(self, today: date) -> list[Order]:
        out = []
        for sub in list(self.subs.values()):
            while sub.status is SubStatus.ACTIVE and sub.next_run <= today:
                out.append(self._convert(sub, sub.next_run))
                sub.next_run += timedelta(days=sub.every_days)   # 无论成败都推进，失败交给通知/重试策略
        return out

    def _convert(self, sub: Subscription, cycle: date) -> Order:
        key = (sub.id, cycle)
        if key in self.orders:                                   # 重跑同一天的任务不会重复下单
            return self.orders[key]
        total = sum(self.prices[p] * q for p, q in sub.items.items())
        if not self.inventory.reserve(sub.items):                # 1) 先预留库存（可撤销）
            order = Order(f"{sub.id}:{cycle}", sub.id, cycle, {}, 0, OrderStatus.SKIPPED_NO_STOCK)
        elif not self.wallet.debit(sub.user_id, total):          # 2) 再扣钱（不可撤销，放在最后）
            self.inventory.release(sub.items)                    # 补偿：扣款失败，归还库存
            order = Order(f"{sub.id}:{cycle}", sub.id, cycle, {}, 0, OrderStatus.SKIPPED_NO_FUNDS)
        else:
            order = Order(f"{sub.id}:{cycle}", sub.id, cycle, dict(sub.items), total, OrderStatus.PLACED)
        self.orders[key] = order
        return order
```

**整体设计。**
`run_due(today)` 遍历所有订阅：对状态为活跃且 `next_run <= today` 的订阅，逐期调用 `_convert`，并把 `next_run` 推进一个周期。`while` 循环会补上因停机而错过的多期，每期用各自的 `cycle` 日期生成订单。

`_convert` 的步骤是整个设计的核心：
1. 先查幂等键 `(sub_id, cycle)`，已经有订单就直接返回，任务重跑不会重复下单。
2. 计算总价（整数分）。
3. 预留库存（可撤销的一步）。库存不足则订单结果为"因库存跳过"，不再碰钱包。
4. 扣钱包（不可撤销的一步，放在最后）。余额不足则归还刚才预留的库存（补偿），订单结果为"因余额跳过"。
5. 两步都成功，生成成功订单。

顺序的原因：把可撤销的动作放前面、不可撤销的放最后，失败时需要撤销的东西最少。反过来先扣钱再预留库存，库存失败时就需要退款，退款本身又可能失败，补偿链更长更危险。

**深入。**

1. 并发与锁：
- 问题：两个订阅同时对同一件仅剩一件的商品预留，如果先检查后扣减不是原子的，会超卖。
- 做法：`Inventory.reserve` 在一把锁内完成"检查全部明细、再扣减全部明细"，所以整单是全有或全无。这里用一把全局锁，简单正确；规模变大后改为按商品加锁，此时必须按商品 ID 的固定顺序（排序后）逐个加锁，避免两个订单以相反顺序加锁而死锁。
- 钱包同理，每个用户一把锁即可；同一用户的多个订阅同时转换时，余额检查与扣减在同一个临界区。
- 持久化版本中，库存与余额的更新用数据库的条件更新（`UPDATE ... SET stock = stock - ? WHERE stock >= ?`，看影响的行数）代替内存锁。

2. 幂等与崩溃恢复：
- 问题：任务在"预留库存"之后、"保存订单"之前崩溃，重跑时会不会重复扣？
- 做法：订单以 `(sub_id, cycle)` 为唯一键；真实系统里，预留、扣款、写订单应当在同一个数据库事务内完成（库存和钱包在同一库时），或者每一步都带上幂等键（以订单 ID 为准），使重试不会再次扣减。对于跨服务的情况，用状态机——订单先以"处理中"落库，再执行步骤，崩溃后由恢复任务扫描"处理中"的订单继续或回滚。
- 单元测试里用内存版本，约束这个属性：对同一天连续调用两次 `run_due`，第二次不产生新订单。

3. 失败后怎么办：
- 余额不足：常见策略有三种——跳过本期并通知用户充值；在宽限期内每天重试几次；连续几期失败后自动暂停订阅。这是产品策略，用一个 `FailurePolicy` 接口承接，不要把重试逻辑写死在转换代码里。
- 库存不足：整单跳过，或按策略对可满足的部分发货（需要部分扣款，复杂度高很多，先实现整单，再说明如何扩展）。
- 无论成败，都推进 `next_run`，否则同一期会被无限重复尝试；重试由失败策略以单独的记录驱动。

4. 价格与金额：
- 金额用整数分，避免浮点误差。订阅创建时不锁定价格，转换时按当时价格计算（用户通常期望按当前价）；如果产品承诺价格保护，则订阅里记录价格上限，超过则暂停并通知。

**取舍与追问。**
- 订单生成时机：提前几天生成"预告订单"让用户有机会修改，扣款在发货前一刻；这要求库存只在扣款时预留，或者两次预留。
- 调度：`run_due` 由定时任务（每天一次或每小时一次）调用；规模大时按订阅 ID 分片并行，每个分片独立处理，幂等键保证多实例重叠时不重复。
- 时区：`next_run` 用用户所在时区的日期，不要用服务器时间，否则午夜附近会错一天。
- 订阅修改在转换期间发生：转换读取订阅的一个快照（版本号），修改只影响下一期；如果要求立即生效，则转换前重新读取并检查版本。
- 库存与钱包分属两个服务时：本地事务不够，需要 Saga；预留库存（可补偿）→ 扣款（枢轴）→ 确认库存，每一步幂等，失败发补偿命令。

**级别期望。**
- 中级：订阅、订单、库存、钱包四个类，到期转订单的主流程，库存与余额都要检查。
- 高级：步骤顺序与补偿（先预留再扣款，失败归还）、幂等键避免重复下单、锁与原子预留、失败结果可区分。
- 资深/Staff：崩溃恢复与状态机、多服务时的 Saga、按商品加锁的顺序避免死锁、失败策略的可扩展性、分片并行调度、时区与价格保护等产品细节。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-concurrency-intro|并发入门]]、[[hi-low-level-design-concurrency-scarcity|稀缺资源]]

**同类题。** [[hi-low-level-design-problem-breakdowns-inventory-management|库存管理]]、[[solution-amz-pizza-order|披萨下单]]、[[solution-online-auction|在线拍卖]]、[[solution-task-scheduler|任务调度器]]
