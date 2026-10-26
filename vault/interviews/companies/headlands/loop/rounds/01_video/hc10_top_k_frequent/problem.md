# hc10 · 前 K 个高频元素

面试官给你一个整数数组和一个 k，让你返回出现次数最多的 k 个不同的值。Part 1 用哈希表计数加大小为 k 的最小堆，O(n log k)。Part 2 是下一步追问：能不能做到 O(n)，答案是按出现次数分桶。数据放不下内存、分布式怎么做、堆和分桶和快速选择怎么选，放在口头追问里。

## 面试官会怎么说

> "Given an integer array `nums` and an integer `k`, return the `k` most frequent distinct values. Return them ordered by frequency, highest first; if two values have the same frequency, the smaller value comes first."
> 接着会问："Can you do better than O(n log n)?" "What if the data doesn't fit in memory?" "What if it is spread across many machines?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：k 一定合法吗？输出要不要排序？次数相同时怎么排？ |
| 3–15 分钟 | **Part 1**：哈希表 + 大小为 k 的最小堆 |
| 15–30 分钟 | **Part 2**：按出现次数分桶 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 哈希表 + 最小堆（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int[] topKHeap(int[] nums, int k)` |
| C++ | `std::vector<int> top_k_heap(const std::vector<int>& nums, int k)` |

- 输出顺序：出现次数从多到少；次数相同时，值小的在前。
- `k < 1` 或者 `k` 大于不同值的个数：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 例子：`[1,1,1,2,2,3]`，`k = 2` → `[1, 2]`。`[3,3,2,2,1,1]`，`k = 2`：三个值都出现 2 次，取最小的两个 → `[1, 2]`。`[6,5,5,4,5]`，`k = 2` → `[5, 4]`（4 和 6 都出现 1 次，取小的）。负数照常处理：`[-1,-1,-2,-2,0]`，`k = 2` → `[-2, -1]`。

## Part 2 · 按出现次数分桶（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int[] topKBucket(int[] nums, int k)` |
| C++ | `std::vector<int> top_k_bucket(const std::vector<int>& nums, int k)` |

- 规则、异常和输出顺序都和 Part 1 一样，两个函数对同一个输入必须给出同样的数组。
- 出现次数最多是 `n`（`n` 是数组长度），所以开 `n + 1` 个桶，第 `f` 个桶放恰好出现 `f` 次的值，从后往前取满 `k` 个。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 数据流太大，哈希表放不下内存，怎么办？
2. Count-Min 草图（Count-Min sketch）怎么工作，误差是哪一边的？
3. Space-Saving 算法怎么保证只用 m 个计数器？
4. 数据分布在很多台机器上，每台算本地前 k 再合并，为什么不对？
5. 堆、分桶、快速选择（quickselect）怎么选？

## 边界

- `k = 1`；`k` 等于不同值的个数
- 所有值都不同；所有值都相同
- 次数相同的值：谁在前
- 负数和 0

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc10_top_k_frequent       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc10_top_k_frequent --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc10_top_k_frequent       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc10_top_k_frequent --tag part1
```
