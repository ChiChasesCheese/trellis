# hc20 · 合并区间

给你一组闭区间，把所有重叠的区间合并，按起点从小到大返回。第一问是「先排序再扫一遍」，第二问是在一个已经合并好、有序的列表里插入一个新区间，要求 O(n) 且不重新排序。最后是口头追问：区间不断流进来、整数区间相邻要不要合并、数据大到放不进内存、比较时怎么避免溢出。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "You are given closed integer intervals intervals[i] = [start, end]. Merge every group of overlapping intervals and return the result sorted by start."
> 接着会问："What if I give you a new interval to insert into the merged list?" "What if intervals keep streaming in?" "What if the input doesn't fit in memory?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：闭区间的端点相碰算不算重叠？`[1,2]` 和 `[3,4]` 合并吗？输入有序吗？能不能改输入？ |
| 3–15 分钟 | **Part 1**：按 start 排序，一遍扫描合并 |
| 15–30 分钟 | **Part 2**：往已合并的有序列表里插一个新区间，O(n) |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 排序 + 一遍扫描（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int[][] merge(int[][] intervals)` |
| C++ | `std::vector<std::vector<int>> merge(const std::vector<std::vector<int>>& intervals)` |

- 区间是闭区间 `[start, end]`，`start <= end`；`start > end` 的输入，Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 因为是闭区间，`[1,3]` 和 `[3,5]` 共用端点 3，**重叠**，合并成 `[1,5]`。
- 整数区间 `[1,2]` 和 `[3,4]` 之间没有共用的点，**不合并**，结果还是两个区间。
- 例子：`[[1,3],[2,6],[8,10],[15,18]]` 得 `[[1,6],[8,10],[15,18]]`；`[[5,6],[1,10],[2,3]]` 得 `[[1,10]]`（输入不要求有序，也可能互相包含）；空输入得空。
- 不修改传进来的数组。端点可以取到 `int` 的最小值和最大值。

## Part 2 · 插入一个新区间（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int[][] insert(int[][] merged, int[] added)` |
| C++ | `std::vector<std::vector<int>> insert(const std::vector<std::vector<int>>& merged, const std::vector<int>& added)` |

- `merged` 已经合并好并按 start 升序（互相不重叠），`added` 是一个新的闭区间。返回插入并合并后的列表，要求 O(n)，不能重新排序。
- 例子：`[[1,3],[6,9]]` 插入 `[2,5]` 得 `[[1,5],[6,9]]`；`[[1,2],[3,5],[6,7],[8,10],[12,16]]` 插入 `[4,8]` 得 `[[1,2],[3,10],[12,16]]`。
- 插到最前面、最后面、插进空列表都要对：`[[1,2],[5,6]]` 插入 `[0,0]` 得 `[[0,0],[1,2],[5,6]]`。
- 端点相碰要合并：`[[1,2],[5,6]]` 插入 `[2,5]` 得 `[[1,6]]`；整数相邻不合并：插入 `[3,4]` 得 `[[1,2],[3,4],[5,6]]`。
- 不修改输入。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 区间一个一个流进来，每次都要能查到当前合并结果，怎么做？
2. 整数区间 `[1,2]` 和 `[3,4]` 相邻，要不要合并？怎么写才不会在边界上出错？
3. 数据大到内存放不下怎么办？
4. 比较端点时为什么不能写 `a[0] - b[0]`？
5. 为什么 Part 2 不需要排序，复杂度为什么是 O(n)？

## 边界

- 空输入；只有一个区间
- 端点相碰（`[1,3]`、`[3,5]`）；整数相邻（`[1,2]`、`[3,4]`）
- 一个区间包住另一个；起点相同；单点区间 `[2,2]`
- 端点是 `Integer.MIN_VALUE` / `Integer.MAX_VALUE`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/02_onsite/hc20_merge_intervals       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/02_onsite/hc20_merge_intervals --tag part1
python3 tools/cpptest.py start loop/rounds/02_onsite/hc20_merge_intervals       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/02_onsite/hc20_merge_intervals --tag part1
```
