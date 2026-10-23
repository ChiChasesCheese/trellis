---
id: hl-c06-unique-iota-prefix
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 6
---
## Q
`std::unique`、`std::iota`、`std::partial_sum`、`std::minmax_element`、`std::next_permutation` 各做什么？`unique` 怎么真正删掉重复？

## A
- `unique`：只去**相邻**重复，通常先 `sort`；它只把保留的元素前移，不改容器大小，必须 `v.erase(std::unique(v.begin(), v.end()), v.end())`。例：`{1,1,2,2,2,3,1}` 得 `1 2 3 1`。
- `iota(first, last, start)`：填递增序列，如 `10 11 12 13 14`。
- `partial_sum`：前缀和，上例得 `10 21 33 46 60`。
- `minmax_element`：一次得到最小和最大元素的迭代器。
- `next_permutation`：原地换成下一个字典序排列，配 `do { ... } while (std::next_permutation(...))` 枚举 `abc acb bac bca cab cba`。
