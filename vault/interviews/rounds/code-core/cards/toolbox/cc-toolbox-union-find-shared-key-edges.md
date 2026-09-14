---
id: cc-toolbox-union-find-shared-key-edges
node: toolbox.union-find
type: qa
---
## Q
10^5 records; two records are linked when they share any identifier (email, phone, device). Pairwise comparison is 10^10. Model it.

## A
**Make each identifier a node too, and union each record with its identifiers.** No pair is ever enumerated.

```python
for r in records:
    for field, value in r.identifiers():
        if value:                                   # empty fields link nothing
            dsu.union(("rec", r.id), (field, value))
```

- Cost is O(total identifiers · α) instead of O(n²).
- **Type the key by field** ([[cc-toolbox-hash-tuple-keys]]) or a phone number equal to an account number merges two unrelated groups — `A:x:y` and `B:y:x` must not link.
- The alternative, if the identifier must not surface in the output: keep a `value -> first record seen` map and union each later record with that first one. Same components, `n − 1` edges, no synthetic nodes to filter out.
- Empty or missing values link nothing; filtering them out is a rule, not a nicety.

## Q zh
10^5 条记录；两条记录只要共享任一标识（email、电话、设备）就相连。两两比较是 10^10。怎么建模？

## A zh
**把每个标识也当作节点，把记录与它的各个标识合并。** 从不枚举任何一对。

```python
for r in records:
    for field, value in r.identifiers():
        if value:                                   # 空字段不连接任何东西
            dsu.union(("rec", r.id), (field, value))
```

- 代价是 O(标识总数 · α)，而不是 O(n²)。
- **key 要按字段带类型**（[[cc-toolbox-hash-tuple-keys]]），否则一个与账号相同的电话号会把两个无关的群合并 —— `A:x:y` 与 `B:y:x` 绝不能相连。
- 若标识不能出现在输出里，另一种做法是：维护 `值 -> 首次见到的记录` 映射，把后来的记录与那条首记录合并。连通块相同，边只有 `n − 1` 条，也没有合成节点需要过滤。
- 空值或缺失值不连接任何东西；把它们滤掉是规则，不是锦上添花。
