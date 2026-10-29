---
id: uth-cpp-sort-3-comparator
node: cpp.sort
type: qa
step: 3
---
## Q
**比较函数写成 <= 会怎样**｜C++ · std::sort

`std::sort(v.begin(), v.end(), [](int a, int b){ return a <= b; })` 为什么可能直接崩溃？

## A
**结构。** `sort` 要求比较函数是严格弱序（strict weak ordering）：`comp(a, a)` 必须为 false。

**细节。**

- 实测 libc++：1000 个相同的 `7` 加上 `<=`，进程直接被信号杀掉，退出码 138
- 实现里的“无边界”扫描依赖哨兵元素挡住指针
- `<=` 让相等元素也满足“小于”，哨兵失效，指针越界

**为什么。** 实现省掉每步的边界检查换速度，前提是你守住严格弱序这份契约。

**坑。** 只在数据里出现相等元素时才触发，测试用例没有重复值时看不出来。

**对应 LeetCode：** LC 179 最大数 · LC 56 合并区间
