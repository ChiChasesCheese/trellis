---
id: fluency-collections-counting-grouping
node: fluency.collections
type: qa
step: 3
---
## Q
购物清单里同一个 SKU 出现多次，要合并数量，再算价格。`dict.get`、`defaultdict`、`Counter` 各怎么写累加？`defaultdict` 在只读时会有什么副作用？

## A
**累加用 get 或 Counter，只读别碰 defaultdict**

- **`d[k] = d.get(k, 0) + n`**：不依赖别的类；插入顺序是键第一次出现的顺序；
- **`Counter`**：`c[k] += n`，缺失的键读出来是 0 且不插入；`most_common(1)`、两个 `Counter` 相加都有现成方法；减法会丢掉非正的结果；
- **`defaultdict(list)` 分组**：`groups[key].append(x)` 一行完成“没有就新建”；
- **只读的副作用**：`defaultdict` 读不存在的键会创建它，`if dd["x"]:` 之后 `"x"` 已经在字典里了；判断存在用 `in`；返回给调用方之前转成普通 `dict`，免得调用方读取时又改动内部状态；
- **先合并再算价**：同一个商品拆成几行输入，应当先合并成一个总数量再套用价格规则，否则分段价格被各行分别套用，结果不同。

```python
from collections import Counter, defaultdict

items = [("b", 1), ("a", 2), ("b", 3)]
qty = Counter()
for sku, n in items:
    qty[sku] += n                     # 同一 SKU 先合并
print(dict(qty), qty["zzz"], "zzz" in qty)    # {'b': 4, 'a': 2} 0 False

groups = defaultdict(list)
for sku, n in items:
    groups[sku].append(n)
print(groups["x"], dict(groups))      # [] {'b': [1, 3], 'a': [2], 'x': []}：读也插入了
```

**知识点：**容器的选择与惯用法（Collections Idioms）
