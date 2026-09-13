# q33 · 分析型数据库（`min_by_key` / `first_by_key` / 比较器 / `sort_by`）

> `problems/q33_analytical_db_min_by_key/` · 4 个 part · technical screen（2019–2023）
> **主题：一步一步把同一个功能重构到更抽象的形式 —— 面试官考的是"能不能复用"。**

## 一句话题意

记录是 `dict[str, int]`。求某个 key 的最小记录；再加方向；再抽出比较器；再做链式比较器和排序。

## 核心考点

`S02` JSON lines 解析 · `S03` 记录即 dict · `S08` 确定性平手 · `S09` 格式 ·
**`S18` 缺 key 的处理** · **`S19` 用比较器重新实现前面的函数** · `S21` `functools.cmp_to_key` / `json`

## 解题思路

### 贯穿全题的一条规则

**不含该 key 的记录，其值视为 0。**（题面原话："Note that keys may map to negative values!"）
所以 `{}` 在 `{"a": -1}` 和 `{"a": 1}` **之间**。

### Part 1 — `min_by_key(key, records)`

值最小的记录；平手**返回输入顺序的第一个**（题面说"任选一个"，但**确定性更好**）；
空列表 → `None`。

### Part 2 — `first_by_key(key, direction, records)`

`asc` 取最小、`desc` 取最大；缺 key = 0；平手取第一个；空 → `None`。
**`min_by_key` 必须改写成 `first_by_key(key, "asc", records)`。**

### Part 3 — `RecordComparator(key, direction).compare(a, b)`

返回 `-1` / `0` / `1`。缺 key = 0。
**`first_by_key` 必须用比较器实现**：保留 `best`，当 `compare(rec, best) == -1` 时替换
（**严格**，所以平手保留第一个）。

```python
class RecordComparator:
    def __init__(self, key, direction): self.key, self.desc = key, direction == "desc"
    def compare(self, a, b):
        x, y = a.get(self.key, 0), b.get(self.key, 0)
        if x == y: return 0
        return (1 if x > y else -1) * (-1 if self.desc else 1)
```

### Part 4 — 链式比较器与 `sort_by`

`ChainedComparator([...])`：用**第一个返回非 0** 的比较器的结果。
`sort_by(specs, records)`：按链**稳定**排序（相等的保持输入序）。
`top_k(specs, k, records)`：前 `k` 个（`k <= 0` → 空；`k > n` → 全部）。

## 坑

1. **缺 key = 0 落在负数和正数之间**：求 min 时 `{"a": -1}` 胜过 `{}`；求 max 时 `{}` 胜过 `{"a": -1}`。
2. 空记录列表 → `None`；单个 `{}` 记录 → 返回 `{}`。
3. **平手取输入序第一个**，`asc` 和 `desc` 都是（**不要用 `<=`**）。
4. `desc` **不是**"把值取负再求 min"（如果你为此修改了记录就错了）——
   **绝不修改输入的 dict**。
5. 比较器必须**反对称**：`compare(a, b) == -compare(b, a)`。
6. **稳定的多键排序**：相等的保持输入序；第二个键只用来打破第一个键的平手。
7. 大值（±10^18）和 10^5 条记录 —— min/first 要 O(n)，排序 O(n log n)。

## 变体

- Java 签名 `Map<String,Integer> minByKey(String key, List<Map<String,Integer>> records)`。
- 函数式写法：`comparator(key, direction)` 返回一个二元函数（仓库也导出了 `make_comparator`）。
- Glassdoor Senior SWE：同样三步，45 分钟。

## Code Core 节点

**`output.ordering`**（`cmp_to_key`、稳定性） · `python.idioms` · `input.structured`（JSON lines） ·
`model.records` · `correctness.invariants`（反对称性）

## 自测清单

- [ ] `{}` 与 `{"a": -1}` 在 min 和 max 下的相对位置
- [ ] 空列表 / 单个 `{}`
- [ ] 平手取第一个（asc 和 desc 各测）
- [ ] 确认没有修改输入 dict
- [ ] `compare(a,b) == -compare(b,a)`
- [ ] 多键稳定排序：第二键只破第一键的平手
- [ ] `k <= 0` / `k > n`
- [ ] ±10^18 与 10^5 条记录
