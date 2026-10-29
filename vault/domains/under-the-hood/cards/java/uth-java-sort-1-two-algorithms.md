---
id: uth-java-sort-1-two-algorithms
node: java.sort
type: qa
step: 1
---
## Q
**Arrays.sort 为什么 int[] 和对象用不同算法**｜Java · OpenJDK 25

`Arrays.sort(int[])` 和 `Arrays.sort(Integer[])` 用的是同一个算法吗？为什么？

## A
**结构。** 基本类型数组用双轴快速排序（`DualPivotQuicksort`）；对象数组用 `TimSort`（有比较器）或 `ComparableTimSort`。

**细节。**

- 两个相等的 `int` 无法区分，不稳定无所谓，快排原地进行，不要额外内存。
- 对象排序要稳定（先按次要键、再按主键才有意义），比较又是方法调用，TimSort 比较次数更少。
- 本机实测 200 万个随机数：`int[]` 约 76 毫秒，`Integer[]` 约 228 毫秒（单次测量，非严格基准）。

**为什么。** 稳定性对基本类型没有意义，对对象却是语义要求。

**对应 LeetCode：** LC 912 排序数组 · LC 56 合并区间
