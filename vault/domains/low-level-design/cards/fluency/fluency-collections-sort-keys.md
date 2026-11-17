---
id: fluency-collections-sort-keys
node: fluency.collections
type: qa
step: 4
---
## Q
推荐结果要按分数降序、热度降序、id 升序排。有人写 `sorted(rows, key=…, reverse=True)`。为什么 id 的顺序错了？多个排序条件、降序与升序混用，怎么写才对？

## A
**key 返回元组，降序的数字取负**

- **`sorted` 稳定**：key 相同的元素保持原来的相对顺序；
- **一次排完**：`key` 返回元组，按元素逐个比较；先比分数，相同再比热度，再比 id；
- **降序取负**：数字字段取负就是降序；字符串不能取负，要么排两次（利用稳定性，先按次要的、后按主要的），要么保持升序；
- **`reverse=True` 是整体翻转**：所有字段都变降序，包括该升序的 id；
- **`sort()` 与 `sorted()`**：`lst.sort()` 原地改，返回 `None`；`sorted(lst)` 返回新列表，不动参数；函数参数不要原地 `sort`，调用方的列表会被悄悄重排；
- **字符串顺序不是数字顺序**：`"payment10" < "payment9"`；编号要按整数比较就把数字部分取出来，`int(s.removeprefix("payment"))`。

```python
rows = [("m1", 4.0, 90), ("m2", 4.0, 70), ("m3", 4.5, 70), ("m0", 4.0, 90)]
print(sorted(rows, key=lambda r: (-r[1], -r[2], r[0])))      # m3 m0 m1 m2
print(sorted(rows, key=lambda r: (r[1], r[2], r[0]), reverse=True))   # m3 m1 m0 m2：id 被翻了

ids = ["payment9", "payment10", "payment2"]
print(sorted(ids))                                            # ['payment10', 'payment2', 'payment9']
print(sorted(ids, key=lambda s: int(s.removeprefix("payment"))))   # payment2, 9, 10
```

**知识点：**容器的选择与惯用法（Collections Idioms）
