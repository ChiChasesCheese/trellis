---
id: fluency-iteration-filter-then-truncate
node: fluency.iteration
type: qa
step: 4
---
## Q
推荐服务先用用户的评分累计各类型的权重，再给候选电影打分，最后取前 `limit` 部。实现者在累计权重的循环里就跳过了已下架的电影，结果用户的口味被削掉一块；另一处是先截断前 `limit` 条再过滤，结果不足。循环里的过滤和截断应放在哪一步？

## A
**累计用全部数据，过滤选候选，截断放最后**

- **按阶段想清每一步的输入**：累计权重的输入是“用户评过的全部电影”，下架电影也代表他喜欢什么；过滤“可推荐”只作用在候选集上；
- **在上游悄悄过滤会改变下游的输入**：权重少了一块，每个候选的分数都变了，没有报错，只是推荐变差；
- **先过滤再截断**：先取前 `limit` 个再删掉不可用的，结果会少于 `limit`；顺序是 过滤 → 排序 → 取前 `limit`；
- **候选不够就少返回**：不补、不报错；
- **想提前停止用生成器加 `islice`**：`islice(candidates, limit)` 凑够就不再往下求值；前提是上游本身已经按需要的顺序给出，否则要先排序。

```python
from collections import Counter
from itertools import islice

rated = [("m1", "drama", True), ("m2", "drama", False), ("m3", "comedy", True)]
# (id, 类型, 是否在架)
weight = Counter(g for _, g, _ in rated)                  # 累计：全部评分，含已下架的
print(weight)                                             # Counter({'drama': 2, 'comedy': 1})
bad = Counter(g for _, g, ok in rated if ok)              # 错：口味被削掉一块
print(bad)                                                # Counter({'drama': 1, 'comedy': 1})

pool = [("m1", 2), ("m3", 1), ("m9", 0)]
cands = (m for m in pool if m[1] > 0)                     # 过滤发生在候选阶段
print(list(islice(cands, 5)))                             # 不够 5 个就少返回
print([m for m in pool[:2] if m[0] != "m1"])              # 错：先截断再过滤，只剩 1 个
```

**知识点：**迭代写法（Iteration Style）
