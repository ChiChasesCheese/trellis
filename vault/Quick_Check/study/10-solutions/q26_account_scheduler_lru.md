# q26 · AccountScheduler（可用性 · 定时锁 · LRU 自动选择）

> `problems/q26_account_scheduler_lru/` · 4 个 part
> **主题：半开区间的锁 + LRU 的完整排序键 + 双堆惰性失效。**

## 一句话题意

一个账户池：可以 `ADD`、查 `AVAILABLE`、`ACQUIRE`（加一个有时长的锁）、
`ACQUIRE_ANY`（自动挑最久未用的可用账户）、`RELEASE`。

## 核心考点

`S03` 类 + 字典建模 · **`S05` 严格 vs 非严格的时间比较** · **`S08` 确定性 tie-break** ·
`S10` 事件流上的状态 · `S11` 幂等的 add/release · `S18` 校验 · `S20` 自测

## 直觉 / Intuition

把这题想成"图书馆借书"：一本书要么在架上（可用），要么被人借走且有明确的还书时间（锁），你不需要维护一个"忙/闲"布尔值，只需要记一个 `locked_until` 时间戳——可用性就退化成一次数字比较，这就是为什么锁天然长成半开区间 `[t0, t0+d)`：到期那一刻已经"还回来了"，不是"还差一秒"。
`ACQUIRE_ANY` 的本质是"每次都要找全场最闲的人"，一旦想清楚这是个排序问题，key 该长什么样就不用硬记：先分层（没借过 vs 借过），层内再按最后一次借的时间排，时间也相等就按 id 兜底——三行英文描述直接翻译成一个 tuple，不需要额外设计。
`RELEASE` 不动 `last_used` 也是同一个心智模型的自然推论：LRU 排的是"你上次被真正使用是什么时候"，不是"你现在锁没锁"，提前还书不等于重新借了一次。
一旦把"可用性"和"LRU 排序"分别看成两个独立的可比较状态（一个时间戳 + 一个排序 key），Part 4 的双堆优化就是水到渠成的事：任何"需要频繁取最小值/最靠前元素"的场景，堆都是默认答案，惰性失效只是因为堆里的元素会被别的操作（RELEASE、下一次 ACQUIRE）弄过时，重新平衡代价太高，不如"删的时候顺手判断还作不作数"。

## 解题思路

### Part 1 — 可用性（半开区间）

**在 `t0` 取的、时长为 `d` 的锁，覆盖 `[t0, t0 + d)` —— 右端开。**

```
is_available(id, t0 + d)     → True     ★
is_available(id, t0 + d - 1) → False
```

`acquire` 成功的条件：账户在 `t` 可用 **且** `duration > 0`。
成功时记 `last_used = t`。重复 `ADD` 同一个 id → no-op（`EXISTS`）。

### Part 2 — `ACQUIRE_ANY` 的 LRU

**排序键（完整写出来）**：

```
(从未被 acquire 过 ? 0 : 1,  last_used,  id)
```

即：**从未用过的优先**（其中取 id 最小的），否则取 `last_used` 最小的，平手按 id 的**普通字符串序**。
锁定方式与 `acquire` 相同，打印它的 id；没有可用账户或 `duration <= 0` → `NONE`。

**只有成功的 acquire 更新 `last_used`** —— 失败的 `ACQUIRE`、`AVAILABLE` 查询、`RELEASE` 都不更新。

### Part 3 — `RELEASE`

立刻清除锁（此后到再次 acquire 之前，任何 `t` 都可用）。
**`last_used` 不变** —— 提前释放的账户仍保持它的 LRU 位置。
释放一个没上锁的账户是无害的 `OK`；未知 id 打印 `UNKNOWN`。

### Part 4 — 性能

10^5 条命令 × 10^4+ 个账户，**`ACQUIRE_ANY` 不能每次扫全部**：

- 一个按 `(never_used, last_used, id)` 排的**可用账户堆**；
- 一个按 `locked_until` 排的**锁到期堆**，处理每条命令前先把到期的弹回可用堆；
- 两个堆都用**惰性失效**（弹出时校验条目是否仍然有效）。

小池子用 O(n) 扫描也行，但**要在注释里说明**这个取舍 —— 面试官问的就是这个。

## 坑

1. **锁的右端是开的**：`t0 + d` 可用，`t0 + d − 1` 不可用；**恰好在到期时刻 acquire 成功**。
2. 未知 id 的 `AVAILABLE`/`ACQUIRE` → `false`；`RELEASE` 未知 → `UNKNOWN`；`ADD` 两次 → `EXISTS`。
3. **LRU：从未用过的排在用过的前面**；`last_used` 相同按 id 序（`a10` < `a2`）；
   **失败的 acquire 不动 `last_used`**。
4. 全部上锁时 `ACQUIRE_ANY` → `NONE`；等一个到期后就选它。
5. **`RELEASE` 保留 `last_used`**（释放过的账户仍算"最近用过"）。
6. `duration <= 0` 拒绝；`t` 为负或倒退仍然按比较来回答。
7. 10^5 × 10^4 的每次 O(n) 扫描 ≈ 10^9 次操作。

## 变体

- `acquire(account_id, duration)` 用隐式时钟（`time.time()` 或构造时注入的 `now`）
  而不是显式的 `t` 参数 —— 同样的逻辑，把时钟注入进来。
- 只存 `locked_until` 并只提供 `is_available(account, ts)`（onsite 的三步递进：
  `is_available → acquire(lock) → LRU 选择`）。
- 面试官要求"生产级代码"：**先列边界再写码**、小方法、被问到规模时能讲清堆 + 惰性失效的升级路径。

## Code Core 节点

**`toolbox.cache`**（LRU） · **`toolbox.heap`**（双堆 + 惰性失效） · **`chrono.intervals`**（半开锁） ·
`model.entity-state` · `output.ordering` · `performance.budget`

## 自测清单

- [ ] `t0+d` / `t0+d−1` 两个时刻
- [ ] 未知 id 的三种命令；`ADD` 两次
- [ ] 从未用过 vs 用过；`last_used` 平手按 id（`a10` / `a2`）
- [ ] 失败的 acquire 不动 `last_used`
- [ ] 全锁 → `NONE`；一个到期后选它
- [ ] `RELEASE` 后 LRU 位置不变
- [ ] `duration <= 0`
- [ ] 10^5 命令 × 10^4 账户的耗时
