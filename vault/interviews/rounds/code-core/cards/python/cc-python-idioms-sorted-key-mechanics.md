---
id: cc-python-idioms-sorted-key-mechanics
node: python.idioms
type: qa
---
## Q
You know the order you want: score descending, then name ascending, then arrival order. Name the three mechanisms Python offers, and the cost of each.

## A
**A tuple key, `reverse=`, and `cmp_to_key` — in that order of preference.**

```python
rows.sort(key=lambda r: (-r.score, r.name, r.seq))
```

- **Tuple key** compares element by element and runs in C. Negate a numeric field for a descending component; you cannot negate a string.
- **`reverse=True`** flips *every* component, so it only works when all keys point the same way.
- **Mixed directions with a string**: rely on stability — sort by the ascending key first, then re-sort by the descending one. `list.sort` and `sorted` are guaranteed stable, so the earlier order survives inside ties.
- **`cmp_to_key`** is the escape hatch when the rule is not a function of one row (e.g. "a before b iff a+b > b+a"); it costs a Python call per comparison.

## Q zh
你已经想清楚要的顺序：分数降序，然后名字升序，最后到达顺序。说出 Python 提供的三种机制，以及各自的代价。

## A zh
**元组键、`reverse=`、`cmp_to_key` —— 优先级依次递减。**

```python
rows.sort(key=lambda r: (-r.score, r.name, r.seq))
```

- **元组键**逐元素比较且跑在 C 里。降序分量把数值字段取负；字符串没法取负。
- **`reverse=True`** 会翻转*所有*分量，只在全部方向一致时可用。
- **方向混合且含字符串**：靠稳定性 —— 先按升序键排一次，再按降序键排一次。`list.sort` 和 `sorted` 保证稳定，所以先前的顺序在平局内部得以保留。
- **`cmp_to_key`** 是当规则不是单行的函数时的逃生口（例如「a 排在 b 前当且仅当 a+b > b+a」）；代价是每次比较一次 Python 调用。
