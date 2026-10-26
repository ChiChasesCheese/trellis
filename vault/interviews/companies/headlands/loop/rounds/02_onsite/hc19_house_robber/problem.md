# hc19 · 打家劫舍

一条直街上每个位置有一笔钱，你要选一些位置，使总金额最大，但不能同时选两个相邻的位置。这是经典的一维动态规划（dynamic programming，DP）。第一问写出 O(n) 时间、O(1) 空间的写法，第二问要求把选了哪些位置也返回，最后是口头追问：环形街、树形街、为什么贪心不行、金额为负怎么办。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "nums[i] is the amount available at position i along a linear street. Choose positions to maximise the total, but never two adjacent positions."
> 接着会问："Can you do it in O(1) space?" "Which positions did you choose?" "What if the street is a circle?" "What if the positions form a tree?" "Why doesn't greedy work?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：金额会不会是负数？数组会不会为空？总和会不会超过 `int`？ |
| 3–15 分钟 | **Part 1**：两个滚动变量（选 / 不选），O(n) 时间 O(1) 空间 |
| 15–30 分钟 | **Part 2**：保留 dp 数组，往回走，返回选中的下标 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 最大总金额（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static long maxLoot(long[] nums)` |
| C++ | `long long max_loot(const std::vector<long long>& nums)` |

- 金额都是非负数；空数组返回 0；金额和结果都用 64 位整数。
- 例子：`[1,2,3,1]` 得 4（选下标 0 和 2）；`[2,7,9,3,1]` 得 12（选下标 0、2、4）；`[2,3,2]` 得 4；`[3,7]` 得 7。
- `[3000000000, 1, 3000000000]` 得 6000000000，超过 `int` 的范围。

## Part 2 · 返回选中的下标（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<Integer> chosenIndices(long[] nums)` |
| C++ | `std::vector<int> chosen_indices(const std::vector<long long>& nums)` |

- 返回一个最优方案选中的下标，升序排列。
- 最优方案不止一个时，规则固定：**总金额相同就优先不选**，所以 `[5,5]` 返回 `[0]`，`[5,5,5]` 返回 `[0,2]`，`[0,0,0]` 返回空。
- 其余例子：`[1,2,3,1]` 返回 `[0,2]`；`[2,7,9,3,1]` 返回 `[0,2,4]`；空数组返回空。
- 选出的金额之和必须等于 Part 1 的答案，且任意两个下标至少差 2。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 街是环形的（最后一个位置和第一个位置相邻）怎么办？
2. 位置组成一棵树，父子不能同时选，怎么办？
3. 为什么「每次拿最大的」不行？给一个反例。
4. 金额可以是负数时，Part 1 的写法还对吗？
5. 为什么返回下标要保留整个数组，不能只用两个变量？

## 边界

- 空数组、只有一个位置、两个位置
- 全是 0；相邻两个相等（决定平局规则）
- 金额超过 `int`（用 64 位）

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/02_onsite/hc19_house_robber       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/02_onsite/hc19_house_robber --tag part1
python3 tools/cpptest.py start loop/rounds/02_onsite/hc19_house_robber       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/02_onsite/hc19_house_robber --tag part1
```
