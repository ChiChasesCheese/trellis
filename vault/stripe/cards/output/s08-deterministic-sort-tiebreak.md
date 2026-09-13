---
id: s08-deterministic-sort-tiebreak
node: stripe.output
type: qa
---

## Q
题面写 "sorted by X" 时，隐藏测试一定会构造平手，怎么把整个排序键一次排完？升序降序混在一起（尤其字符串列降序）怎么处理？没说 tie-break 规则时该怎么办？

## A
**为什么考**：几乎每道题的输出都是 "sorted by X"，而隐藏测试一定会构造平手。

**标准做法**：把整个排序键写成一个元组，一次排完：

```python
rows.sort(key=lambda r: (-r.score, r.name))        # score 降序，name 升序
```

**降序和升序混在一起怎么办**：
- 数值列降序：取负号 `-r.score`。
- 字符串列降序：**不能取负号**。要么先按字符串升序排一遍再按其他列稳定排（利用 `sort` 的稳定性，
  从最次要的键开始逐个排），要么用 `functools.cmp_to_key` 写比较函数。

```python
rows.sort(key=lambda r: r.name)          # 最次要的键，先排
rows.sort(key=lambda r: r.score, reverse=True)   # 最主要的键，后排（稳定性保住前一次）
```

**字典序 vs 数值序**：`"acct_10" < "acct_2"` 是**真的**（字符 `1` < `2`）。
题面写 "lexicographically sorted" 就是这个意思，不要偷偷按数字排。

**没说 tie-break 怎么办**：按一个天然唯一的键（id）升序，并写注释。
沉默的平手是不确定输出，一定挂 perf/fmt 测试。
