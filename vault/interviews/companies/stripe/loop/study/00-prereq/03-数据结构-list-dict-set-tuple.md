# 03 · 四个内置数据结构：list / dict / set / tuple（+ collections 三件套）

> 面试题 95% 只用这四个 + `defaultdict` / `Counter` / `deque`。每个都要知道：怎么建、怎么加、怎么查、怎么遍历、复杂度。

## 1. list —— 有序、可变、允许重复（≈ 表 / 数组）

```python
xs = []                 # 空
xs = [3, 1, 2]
xs.append(5)            # 尾部加         O(1)
xs.pop()                # 尾部弹出并返回 O(1)
xs.pop(0)               # 头部弹出       O(n)  ← 慢！要头部弹出用 deque
xs[0]; xs[-1]           # 首、尾
xs[1:3]                 # 切片 [1,2)：下标 1、2
len(xs)
3 in xs                 # 查找 O(n)  ← 大列表别这么查，用 set
xs.sort()               # 原地排序
sorted(xs)              # 返回新列表
xs.sort(key=lambda v: -v)          # 自定义 key
xs.reverse(); xs[::-1]             # 反转
for i, v in enumerate(xs): ...     # 带下标遍历
[v * 2 for v in xs if v > 1]       # 推导式
```

陷阱：
- `xs = ys` 不是复制，是**同一个列表两个名字**。复制用 `ys = xs[:]` 或 `list(xs)`。
- `[[0] * 3] * 3` 三行是同一个对象；二维要写 `[[0] * 3 for _ in range(3)]`。
- 遍历时不要删元素；要过滤就建新列表。

## 2. dict —— key → value，O(1) 查找（≈ 索引 / 行 / GROUP BY 结果）

```python
d = {}
d = {"a": 1, "b": 2}
d["c"] = 3              # 写
d["a"]                  # 读；没有会 KeyError
d.get("z", 0)           # 读；没有返回默认值
"a" in d                # 判断有没有 key  O(1)
del d["a"]
d.pop("b", None)        # 删并返回；没有返回 None
len(d)
for k in d: ...                     # 遍历 key（保持插入顺序！Python 3.7+）
for k, v in d.items(): ...          # 遍历键值对
list(d.keys()); list(d.values())
sorted(d)                           # key 排序后的列表
sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))   # 按 value 降序、key 升序
d.setdefault("k", []).append(x)     # 没有就先放个 []，再 append
{k: v for k, v in pairs}            # dict 推导式
```

- **key 必须是不可变的**：str、int、tuple 可以；list 不行（用 tuple）。
- 组合键：`d[(merchant, customer)]`。
- 嵌套：`d = {"m_a": {"sum": 0, "n": 0}}`，读 `d["m_a"]["sum"]`。

## 3. collections 三件套

```python
from collections import defaultdict, Counter, deque

# defaultdict：访问不存在的 key 时自动生成默认值
cnt = defaultdict(int);   cnt["x"] += 1          # int() == 0
grp = defaultdict(list);  grp["x"].append(1)     # list() == []
nested = defaultdict(lambda: defaultdict(int))   # 两层

# Counter：专门数数
c = Counter(["a", "b", "a"])     # Counter({'a': 2, 'b': 1})
c["a"]                           # 2；没有的 key 返回 0，不报错
c.most_common(2)                 # [('a', 2), ('b', 1)]  ← 并列时按插入顺序，不是字典序！要字典序自己 sorted
c.update(["a"])                  # 再加

# deque：两头都 O(1) 的队列
q = deque()
q.append(1); q.appendleft(0)
q.popleft(); q.pop()
q = deque(maxlen=3)              # 固定长度滑动窗口，满了自动挤掉最老的
```

`Counter.most_common` 的并列顺序是**插入顺序**，面试题要求"并列取字典序最小"时，必须 `min(c, key=lambda k: (-c[k], k))` 或者 `sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))`。这是高频挂点。

## 4. set —— 无序、不重复、O(1) 查（≈ DISTINCT / 集合运算）

```python
s = set()               # 空 set（{} 是空 dict！）
s = {1, 2, 3}
s.add(4); s.discard(9)  # discard 不存在不报错；remove 会报错
2 in s                  # O(1)
a | b   # 并      a & b  # 交      a - b  # 差      a ^ b  # 对称差
len(s)
sorted(s)               # 要输出必须先排序，set 没有顺序
```

用途：去重、"见过没有"（`seen = set()`）、两组 id 的交并差。

**保序去重**：`list(dict.fromkeys(xs))`。

## 5. tuple —— 不可变的 list（≈ 组合键 / 多返回值 / 排序 key）

```python
t = (1, "a")
t[0]
x, y = t                # 解包
d[(a, b)] = ...         # 当 dict 的 key
sorted(rows, key=lambda r: (r["a"], -r["b"]))   # 排序 key
return total, count     # 多返回值其实是 tuple
```

- 单元素 tuple 要写 `(1,)`，`(1)` 只是数字 1。
- 元组比较是**逐项比较**：`(1, "b") < (1, "c")`。这就是排序 key 用元组的原因。

## 6. 复杂度一张表（面试官会问"你这个是 O 多少"）

| 操作 | list | dict / set | deque |
|---|---|---|---|
| 尾部加 | O(1) | O(1) | O(1) |
| 头部加/删 | O(n) | — | O(1) |
| 按 key/下标读 | O(1) | O(1) | O(1) 两端 |
| `x in ...` | **O(n)** | **O(1)** | O(n) |
| 排序 | O(n log n) | — | — |
| 遍历 | O(n) | O(n) | O(n) |

规则：**要查"在不在"/"对应什么"，用 dict/set；要顺序，用 list；两头进出用 deque。** 10^5 条数据、双重循环 = 10^10 = 超时。

## 7. 选型速查（看到题目怎么选）

| 题目说 | 用 |
|---|---|
| "每个 merchant 的…" | `defaultdict(int/list)`，key = merchant |
| "每个 (customer, merchant) 的…" | `defaultdict`，key = tuple |
| "去重 / 是否出现过" | `set` |
| "最近 k 个 / 滑动窗口" | `deque` |
| "前 k 大" | `sorted(...)[:k]` 或 `heapq.nlargest(k, ...)` |
| "按 id 查详情" | `dict`：id → 记录 |
| "顺序很重要，最后要按输入顺序输出" | `list` + 保存原下标 |
| "状态：pending → succeeded → refunded" | `dict`：id → 状态字符串 |

## 8. 练习

`exercises/ex03_structures.py`：
1. `dedupe_keep_order(xs)`：保序去重。
2. `group_by(rows, key)`：返回 dict：key 值 → 行列表（保持输入顺序）。
3. `top_k_by_count(items, k)`：出现次数前 k 的元素，次数降序、元素字典序。
4. `sliding_max(xs, w)`：窗口大小 w 的每个窗口最大值（用 deque 或简单方法都行，先做对）。
5. `invert(d)`：{k: v} → {v: [k, ...]}，每个 list 内按 k 排序。

`python -m pytest test_ex03.py -q`

## 9. 自查

- [ ] 空 set 是 `set()`，`{}` 是 dict
- [ ] `in` 对 list 是 O(n)，对 set/dict 是 O(1)
- [ ] `Counter.most_common` 并列不是字典序
- [ ] 排序 key 用元组，负号只对数字有效
- [ ] dict 的 key 不能是 list
