---
id: uth-java-sort-3-timsort-contract
node: java.sort
type: qa
step: 3
---
## Q
**Comparator 写错会怎样**｜Java · OpenJDK 25

用 `(p, q) -> p - q` 当比较器排序 `Integer`，为什么可能排错？TimSort 还会抛出什么异常？

## A
**结构。** Java 的 `TimSort` 做法和 Python 一致：找 run、二分插入补到 `minrun`、按栈规则归并；`minrun` 在 16 到 32 之间（Python 是 32 到 64）。

**细节。**

- 实测 10 万个元素的比较次数：有序 99999，倒序 99999，随机约 153 万。
- `p - q` 在 `MAX_VALUE` 与负数相减时溢出，实测 `[MAX, -5, 3, MIN, 0]` 排成 `[MAX, -5, 0, 3, MIN]`。
- 比较结果前后矛盾（实测用随机数）时，可能抛 `IllegalArgumentException: Comparison method violates its general contract!`。

**为什么。** 归并依赖比较结果可传递；违反它，算法的不变式就被破坏。

**坑。** 用 `Integer.compare(p, q)` 或 `Comparator.comparingInt`。

**对应 LeetCode：** LC 179 最大数 · LC 937 重新排列日志文件
