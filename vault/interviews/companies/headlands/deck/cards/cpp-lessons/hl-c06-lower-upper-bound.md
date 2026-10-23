---
id: hl-c06-lower-upper-bound
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 3
---
## Q
`std::lower_bound`、`std::upper_bound`、`std::binary_search` 各返回什么？对已排序数组 `{1,3,3,5,8,13,21}` 查 3 的结果是什么？怎么求相等元素个数？

## A
- `lower_bound(first, last, x)`：第一个 **`>= x`** 的元素的迭代器。
- `upper_bound(first, last, x)`：第一个 **`> x`** 的元素的迭代器。
- `binary_search`：只返回是否存在（`bool`）。
- 例：`lower_bound(3)` 下标 1，`upper_bound(3)` 下标 3，**两者之差 = 2** 就是等于 3 的元素个数；`binary_search(8)` 为 true。
- 只能用于**已排序**区间；对未排序区间结果无意义。

```cpp
auto lo = std::lower_bound(v.begin(), v.end(), 3);
auto hi = std::upper_bound(v.begin(), v.end(), 3);
auto cnt = hi - lo;
```
