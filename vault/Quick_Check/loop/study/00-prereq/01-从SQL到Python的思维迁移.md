# 01 · 从 SQL 到 Python 的思维迁移

> 你只写过 SQL，这不是劣势——SQL 已经教会了你"数据 → 过滤 → 分组 → 聚合 → 排序 → 输出"这条主线。
> Python 面试题（Stripe 电面 / onsite coding / OA）本质上就是**用手写循环把这条 SQL 主线跑一遍**。
> 本章的目标：把你脑子里每一个 SQL 关键字，对应到一段你能徒手写出来的 Python。

## 0. 先建立一个总对照表

| 你在 SQL 里做的事 | Python 里怎么做 | 关键语法 |
|---|---|---|
| 一张表 | 一个 `list`，每行是一个 `dict`（或 tuple / dataclass） | `rows = [{"id": "a", "amt": 10}, ...]` |
| 一行 | `dict`：列名 → 值 | `row["amt"]` |
| `SELECT col FROM t` | 列表推导式 | `[r["amt"] for r in rows]` |
| `WHERE amt > 10` | 推导式里加 `if` | `[r for r in rows if r["amt"] > 10]` |
| `GROUP BY merchant` | 一个 `dict`，key = 分组字段，value = 累加器 | `by = defaultdict(int); by[r["m"]] += r["amt"]` |
| `COUNT(*)` / `SUM` / `MAX` | `len` / `sum` / `max` 或者边循环边累加 | `sum(r["amt"] for r in rows)` |
| `JOIN t2 ON t1.k = t2.k` | 先把 t2 做成 `dict`（k → 行），再循环 t1 查字典 | `idx = {r["k"]: r for r in t2}; idx[r1["k"]]` |
| `ORDER BY a DESC, b ASC` | `sorted(..., key=lambda r: (-r["a"], r["b"]))` | 排序 key 是一个元组 |
| `LIMIT 5` | 切片 | `rows[:5]` |
| `DISTINCT` | `set` 或者 `dict.fromkeys`（保序） | `list(dict.fromkeys(xs))` |
| `CASE WHEN` | `if / elif / else` | — |
| `NULL` | `None` | `if x is None:` |
| 窗口函数 `ROW_NUMBER() OVER (PARTITION BY k ORDER BY t)` | 先 `GROUP BY` 成 dict of list，再每组内排序、`enumerate` | 见 §5 |
| 一条 SQL 语句 | 一个函数 `def part1(lines): ... return out_lines` | — |
| 结果集 | `return` 一个 list，或者 `print` 出来 | — |

**心法**：SQL 是"声明式"——你说要什么，引擎去跑。Python 是"命令式"——你得自己写"引擎"：
一个 `for` 循环扫一遍表，一路把结果攒进 `dict` / `list`。**面试题 95% 就是这一个 `for` 循环。**

## 1. 表 = list of dict

```python
# SQL: 一张 charges 表
# charge_id | merchant | amount | status
rows = [
    {"charge_id": "ch_1", "merchant": "m_a", "amount": 1000, "status": "ok"},
    {"charge_id": "ch_2", "merchant": "m_a", "amount": 500,  "status": "disputed"},
    {"charge_id": "ch_3", "merchant": "m_b", "amount": 700,  "status": "ok"},
]
```

- `rows` 是一个 **list**（有顺序，可以按下标取 `rows[0]`）。
- 每个元素是一个 **dict**（键值对，`rows[0]["amount"]` 是 1000）。
- 面试时，输入通常是一行行字符串（stdin / 参数），你要**自己把每一行拆成 dict**——这就是"解析"（见第 04 章）。

## 2. SELECT / WHERE → 列表推导式

```python
# SELECT amount FROM charges WHERE status = 'ok'
amounts = [r["amount"] for r in rows if r["status"] == "ok"]
# → [1000, 700]
```

读法："对 rows 里的每个 r，如果 r 的 status 是 ok，就取 r 的 amount，放进新列表"。

不习惯推导式就先写成普通循环，**两者完全等价**：

```python
amounts = []
for r in rows:
    if r["status"] == "ok":
        amounts.append(r["amount"])
```

面试时哪种都行。**先写循环，熟了再压成推导式。**

## 3. GROUP BY + 聚合 → dict 累加器

这是面试里出现最多的形态，务必练到肌肉记忆。

```python
# SELECT merchant, SUM(amount), COUNT(*) FROM charges GROUP BY merchant
from collections import defaultdict

total = defaultdict(int)   # merchant -> 总额；不存在的 key 自动当 0
count = defaultdict(int)
for r in rows:
    total[r["merchant"]] += r["amount"]
    count[r["merchant"]] += 1

# total == {"m_a": 1500, "m_b": 700}
# count == {"m_a": 2,    "m_b": 1}
```

- `defaultdict(int)`：访问不存在的 key 时自动放一个 `0`，这样 `+=` 不会报错。
- 不用 defaultdict 的写法：`total[k] = total.get(k, 0) + r["amount"]`。
- 多个聚合放一起：value 用一个小 dict 或 list：`agg[k] = {"sum": 0, "n": 0}`。

**GROUP BY 两个字段**：key 用元组。
```python
# GROUP BY merchant, customer
by = defaultdict(int)
for r in rows:
    by[(r["merchant"], r["customer"])] += r["amount"]
```

**GROUP BY 后要"每组的所有行"**（相当于 `ARRAY_AGG`）：
```python
groups = defaultdict(list)
for r in rows:
    groups[r["merchant"]].append(r)
# groups["m_a"] == [ch_1 的 dict, ch_2 的 dict]
```

