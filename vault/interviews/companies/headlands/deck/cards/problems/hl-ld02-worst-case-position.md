---
id: hl-ld02-worst-case-position
node: problems.ld02-trading-ood
type: qa
step: 8
---
## Q
风控的「最坏情况仓位」（`POSITION_LIMIT`）怎么算？为什么只看净仓不够？

## A
假设该标的**所有未完成买单都成交**，或**所有未完成卖单都成交**（含本单）：
```
net + 未完成买单剩余(+本单若为买) <= maxPosition
net - 未完成卖单剩余(+本单若为卖) >= -maxPosition
```
```java
long buyLeaves  = orders.openLeaves(sym, Side.BUY)  + (o.side() == Side.BUY  ? o.qty() : 0);
long sellLeaves = orders.openLeaves(sym, Side.SELL) + (o.side() == Side.SELL ? o.qty() : 0);
long net = positions.netQty(sym);
if (net + buyLeaves > limits.maxPosition() || net - sellLeaves < -limits.maxPosition())
    return reject(POSITION_LIMIT);
```
**只看净仓不够**：净仓 2500，还挂着 2000 股买单随时可能成交，真实风险 4500。maxPosition=5000，新买 500：`2500 + 2000 + 500 = 5000 ≤ 5000` 通过；买 501 → 5001 拒绝（`POSITION_LIMIT`）。卖方向对称处理：净仓 2500 挂买 2000，卖 4000：`2500 − 0 − 4000 = −1500 ≥ −5000` 通过，买方向暴露 4500 不变。

`orders.openLeaves` O(1)（增量维护），`positions.netQty` 遍历该标的 lot（通常很短，成为瓶颈可缓存 `netQty`）。

**PENDING 订单计入**，因为回报滞后风险不滞后；`PENDING_CANCEL`（撤单请求已发、确认未到）期间订单仍可能成交，所以最坏情况仓位仍要算上它的剩余数量——撤单是竞态不是瞬间，风控的未完成剩余量不能在请求时减，要等确认。

为什么 `check` 必须在 `orders.submit` **之前**：否则这张单把自己算进未完成数量，恰好顶格的订单被误拒（「不把自己算两遍」）。

风控扩展：新增一条规则要加一个 `RiskReason` 枚举值（它的位置就是优先级）和一个 `if`；想可组合可重构为 `List<RiskCheck>` 责任链，但热路径保持内联；和时间有关的规则（速率限制）要把时间作为事件传进来（如 `Tick`），不能在检查里读时钟，否则重放不确定。
