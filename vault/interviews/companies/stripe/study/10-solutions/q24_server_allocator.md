# q24 · 服务器编号分配（最小空闲号 + 堆）

> `problems/q24_server_allocator/` · 4 个 part
> **主题：first missing positive → 堆维护空闲号池 → O(log n) 每操作。**

## 一句话题意

主机名 = 类型 + 序号（`apibox1`）。分配时取该类型**最小的空闲号**；
释放后号回到池子。10^6 条命令，每次操作要 O(log n)。

## 输入 / 输出

```
PART 1
5 3 1                  每行一个查询（空格或逗号分隔；空行或 [] 表示空列表）

PART 2|3|4
ALLOCATE apibox
DEALLOCATE apibox1
```
输出：P1 每行一个整数；P2–4 每个 `ALLOCATE` 打印主机名，`DEALLOCATE` 不打印
（未知主机名**静默忽略**）。

## 核心考点

`S03` 每类型状态 · **`S08` 确定性的"最小空闲"** · **`S11` 幂等（重复释放）** ·
`S18` 畸形名字的校验 · `S19` 增量 · **`S21` heapq** · `A15` 堆选择

## 解题思路

### Part 1 — first missing positive

```python
def next_server_number(allocated) -> int:
    s = {x for x in allocated if isinstance(x, int) and x > 0}   # 忽略 0、负数、非整数
    n = 1
    while n in s: n += 1
    return n
```

用 `set` 做到 O(n)。重复、0、负数、浮点（2018 年的 gist 会传 `1.5, 2.5`）**都忽略** ——
它们既不可能是答案，也挡不住答案。`[]` → 1。

### Part 2–3 — Tracker（重点在数据结构）

```python
class Tracker:
    def __init__(self):
        self.nxt  = defaultdict(lambda: 1)   # 该类型发过的最大号 + 1（high-water mark）
        self.free = defaultdict(list)        # 该类型的空闲号最小堆
        self.live = set()                    # 当前在用的主机名 → 挡住重复释放
    def allocate(self, t):
        if not t or t[-1].isdigit(): raise ValueError
        if self.free[t]: n = heapq.heappop(self.free[t])
        else:            n = self.nxt[t]; self.nxt[t] += 1
        name = f"{t}{n}"; self.live.add(name); return name
    def deallocate(self, name):
        t, n = split_trailing_digits(name)
        if name not in self.live: return False      # ★ 未知 / 已释放 / 畸形 → 忽略
        self.live.discard(name); heapq.heappush(self.free[t], n); return True
```

三个关键点：
1. **`nxt` 是 high-water mark，不是 `len(live) + 1`** —— 空闲池空了之后从最高号继续。
2. **`live` 集合挡住重复释放** —— 否则同一个号会被压进堆两次，导致两个 `apibox1` 同时存在。
3. **主机名按结尾的数字串切分**：`apibox12` → `("apibox", 12)`。
   因此类型名不能以数字结尾（`allocate("box2")` → `ValueError`），也不能为空。
   带前导零的号（`apibox01`）视为**未知**。

## 坑

1. `[]` → 1；不含 1 的列表 → 1；连续 `1..n` → `n+1`。
2. 列表里的重复 / 0 / 负数 / 浮点。
3. **释放未知、已释放、畸形的名字（`apibox`、`apibox0`、`sitebox9`）是 no-op。**
4. **重复释放不能让同一个号可用两次**（否则两个 `apibox1` 同时在用）。
5. 释放多个号后，**分配顺序是升序**（先释放 3 再释放 1 → 下次给 1，再下次给 3）。
6. **空闲池空了之后从 high-water mark 继续**，不是 `len(live)+1`。
7. **类型之间独立**：释放 `apibox2` 不影响 `sitebox`。
8. **多位数字**：`apibox10` → 10，不是 `apibox1` + `0`。
9. **10^6 条命令 < 2 s** —— 每次 allocate 不能扫全表。

## 变体

- 类名叫 `ServerManager`；`deallocate` 返回 `None`。
- Part 1 作为 LC "first missing positive"（O(1) 额外空间、原地）。
- 校验 follow-up：未知释放**抛异常**而不是忽略 → `Tracker(strict=True)` 抛 `KeyError`。

## Code Core 节点

**`toolbox.heap`** · `model.idempotency`（重复释放） · `model.index` ·
`input.malformed`（主机名切分） · **`performance.budget`** · `algorithms.recognition`

## 自测清单

- [ ] `[]` / 无 1 / 连续 1..n / 重复 / 0 / 负 / 浮点
- [ ] 释放未知 / 已释放 / `apibox` / `apibox0` / `apibox01`
- [ ] 重复释放后不出现两个同名
- [ ] 先释放 3 再释放 1 → 下次给 1
- [ ] 空闲池空后从 high-water mark 继续
- [ ] 两种类型互不影响
- [ ] `apibox10` 的切分
- [ ] 10^6 条命令的耗时
