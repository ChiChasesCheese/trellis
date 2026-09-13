# q35 · 用户积分（按时间戳 FIFO 消费）

> `problems/q35_user_points_fifo/` · 4 个 part · phone screen（~35 分钟活编码）
> **主题：按时间排序的 FIFO 批次消费 + 负数修正的特殊语义。**

## 一句话题意

用户从多个 payer 那里积累积分。`spend(points)` 按**时间戳最早优先**消费，
返回每个 payer 被扣了多少。Part 3 引入"负数交易"作为该 payer 的修正。

## 核心考点

`S02` 解析 · `S03` 领域建模 · `S08` 确定性顺序 · **`S10` 事件流** · `S12` 时间戳 ·
**`S17` 台账余额** · `S18` 错误路径

## 解题思路

### Part 1

`add(payer, points, timestamp)`；`balances()` 返回每个 payer 的余额，按**首次 add 的顺序**。

### Part 2 — FIFO 消费

```python
entries.sort(key=lambda e: (e.ts, e.seq))       # 时间戳，平手按插入序
need = points
taken = {}                                       # payer → 扣掉多少
for e in entries:
    if need == 0: break
    if e.remaining <= 0: continue
    take = min(e.remaining, need)
    e.remaining -= take; need -= take
    taken[e.payer] = taken.get(e.payer, 0) + take
return [(p, -amt) for p, amt in taken.items()]   # 按首次被消费的顺序
```

**每条记录记住自己还剩多少**，所以下一次 `spend` 从上次停下的地方继续。
返回值**按 payer 聚合**，顺序按**首次被消费**的顺序。

### Part 3 — 负数交易

负数交易是**该 payer 自己的修正**。在 FIFO 消费**之前**，
每条负数交易（按时间戳顺序）**抵消该 payer 最早剩余的正积分**，
**不管那些正积分是在它之前还是之后赚到的** —— 减的是**这个 payer 的**积分，不是用户的。

一条会让该 payer 余额变负的 `ADD` → 拒绝（`ERROR`）。

### Part 4 — 多次消费与积分不足（重构）

`spend` 是**原子**的：`points` 超过总余额 → 抛 `ValueError`（stdout 打印 `ERROR`），**什么都不改**。
可以多次 spend，每次从剩余的继续消费。

## 坑

1. **add 可能不按时间戳顺序到达**（逐字样例就是这样）—— 必须排序，不能靠输入序。
2. **负数交易的日期可能早于它要抵消的正积分**；也可能该 payer 只有更晚的正积分。
3. `SPEND` 恰好等于总余额（OK）、多 1（`ERROR` 且**状态不变**）、`SPEND,0`。
4. **两条记录同一时间戳 → 按插入顺序。**
5. 余额为 0 的 payer **仍要列出**；payer 名字可能带空格（`MILLER COORS`）。
6. 同一个 payer 有多条被消费的记录时，输出要**按 payer 聚合**成一条。

## 变体

- Fetch Rewards 的 take-home：同样的规则包成 HTTP 服务（`/add`、`/spend`、`/balance`）。
  它的断言用 Java `HashMap` 顺序，也就是**不保证顺序**。
- 记录里 points 是 `String`（源码笔误）；当整数处理。

## Code Core 节点

**`algorithms.settlement`**（FIFO 批次消费） · `chrono.parsing` · `model.event-stream` ·
`rules.money` · `output.ordering` · `input.malformed`

## 自测清单

- [ ] add 乱序到达
- [ ] 负数交易在正积分之前 / 该 payer 只有更晚的正积分
- [ ] `SPEND == 总余额` / `+1` / `0`
- [ ] 同时间戳的两条记录
- [ ] 余额 0 的 payer 仍列出；带空格的 payer 名
- [ ] 同 payer 多条记录被消费 → 聚合成一条
- [ ] 会让余额变负的 ADD → `ERROR`
