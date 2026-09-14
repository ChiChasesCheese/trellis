# q36 · 时间键值映射（MultiTimeMap：版本化 get · 历史 · TTL）

> `problems/q36_time_kv_map/` · 4 个 part（LC 981 / Daily Coding Problem #97）
> **主题：`bisect` 找"≤ t 的最大写入" + TTL 的半开区间。**

## 一句话题意

`set(key, value, time)` / `get(key, time)`：返回**写入时间 ≤ `time` 的最大那一次**的值。
写入**可能乱序到达**。Part 3 加 TTL。

## 核心考点

`S03` 领域建模 · **`S12` 时间处理** · **`S13` 闭/开区间边界** · `S18` 错误路径 · `S19` 增量

## 解题思路

```python
from bisect import bisect_right, insort
store = defaultdict(list)          # key → [(time, value, ttl), ...] 按 time 升序

def set_(key, value, t, ttl=None):
    lst = store[key]
    i = bisect_left([x[0] for x in lst], t)     # 实际实现用平行的 times 列表
    if i < len(lst) and lst[i][0] == t:
        lst[i] = (t, value, ttl)                 # ★ 同 key 同 time → 覆盖
    else:
        lst.insert(i, (t, value, ttl))           # 乱序写入 → insort

def get(key, t):
    lst = store.get(key, [])
    i = bisect_right([x[0] for x in lst], t) - 1   # ≤ t 的最大写入
    if i < 0: return None
    tm, v, ttl = lst[i]
    if ttl is not None and t >= tm + ttl: return None   # ★ 过期不回退到更老的版本
    return v
```

**LC 981 保证时间戳递增**（可以 append + `bisect_right`）；
**这道题不保证**，所以要 `insort`。

### Part 2 — `get_all(key, time)`

写入时间 ≤ `time` 的所有版本，按写入时间升序（同 time 会覆盖，所以每个 time 一个值）。
没有 → **空列表**（输出是空行，**不是 `null`**）。

### Part 3 — TTL

版本在 `t ∈ [time, time + ttl)` 内有效 —— **`time + ttl` 本身已过期**。
`get(key, t)` 仍取"≤ t 的最大写入时间"的版本；**若那个版本已过期就返回 `None`，
绝不回退到更老的版本**（因为新的写入已经取代了它）。`ttl=None` 永不过期。

### Part 4 — `first_missing_positive(nums)`

最小的不在列表里的正整数，线性时间（`set` 或原地打标记）。`[]` → 1。

## 坑

1. **第一次写入之前的 `get` → `null`**；**恰好在写入时刻的 `get` → 那个值**（`≤` 不是 `<`）。
2. **同 key 同 time 的写入覆盖**；写入**可能乱序**。
3. **TTL 边界**：`time + ttl - 1` 存活，`time + ttl` 过期；**`ttl = 0` 永远读不到**。
4. **过期的新版本会遮住旧版本**（不回退）。
5. 未知 key；`GETALL` 无结果 → **空行**，不是 `null`。
6. Part 4：`[]` → 1，`[1]` → 2，`[1,1,2,2]` → 3，全负 → 1，`[2]` → 1。

## 变体

- 源笔记把 DCP #97 的三个样例块粘成一串；作为**同一个 map** 读会自相矛盾
  （`set(1,1,0)` 之后 `get(1,0) → null`），所以主线按**三个独立的 map** 理解。
- LC 981 保证每个 key 的时间戳严格递增（append + `bisect_right`）。
- "timestamp cache" 变体加淘汰/过期 —— 就是 Part 3。

## Code Core 节点

**`toolbox.cache`**（版本化 map） · **`toolbox.sorted`**（`bisect`） · `chrono.intervals`（TTL 半开） ·
`algorithms.binary-search` · `model.entity-state`

## 自测清单

- [ ] 首次写入之前 / 恰好在写入时刻
- [ ] 同 time 覆盖 / 乱序写入
- [ ] `time + ttl - 1` / `time + ttl` / `ttl = 0`
- [ ] 过期的新版本不回退
- [ ] `GETALL` 空结果的输出形状
- [ ] Part 4 的五个用例
