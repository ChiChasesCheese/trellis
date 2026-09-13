# q31 · 心愿单 / 互选排名（公寓互换配对）

> `problems/q31_wishlist_mutual_rank/` · 4 个 part · phone screen
> **主题：下标纪律 + "假设交换但不真的交换" 的差分判断。**

## 一句话题意

每个用户有一个按偏好排序的心愿单。判断"互为第一志愿"、"同一 rank 上互选"；
Part 2 问"把某一项往上提一位，会改变哪些配对关系"（**只算不做**）。

## 核心考点

`S02` 解析 · `S03` 按 id 建记录 · `S08` 确定性顺序 · **`S13` 下标 / off-by-one 纪律** ·
`S18` 缺失 key 和 rank 的校验 · `S20` 自测

## 解题思路

### Part 1

```python
def has_mutual_pair_for_rank(u, r) -> bool:
    lu = lists.get(u, [])
    if not (0 <= r < len(lu)): return False
    v = lu[r]
    lv = lists.get(v, [])
    return 0 <= r < len(lv) and lv[r] == u
```
`FIRST u` ≡ `RANK u 0`。未知用户、`r >= len`、`r < 0` → `false`（**绝不 IndexError**）。

### Part 2 — BUMP（本题的核心）

`BUMP u r`：把 `u` 的第 `r` 项和第 `r−1` 项**假想地**交换，问哪些用户与 `u` 的
"同 rank 互选"状态会**得到或失去**。

```
y = list[u][r]      往上移到 r−1
z = list[u][r-1]    往下移到 r

y 受影响 ⟺ (list[y][r] == u) != (list[y][r-1] == u)
z 受影响 ⟺ (list[z][r-1] == u) != (list[z][r] == u)
```

**输出顺序：先 `y` 再 `z`**（只输出受影响的）；都没有 → `NONE`。
`r = 0`（上面没东西可换）、`r >= len`、未知用户 → `NONE`。

**关键：交换不真的执行。** 用异或（`!=`）来判断"状态是否翻转"，比分别模拟两次更短更不容易错。

### Part 3 — 任意 rank 的互选（重构）

`u` 和 `v` 互选 ⟺ `v ∈ list[u]` 且 `u ∈ list[v]`（rank 可以不同）。
**分数 = `rank_u(v) + rank_v(u)`**（越低越好，0 = 互为第一志愿）。

`PAIRS`：每对一行 `u v score`，其中 `u < v`（字符串序），按 **score → u → v** 排序；无则 `NONE`。
`BEST u`：`u` 分数最低的互选；平手取 **`rank_u(v)` 更小的**，再取名字更小的；无则 `NONE`。

### Part 4 — 交换环（重构）

`CYCLES k`：所有长度为 `k`（2 ≤ k ≤ 5）的简单环 `u1 → u2 → … → uk → u1`，
每个用户想要下一个人的公寓。**每个环只打印一次**，**旋转到从最小的名字开始**，行按字符串序排。
`k = 2` 就是互选对（不带分数）。

## 坑

1. **rank 超出对方列表长度**（`RANK b 2` 而 b 只有 2 项）→ `false`，**不能 IndexError**。
2. 任何查询里的未知用户 → `false` / `NONE`。
3. `BUMP u 0`（上面没东西）和 `BUMP u r` 且 `r >= len` → `NONE`。
4. **用户把自己列进去时，配对忽略它**；空心愿单 `u:` 合法。
5. **只出现在别人心愿单里、自己没定义列表的用户**，视为空列表。
6. `BUMP` 可能返回**两个**受影响的用户（先往上移的，再被挤下去的）。
7. `PAIRS` 每对只打印一次且 `u < v`；分数平手按名字排。
8. `CYCLES` **不能打印同一个环的旋转/重复**；`CYCLES 2` 等于不带分数的 `PAIRS`。

## 变体

- Part 2 叫 `changed_antipairings(username, rank)` —— 语义相同。
- 输入是一个 dict `{'a': ['c','d'], ...}` 直接传给函数，而不是 stdin。
- Part 3–4 是对"只报了标题"的 follow-up 的重构。

## Code Core 节点

`model.index` · **`output.ordering`**（规范化环 + 多键排序） · `input.malformed`（下标边界） ·
`algorithms.graph-traversal`（环检测） · `correctness.edge-catalog`

## 自测清单

- [ ] rank 超出对方长度、超出自己长度、负 rank、未知用户
- [ ] `BUMP u 0` / `BUMP u len`
- [ ] 自己列自己 / 空心愿单 / 只被别人列过的用户
- [ ] `BUMP` 返回两个受影响者的顺序
- [ ] `PAIRS` 的 `u < v` 与三级排序
- [ ] `BEST` 的平手规则
- [ ] `CYCLES` 的旋转去重；`CYCLES 2` == `PAIRS`