## 4. JOIN → 先建索引 dict，再查

SQL 引擎的 hash join，你手写就是：

```python
# merchants 表: merchant_id | name
merchants = [{"merchant_id": "m_a", "name": "Alpha"}, {"merchant_id": "m_b", "name": "Beta"}]

# 第一步：把"右表"变成 dict（主键 -> 行）。这叫"建索引"。
name_of = {m["merchant_id"]: m["name"] for m in merchants}

# 第二步：循环"左表"，用 key 去查。
# SELECT c.charge_id, m.name FROM charges c JOIN merchants m ON c.merchant = m.merchant_id
out = []
for r in rows:
    out.append((r["charge_id"], name_of[r["merchant"]]))
```

- `LEFT JOIN`（右边可能没有）：`name_of.get(r["merchant"], "UNKNOWN")`。
- 查 dict 是 O(1)。**千万不要**写双重循环 `for r in rows: for m in merchants: if ...`——那是 O(n·m)，大数据量会超时。

## 5. ORDER BY → sorted + key 元组

```python
# ORDER BY amount DESC, charge_id ASC
ordered = sorted(rows, key=lambda r: (-r["amount"], r["charge_id"]))
```

- `key=` 给每一行算一个"排序用的元组"，Python 按元组逐项比较。
- 数字降序：加负号 `-r["amount"]`。
- **字符串降序**不能加负号：用 `reverse=True`，或分两次排序（Python 排序是稳定的：先按次要键排，再按主要键排）。
- 面试题几乎必带 tie-break（"金额相同按 id 字典序"）——**排序 key 必须写全**，否则输出顺序不确定，隐藏测试挂。

**窗口函数**（每组内排名）：
```python
# ROW_NUMBER() OVER (PARTITION BY merchant ORDER BY amount DESC)
groups = defaultdict(list)
for r in rows:
    groups[r["merchant"]].append(r)
for m, rs in groups.items():
    rs.sort(key=lambda r: -r["amount"])
    for rank, r in enumerate(rs, start=1):
        r["rank"] = rank
```

## 6. 输出 → 拼字符串

SQL 结果集是表；面试题要求你打印**一模一样**的文本。

```python
for m in sorted(total):                      # 按 merchant 字典序
    print(f"{m},{total[m]}")                 # f-string：花括号里放表达式
```

- `f"{x:.2f}"` 保留两位小数；`f"{x:>8}"` 右对齐宽 8。
- `",".join(list_of_str)` 把列表拼成一行，**元素必须先是字符串**：`",".join(str(v) for v in vals)`。
- 金额不要用 float（`0.1 + 0.2 != 0.3`）——用整数"分"，输出时 `f"{cents // 100}.{cents % 100:02d}"`。详见 OA 仓库 `study/00-essentials/04-money-and-rounding.md`。

## 7. 一个完整例子：把一条 SQL 徒手翻译成 Python

题：给定 charges（`charge_id,merchant,amount,status`），输出每个 merchant 的 **争议率**（disputed 数 / 总数），只输出争议率 > 0.5 的，按 merchant 字典序。

SQL 版（你熟悉的）：
```sql
SELECT merchant
FROM charges
GROUP BY merchant
HAVING SUM(CASE WHEN status='disputed' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) > 0.5
ORDER BY merchant;
```

Python 版（你要能徒手写出来的）：
```python
from collections import defaultdict

def flagged_merchants(lines: list[str]) -> list[str]:
    total = defaultdict(int)
    disputed = defaultdict(int)
    for line in lines:                                  # FROM
        charge_id, merchant, amount, status = line.split(",")   # 解析一行
        total[merchant] += 1                            # GROUP BY + COUNT
        if status == "disputed":                        # CASE WHEN
            disputed[merchant] += 1
    out = []
    for m in sorted(total):                             # ORDER BY
        if disputed[m] * 2 > total[m]:                  # HAVING（用整数比较，避免浮点）
            out.append(m)
    return out
```

注意最后一行：`d / t > 0.5` 改写成 `2d > t`——**交叉相乘避免浮点误差**，这是 Stripe 题的常见陷阱。

## 8. 练习（手写，不许看答案，写完跑测试）

文件：`exercises/ex01_sql_to_python.py`，测试：`exercises/test_ex01.py`。

```bash
cd loop/study/00-prereq/exercises
python -m pytest test_ex01.py -q
```

1. `select_where(rows, min_amount)`：返回 amount ≥ min_amount 的 charge_id 列表，保持输入顺序。
2. `sum_by_merchant(rows)`：返回 dict：merchant → amount 总和。
3. `join_names(rows, merchants)`：返回 `(charge_id, merchant_name)` 列表；找不到的用 `"UNKNOWN"`。
4. `top_k(rows, k)`：按 amount 降序、charge_id 升序取前 k 个 charge_id。
5. `dispute_ratio_over(rows, num, den)`：争议率 > num/den 的 merchant，字典序。**禁止用除法。**

每题写之前先在纸上写出对应的 SQL，再翻译。做完对照 `exercises/solutions/ex01_solution.py`。

## 9. 自查清单

- [ ] 我能不看资料写出 `defaultdict(int)` 累加分组
- [ ] 我知道 JOIN = 先 dict 索引再查，不写双重循环
- [ ] 我的 `sorted` key 永远写全 tie-break
- [ ] 比较比率时我用交叉相乘
- [ ] 我知道 list 是"表"，dict 是"行"或"索引"，set 是"DISTINCT"
