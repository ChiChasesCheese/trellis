---
id: hl-hc05-freelist-unlink
node: problems.hc05-market-order-book
type: qa
step: 14
---
## Q
`TickBook` 里槽位池的 free list、侵入式链表的 `unlink` 怎么写？

## A
**free list**：初始 `next[i] = i + 1` 串成空闲链，`freeHead = 0`。分配 `slot = freeHead; freeHead = next[slot]`；释放 `next[slot] = freeHead; freeHead = slot`。都 O(1) 且不分配内存。

**`rest`（挂簿）**：槽位接到 `tail[s][p]` 之后；价位原本为空（`t < 0`）时还要设队头、位图置位、必要时更新 `bestBid / bestAsk`。

**`unlink`（摘除，撮合吃光和撤单共用）**：
```java
if (pr >= 0) next[pr] = nx; else head[s][p] = nx;   // 没有前驱说明我是队头
if (nx >= 0) prev[nx] = pr; else tail[s][p] = pr;   // 没有后继说明我是队尾
```
价位变空后清位图；若它正是最优价，用位图找下一档：`bestBid = atOrBelow(bits[0], p - 1)`（买盘：找 ≤ p−1 的最高非空价位），`bestAsk = atOrAbove(bits[1], p + 1)`（卖盘：找 ≥ p+1 的最低非空价位）。

**位图**：`long[]` 的第 p 位为 1 表示价位 p 非空，一次查 64 个。`atOrAbove`：取 `from` 所在的 64 位字，用 `-1L << (from & 63)` 屏蔽 `from` 之前的位；字非零就 `Long.numberOfTrailingZeros` 定位最低的 1，否则看下一个字（C++ 用 `std::countr_zero`）。

**哨兵值**：`bestBid = 0` 表示没买盘（合法价格 ≥ 1），`bestAsk = maxTicks` 表示没卖盘。撮合条件 `bestAsk <= p`（买）/ `bestBid >= p`（卖）在对面为空时自然为假，**循环里不用判空**。

必须跨过上万个空价位找到下一档——最优价被吃光 / 撤光后没更新是常见 bug。
