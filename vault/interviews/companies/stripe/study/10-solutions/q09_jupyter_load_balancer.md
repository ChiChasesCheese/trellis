# q09 · Jupyter 负载均衡（连接路由 + 对象粘性 + 容量 + 停机重路由）

> `problems/q09_jupyter_load_balancer/` · 5 个 part · **刷题顺序第 2 题**（13 个来源，需要堆才能过 perf）
> **主题：堆 + 惰性删除，以及"停机后按原到达序重路由"。**

## 一句话题意

`num_targets` 台服务器后面接一个负载均衡器。每个 CONNECT 去**当前连接数最少**的服务器（平手取小下标）；
带 `objectId` 的连接必须**粘在同一台**；每台有容量上限；`SHUTDOWN` 要把该机的连接
**按原到达顺序**逐个重新路由。

## 输入 / 输出

```
num_targets max_connections_per_target
CONNECT <connectionId> <userId> [<objectId>]
DISCONNECT <connectionId>
SHUTDOWN <targetIndex>            1-based
```
约束：`num_targets ≤ 10^5`，请求 ≤ 2·10^5，容量 ≤ 10^9。

输出：每次**成功**放置一行 `connectionId,userId,targetIndex`（**1-based**，无空格）。
被拒绝/被丢弃的连接、DISCONNECT、SHUTDOWN 都不输出。**没有 `PART` 行**，规则是累积的。

## 核心考点

`S01` 读全 spec · `S02` 解析 · `S03` 按 id 建记录 · **`S10` 有反向事件的有序流** ·
`S11` 重复 CONNECT 幂等 · `S18` 校验/忽略 · `S19` 增量 · **`S21` heapq** · `A15` 堆选最闲

## 解题思路

### 状态

```python
load   = [0] * n                     # 每台的活跃连接数
conn   = {}                          # connectionId → (target, userId, objectId, arrival_seq)
pin    = {}                          # objectId → target（粘性）
on     = [set() for _ in range(n)]   # 每台持有的 connectionId（SHUTDOWN 要用）
heap   = [(0, i) for i in range(n)]  # (load, index) 最小堆
```

### 选最闲的一台（堆 + 惰性删除）

```python
def pick(exclude=None):
    buf = []
    out = None
    while heap:
        l, i = heapq.heappop(heap)
        if l != load[i] or i == exclude:      # 过期条目 / 被排除的机器
            buf.append((l, i)) if i == exclude else None
            continue
        if load[i] >= cap:                    # 满了，这条也丢掉
            continue
        out = i; break
    for item in buf: heapq.heappush(heap, item)   # 被排除的放回去
    return out
```

**为什么必须用堆**：10^5 台 × 2·10^5 请求，每次线性扫一遍是 2·10^10 —— 必挂。
**为什么必须惰性删除**：负载变化后堆里留着旧值，弹出时用 `l != load[i]` 判掉。

放置时 `load[i] += 1; heapq.heappush(heap, (load[i], i))`。

### Part 1–2

- 重复的活跃 `connectionId` → **忽略**（不输出、不改状态）。
- `DISCONNECT` 未知或已断开的 id → **忽略**。id 可以被后来的 CONNECT 复用。

### Part 3 — 对象粘性

- 对象第一次出现时按 Part 1 规则选机，并**钉住**。
- **钉子在断开后仍然保留**（kernel 留在它启动的那台），**只有该机 SHUTDOWN 才清除**。

### Part 4 — 容量

- `load == cap` 就是满。
- **粘性目标满了就拒绝，即使别的机器有空位**（这是本题的招牌坑）。

### Part 5 — 停机

```python
victims = sorted(on[t], key=lambda cid: conn[cid].arrival_seq)   # ★ 原到达顺序
for obj in objects_pinned_to(t): del pin[obj]                    # ★ 先清钉子
mark t unavailable
for cid in victims:
    place(cid, exclude=t)     # 同样的规则：最闲 + 粘性 + 容量；放不下就丢弃，不输出
mark t available with load 0                                     # ★ 重新入池，负载归零
```

三个 ★ 都是隐藏测试点：**原到达序**、**先清钉子**（于是同一对象的第一条重新选机、其余跟随）、
**停机机在自己的重路由期间不可选，之后以 load 0 回到池子**。

`SHUTDOWN` 下标越界 → 忽略。

## 坑

1. **1-based 下标**（日志里和 `SHUTDOWN t` 里都是），平手取**最小**下标。
2. DISCONNECT 未知 id / 已断开 → 静默忽略。
3. 活跃期间重复 CONNECT id → 忽略；断开后可复用。
4. **粘性目标满 → 拒绝，哪怕别的机器有空**。
5. `load == cap` 即满：第 `cap` 个成功，第 `cap+1` 个失败。
6. **重路由按原到达序**，且重路由后同对象的连接**重新粘在一起**。
7. 停机机在自己的重路由期间不可选；结束后 **load = 0** 重新入池。
8. 空机或越界的 SHUTDOWN 是 no-op。
9. **10^5 × 2·10^5 必须用堆 + 惰性删除**，不能每次扫全部。

## 变体

- **prachub 变体 B**：`CONNECT connectionId objectId`（每条都粘），日志是空格分隔的
  `connectionId serverIndex`。仓库里是 `variant_b=True`。
- **programhelp**：停机的机器**永久**移出池子；装不下的连接被丢弃。`shutdown_permanent=True`。
- 1point3acres 把 part 描述成 "round-robin → 去重 → 断开 → 容量 → SHUTDOWN"——
  没人断开时，"最闲+最小下标"就是 round-robin。

## Code Core 节点

**`toolbox.heap`**（惰性删除） · `model.entity-state` · **`model.reversal`**（SHUTDOWN 重路由） ·
`model.idempotency` · `model.index`（三个索引：conn / pin / on） · **`performance.budget`** ·
`performance.amortized` · `algorithms.greedy`

## 自测清单

- [ ] 题面的 worked example
- [ ] 平手取最小下标（前几条连接的分配序列）
- [ ] 重复 CONNECT / 未知 DISCONNECT / 复用 id
- [ ] 粘性：同对象第二条去同一台；该台满了 → 拒绝
- [ ] 容量恰好：第 cap 个成功、第 cap+1 个失败
- [ ] SHUTDOWN：重路由顺序、钉子重建、停机机 load 0 回池
- [ ] SHUTDOWN 空机 / 越界
- [ ] 10^5 台 + 2·10^5 请求的耗时（必须用堆）
