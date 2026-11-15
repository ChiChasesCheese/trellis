---
slug: relative-sort-array
---
## Q
**LC 1122 数组的相对排序**｜Easy

`arr2` 中的元素互不相同，且都出现在 `arr1` 中。对 `arr1` 排序：先按 `arr2` 的顺序排列 `arr2` 里的元素，没出现在 `arr2` 的元素按升序放在末尾。

## A
**一句话。** 自定义排序键：在 `arr2` 里的用它的位置，不在的用「一个大于所有位置的数」，再按值升序。

```python
def relative_sort_array(arr1, arr2):
    rank = {x: i for i, x in enumerate(arr2)}
    big = len(arr2)               # 不在 arr2 里的排最后
    return sorted(arr1, key=lambda x: (rank.get(x, big), x))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 键里没有第二项 `x`：不在 `arr2` 中的元素需要按值升序，只靠 `big` 它们会保持原顺序。
- 对 `arr2` 元素查线性位置：每次 `O(m)`，先建 `rank` 字典。

**追问。**
- 值域很小怎么办？：计数排序，先数 `arr1` 的频次，按 `arr2` 顺序输出，再按值升序输出剩余，`O(n + 值域)`。
- 为什么 `rank.get(x, big)` 够用？：保证不在 `arr2` 的元素的第一关键字全相等且大于所有排名。

**同模式。** LC 1636 按照频率将数组升序排序、LC 179 最大数、LC 274 H 指数、LC 1337 矩阵中战斗力最弱的 K 行
