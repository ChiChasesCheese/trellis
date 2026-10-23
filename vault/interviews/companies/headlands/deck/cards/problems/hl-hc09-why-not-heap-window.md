---
id: hl-hc09-why-not-heap-window
node: problems.hc09-top-trades-by-notional
type: qa
step: 8
---
## Q
滑动窗口 top-k ticker 为什么只用 `PriorityQueue` 不行？有哪三种补救，为什么选 `TreeSet`？

## A
窗口里 A 总额 500、B 300、C 100，k=2，堆 {A, B}（堆顶 B=300 守门员）。
- 事件 1：C 来一笔变 400，比守门员强 → 踢掉 B，C 进堆。**但 B 还在窗口里**，只是被挤出堆，堆不再记得它。
- 事件 2：A 的老成交过期，A 从 500 降到 50。B（300）应回到 top-2，可堆里没有 B 了，**必须重建**。

根本原因：ticker 总额既会涨（新成交）也会跌（旧成交过期），要「找到它、改它的键」。堆高效支持 `add` 和弹出堆顶，但不支持**找到任意元素**（线性扫描）、**改键**（`PriorityQueue` 没有 decrease-key）、**删除任意元素**（`remove(Object)` O(m)）。

三种补救：
| 方案 | 做法 | 代价 |
|---|---|---|
| A 查询时重建堆 | 每次 `top()` 过一遍所有活跃 ticker | 每次查询 O(m log k) |
| B 惰性删除 | 总额变化时再插一条新的，弹出时发现与当前总额不符就丢弃 | 堆里累积垃圾可到 O(事件数)；`top()` 要弹 k 个有效条目再放回 |
| C `TreeSet` | 总额变化：O(log m) 删旧键、O(log m) 插新键；`top()` 直接按序读前 k 个 | 红黑树常数比堆大，但所有操作有上界 |

选 C：查询要看前 k 个而非仅堆顶，且要任意元素更新。口述：「ticker 总额既涨又跌，要改任意元素的键，所以用 `TreeSet`：删旧键、插新键各 O(log m)，top-k 顺序读前 k 个。」

`TreeSet` 是红黑树，`add / remove / first / 遍历` 每个操作 O(log m)。**`TreeSet` 用比较器判断「是不是同一个元素」**：`compare(a,b) == 0` 即同一个，`add` 会被拒绝。比较器 `BEST_TICKER_FIRST`（总额降序 + ticker 升序）里 ticker 唯一没问题；只看总额的话，总额相同的两个 ticker 会有一个被悄悄吞掉。
