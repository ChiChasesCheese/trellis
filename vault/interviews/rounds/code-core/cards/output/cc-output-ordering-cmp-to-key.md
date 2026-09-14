---
id: cc-output-ordering-cmp-to-key
node: output.ordering
type: qa
---
## Q
The order is "by key k1 ascending, then k2 descending, where a missing key reads as 0" — and the key list is given at runtime. Write it.

## A
**`functools.cmp_to_key` is for orders no key tuple expresses.**

```python
def chained(specs):
    def cmp(a, b):
        for k, d in specs:
            va, vb = a.get(k, 0), b.get(k, 0)
            if va != vb:
                return (1 if va > vb else -1) * (1 if d == "asc" else -1)
        return 0
    return cmp
rows.sort(key=cmp_to_key(chained(specs)))
```

- The comparator must be **antisymmetric** (`cmp(a,b) == -cmp(b,a)`) and return 0 for real ties, or ties stop landing in input order.
- A missing key defaulting to 0 sits *between* negative and positive values — that is a modelling decision, and it is graded.
- Cost: one Python call per comparison, ~2–3× a tuple key ([[cc-toolbox-sorted-key-once]]). Use a tuple key whenever one exists.
- For "first/min under this comparator", replace the incumbent only on a strict `-1`, so ties keep the earlier record.

## Q zh
排序规则是「先按 k1 升序，再按 k2 降序，缺失的 key 视为 0」—— 而 key 列表是运行时给出的。写出来。

## A zh
**`functools.cmp_to_key` 用于任何 key tuple 都表达不了的顺序。**

```python
def chained(specs):
    def cmp(a, b):
        for k, d in specs:
            va, vb = a.get(k, 0), b.get(k, 0)
            if va != vb:
                return (1 if va > vb else -1) * (1 if d == "asc" else -1)
        return 0
    return cmp
rows.sort(key=cmp_to_key(chained(specs)))
```

- 比较器必须**反对称**（`cmp(a,b) == -cmp(b,a)`），并对真正的并列返回 0，否则并列项就不再落在输入顺序上。
- 缺失 key 默认为 0 时，它位于负值与正值*之间* —— 这是个建模决定，而且会被判分。
- 代价：每次比较一次 Python 调用，约为 tuple key 的 2–3 倍（[[cc-toolbox-sorted-key-once]]）。只要存在 tuple key 就用它。
- 求「该比较器下的第一/最小」时，只在严格 `-1` 时替换当前最优，这样并列会保留更早的记录。
