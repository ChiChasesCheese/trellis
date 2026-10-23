---
id: hl-hc11-online-structures
node: problems.hc11-order-interval-overlap
type: qa
step: 6
---
## Q
在线版 `OnlineOverlap` 每个车道维护哪些字段？`place`、`cancel`、`advanceTo` 各怎么做，`liveAt` 怎么答？

## A
事件按时间到达，排序已由时间做完，要**边到边扫**。`live` 在 now 的值需要知道哪些订单已在 now 之前结束，用按结束时间排序的 `TreeMap`，这是差分数组的**未来部分** `d[end] -= 1`，过去部分已累加进 `live`。

每个车道（BUY / SELL / ALL）字段：
| 字段 | 含义 |
|---|---|
| `expiries` | `TreeMap<结束时间, 订单数>`（未来的 −1） |
| `live` | 当前（now）活着的订单数 |
| `history` | `TreeMap<时间, 活跃数>`，只记变化点（阶梯函数） |
| `committedMax / committedTime` | 已经「过去」的时间戳里的最大值及其最早时刻 |

操作：
- `place(id, side, start, end)`：先 `advanceTo(start)`，再 `live++`、`expiries[end] += 1`、`history[now] = live`；`start` 必须 ≥ 上一个事件的时间（相等允许），`id` 重复 → `IllegalArgumentException`；
- `cancel(id, time)`：先校验（未知 id、时间倒退抛 IAE，**校验在改状态之前**），再 `advanceTo(time)`；若 `o.end() > time`（还活着）：`live--`、从 `expiries` 里撤掉原结束时间、`history[now] = live`，用新 record 替换订单（`end = time`），返回 `true`；已自然结束 / 已撤过返回 `false`；
- `advanceTo(t)`：先封账当前时间戳，再把 `expiries` 里键 ≤ t 的依次 `pollFirstEntry`：`live -= count`，`history[键] = live`；
- `liveAt(t)`：`history.floorEntry(t)`（不晚于 t 的最近变化点），其值就是 t 时刻活跃数（阶梯函数），无则 0，O(log n)；`0 ≤ t ≤ now`，`t > now` 抛 IAE。

TreeMap API：`put/get/remove` O(log n)，`firstEntry()`、`pollFirstEntry()`（删除并返回最小）、`floorEntry(x)`（≤ x 的最大键）；`expiries.compute(end, (k, c) -> c == 1 ? null : c - 1)`：计数减到 0 返回 `null` 删键，否则 `firstEntry` 会反复折叠 0。C++：`begin()` / `upper_bound` + `prev`，`operator[]` 会插入，所以用 `find`；`prev(upper_bound(t))` 不检查 `begin()` 是 UB。

每个事件 O(log n)；60 万 place + 20 万 cancel 约 305–320 ms；80 万事件 < 2 s。
